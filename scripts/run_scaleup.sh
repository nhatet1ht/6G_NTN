#!/usr/bin/env bash
# Scale-up run toward the paper's regime, sized to finish in ~5-7 h wall-clock
# on this CPU.  Made feasible by: vectorised episode geometry (~10x), fused
# nn.GRU + compact pooled mixer state, memory-aware float16 replay,
# learn-every-2 and a 450 s training horizon.
#
#   N_max = 27 (paper), 48 agents, 450 s training episodes (paper eval: 600 s).
#
# Produces runs/su_* and runs/xeval2_* ; regenerates report_assets at the end.
set -uo pipefail
cd "$(dirname "$0")/.."
export UV_LINK_MODE=copy
export PYTHONUNBUFFERED=1

AG=48
NMAX=27
HZ=420
LE=3
BATCH=12
UES=${UES:-5,20,40,70,100}
EVAL_SEEDS=${EVAL_SEEDS:-3}
EVAL_EP=${EVAL_EP:-3}

common="--mode qmix --train-ues $AG --horizon $HZ --n-max $NMAX --learn-every $LE --batch $BATCH"

echo "############ [1/6] ILCHO sigmoid — ${AG} agents, 2800 ep ############ $(date)"
uv run ilcho-train --reward sigmoid $common --episodes 2800 --eps-anneal 1700 \
    --seed 0 --out runs/su_ilcho_sigmoid || echo "FAILED su_ilcho_sigmoid"

echo "############ [2/6] ILCHO linear (Eq. 30 ablation) — 2000 ep ############ $(date)"
uv run ilcho-train --reward linear $common --episodes 2000 --eps-anneal 1200 \
    --seed 0 --out runs/su_ilcho_linear || echo "FAILED su_ilcho_linear"

echo "############ [3/6] LBSH (IQL) — 2000 ep ############ $(date)"
uv run ilcho-train --mode iql --train-ues $AG --horizon $HZ --n-max $NMAX \
    --learn-every $LE --batch $BATCH --episodes 2000 --eps-anneal 1200 \
    --seed 0 --out runs/su_lbsh || echo "FAILED su_lbsh"

echo "############ [4/6] diagnostics (Fig. 5 / HO interval / link budget) ############ $(date)"
uv run python -m ilcho.analysis --out runs/analysis || echo "FAILED analysis"

for C in starlink_phase_2a starlink_phase_1a hybrid; do
  echo "############ [5/6] eval sweep: $C ############ $(date)"
  uv run ilcho-eval --constellation "$C" --ues "$UES" \
      --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon 600 --n-max "$NMAX" \
      --ilcho runs/su_ilcho_sigmoid/policy.pt \
      --ilcho-linear runs/su_ilcho_linear/policy.pt \
      --lbsh runs/su_lbsh/policy.pt \
      --out "runs/xeval2_$C" || echo "FAILED xeval2_$C"
done

echo "############ [6/6] matched reward ablation + sensitivity ############ $(date)"
uv run ilcho-eval --constellation starlink_phase_2a --ues "$UES" \
    --episodes "$EVAL_EP" --seeds "$EVAL_SEEDS" --horizon 600 --n-max "$NMAX" \
    --ilcho runs/su_ilcho_sigmoid/policy.pt \
    --ilcho-linear runs/su_ilcho_linear/policy.pt \
    --out runs/xeval2_reward_ablation || echo "FAILED xeval2_reward_ablation"

uv run python -m ilcho.sensitivity --ilcho runs/su_ilcho_sigmoid/policy.pt \
    --constellation starlink_phase_2a --n-ue 50 --horizon 600 --episodes 3 \
    --n-max "$NMAX" --out runs/sensitivity2 || echo "FAILED sensitivity2"

uv run python scripts/make_report_tables.py || true
echo "### SCALE-UP DONE -- $(date)"
