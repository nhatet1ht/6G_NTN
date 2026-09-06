"""ILCHO reproduction package.

Reproduction of:
    M. Choi, M. Park, J. Kim, J.-M. Chung,
    "Intelligent Handover Scheme for Improved 6G NTN LEO Satellite Network
     Performance," IEEE Transactions on Mobile Computing, vol. 25, no. 5,
     May 2026, pp. 6863-6880.

The package implements, from the paper:
    * Walker-Delta LEO constellation geometry (Lemma 1)
    * Satellite accessibility via minimum elevation angle (Lemma 2)
    * 3GPP TR 38.811 / 38.821 based link budget and Shannon throughput
    * A Conditional-Handover (CHO) multi-agent environment with a
      distance-based execution event (Eq. 28)
    * QMIX multi-agent RL controller (ILCHO) with the sigmoid reward (Eq. 27)
      and the linear reward ablation (Eq. 30)
    * Baselines: MD-CHO, MVT-CHO, HSNF (network-flow), LBSH (IQL + load balance)
    * Metrics: HO count, HO failure count, spectral efficiency, Jain's fairness
      index, channel-occupancy variance
"""

__version__ = "0.1.0"
