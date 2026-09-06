#!/usr/bin/env bash
# End-to-end reproduction pipeline.
#   bash scripts/run_all.sh
# Produces trained policies under runs/ and evaluation output under runs/eval_*.
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_LINK_MODE=copy
export PYTHONUNBUFFERED=1

EP_ILCHO=${EP_ILCHO:-1200}
EP_LIN=${EP_LIN:-900}
EP_LBSH=${EP_LBSH:-900}
HZ=${HZ:-300}
UES=${UES:-5,10,20,30,40,50}
EVAL_EP=${EVAL_EP:-6}

echo "############ 1/5  train ILCHO (QMIX, sigmoid reward, Eq. 27) ############"
uv run ilcho-train --reward sigmoid --mode qmix --episodes "$EP_ILCHO" \
    --train-ues 10 --horizon "$HZ" --eps-anneal 600 --seed 0 \
    --out runs/ilcho_sigmoid

echo "############ 2/5  train ILCHO (QMIX, linear reward, Eq. 30) #############"
uv run ilcho-train --reward linear --mode qmix --episodes "$EP_LIN" \
    --train-ues 10 --horizon "$HZ" --eps-anneal 500 --seed 0 \
    --out runs/ilcho_linear

echo "############ 3/5  train LBSH (IQL + load-balance reward, [26]) ##########"
uv run ilcho-train --mode iql --episodes "$EP_LBSH" \
    --train-ues 10 --horizon "$HZ" --eps-anneal 500 --seed 0 \
    --out runs/lbsh

echo "############ 4/5  evaluation sweep (Starlink Phase 2-a) ################"
uv run ilcho-eval --constellation starlink_phase_2a --ues "$UES" \
    --episodes "$EVAL_EP" --horizon 600 \
    --ilcho runs/ilcho_sigmoid/policy.pt --lbsh runs/lbsh/policy.pt \
    --out runs/eval_phase2a

echo "############ 5/5  evaluation sweep (Starlink Phase 1-a) ################"
uv run ilcho-eval --constellation starlink_phase_1a --ues "$UES" \
    --episodes "$EVAL_EP" --horizon 600 \
    --ilcho runs/ilcho_sigmoid/policy.pt --lbsh runs/lbsh/policy.pt \
    --out runs/eval_phase1a

echo "DONE."
