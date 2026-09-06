#!/usr/bin/env bash
# Runs after runs/ilcho_sigmoid_v2 finishes: linear-reward ablation, LBSH,
# and both evaluation sweeps.  Waits for the v2 policy to appear first.
set -uo pipefail
cd "$(dirname "$0")/.."
export UV_LINK_MODE=copy
export PYTHONUNBUFFERED=1

echo "waiting for runs/ilcho_sigmoid_v2/policy.pt ..."
while [ ! -f runs/ilcho_sigmoid_v2/policy.pt ]; do sleep 20; done
echo "v2 done -- continuing $(date)"

echo "############ linear-reward ablation (Eq. 30) ############"
uv run ilcho-train --reward linear --mode qmix --episodes 800 \
    --train-ues 12 --horizon 300 --eps-anneal 450 --seed 0 \
    --out runs/ilcho_linear || echo "linear train FAILED"

echo "############ LBSH (IQL + load-balance reward) ############"
uv run ilcho-train --mode iql --episodes 800 \
    --train-ues 12 --horizon 300 --eps-anneal 450 --seed 0 \
    --out runs/lbsh || echo "lbsh train FAILED"

echo "############ evaluation: Starlink Phase 2-a ############"
uv run ilcho-eval --constellation starlink_phase_2a --ues 5,10,20,30,40,50 \
    --episodes 5 --horizon 600 \
    --ilcho runs/ilcho_sigmoid_v2/policy.pt --lbsh runs/lbsh/policy.pt \
    --out runs/eval_phase2a || echo "eval p2a FAILED"

echo "############ evaluation: Starlink Phase 1-a ############"
uv run ilcho-eval --constellation starlink_phase_1a --ues 5,10,20,30,40,50 \
    --episodes 5 --horizon 600 \
    --ilcho runs/ilcho_sigmoid_v2/policy.pt --lbsh runs/lbsh/policy.pt \
    --out runs/eval_phase1a || echo "eval p1a FAILED"

echo "############ report assets ############"
uv run python scripts/make_report_tables.py || echo "tables FAILED"
echo "ALL DONE $(date)"
