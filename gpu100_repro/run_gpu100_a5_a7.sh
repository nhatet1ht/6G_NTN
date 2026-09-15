#!/usr/bin/env bash
# Closes 2 of the remaining open items in CHUA_LAM_DUOC.md:
#
#   A5 — train ILCHO natively on Phase 1-a and on hybrid (previously only
#        zero-shot transfer from a Phase 2-a-trained policy was tested).
#   A7 — one point on the batch/learn-every trade-off axis not yet tried:
#        batch=4 (half of the round-3 batch=8) at the same learn-every=1,
#        same episode budget, same everything else, to see if the smaller
#        batch changes the converged policy.
#
# (A1 needs >8GB VRAM or a code change (truncated BPTT) -- not just a run.
#  A2's remaining 2 seeds and A3 (re-implementing HSNF/LBSH from their
#  original references) are left for later -- see CHUA_LAM_DUOC.md.)
#
# All hyperparameters match round 3 exactly except the one axis under test.
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
DEV=cuda
UES=${UES:-5,20,40,70,100}
EVAL_SEEDS=${EVAL_SEEDS:-3}
EVAL_EP=${EVAL_EP:-3}

echo "############ [A5 1/4] native train: Phase 1-a, 3000 ep ############ $(date)"
"$BIN/ilcho-train" --constellation starlink_phase_1a --reward sigmoid --mode qmix \
    --train-ues $AG --horizon $HZ --n-max $NMAX --learn-every $LE --batch 8 --device $DEV \
    --episodes 3000 --eps-anneal 1800 --seed 0 \
    --out "$HERE/runs/g100_ilcho_sigmoid_native_phase1a" \
    || echo "FAILED native_phase1a train"

echo "############ [A5 2/4] eval native Phase 1-a policy on Phase 1-a ############ $(date)"
"$BIN/ilcho-eval" --constellation starlink_phase_1a --ues "$UES" \
    --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon $HZ --n-max "$NMAX" --device $DEV \
    --ilcho "$HERE/runs/g100_ilcho_sigmoid_native_phase1a/policy.pt" \
    --out "$HERE/runs/g100_eval_starlink_phase_1a_native" \
    || echo "FAILED native_phase1a eval"

echo "############ [A5 3/4] native train: hybrid, 3000 ep ############ $(date)"
"$BIN/ilcho-train" --constellation hybrid --reward sigmoid --mode qmix \
    --train-ues $AG --horizon $HZ --n-max $NMAX --learn-every $LE --batch 8 --device $DEV \
    --episodes 3000 --eps-anneal 1800 --seed 0 \
    --out "$HERE/runs/g100_ilcho_sigmoid_native_hybrid" \
    || echo "FAILED native_hybrid train"

echo "############ [A5 4/4] eval native hybrid policy on hybrid ############ $(date)"
"$BIN/ilcho-eval" --constellation hybrid --ues "$UES" \
    --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon $HZ --n-max "$NMAX" --device $DEV \
    --ilcho "$HERE/runs/g100_ilcho_sigmoid_native_hybrid/policy.pt" \
    --out "$HERE/runs/g100_eval_hybrid_native" \
    || echo "FAILED native_hybrid eval"

echo "############ [A7 1/2] batch=4 (vs batch=8 round-3), 4000 ep, Phase 2-a ############ $(date)"
"$BIN/ilcho-train" --constellation starlink_phase_2a --reward sigmoid --mode qmix \
    --train-ues $AG --horizon $HZ --n-max $NMAX --learn-every $LE --batch 4 --device $DEV \
    --episodes 4000 --eps-anneal 2400 --seed 0 \
    --out "$HERE/runs/g100_ilcho_sigmoid_batch4" \
    || echo "FAILED batch4 train"

echo "############ [A7 2/2] eval batch=4 policy on Phase 2-a ############ $(date)"
"$BIN/ilcho-eval" --constellation starlink_phase_2a --ues "$UES" \
    --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon $HZ --n-max "$NMAX" --device $DEV \
    --ilcho "$HERE/runs/g100_ilcho_sigmoid_batch4/policy.pt" \
    --out "$HERE/runs/g100_eval_starlink_phase_2a_batch4" \
    || echo "FAILED batch4 eval"

echo "### A5+A7 RUN DONE -- $(date)"
