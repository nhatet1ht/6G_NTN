"""Non-learning / centrally-greedy handover baselines.

* **MD-CHO**  - minimum-distance target selection (Sec. VI).
* **MVT-CHO** - maximum visible-time target selection (Sec. VI).
* **HSNF**    - network-flow based selection: a per-slot capacity-constrained
  assignment that maximises the sum spectral efficiency (an approximation of
  Zhang et al., IEEE Commun. Lett. 2021, [22] in the paper).

All policies only choose the CHO *target*; the distance-based execution event
(Eq. 28) in :class:`~ilcho.environment.CHOEnv` still gates the actual handover.
"""
from __future__ import annotations

import numpy as np

from .environment import CHOEnv, FEATS_PER_CAND


def _unpack(obs: np.ndarray, n_max: int) -> dict[str, np.ndarray]:
    b = obs.reshape(obs.shape[0], n_max, FEATS_PER_CAND)
    return {
        "idx": b[..., 0],
        "dist": b[..., 1],
        "load": b[..., 2],
        "rvt": b[..., 3],
        "serving": b[..., 4],
    }


class MDCHO:
    """Pick the accessible satellite at the shortest distance."""

    name = "MD-CHO"

    def __init__(self, n_max: int):
        self.n_max = n_max

    def reset(self, k: int) -> None:  # noqa: D401  (stateless)
        pass

    def act(self, obs: np.ndarray, avail: np.ndarray) -> np.ndarray:
        f = _unpack(obs, self.n_max)
        d = np.where(avail > 0, f["dist"], np.inf)
        return np.argmin(d, axis=1)


class MVTCHO:
    """Pick the accessible satellite with the longest remaining visible time."""

    name = "MVT-CHO"

    def __init__(self, n_max: int):
        self.n_max = n_max

    def reset(self, k: int) -> None:
        pass

    def act(self, obs: np.ndarray, avail: np.ndarray) -> np.ndarray:
        f = _unpack(obs, self.n_max)
        v = np.where(avail > 0, f["rvt"], -np.inf)
        return np.argmax(v, axis=1)


class HSNF:
    """Centralised capacity-constrained max-throughput assignment.

    Needs the environment itself to see every UE's candidate spectral
    efficiencies and the global channel load.
    """

    name = "HSNF"

    def __init__(self, env: CHOEnv):
        self.env = env
        self.n_max = env.n_max

    def reset(self, k: int) -> None:
        pass

    def act(self, obs: np.ndarray, avail: np.ndarray) -> np.ndarray:
        env = self.env
        geo = env._geo
        t = env.t
        K = env.K
        J = env.J
        free = (J - env.load).clip(min=0)                       # per-sat capacity

        # candidate (UE, slot) pairs ranked by spectral efficiency
        pairs = []
        for k in range(K):
            for slot in range(self.n_max):
                if geo.mask[t, k, slot]:
                    pairs.append((geo.se[t, k, slot], k, slot))
        pairs.sort(reverse=True)

        actions = np.zeros(K, np.int64)
        assigned = np.zeros(K, bool)
        cap = free.copy()
        for se, k, slot in pairs:
            if assigned[k]:
                continue
            sid = int(geo.sat_id[t, k, slot])
            serv = int(env.serving[k])
            if sid == serv or cap[sid] > 0:
                actions[k] = slot
                assigned[k] = True
                if sid != serv:
                    cap[sid] -= 1
        # UEs with no room keep their current serving slot if still visible
        for k in range(K):
            if not assigned[k]:
                s = env._serving_slot(k)
                actions[k] = s if s >= 0 else 0
        return actions


BASELINES = {"MD-CHO": MDCHO, "MVT-CHO": MVTCHO, "HSNF": HSNF}
