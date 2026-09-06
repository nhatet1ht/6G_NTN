"""Diagnostic analyses that back up the reproduction (not in the paper's main
comparison but referenced by it).

    uv run python -m ilcho.analysis --out runs/analysis
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from .config import CONSTELLATIONS, ChannelConfig, EnvConfig, resolve_constellation
from .channel import LinkBudget
from .constellation import Constellation, latlon_to_ecef
from .environment import CHOEnv
from .baselines import MDCHO


def accessible_vs_latitude(out: str) -> dict:
    """Reproduce Fig. 5: mean & peak accessible satellites vs UE latitude."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    res = {}
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for j, key in enumerate(("starlink_phase_1a", "starlink_phase_2a")):
        cons = Constellation(CONSTELLATIONS[key])
        lats = np.arange(0.0, 90.0, 2.0)
        ue = latlon_to_ecef(lats, np.full_like(lats, 40.0))
        ts = np.arange(0, 6000, 15.0)
        counts = np.zeros((len(ts), len(lats)))
        for i, t in enumerate(ts):
            acc = cons.access_matrix(cons.positions(float(t)), ue, 30.0)
            counts[i] = acc.sum(axis=1)
        mean_c, peak_c = counts.mean(axis=0), counts.max(axis=0)
        res[key] = {"lat": lats.tolist(), "mean": mean_c.tolist(),
                    "peak": peak_c.tolist(), "global_peak": float(peak_c.max())}
        ax[j].plot(lats, mean_c, "-o", ms=3, label="mean")
        ax[j].plot(lats, peak_c, "--s", ms=3, label="peak (N_max)")
        ax[j].set_title(f"{key}  (global peak = {peak_c.max():.0f})")
        ax[j].set_xlabel("UE latitude [deg]")
        ax[j].set_ylabel("# accessible LEO satellites")
        ax[j].grid(alpha=0.3); ax[j].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig5_accessible_vs_latitude.png"), dpi=120)
    plt.close(fig)
    return res


def ho_interval_distribution(out: str, constellation="starlink_phase_2a",
                             n_ue=30, horizon=600, episodes=6) -> dict:
    """Distribution of time between consecutive HOs for a UE (paper: the UE
    'relative location' drives a HO every 6.61-132.28 s, TR 38.821)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    intervals = []
    dwell = []
    for ep in range(episodes):
        env = CHOEnv(EnvConfig(num_ues=n_ue, service_duration_s=horizon,
                               n_max=16),
                     resolve_constellation(constellation), ChannelConfig(),
                     seed=1000 + ep)
        obs, av = env.reset(ue_seed=1000 + ep)
        pol = MDCHO(16)
        last_ho = np.full(n_ue, -1)
        serving_since = np.zeros(n_ue)
        for t in range(env.T):
            obs, av, r, d, info = env.step(pol.act(obs, av))
            for k in np.where(info.ho)[0]:
                if last_ho[k] >= 0:
                    intervals.append(t - last_ho[k])
                last_ho[k] = t
            if d:
                break
    intervals = np.asarray(intervals, float)
    res = {
        "constellation": constellation, "n_samples": int(intervals.size),
        "min": float(intervals.min()) if intervals.size else None,
        "max": float(intervals.max()) if intervals.size else None,
        "mean": float(intervals.mean()) if intervals.size else None,
        "median": float(np.median(intervals)) if intervals.size else None,
        "paper_range_s": [6.61, 132.28],
    }
    if intervals.size:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(intervals, bins=40, color="tab:blue", alpha=0.8)
        ax.axvline(6.61, color="k", ls="--", label="paper min 6.61 s")
        ax.axvline(132.28, color="r", ls="--", label="paper max 132.28 s")
        ax.set_xlabel("Time between consecutive HOs [s] (MD-CHO)")
        ax.set_ylabel("count"); ax.set_title(f"HO interval — {constellation}")
        ax.legend(); ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(out, "ho_interval_hist.png"), dpi=120)
        plt.close(fig)
    return res


def link_budget_curve(out: str) -> dict:
    """Spectral efficiency vs elevation for both altitudes."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lb = LinkBudget(ChannelConfig())
    Re = 6_371_000.0
    elevs = np.linspace(30, 90, 40)
    fig, ax = plt.subplots(figsize=(6, 4))
    res = {}
    for alt in (340.0, 550.0, 1200.0):
        h = alt * 1e3
        e = np.deg2rad(elevs)
        d = np.sqrt(Re**2 * np.sin(e) ** 2 + h**2 + 2 * h * Re) - Re * np.sin(e)
        se = lb.spectral_efficiency(lb.snr_db(lb.path_loss_db(d, elevs)))
        ax.plot(elevs, se, label=f"{alt:.0f} km")
        res[f"{alt:.0f}km"] = {"elev": elevs.tolist(), "se": se.tolist()}
    ax.set_xlabel("Elevation angle [deg]")
    ax.set_ylabel("Spectral efficiency [bps/Hz]")
    ax.set_title("Link budget (Eq. 8-13); paper avg ~3.76-3.85 bps/Hz")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out, "link_budget_vs_elevation.png"), dpi=120)
    plt.close(fig)
    return res


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="runs/analysis")
    args = p.parse_args()
    os.makedirs(args.out, exist_ok=True)
    summary = {
        "accessible_vs_latitude": accessible_vs_latitude(args.out),
        "ho_interval": ho_interval_distribution(args.out),
        "link_budget": {k: "see figure" for k in ("340km", "550km", "1200km")},
    }
    link_budget_curve(args.out)
    with open(os.path.join(args.out, "analysis.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps({k: v for k, v in summary.items()
                      if k != "accessible_vs_latitude"}, indent=2))
    print("global peaks:",
          {k: v["global_peak"]
           for k, v in summary["accessible_vs_latitude"].items()})


if __name__ == "__main__":
    main()
