#!/usr/bin/env bash
# GPU-accelerated scale-up toward the paper's full regime (RTX 3060 Ti + i5-12400F).
#
#   100 agents (paper max), N_max = 27 (paper, Phase 2-a), horizon = 600 s for
#   BOTH training and evaluation (paper Table II T_s = 600 s -- previous rounds
#   trained at 300-420 s and only evaluated at 600 s; this round removes that
#   deviation).  learn() runs on CUDA every episode (batch=8, VRAM-limited on
#   an 8 GB card at K=100/T=600 -- see report_assets/../REPORT.md for the
#   benchmark that picked this).  Rollout (action selection) cost is the same
#   on CPU or GPU for this workload (tiny per-step forward pass, Python-loop
#   bound) so the whole controller just lives on 'cuda' for simplicity.
#
# Uses a separate GPU-enabled venv (torch+cu126) at /tmp/gpu_bench/.venv --
# the project's own `uv sync` environment stays CPU-only / paper-independent
# of any GPU, per pyproject.toml. All outputs are self-contained under
# gpu100_repro/ so they never overwrite runs/ or REPORT.md from the earlier
# CPU-only rounds.
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

common="--mode qmix --train-ues $AG --horizon $HZ --n-max $NMAX --learn-every $LE --batch $BATCH --device $DEV"

echo "############ [0/7] geometry / link-budget sanity ############ $(date)"
"$PY" -m ilcho.sanity || echo "FAILED sanity"
"$PY" -m ilcho.analysis --out "$HERE/runs/analysis" || echo "FAILED analysis"

echo "############ [1/7] ILCHO sigmoid -- 100 agents, 600s, 4000 ep ############ $(date)"
"$BIN/ilcho-train" --reward sigmoid $common --episodes 4000 --eps-anneal 2400 \
    --seed 0 --out "$HERE/runs/g100_ilcho_sigmoid" || echo "FAILED g100_ilcho_sigmoid"

echo "############ [2/7] ILCHO linear (Eq. 30 ablation) -- 3000 ep ############ $(date)"
"$BIN/ilcho-train" --reward linear $common --episodes 3000 --eps-anneal 1800 \
    --seed 0 --out "$HERE/runs/g100_ilcho_linear" || echo "FAILED g100_ilcho_linear"

echo "############ [3/7] LBSH (IQL) -- 3000 ep ############ $(date)"
"$BIN/ilcho-train" --mode iql --train-ues $AG --horizon $HZ --n-max $NMAX \
    --learn-every $LE --batch $BATCH --device $DEV --episodes 3000 --eps-anneal 1800 \
    --seed 0 --out "$HERE/runs/g100_lbsh" || echo "FAILED g100_lbsh"

for C in starlink_phase_2a starlink_phase_1a hybrid; do
  echo "############ [4/7] eval sweep: $C ############ $(date)"
  "$BIN/ilcho-eval" --constellation "$C" --ues "$UES" \
      --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon $HZ --n-max "$NMAX" \
      --device $DEV \
      --ilcho "$HERE/runs/g100_ilcho_sigmoid/policy.pt" \
      --ilcho-linear "$HERE/runs/g100_ilcho_linear/policy.pt" \
      --lbsh "$HERE/runs/g100_lbsh/policy.pt" \
      --out "$HERE/runs/g100_eval_$C" || echo "FAILED g100_eval_$C"
done

echo "############ [5/7] matched reward ablation ############ $(date)"
"$BIN/ilcho-eval" --constellation starlink_phase_2a --ues "$UES" \
    --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon $HZ --n-max "$NMAX" \
    --device $DEV \
    --ilcho "$HERE/runs/g100_ilcho_sigmoid/policy.pt" \
    --ilcho-linear "$HERE/runs/g100_ilcho_linear/policy.pt" \
    --out "$HERE/runs/g100_reward_ablation" || echo "FAILED g100_reward_ablation"

echo "############ [6/7] sensitivity (50 UE, Phase 2-a) ############ $(date)"
"$PY" -m ilcho.sensitivity --ilcho "$HERE/runs/g100_ilcho_sigmoid/policy.pt" \
    --constellation starlink_phase_2a --n-ue 50 --horizon $HZ --episodes 3 \
    --n-max "$NMAX" --device $DEV --out "$HERE/runs/g100_sensitivity" || echo "FAILED g100_sensitivity"

echo "############ [7/7] report tables ############ $(date)"
"$PY" "$HERE/make_report_tables_gpu100.py" || true
echo "### GPU100 RUN DONE -- $(date)"
