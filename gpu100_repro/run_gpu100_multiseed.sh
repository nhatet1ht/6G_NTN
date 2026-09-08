#!/usr/bin/env bash
# Multi-seed extension of run_gpu100.sh (A2 in CHUA_LAM_DUOC.md).
#
# seed=0 already exists (runs/g100_ilcho_sigmoid, g100_ilcho_linear, g100_lbsh --
# the round-3 primary policies). This script trains seed=1 and seed=2 for each
# of the 3 policies with IDENTICAL hyperparameters (100 agents, N_max=27,
# horizon=600s, batch=8, learn-every=1, device=cuda), then evaluates each new
# seed's trio on Starlink Phase 2-a (the primary comparison scenario, Fig. 8)
# so a cross-seed mean+-std of the final policy can be computed.
set -uo pipefail
cd "$(dirname "$0")/.."
HERE="gpu100_repro"
PY="/tmp/gpu_bench/.venv/Scripts/python.exe"
BIN="/tmp/gpu_bench/.venv/Scripts"
export PYTHONUNBUFFERED=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

AG=100
NMAX=27
HZ=600
LE=1
BATCH=8
DEV=cuda
UES=${UES:-5,20,40,70,100}
EVAL_SEEDS=${EVAL_SEEDS:-3}
EVAL_EP=${EVAL_EP:-3}
SEEDS=${SEEDS:-"1 2"}

common="--mode qmix --train-ues $AG --horizon $HZ --n-max $NMAX --learn-every $LE --batch $BATCH --device $DEV"

for SEED in $SEEDS; do
  echo "############ [seed=$SEED 1/4] ILCHO sigmoid -- 4000 ep ############ $(date)"
  "$BIN/ilcho-train" --reward sigmoid $common --episodes 4000 --eps-anneal 2400 \
      --seed "$SEED" --out "$HERE/runs/g100_ilcho_sigmoid_seed${SEED}" \
      || echo "FAILED g100_ilcho_sigmoid_seed${SEED}"

  echo "############ [seed=$SEED 2/4] ILCHO linear -- 3000 ep ############ $(date)"
  "$BIN/ilcho-train" --reward linear $common --episodes 3000 --eps-anneal 1800 \
      --seed "$SEED" --out "$HERE/runs/g100_ilcho_linear_seed${SEED}" \
      || echo "FAILED g100_ilcho_linear_seed${SEED}"

  echo "############ [seed=$SEED 3/4] LBSH (IQL) -- 3000 ep ############ $(date)"
  "$BIN/ilcho-train" --mode iql --train-ues $AG --horizon $HZ --n-max $NMAX \
      --learn-every $LE --batch $BATCH --device $DEV --episodes 3000 --eps-anneal 1800 \
      --seed "$SEED" --out "$HERE/runs/g100_lbsh_seed${SEED}" \
      || echo "FAILED g100_lbsh_seed${SEED}"

  echo "############ [seed=$SEED 4/4] eval Phase 2-a ############ $(date)"
  "$BIN/ilcho-eval" --constellation starlink_phase_2a --ues "$UES" \
      --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon $HZ --n-max "$NMAX" \
      --device $DEV \
      --ilcho "$HERE/runs/g100_ilcho_sigmoid_seed${SEED}/policy.pt" \
      --ilcho-linear "$HERE/runs/g100_ilcho_linear_seed${SEED}/policy.pt" \
      --lbsh "$HERE/runs/g100_lbsh_seed${SEED}/policy.pt" \
      --out "$HERE/runs/g100_eval_starlink_phase_2a_seed${SEED}" \
      || echo "FAILED g100_eval_starlink_phase_2a_seed${SEED}"
done

echo "############ aggregate cross-seed mean+-std ############ $(date)"
"$PY" "$HERE/aggregate_multiseed.py" || echo "FAILED aggregate_multiseed"
echo "### MULTISEED RUN DONE -- $(date)"
