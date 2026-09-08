# ILCHO reproduction

Reproduction of

> M. Choi, M. Park, J. Kim, J.-M. Chung,
> **"Intelligent Handover Scheme for Improved 6G NTN LEO Satellite Network
> Performance,"** *IEEE Transactions on Mobile Computing*, vol. 25, no. 5,
> May 2026, pp. 6863–6880.

The paper proposes **ILCHO** = 3GPP Conditional Handover (CHO) + multi-agent
reinforcement learning (**QMIX**) for target-satellite selection in a
mega-constellation LEO non-terrestrial network.

## What is implemented

| Paper element | Module |
|---|---|
| Walker-Delta geometry, satellite state (Lemma 1) | `ilcho/constellation.py` |
| Accessibility via min. elevation angle (Lemma 2) | `ilcho/constellation.py` |
| Remaining visible time (RVT) from ephemeris | `ilcho/constellation.py` |
| 3GPP TR 38.811/38.821 link budget, Shannon rate (Eq. 8–13) | `ilcho/channel.py` |
| CHO multi-agent env, distance-based execution event (Eq. 28) | `ilcho/environment.py` |
| Sigmoid reward (Eq. 27) / linear reward ablation (Eq. 30) | `ilcho/environment.py` |
| QMIX learner (DRQN agents + monotonic mixer), IQL variant | `ilcho/qmix.py` |
| Baselines MD-CHO, MVT-CHO, HSNF | `ilcho/baselines.py` |
| Metrics: HO, HOF, spectral efficiency, Jain fairness, load variance | `ilcho/environment.py` |

## Environment

```bash
uv sync                     # installs numpy, torch (CPU), matplotlib, ...
uv run ilcho-sanity         # geometry / link-budget checks vs. the paper
```

## Reproduce

Full pipeline actually used (each step waits on the previous one's output):

```bash
bash scripts/run_rest.sh              # train sigmoid v2/linear/lbsh + base eval sweeps
bash scripts/run_extended.sh          # train sigmoid v3 (primary) + big sweeps + sensitivity
bash scripts/run_ablation.sh          # matched sigmoid-vs-linear ablation (v3-scale)
bash scripts/run_phase1a_native.sh    # ILCHO trained natively on Phase 1-a
uv run python scripts/make_report_tables.py   # -> report_assets/{TABLES.md,*.png}
```

Individual steps:

```bash
uv run ilcho-train --reward sigmoid --episodes 1800 --train-ues 16 --out runs/x
uv run ilcho-eval  --constellation hybrid --ues 5,10,30,60,100 \
                   --ilcho runs/x/policy.pt --seeds 3 --out runs/eval_x
uv run python -m ilcho.analysis --out runs/analysis
uv run python -m ilcho.sensitivity --ilcho runs/x/policy.pt --out runs/sensitivity
```

## Results & documentation

All runs referenced above have **completed**; final numbers, figures, and an
honest discussion of what did and didn't reproduce are in **`REPORT.md`**
(tiếng Việt). A newer, closer-to-paper round (100 agents, 600 s training
horizon — matching Table II exactly, GPU-accelerated) lives self-contained in
**[`gpu100_repro/REPORT.md`](gpu100_repro/REPORT.md)** and does not overwrite
anything below. Design-decision write-ups (also tiếng Việt):

* `docs/PHUONG_PHAP_XAY_DUNG_CODE.md` — how the code was built from the paper,
  module by module, with the reasoning behind every choice.
* `docs/METHODOLOGY.html` — same material with diagrams; **§2 is a glossary**
  of every NTN/3GPP and RL/MARL term used, each with a source to read further.
* `docs/KE_HOACH_TAI_TAO_DAY_DU.md` — roadmap for closing the remaining gap to
  the paper's full scale, and an explicit list of what can *never* be closed
  without the authors' unpublished parameters (no public code/preprint exists
  for this paper — checked).

## Scope / deviations from the paper

This is a **scaled-down** reproduction (single CPU, hours not GPU-weeks).
The qualitative findings of the paper are the target, not bit-exact numbers.
See `REPORT.md` §8 for the full deviations table; the headline ones:

* training uses 12–16 agents / 300 s episodes / 0.8–1.8 k episodes
  (paper: up to 100 agents, 600 s, 3 k–30 k episodes) — this is the deviation
  most responsible for ILCHO's HOF advantage narrowing beyond ~50 UEs;
* the action space is `N_max = 16` (peak visible sats inside the
  [39–41° N] region) rather than 27 — checked by sensitivity, no effect found;
* a handful of parameters the paper does not publish (carrier frequency,
  HO offset `O_off`, reward constants `c1,c2,c3`, Walker phasing factor `F`)
  are chosen here and listed explicitly in `ilcho/config.py`;
* two paper claims did **not** reproduce at this scale and are reported as
  negative results: ILCHO having the *highest* throughput of all methods, and
  the linear reward (Eq. 30) training unstably — see `REPORT.md` §5, §9.
