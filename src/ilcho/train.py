"""Train the ILCHO (QMIX) controller or the LBSH (IQL) baseline.

Examples
--------
    uv run ilcho-train --reward sigmoid --episodes 1500 --out runs/ilcho_sigmoid
    uv run ilcho-train --reward linear  --episodes 1500 --out runs/ilcho_linear
    uv run ilcho-train --mode iql       --episodes 1200 --out runs/lbsh
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np
import torch

from .config import (CONSTELLATION_NAMES, ChannelConfig, EnvConfig, QMixConfig,
                     resolve_constellation)
from .environment import CHOEnv
from .qmix import MARLController, ReplayBuffer
from .rollout import run_learning_episode


def build_env(args, num_ues: int, horizon_s: int, seed: int) -> CHOEnv:
    env_cfg = EnvConfig(
        num_ues=num_ues,
        service_duration_s=horizon_s,
        reward_type=args.reward,
        n_max=args.n_max,
    )
    if args.mode == "iql":
        # LBSH reward: RVT + load balance, heavy penalty on HO  (paper [26])
        env_cfg.reward_type = "linear"
        env_cfg.lin_w1_se = 0.05
        env_cfg.lin_w2_rvt = 0.02
        env_cfg.p1_ho_success = 3.0
        env_cfg.p2_ho_failure = 6.0
    return CHOEnv(env_cfg, resolve_constellation(args.constellation),
                  ChannelConfig(), seed=seed)


def main() -> None:
    try:                                   # make progress visible when piped
        import sys
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--constellation", default="starlink_phase_2a",
                   choices=CONSTELLATION_NAMES)
    p.add_argument("--reward", default="sigmoid", choices=["sigmoid", "linear"])
    p.add_argument("--mode", default="qmix", choices=["qmix", "iql"])
    p.add_argument("--episodes", type=int, default=1500)
    p.add_argument("--train-ues", type=int, default=10)
    p.add_argument("--horizon", type=int, default=300,
                   help="training episode length [s] (paper eval uses 600)")
    p.add_argument("--n-max", type=int, default=16)
    p.add_argument("--eps-anneal", type=int, default=800)
    p.add_argument("--learn-every", type=int, default=1)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", required=True)
    p.add_argument("--device", default="cpu")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    env = build_env(args, args.train_ues, args.horizon, args.seed)
    obs_dim = env.obs_dim
    # memory-aware replay size: obs float16 dominates -> cap the buffer at ~3 GB
    n_steps = int(round(args.horizon)) + 1        # env.T is only set after reset()
    ep_bytes = n_steps * args.train_ues * (obs_dim * 2 + env.n_actions)
    buf_size = int(np.clip(3_000_000_000 // max(ep_bytes, 1), 64, 5000))
    qcfg = QMixConfig(
        num_episodes=args.episodes,
        eps_anneal_episodes=args.eps_anneal,
        train_ues=args.train_ues,
        buffer_size=buf_size,
        batch_size=args.batch,
    )
    print(f"replay buffer: {buf_size} episodes ({ep_bytes/1e6:.1f} MB/episode)")
    ctrl = MARLController(
        obs_dim=obs_dim,
        state_dim=2 * obs_dim,   # compact pooled state (mean+max over agents)
        n_actions=env.n_actions,
        n_agents=args.train_ues,
        cfg=qcfg,
        mode=args.mode,
        device=args.device,
        seed=args.seed,
    )
    buf = ReplayBuffer(qcfg.buffer_size)
    rng = np.random.default_rng(args.seed)

    hist = {"episode": [], "return": [], "ho": [], "hof": [], "se": [],
            "loss": [], "eps": []}
    t_start = time.time()
    for ep in range(1, args.episodes + 1):
        batch, metrics, ret = run_learning_episode(
            env, ctrl, ep, ue_seed=int(rng.integers(1 << 30))
        )
        buf.add(batch)
        loss = float("nan")
        if len(buf) >= qcfg.batch_size and ep % args.learn_every == 0:
            loss = ctrl.learn(buf.sample(qcfg.batch_size, rng))

        hist["episode"].append(ep)
        hist["return"].append(ret)
        hist["ho"].append(metrics["ho"])
        hist["hof"].append(metrics["hof"])
        hist["se"].append(metrics["se"])
        hist["loss"].append(loss)
        hist["eps"].append(ctrl.epsilon(ep))

        if ep % 25 == 0 or ep == 1:
            w = slice(max(0, ep - 25), ep)
            line = (
                f"ep {ep:5d} | eps {ctrl.epsilon(ep):.2f} | "
                f"return {np.mean(hist['return'][w]):8.2f} | "
                f"HO {np.mean(hist['ho'][w]):6.2f} | "
                f"HOF {np.mean(hist['hof'][w]):5.2f} | "
                f"SE {np.mean(hist['se'][w]):5.2f} | "
                f"loss {np.nanmean(hist['loss'][w]):.4f} | "
                f"{time.time() - t_start:6.0f}s"
            )
            print(line, flush=True)
            with open(os.path.join(args.out, "progress.log"), "a") as fh:
                fh.write(line + "\n")

    ctrl.save(os.path.join(args.out, "policy.pt"))
    np.savez(os.path.join(args.out, "history.npz"),
             **{k: np.asarray(v, dtype=float) for k, v in hist.items()})
    with open(os.path.join(args.out, "train_config.json"), "w") as fh:
        json.dump(vars(args), fh, indent=2)
    _plot_history(hist, args.out)
    print(f"saved -> {args.out}  ({time.time() - t_start:.0f}s)")


def _plot_history(hist: dict, out: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ep = np.asarray(hist["episode"])

    def smooth(x, w=41):
        x = np.asarray(x, float)
        if len(x) < w:
            return x
        k = np.ones(w) / w
        return np.convolve(x, k, mode="same")

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    ax[0].plot(ep, hist["return"], alpha=0.25, color="tab:purple")
    ax[0].plot(ep, smooth(hist["return"]), color="tab:purple")
    ax[0].set_title("Total train score / episode (cf. Fig. 6a / 7a)")
    ax[0].set_xlabel("episode"); ax[0].set_ylabel("mean team reward")

    ax[1].plot(ep, smooth(hist["ho"]), color="tab:blue", label="avg # HO")
    ax[1].plot(ep, smooth(hist["hof"]), color="tab:red", label="avg # HOF")
    ax[1].set_title("HO / HOF per agent (cf. Fig. 6b / 7b)")
    ax[1].set_xlabel("episode"); ax[1].legend()

    ax[2].plot(ep, hist["se"], alpha=0.25, color="tab:cyan")
    ax[2].plot(ep, smooth(hist["se"]), color="tab:cyan")
    ax[2].set_title("Throughput per agent [bps/Hz] (cf. Fig. 6c / 7c)")
    ax[2].set_xlabel("episode"); ax[2].set_ylabel("spectral efficiency")

    fig.tight_layout()
    fig.savefig(os.path.join(out, "training_curves.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
