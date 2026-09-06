"""Conditional-Handover multi-agent environment for LEO NTN.

One agent per UE (Sec. V).  Each step:

  1. geometry is evaluated from the deterministic ephemeris (Lemma 1/2);
  2. every agent observes ``o_k`` (Eq. 26) and proposes a *target* T-LEO
     (the CHO preparation-phase decision);
  3. the distance-based execution event (Eq. 28) decides whether the HO fires;
  4. admission control on the target satellite's ``J`` channels decides
     success / failure (HOF);
  5. rewards follow Eq. (27) (sigmoid) or Eq. (30) (linear).

Metrics accumulated over an episode: HO count, HOF count, per-UE average
spectral efficiency, per-satellite channel occupancy.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .channel import LinkBudget
from .config import ChannelConfig, ConstellationConfig, EnvConfig, R_EARTH
from .constellation import Constellation, make_constellation, sample_ue_positions


# --------------------------------------------------------------------------- #
# Per-episode geometry pre-computation                                         #
# --------------------------------------------------------------------------- #
@dataclass
class EpisodeGeometry:
    """Compact per-(t, UE, candidate) tensors for one episode.

    Shapes are ``(T, K, N_max)`` except ``se_serving_lookup`` helpers.
    Candidates are the ``N_max`` nearest *accessible* satellites, sorted by
    slant range.  Invalid slots are marked by ``mask == 0``.
    """

    sat_id: np.ndarray       # int32  logical index of candidate satellite
    dist_m: np.ndarray       # float32 slant range [m]
    se: np.ndarray           # float32 spectral efficiency [bps/Hz]
    rvt_s: np.ndarray        # float32 remaining visible time [s]
    mask: np.ndarray         # bool    candidate slot valid
    T: int
    K: int
    M: int
    dt: float

    def candidate_of(self, t: int, k: int, sat: int) -> int:
        """Return slot index of ``sat`` among UE ``k`` candidates at ``t`` or -1."""
        row = self.sat_id[t, k]
        hit = np.where((row == sat) & self.mask[t, k])[0]
        return int(hit[0]) if hit.size else -1


def _shell_altitudes_m(cons) -> list[float]:
    if hasattr(cons, "shells"):
        return [s.cfg.altitude_km * 1_000.0 for s in cons.shells]
    return [cons.cfg.altitude_km * 1_000.0]


def build_episode_geometry(
    cons: Constellation,
    link: LinkBudget,
    ue_ecef: np.ndarray,
    t0: float,
    env_cfg: EnvConfig,
    rng: np.random.Generator,
    time_chunk: int = 150,
) -> EpisodeGeometry:
    """Fully vectorised per-episode geometry.

    Two accelerations over the naive version:
      1. **Satellite pre-filter** — a satellite that never comes within the LEO
         visibility radius of the UE region cannot be a candidate, so it is
         dropped before the per-slot maths (typically 5284 -> a few hundred).
      2. **No Python time loop** — the forward pass (distance/elevation/nearest
         ``N_max``) and the RVT backward pass are computed as batched array ops,
         chunked over time only to bound peak memory.
    The output is bit-identical to the naive version.
    """
    T = int(round(env_cfg.service_duration_s / env_cfg.time_step_s))
    K = ue_ecef.shape[0]
    dt = env_cfg.time_step_s
    n_max = env_cfg.n_max
    min_elev_rad = np.deg2rad(link.cfg.min_elevation_deg)

    times = t0 + np.arange(T) * dt
    positions = cons.positions(times).astype(np.float64)          # (T, M_all, 3)
    M_all = positions.shape[1]

    # ---- 1. satellite pre-filter -------------------------------------- #
    centroid = ue_ecef.mean(axis=0)                               # (3,)
    d_cen = np.linalg.norm(positions - centroid[None, None, :], axis=-1)  # (T,M_all)
    d_cen_min = d_cen.min(axis=0)                                 # (M_all,)
    h_max = max(_shell_altitudes_m(cons))
    e = min_elev_rad
    d_horizon = (np.sqrt(R_EARTH ** 2 * np.sin(e) ** 2 + h_max ** 2
                         + 2 * h_max * R_EARTH) - R_EARTH * np.sin(e))
    region_span_m = 400_000.0        # generous margin for the UE region extent
    keep = np.where(d_cen_min < d_horizon + region_span_m)[0]
    if keep.size < 4 * n_max:        # degenerate region -> keep everything
        keep = np.arange(M_all)
    pos = positions[:, keep, :]                                   # (T, Msub, 3)
    Msub = keep.size

    ue = ue_ecef[None, :, None, :]                                # (1,K,1,3)
    ue_norm = np.linalg.norm(ue_ecef, axis=-1)[None, :, None]     # (1,K,1)

    sat_local = np.zeros((T, K, n_max), np.int64)
    dist_m = np.zeros((T, K, n_max), np.float32)
    se = np.zeros((T, K, n_max), np.float32)
    mask = np.zeros((T, K, n_max), bool)
    access_ts = np.zeros((T, K, Msub), bool)

    # ---- 2. forward pass, chunked over time -------------------------- #
    for a in range(0, T, time_chunk):
        b = min(a + time_chunk, T)
        rel = pos[a:b, None, :, :] - ue                          # (c,K,Msub,3)
        dist = np.linalg.norm(rel, axis=-1)                      # (c,K,Msub)
        cos_zen = np.clip(
            np.sum(ue * rel, axis=-1) / np.maximum(ue_norm * dist, 1e-9),
            -1.0, 1.0,
        )
        elev = np.pi / 2.0 - np.arccos(cos_zen)                  # (c,K,Msub)
        acc = elev >= min_elev_rad
        access_ts[a:b] = acc

        masked = np.where(acc, dist, np.inf)
        part = np.argpartition(masked, min(n_max, Msub - 1), axis=-1)[..., :n_max]
        take = np.take_along_axis(masked, part, axis=-1)
        order = np.take_along_axis(part, np.argsort(take, axis=-1), axis=-1)

        d_sel = np.take_along_axis(dist, order, axis=-1)
        e_sel = np.take_along_axis(elev, order, axis=-1)
        valid = np.take_along_axis(acc, order, axis=-1)
        pl = link.path_loss_db(d_sel, np.rad2deg(e_sel), rng=rng)
        se_sel = link.spectral_efficiency(link.snr_db(pl))

        sat_local[a:b] = order
        dist_m[a:b] = d_sel.astype(np.float32)
        se[a:b] = np.where(valid, se_sel, 0.0).astype(np.float32)
        mask[a:b] = valid

    sat_id = keep[sat_local].astype(np.int32)                    # local -> global

    # ---- 3. RVT: consecutive-visible run length, vectorised -------- #
    rev = access_ts[::-1]                                        # reversed time
    idx = np.arange(T).reshape(-1, 1, 1)
    false_pos = np.where(rev, -1, idx)
    last_false = np.maximum.accumulate(false_pos, axis=0)
    run_rev = np.where(rev, idx - last_false, 0).astype(np.int32)
    run = run_rev[::-1]                                          # (T,K,Msub) forward
    rvt_local = np.take_along_axis(run, sat_local, axis=-1)     # (T,K,n_max)
    rvt_s = np.where(mask, rvt_local.astype(np.float32) * dt, 0.0)

    return EpisodeGeometry(sat_id, dist_m, se, rvt_s, mask, T, K, M_all, dt)


# --------------------------------------------------------------------------- #
# Environment                                                                  #
# --------------------------------------------------------------------------- #
@dataclass
class StepInfo:
    ho: np.ndarray          # bool (K,)  successful HO this step
    hof: np.ndarray         # bool (K,)  HO failure this step
    se: np.ndarray          # float (K,) spectral efficiency delivered
    connected: np.ndarray   # bool (K,)
    serving: np.ndarray     # int (K,)   serving satellite id (-1 if none)


# feature layout of the per-candidate observation block
FEATS_PER_CAND = 5   # [idx_norm, dist_norm, load_norm, rvt_norm, is_serving]


class CHOEnv:
    """Discrete-time CHO environment (one episode == one service duration)."""

    def __init__(
        self,
        env_cfg: EnvConfig,
        cons_cfg,
        chan_cfg: ChannelConfig,
        seed: int = 0,
    ):
        self.cfg = env_cfg
        self.cons = make_constellation(cons_cfg)
        self.link = LinkBudget(chan_cfg)
        self.rng = np.random.default_rng(seed)
        self.K = env_cfg.num_ues
        self.n_max = env_cfg.n_max
        self.J = env_cfg.max_channels
        self.obs_dim = self.n_max * FEATS_PER_CAND
        self.n_actions = self.n_max

        self._geo: EpisodeGeometry | None = None
        self.t = 0
        self.T = 0

    # ------------------------------------------------------------------ #
    def reset(self, ue_seed: int | None = None) -> tuple[np.ndarray, np.ndarray]:
        if ue_seed is not None:
            self.rng = np.random.default_rng(ue_seed)
        self.ue_ecef, self.ue_latlon = sample_ue_positions(
            self.cfg.region_deg, self.K, self.rng
        )
        t0 = float(self.rng.uniform(0.0, 5_700.0))   # random constellation epoch
        self._geo = build_episode_geometry(
            self.cons, self.link, self.ue_ecef, t0, self.cfg, self.rng
        )
        self.T = self._geo.T
        self.t = 0

        self.load = np.zeros(self.cons.M, np.int32)          # channels used / sat
        self.serving = np.full(self.K, -1, np.int32)
        self.target = np.full(self.K, -1, np.int32)          # current CHO target
        self.cooldown = np.zeros(self.K, np.float32)         # HO guard time [s]

        # initial attach: nearest accessible sat with a free channel
        geo = self._geo
        for k in range(self.K):
            for slot in range(self.n_max):
                if not geo.mask[0, k, slot]:
                    break
                sid = int(geo.sat_id[0, k, slot])
                if self.load[sid] < self.J:
                    self.load[sid] += 1
                    self.serving[k] = sid
                    self.target[k] = sid
                    break

        # per-episode accumulators
        self.ho_count = np.zeros(self.K, np.int64)
        self.hof_count = np.zeros(self.K, np.int64)
        self.se_sum = np.zeros(self.K, np.float64)
        self.unserved_sum = np.zeros(self.K, np.int64)
        self.outage_timer = np.zeros(self.K, np.float32)   # data-plane outage [s]
        self.occ_var_sum = 0.0
        self.occ_steps = 0

        return self._observe()

    # ------------------------------------------------------------------ #
    def _serving_slot(self, k: int) -> int:
        geo = self._geo
        if self.serving[k] < 0:
            return -1
        return geo.candidate_of(self.t, k, int(self.serving[k]))

    def _observe(self) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(obs (K, obs_dim), avail_actions (K, n_actions))``."""
        geo = self._geo
        t = self.t
        obs = np.zeros((self.K, self.obs_dim), np.float32)
        avail = np.zeros((self.K, self.n_actions), np.float32)

        idx_norm = geo.sat_id[t].astype(np.float32) / max(self.cons.M, 1)
        dist_norm = geo.dist_m[t] / 3.0e6                         # ~3000 km scale
        load_norm = self.load[geo.sat_id[t]].astype(np.float32) / self.J
        rvt_norm = geo.rvt_s[t] / float(self.cfg.service_duration_s)
        is_serv = (geo.sat_id[t] == self.serving[:, None]) & geo.mask[t]

        block = np.stack(
            [idx_norm, dist_norm, load_norm, rvt_norm, is_serv.astype(np.float32)],
            axis=-1,
        )                                                        # (K, n_max, 5)
        block *= geo.mask[t][:, :, None]
        obs[:] = block.reshape(self.K, -1)
        avail[:] = geo.mask[t].astype(np.float32)
        # guarantee at least one legal action to avoid NaNs
        avail[avail.sum(axis=1) == 0, 0] = 1.0
        return obs, avail

    # ------------------------------------------------------------------ #
    def step(self, actions: np.ndarray) -> tuple[
        np.ndarray, np.ndarray, np.ndarray, bool, StepInfo
    ]:
        geo = self._geo
        t = self.t
        K, J = self.K, self.J
        ho = np.zeros(K, bool)
        hof = np.zeros(K, bool)

        # ---- 1. resolve CHO target from the action --------------------- #
        for k in range(K):
            a = int(actions[k])
            if 0 <= a < self.n_max and geo.mask[t, k, a]:
                self.target[k] = int(geo.sat_id[t, k, a])
            # else: keep previous target

        # ---- 2. execution event + admission control ------------------- #
        # process UEs in a random order so channel contention is fair
        self.cooldown = np.maximum(0.0, self.cooldown - self.cfg.time_step_s)
        for k in self.rng.permutation(K):
            serv = int(self.serving[k])
            tgt = int(self.target[k])
            serv_slot = geo.candidate_of(t, k, serv) if serv >= 0 else -1
            serv_lost = serv < 0 or serv_slot < 0        # serving link gone

            tgt_slot = geo.candidate_of(t, k, tgt) if tgt >= 0 else -1
            tgt_ok = tgt_slot >= 0

            d_serv = geo.dist_m[t, k, serv_slot] if serv_slot >= 0 else np.inf
            d_tgt = geo.dist_m[t, k, tgt_slot] if tgt_ok else np.inf
            off = self.cfg.handover_offset_km * 1_000.0
            exec_event = (
                tgt_ok and tgt != serv and (d_tgt < d_serv - off)
                and self.cooldown[k] <= 0.0
            )

            if serv_lost and not (tgt_ok and tgt != serv):
                # link dropped with no prepared target -> forced recovery
                self._release(serv)
                self.serving[k] = -1
                # emergency attach to nearest free accessible sat
                rec = self._nearest_free(t, k)
                if rec >= 0:
                    self.load[rec] += 1
                    self.serving[k] = rec
                    self.target[k] = rec
                hof[k] = True                            # counted as a failure
                continue

            if not (exec_event or serv_lost):
                continue                                 # stay put

            # attempt HO to target -- start the guard timer
            self.cooldown[k] = self.cfg.ho_cooldown_s
            rvt_tgt = geo.rvt_s[t, k, tgt_slot] if tgt_ok else 0.0
            resources = tgt_ok and self.load[tgt] < J
            has_rvt = rvt_tgt > self.cfg.time_step_s
            if tgt_ok and resources and has_rvt:
                self._release(serv)
                self.load[tgt] += 1
                self.serving[k] = tgt
                ho[k] = True
            else:
                hof[k] = True
                if serv_lost:                            # cannot stay -> recover
                    self._release(serv)
                    self.serving[k] = -1
                    rec = self._nearest_free(t, k)
                    if rec >= 0:
                        self.load[rec] += 1
                        self.serving[k] = rec
                        self.target[k] = rec

        # ---- 3. throughput delivered this step ------------------------ #
        se_now = np.zeros(K, np.float32)
        connected = np.zeros(K, bool)
        for k in range(K):
            slot = self._serving_slot(k)
            if slot >= 0:
                se_now[k] = geo.se[t, k, slot]
                connected[k] = True
        # A handover failure disrupts the data plane (RLF detection +
        # re-establishment).  Model it as a short outage window during which the
        # UE carries no traffic -- this is what makes the *delivered* throughput
        # of HOF-prone schemes (MD/MVT) drop, as in the paper's Fig. 8c.
        self.outage_timer = np.maximum(0.0, self.outage_timer - self.cfg.time_step_s)
        self.outage_timer[hof] = self.cfg.hof_outage_s
        outage = self.outage_timer > 0.0
        se_now[outage] = 0.0
        connected[outage] = False
        self.se_sum += se_now
        self.unserved_sum += ~connected
        self.ho_count += ho
        self.hof_count += hof

        # load-balance metric: variance of channel occupancy O_m = L_m / J over
        # the common pool of satellites accessible to the UE population (Table IV)
        cand_sats = np.unique(geo.sat_id[t][geo.mask[t]])
        if cand_sats.size:
            occ_t = self.load[cand_sats] / J
            self.occ_var_sum += float(np.var(occ_t))
        self.occ_steps += 1

        # ---- 4. reward ---------------------------------------------------- #
        rvt_serv = np.zeros(K, np.float32)
        for k in range(K):
            slot = self._serving_slot(k)
            rvt_serv[k] = geo.rvt_s[t, k, slot] if slot >= 0 else 0.0
        rewards = self._reward(ho, hof, se_now, rvt_serv)

        info = StepInfo(ho, hof, se_now, connected, self.serving.copy())
        self.t += 1
        done = self.t >= self.T
        if done:
            obs, avail = self._empty_obs()
        else:
            obs, avail = self._observe()
        return obs, avail, rewards, done, info

    # ------------------------------------------------------------------ #
    def _reward(self, ho, hof, se_now, rvt_serv) -> np.ndarray:
        c = self.cfg
        r = np.zeros(self.K, np.float32)
        steady = ~(ho | hof)

        if c.reward_type == "sigmoid":
            # U_k(x) = c3 / (1 + exp(c1 (x - c2)))                     (Eq. 27)
            u_se = c.se_c3 / (1.0 + np.exp(c.se_c1 * (se_now - c.se_c2)))
            u_rvt = c.rvt_c3 / (1.0 + np.exp(c.rvt_c1 * (rvt_serv - c.rvt_c2)))
            steady_r = u_se + u_rvt        # higher SE -> up; low RVT -> penalty
        elif c.reward_type == "linear":
            steady_r = c.lin_w1_se * se_now + c.lin_w2_rvt * rvt_serv   # (Eq. 30)
        else:
            raise ValueError(c.reward_type)

        r[steady] = steady_r[steady]
        r[ho] = -c.p1_ho_success
        r[hof] = -c.p2_ho_failure
        return r

    # ------------------------------------------------------------------ #
    def _release(self, sat: int) -> None:
        if sat >= 0 and self.load[sat] > 0:
            self.load[sat] -= 1

    def _nearest_free(self, t: int, k: int) -> int:
        geo = self._geo
        for slot in range(self.n_max):
            if not geo.mask[t, k, slot]:
                break
            sid = int(geo.sat_id[t, k, slot])
            if self.load[sid] < self.J:
                return sid
        return -1

    def _empty_obs(self):
        return (
            np.zeros((self.K, self.obs_dim), np.float32),
            np.ones((self.K, self.n_actions), np.float32),
        )

    # ------------------------------------------------------------------ #
    def episode_metrics(self) -> dict:
        """Aggregate metrics after an episode finishes."""
        se_avg = self.se_sum / self.T                       # per-UE mean SE
        jfi = float(se_avg.sum() ** 2 / (self.K * np.sum(se_avg ** 2) + 1e-12))
        occ_var = self.occ_var_sum / max(self.occ_steps, 1)
        return {
            "ho": float(self.ho_count.mean()),
            "hof": float(self.hof_count.mean()),
            "se": float(se_avg.mean()),
            "se_per_ue": se_avg,
            "jfi": jfi,
            "occ_var": occ_var,
            "unserved": float(self.unserved_sum.mean() / self.T),  # outage frac
        }
