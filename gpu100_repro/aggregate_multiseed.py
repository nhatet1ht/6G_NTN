"""Aggregate cross-training-seed mean+-std for the multi-seed extension (A2).

Combines seed=0 (runs/g100_eval_starlink_phase_2a, from the round-3 primary
run) with seed=1, seed=2 (runs/g100_eval_starlink_phase_2a_seed{1,2}, from
run_gpu100_multiseed.sh) into a mean +- std ACROSS TRAINING SEEDS, for every
UE count and every metric -- distinct from the within-run std across eval
seeds that each results.json already carries.

    /tmp/gpu_bench/.venv/Scripts/python.exe gpu100_repro/aggregate_multiseed.py
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")

SEED_DIRS = {
    0: "g100_eval_starlink_phase_2a",
    1: "g100_eval_starlink_phase_2a_seed1",
    2: "g100_eval_starlink_phase_2a_seed2",
}
METRICS = ("ho", "hof", "se", "jfi", "occ_var", "unserved")
# ILCHO/ILCHO-lin/LBSH depend on the training seed; MD-CHO/MVT-CHO/HSNF don't
# (rule-based, not learned) -- kept as a sanity check that they stay put.
METHOD_ORDER = ["ILCHO", "ILCHO-lin", "LBSH", "MD-CHO", "MVT-CHO", "HSNF"]


def main() -> None:
    loaded = {}
    for seed, d in SEED_DIRS.items():
        p = os.path.join(RUNS, d, "results.json")
        if not os.path.exists(p):
            print(f"[skip] seed={seed}: {p} not found")
            continue
        with open(p, encoding="utf-8") as fh:
            loaded[seed] = json.load(fh)

    if len(loaded) < 2:
        print("Need at least 2 seed runs to aggregate -- found", len(loaded))
        return

    seeds = sorted(loaded)
    ue_list = loaded[seeds[0]]["ue_list"]
    out = {"seeds_used": seeds, "ue_list": ue_list, "methods": {}}

    lines = [f"# Cross-training-seed aggregate (seeds={seeds})\n",
             f"Starlink Phase 2-a, UE = {ue_list}\n"]

    for method in METHOD_ORDER:
        if not all(method in loaded[s]["methods"] for s in seeds):
            continue
        out["methods"][method] = {}
        for metric in METRICS:
            per_ue_mean, per_ue_std, per_ue_raw = [], [], []
            for i, _ue in enumerate(ue_list):
                vals = [loaded[s]["methods"][method][metric]["mean"][i] for s in seeds]
                per_ue_raw.append(vals)
                per_ue_mean.append(float(np.mean(vals)))
                per_ue_std.append(float(np.std(vals)))
            out["methods"][method][metric] = {
                "mean": per_ue_mean, "std_across_seeds": per_ue_std,
                "per_seed": per_ue_raw,
            }

        lines.append(f"\n## {method}\n")
        for metric in ("hof", "se", "ho"):
            d = out["methods"][method][metric]
            row = " | ".join(f"{m:.2f}±{s:.2f}" for m, s in
                             zip(d["mean"], d["std_across_seeds"]))
            lines.append(f"- **{metric}**: {row}  (UE={ue_list})")

    with open(os.path.join(RUNS, "multiseed_aggregate.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    with open(os.path.join(RUNS, "multiseed_aggregate.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote runs/multiseed_aggregate.{json,md}")


if __name__ == "__main__":
    main()
