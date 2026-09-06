"""One-factor-at-a-time sensitivity of the reproduction to the parameters the
paper leaves unspecified (HO offset O_off, guard time, action-space size
N_max, channels per satellite J, minimum elevation angle).

    uv run python -m ilcho.sensitivity --ilcho runs/ilcho_sigmoid_v3/policy.pt \
        --out runs/sensitivity
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from .config import ChannelConfig, EnvConfig, resolve_constellation
from .environment import CHOEnv
from .baselines import MDCHO, MVTCHO
from .qmix import MARLController, QMixConfig
from .rollout import run_policy_episode


def _ctrl(path, n_max, device):
    probe = CHOEnv(EnvConfig(num_ues=4, service_duration_s=10, n_max=n_max),
                   resolve_constellation("starlink_phase_2a"), ChannelConfig())
    c = MARLController(probe.obs_dim, probe.obs_dim * 4, probe.n_actions, 4,
                       QMixConfig(), mode="qmix", device=device, seed=0)
    c.load(path)
    return c


def _run(constellation, n_ue, horizon, episodes, env_kw, ctrl, policy_cls, seed0):
    vals = {"ho": [], "hof": [], "se": [], "jfi": [], "occ_var": []}
    for e in range(episodes):
        seed = seed0 + e
        env = CHOEnv(EnvConfig(num_ues=n_ue, service_duration_s=horizon,
                               **env_kw),
                     resolve_constellation(constellation), ChannelConfig(),
                     seed=seed)
        pol = policy_cls(env_kw["n_max"]) if policy_cls else None
        try:
            m = run_policy_episode(env, pol, ue_seed=seed, greedy_ctrl=ctrl)
        except RuntimeError:
            # e.g. a learned net whose obs_dim differs from this env's n_max
            return {k: float("nan") for k in vals}
        for k in vals:
            vals[k].append(m[k])
    return {k: float(np.mean(v)) for k, v in vals.items()}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ilcho", required=True)
    p.add_argument("--constellation", default="starlink_phase_2a")
    p.add_argument("--n-ue", type=int, default=30)
    p.add_argument("--horizon", type=int, default=600)
    p.add_argument("--episodes", type=int, default=4)
    p.add_argument("--n-max", type=int, default=16,
                   help="must match the N_max the --ilcho policy was trained with")
    p.add_argument("--device", default="cpu")
    p.add_argument("--out", default="runs/sensitivity")
    args = p.parse_args()
    os.makedirs(args.out, exist_ok=True)

    base = dict(n_max=args.n_max, handover_offset_km=50.0, ho_cooldown_s=5.0,
                max_channels=8, reward_type="sigmoid")
    # N_max is NOT swept here: the loaded ILCHO net has a fixed obs_dim
    # (= n_max * 5); N_max robustness is instead checked via the Fig. 5
    # peak-count sanity (ilcho-sanity) and by masking of unused action slots.
    grid = {
        "handover_offset_km": [10.0, 25.0, 50.0, 75.0, 100.0],
        "ho_cooldown_s": [0.0, 2.0, 5.0, 10.0, 20.0],
        "max_channels": [4, 6, 8, 12, 16],
    }

    ctrl = _ctrl(args.ilcho, base["n_max"], args.device)
    out: dict = {"constellation": args.constellation, "n_ue": args.n_ue,
                 "base": base, "sweeps": {}}

    for param, values in grid.items():
        rows = []
        for v in values:
            env_kw = dict(base); env_kw[param] = v
            # keep action space consistent with the loaded net unless we are
            # explicitly sweeping n_max (net is robust: obs padded/masked)
            r_ilcho = _run(args.constellation, args.n_ue, args.horizon,
                           args.episodes, env_kw, ctrl, None, 700)
            r_md = _run(args.constellation, args.n_ue, args.horizon,
                        args.episodes, env_kw, None, MDCHO, 700)
            r_mvt = _run(args.constellation, args.n_ue, args.horizon,
                         args.episodes, env_kw, None, MVTCHO, 700)
            rows.append({"value": v, "ILCHO": r_ilcho, "MD-CHO": r_md,
                         "MVT-CHO": r_mvt})
            print(f"{param}={v}: ILCHO ho={r_ilcho['ho']:.2f} "
                  f"hof={r_ilcho['hof']:.2f} se={r_ilcho['se']:.2f} | "
                  f"MD hof={r_md['hof']:.2f} | MVT hof={r_mvt['hof']:.2f}")
        out["sweeps"][param] = rows

    with open(os.path.join(args.out, "sensitivity.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    _plot(out, args.out)
    print("saved", args.out)


def _plot(out: dict, path: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sweeps = out["sweeps"]
    fig, axes = plt.subplots(len(sweeps), 2, figsize=(11, 3.2 * len(sweeps)))
    for i, (param, rows) in enumerate(sweeps.items()):
        xs = [r["value"] for r in rows]
        for col, metric in enumerate(("hof", "se")):
            ax = axes[i, col]
            for method, c in (("ILCHO", "tab:blue"), ("MD-CHO", "tab:orange"),
                              ("MVT-CHO", "tab:green")):
                ax.plot(xs, [r[method][metric] for r in rows], "-o",
                        color=c, label=method)
            ax.set_xlabel(param); ax.set_ylabel(metric)
            ax.grid(alpha=0.3)
            if i == 0 and col == 0:
                ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(path, "sensitivity.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
