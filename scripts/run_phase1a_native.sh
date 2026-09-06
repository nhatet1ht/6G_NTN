#!/usr/bin/env bash
# Train an ILCHO policy *natively* on Starlink Phase 1-a (the base pipeline only
# trained on Phase 2-a and evaluated Phase 1-a zero-shot).  Waits until the two
# v3 trainings free a CPU slot.
set -uo pipefail
cd "$(dirname "$0")/.."
export UV_LINK_MODE=copy
export PYTHONUNBUFFERED=1

echo "### waiting for v3 trainings to finish (frees CPU) ..."
while [ ! -f runs/ilcho_sigmoid_v3/policy.pt ] || [ ! -f runs/ilcho_linear_v3/policy.pt ]; do
  sleep 60
done
sleep 5
echo "### training ILCHO on Phase 1-a -- $(date)"

uv run ilcho-train --constellation starlink_phase_1a --reward sigmoid --mode qmix \
    --episodes 1500 --train-ues 16 --horizon 300 --eps-anneal 800 --seed 0 \
    --out runs/ilcho_sigmoid_v3_p1a || echo "p1a train FAILED"

uv run ilcho-eval --constellation starlink_phase_1a --ues 5,10,20,30,50,75,100 \
    --episodes 3 --seeds 3 --horizon 600 --n-max 16 \
    --ilcho runs/ilcho_sigmoid_v3_p1a/policy.pt \
    --lbsh runs/lbsh/policy.pt \
    --out runs/xeval_phase1a_native || echo "p1a eval FAILED"

uv run python scripts/make_report_tables.py || true
echo "### PHASE-1A NATIVE DONE -- $(date)"
