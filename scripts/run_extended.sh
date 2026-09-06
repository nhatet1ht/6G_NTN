#!/usr/bin/env bash
# Extended experiment suite.  Chains after scripts/run_rest.sh:
#   - retrains ILCHO with a rebalanced sigmoid reward (v3)
#   - large multi-seed UE sweeps (5..100) on Phase 2-a / Phase 1-a / hybrid
#   - OneWeb spot check
#   - parameter sensitivity study
#   - diagnostic analyses (Fig. 5, HO-interval, link budget)
#   - regenerates report tables
set -uo pipefail
cd "$(dirname "$0")/.."
export UV_LINK_MODE=copy
export PYTHONUNBUFFERED=1

echo "### waiting for base pipeline (runs/lbsh/policy.pt) ..."
while [ ! -f runs/lbsh/policy.pt ]; do sleep 30; done
sleep 5
echo "### base pipeline done -- $(date)"

SIG=runs/ilcho_sigmoid_v3
LIN=runs/ilcho_linear/policy.pt
LBSH=runs/lbsh/policy.pt

echo "############ retrain ILCHO -- rebalanced sigmoid reward (v3) ############"
uv run ilcho-train --reward sigmoid --mode qmix --episodes 1800 \
    --train-ues 16 --horizon 300 --eps-anneal 900 --seed 0 \
    --out "$SIG" || echo "v3 train FAILED"

echo "############ diagnostics (Fig. 5 / HO interval / link budget) ############"
uv run python -m ilcho.analysis --out runs/analysis || echo "analysis FAILED"

for C in starlink_phase_2a starlink_phase_1a hybrid; do
  echo "############ big sweep: $C ############"
  uv run ilcho-eval --constellation "$C" --ues 5,10,20,30,50,75,100 \
      --episodes 3 --seeds 3 --horizon 600 --n-max 16 \
      --ilcho "$SIG/policy.pt" --ilcho-linear "$LIN" --lbsh "$LBSH" \
      --out "runs/xeval_$C" || echo "sweep $C FAILED"
done

echo "############ OneWeb spot check ############"
uv run ilcho-eval --constellation oneweb_phase_1 --ues 5,20,50 \
    --episodes 3 --seeds 2 --horizon 600 --n-max 16 \
    --ilcho "$SIG/policy.pt" --ilcho-linear "$LIN" --lbsh "$LBSH" \
    --out runs/xeval_oneweb_phase_1 || echo "oneweb FAILED"

echo "############ sensitivity study ############"
uv run python -m ilcho.sensitivity --ilcho "$SIG/policy.pt" \
    --constellation starlink_phase_2a --n-ue 30 --horizon 600 --episodes 4 \
    --out runs/sensitivity || echo "sensitivity FAILED"

echo "############ report tables ############"
uv run python scripts/make_report_tables.py || echo "tables FAILED"
echo "### EXTENDED SUITE DONE -- $(date)"
