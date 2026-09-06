"""Geometry / link-budget sanity checks against numbers quoted in the paper.

Run:  uv run ilcho-sanity
"""
from __future__ import annotations

import numpy as np

from .config import CONSTELLATIONS, ChannelConfig
from .channel import LinkBudget
from .constellation import Constellation, latlon_to_ecef, sample_ue_positions


def max_accessible(shell_key: str, region, duration_s=600, dt=5.0,
                   min_elev=30.0, n_ue=40, seed=0):
    """Peak / mean accessible-satellite count inside the region of interest."""
    rng = np.random.default_rng(seed)
    cons = Constellation(CONSTELLATIONS[shell_key])
    ue_pos, _ = sample_ue_positions(region, n_ue, rng)
    ts = np.arange(0, duration_s, dt)
    counts = []
    for t in ts:
        pos = cons.positions(float(t))
        acc = cons.access_matrix(pos, ue_pos, min_elev)      # (K, M)
        counts.append(acc.sum(axis=1))
    counts = np.concatenate(counts)
    return int(counts.max()), float(counts.mean())


def max_accessible_vs_latitude(shell_key: str, lon0=40.0, duration_s=6000,
                               dt=20.0, min_elev=30.0, seed=0):
    """Global peak accessible count over latitudes 0-90 deg (cf. Fig. 5)."""
    cons = Constellation(CONSTELLATIONS[shell_key])
    lats = np.arange(0.0, 90.0, 2.0)
    lons = np.full_like(lats, lon0)
    ue_pos = latlon_to_ecef(lats, lons)
    ts = np.arange(0, duration_s, dt)
    peak = np.zeros_like(lats)
    for t in ts:
        pos = cons.positions(float(t))
        acc = cons.access_matrix(pos, ue_pos, min_elev)      # (K, M)
        peak = np.maximum(peak, acc.sum(axis=1))
    return int(peak.max()), lats[int(np.argmax(peak))]


def link_budget_probe():
    lb = LinkBudget(ChannelConfig())
    for elev in (30.0, 45.0, 90.0):
        for alt_km in (340.0, 550.0):
            # slant range for given elevation & altitude (law of sines, sphere)
            Re = 6_371_000.0
            h = alt_km * 1_000.0
            e = np.deg2rad(elev)
            d = np.sqrt(Re**2 * np.sin(e) ** 2 + h**2 + 2 * h * Re) - Re * np.sin(e)
            pl = lb.path_loss_db(np.array([d]), np.array([elev]))
            snr = lb.snr_db(pl)
            se = lb.spectral_efficiency(snr)
            print(f"  elev={elev:4.0f} deg  alt={alt_km:5.0f} km  "
                  f"d={d/1e3:7.1f} km  PL={pl[0]:6.1f} dB  "
                  f"SNR={snr[0]:6.2f} dB  SE={se[0]:5.2f} bps/Hz")


def main() -> None:
    region = (39.0, 41.0, 39.0, 41.0)
    print("=== Accessible LEO satellites inside region [39-41 N] ===")
    for key, ref in (("starlink_phase_1a", 17), ("starlink_phase_2a", 27)):
        mx, mean = max_accessible(key, region)
        print(f"  {key:20s}: region-max={mx:3d}  region-mean={mean:5.2f}")

    print("\n=== Global peak accessible count over latitude 0-90 (cf. Fig. 5) ===")
    for key, ref in (("starlink_phase_1a", 17), ("starlink_phase_2a", 27)):
        mx, lat = max_accessible_vs_latitude(key)
        print(f"  {key:20s}: peak={mx:3d} at lat={lat:4.1f} deg   "
              f"(paper N_max={ref})")

    print("\n=== Link-budget probe (cf. throughput ~3.7-3.85 bps/Hz) ===")
    link_budget_probe()


if __name__ == "__main__":
    main()
