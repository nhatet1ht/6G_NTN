#!/usr/bin/env bash
# Apples-to-apples sigmoid (Eq. 27) vs linear (Eq. 30) reward ablation:
# both policies trained with identical settings (16 agents, 1800 episodes).
# Waits for both policies, then runs a head-to-head sweep + copies training
# curves side by side.
set -uo pipefail
cd "$(dirname "$0")/.."
export UV_LINK_MODE=copy
export PYTHONUNBUFFERED=1

echo "### waiting for ilcho_sigmoid_v3 + ilcho_linear_v3 policies ..."
while [ ! -f runs/ilcho_sigmoid_v3/policy.pt ] || [ ! -f runs/ilcho_linear_v3/policy.pt ]; do
  sleep 30
done
sleep 5
echo "### both ready -- $(date)"

uv run ilcho-eval --constellation starlink_phase_2a --ues 5,10,20,30,50,75,100 \
    --episodes 3 --seeds 3 --horizon 600 --n-max 16 \
    --ilcho runs/ilcho_sigmoid_v3/policy.pt \
    --ilcho-linear runs/ilcho_linear_v3/policy.pt \
    --out runs/xeval_reward_ablation || echo "ablation eval FAILED"

uv run python scripts/make_report_tables.py || true
echo "### ABLATION DONE -- $(date)"
