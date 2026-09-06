"""Assemble markdown tables + copy figures for REPORT.md from run outputs.

    uv run python scripts/make_report_tables.py
"""
from __future__ import annotations

import json
import os
import shutil

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "runs")
ASSETS = os.path.join(ROOT, "report_assets")


def _fmt_row(name, vals, w=8):
    return "| " + name.ljust(10) + " | " + " | ".join(f"{v:{w}.3f}" for v in vals) + " |"


def _series(d, metric):
    """Support both the old (list) and new ({'mean':...}) results schema."""
    v = d[metric]
    return v["mean"] if isinstance(v, dict) else v


def sweep_tables(path: str, tag: str) -> str:
    with open(os.path.join(path, "results.json"), encoding="utf-8") as fh:
        r = json.load(fh)
    ue = r["ue_list"]
    seeds = r.get("seeds", 1)
    out = [f"### {tag} - `{r['constellation']}`, "
           f"{r['episodes_per_point']} ep/point × {seeds} seed(s), "
           f"horizon {r.get('horizon_s', '?')} s\n"]
    for metric, title in [("ho", "Average # handovers per UE"),
                          ("hof", "Average # handover failures per UE"),
                          ("se", "Average spectral efficiency [bps/Hz]"),
                          ("jfi", "Jain fairness index"),
                          ("occ_var", "Channel-occupancy variance"),
                          ("unserved", "Outage fraction (UE-slots unserved)")]:
        out.append(f"\n**{title}**\n")
        out.append("| method | " + " | ".join(f"{u} UE" for u in ue) + " |")
        out.append("|" + "---|" * (len(ue) + 1))
        for m, d in r["methods"].items():
            if metric in d:
                out.append(_fmt_row(m, _series(d, metric)))
    return "\n".join(out) + "\n"


def training_summary(path: str, tag: str) -> str:
    h = np.load(os.path.join(path, "history.npz"))
    ep = h["episode"]
    n = len(ep)
    first = slice(0, max(1, n // 10))
    last = slice(max(0, n - n // 10), n)
    rows = []
    for key in ["return", "ho", "hof", "se"]:
        v = h[key]
        rows.append(f"| {key:8s} | {np.nanmean(v[first]):8.3f} | "
                    f"{np.nanmean(v[last]):8.3f} |")
    return (f"### {tag} ({int(ep[-1])} episodes)\n\n"
            "| metric | first 10% | last 10% |\n|---|---|---|\n"
            + "\n".join(rows) + "\n")


def main() -> None:
    os.makedirs(ASSETS, exist_ok=True)
    parts = ["# Auto-generated report assets\n"]

    train_runs = sorted(
        d for d in os.listdir(RUNS)
        if os.path.exists(os.path.join(RUNS, d, "history.npz"))
    )
    for run in train_runs:
        p = os.path.join(RUNS, run)
        parts.append(training_summary(p, run))
        src = os.path.join(p, "training_curves.png")
        if os.path.exists(src):
            dst = os.path.join(ASSETS, f"{run}_training_curves.png")
            shutil.copy(src, dst)
            parts.append(f"\n![{run}](report_assets/{run}_training_curves.png)\n")

    eval_dirs = sorted(d for d in os.listdir(RUNS)
                       if d.startswith(("eval_", "xeval_", "xeval2_"))
                       and os.path.exists(os.path.join(RUNS, d, "results.json")))
    for run in eval_dirs:
        p = os.path.join(RUNS, run)
        parts.append(sweep_tables(p, run))
        for f in sorted(os.listdir(p)):
            if f.endswith(".png"):
                dst = os.path.join(ASSETS, f"{run}_{f}")
                shutil.copy(os.path.join(p, f), dst)
                parts.append(f"\n![{f}](report_assets/{run}_{f})\n")

    for extra in ("analysis", "sensitivity", "sensitivity2"):
        p = os.path.join(RUNS, extra)
        if os.path.isdir(p):
            parts.append(f"\n### {extra}\n")
            for f in sorted(os.listdir(p)):
                if f.endswith(".png"):
                    dst = os.path.join(ASSETS, f"{extra}_{f}")
                    shutil.copy(os.path.join(p, f), dst)
                    parts.append(f"\n![{f}](report_assets/{extra}_{f})\n")

    with open(os.path.join(ROOT, "report_assets", "TABLES.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    print("wrote report_assets/TABLES.md and figures")


if __name__ == "__main__":
    main()
