"""Evaluate ILCHO against the baselines and reproduce the paper's figures.

Produces, under ``--out``:
    results.json           -- all numbers (mean + std over seeds)
    fig_ho_vs_ue.png       -- cf. Fig. 8a / 9a / 10a
    fig_hof_vs_ue.png      -- cf. Fig. 8b / 9b / 10b
    fig_se_vs_ue.png       -- cf. Fig. 8c / 9c / 10c
    fig_fairness_cdf.png   -- cf. Fig. 11
    fig_load_balance.png   -- cf. Table IV
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from .config import (CONSTELLATION_NAMES, ChannelConfig, EnvConfig,
                     resolve_constellation)
from .environment import CHOEnv
from .baselines import MDCHO, MVTCHO, HSNF
from .qmix import MARLController, QMixConfig
from .rollout import run_policy_episode


METHOD_ORDER = ["ILCHO", "ILCHO-lin", "MD-CHO", "MVT-CHO", "HSNF", "LBSH"]
METHOD_COLOR = {
    "ILCHO": "tab:blue", "ILCHO-lin": "tab:purple", "MD-CHO": "tab:orange",
    "MVT-CHO": "tab:green", "HSNF": "black", "LBSH": "tab:red",
}
METRICS = ("ho", "hof", "se", "jfi", "occ_var", "unserved")


def make_env(constellation, num_ues, horizon, n_max, seed, **env_kw) -> CHOEnv:
    cfg = EnvConfig(num_ues=num_ues, service_duration_s=horizon,
                    reward_type="sigmoid", n_max=n_max, **env_kw)
    return CHOEnv(cfg, resolve_constellation(constellation), ChannelConfig(),
                  seed=seed)


def load_ctrl(path: str, mode: str, device: str, n_max: int) -> MARLController:
    probe = make_env("starlink_phase_2a", 4, 10, n_max, 0)
    ctrl = MARLController(
        obs_dim=probe.obs_dim, state_dim=2 * probe.obs_dim,
        n_actions=probe.n_actions, n_agents=4,
        cfg=QMixConfig(), mode=mode, device=device, seed=0,
    )
    ctrl.load(path)
    return ctrl


def evaluate(args) -> dict:
    os.makedirs(args.out, exist_ok=True)
    ue_list = [int(x) for x in args.ues.split(",")]
    n_seeds = args.seeds
    base_rng = np.random.default_rng(args.seed)

    # method -> learned controller (or None for rule-based)
    learned = {}
    if args.ilcho and os.path.exists(args.ilcho):
        learned["ILCHO"] = load_ctrl(args.ilcho, "qmix", args.device, args.n_max)
    if args.ilcho_linear and os.path.exists(args.ilcho_linear):
        learned["ILCHO-lin"] = load_ctrl(args.ilcho_linear, "qmix",
                                         args.device, args.n_max)
    if args.lbsh and os.path.exists(args.lbsh):
        learned["LBSH"] = load_ctrl(args.lbsh, "iql", args.device, args.n_max)

    active = [m for m in METHOD_ORDER
              if m in learned or m in ("MD-CHO", "MVT-CHO", "HSNF")]
    print(f"methods: {active}")

    results: dict = {
        "ue_list": ue_list, "constellation": args.constellation,
        "episodes_per_point": args.episodes, "seeds": n_seeds,
        "horizon_s": args.horizon, "n_max": args.n_max, "methods": {},
    }
    per_ue_se_cache: dict[str, list] = {}

    for method in active:
        stats = {k: {"mean": [], "std": []} for k in METRICS}
        for n_ue in ue_list:
            samples = {k: [] for k in METRICS}
            for s in range(n_seeds):
                for e in range(args.episodes):
                    seed = int(base_rng.integers(1 << 30))
                    env = make_env(args.constellation, n_ue, args.horizon,
                                   args.n_max, seed)
                    ctrl = learned.get(method)
                    policy = {"MD-CHO": MDCHO, "MVT-CHO": MVTCHO}.get(method)
                    policy = policy(args.n_max) if policy else None
                    if method == "HSNF":
                        policy = HSNF(env)
                    m = run_policy_episode(env, policy, ue_seed=seed,
                                           greedy_ctrl=ctrl)
                    for k in METRICS:
                        samples[k].append(m[k])
                    if (method == "ILCHO" and s == 0 and e == 0
                            and n_ue in (ue_list[0],
                                         ue_list[len(ue_list) // 2],
                                         ue_list[-1])):
                        per_ue_se_cache[str(n_ue)] = list(m["se_per_ue"])
            for k in METRICS:
                stats[k]["mean"].append(float(np.mean(samples[k])))
                stats[k]["std"].append(float(np.std(samples[k])))
            print(f"{method:10s} {args.constellation:18s} UE={n_ue:3d} | "
                  + " | ".join(f"{k} {np.mean(samples[k]):7.3f}"
                               for k in ("ho", "hof", "se", "jfi", "occ_var")))
        results["methods"][method] = stats

    results["ilcho_se_per_ue_cdf"] = per_ue_se_cache
    with open(os.path.join(args.out, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2)
    _plot(results, args.out)
    return results


# --------------------------------------------------------------------------- #
def _plot(res: dict, out: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ue = res["ue_list"]

    def line_fig(metric, ylabel, title, fname):
        fig, ax = plt.subplots(figsize=(6.2, 4.2))
        for m in METHOD_ORDER:
            if m not in res["methods"]:
                continue
            d = res["methods"][m][metric]
            mean = np.asarray(d["mean"]); std = np.asarray(d["std"])
            ax.plot(ue, mean, marker="o", ms=4, color=METHOD_COLOR[m], label=m)
            ax.fill_between(ue, mean - std, mean + std, color=METHOD_COLOR[m],
                            alpha=0.15)
        ax.set_xlabel("Number of UEs"); ax.set_ylabel(ylabel)
        ax.set_title(title); ax.grid(alpha=0.3); ax.legend(fontsize=8)
        fig.tight_layout(); fig.savefig(os.path.join(out, fname), dpi=120)
        plt.close(fig)

    line_fig("ho", "Number of handovers / UE",
             f"HO vs UE — {res['constellation']} (cf. Fig. 8a/9a/10a)",
             "fig_ho_vs_ue.png")
    line_fig("hof", "Number of HO failures / UE",
             f"HOF vs UE — {res['constellation']} (cf. Fig. 8b/9b/10b)",
             "fig_hof_vs_ue.png")
    line_fig("se", "Spectral efficiency [bps/Hz]",
             f"Throughput vs UE — {res['constellation']} (cf. Fig. 8c/9c/10c)",
             "fig_se_vs_ue.png")
    line_fig("occ_var", "Channel-occupancy variance",
             f"Load balance vs UE — {res['constellation']} (cf. Table IV)",
             "fig_loadvar_vs_ue.png")
    line_fig("jfi", "Jain fairness index",
             f"Fairness vs UE — {res['constellation']}", "fig_jfi_vs_ue.png")

    cdf = res.get("ilcho_se_per_ue_cdf") or {}
    if cdf:
        fig, ax = plt.subplots(figsize=(6.2, 4.2))
        for k, vals in cdf.items():
            v = np.sort(np.asarray(vals, float))
            if v.size == 0:
                continue
            y = np.arange(1, len(v) + 1) / len(v)
            jfi = v.sum() ** 2 / (len(v) * np.sum(v ** 2) + 1e-12)
            p10 = np.percentile(v, 10)
            ax.plot(v, y, label=f"{k} UEs (JFI={jfi:.3f}, p10={p10:.2f})")
        ax.set_xlabel("UE spectral efficiency [bps/Hz]"); ax.set_ylabel("CDF")
        ax.set_title(f"ILCHO throughput CDF — {res['constellation']} (cf. Fig. 11)")
        ax.grid(alpha=0.3); ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(out, "fig_fairness_cdf.png"), dpi=120)
        plt.close(fig)

    # load-balance bar at the middle UE count
    mid = len(ue) // 2
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    xs = [m for m in METHOD_ORDER if m in res["methods"]]
    ys = [res["methods"][m]["occ_var"]["mean"][mid] for m in xs]
    ax.bar(xs, ys, color=[METHOD_COLOR[m] for m in xs])
    ax.set_ylabel("Channel-occupancy variance")
    ax.set_title(f"Load balance @ {ue[mid]} UEs — {res['constellation']} "
                 f"(cf. Table IV)")
    plt.xticks(rotation=20)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_load_balance.png"),
                                    dpi=120)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--constellation", default="starlink_phase_2a",
                   choices=CONSTELLATION_NAMES)
    p.add_argument("--ues", default="5,10,20,30,40,50")
    p.add_argument("--episodes", type=int, default=4)
    p.add_argument("--seeds", type=int, default=1)
    p.add_argument("--horizon", type=int, default=600)
    p.add_argument("--n-max", type=int, default=16)
    p.add_argument("--ilcho", default="")
    p.add_argument("--ilcho-linear", default="")
    p.add_argument("--lbsh", default="")
    p.add_argument("--seed", type=int, default=123)
    p.add_argument("--device", default="cpu")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    evaluate(args)


if __name__ == "__main__":
    main()
