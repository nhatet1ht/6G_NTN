"""Walker-Delta LEO constellation geometry.

Implements Lemma 1 (satellite Cartesian state) and Lemma 2 (accessibility via
minimum elevation angle) from Choi et al., IEEE TMC 2026.

All positions are expressed in an Earth-centred inertial (ECI-like) frame.
Following the paper's simplifying assumptions the Earth's rotation is neglected
and UEs are stationary VSAT terminals (Sec. III-B).
"""
from __future__ import annotations

import numpy as np

from .config import ConstellationConfig, MU_EARTH, R_EARTH


class Constellation:
    """Vectorised Walker-Delta constellation.

    Parameters
    ----------
    cfg:
        Shell definition (altitude, inclination, planes, sats/plane, phasing).
    """

    def __init__(self, cfg: ConstellationConfig):
        self.cfg = cfg
        self.M = cfg.total_sats
        self.a = cfg.semi_major_axis_m                       # semi-major axis [m]
        self.mean_motion = np.sqrt(MU_EARTH / self.a ** 3)   # omega [rad/s]
        self.inc = np.deg2rad(cfg.inclination_deg)           # alpha [rad]

        # Logical index m = (v-1) * N_L + h   (paper, Sec. III-A)
        v = np.repeat(np.arange(cfg.num_planes), cfg.sats_per_plane)   # plane idx
        h = np.tile(np.arange(cfg.sats_per_plane), cfg.num_planes)     # in-plane

        # RAAN of each plane: Omega_v = 2*pi/N_p * (v-1)   (Walker-Delta: full 2pi)
        self.raan = 2.0 * np.pi * v / cfg.num_planes                    # [M]
        # In-plane phase: Phi_h = 2*pi*h / N_L  plus inter-plane phasing
        #   Delta_f = 2*pi*F / N_total   (paper, Sec. III-A)
        self.phase0 = (
            2.0 * np.pi * h / cfg.sats_per_plane
            + 2.0 * np.pi * cfg.phasing_factor * v / self.M
        )                                                             # [M]
        self.plane_idx = v
        self.inplane_idx = h

    # --------------------------------------------------------------------- #
    # Lemma 1                                                              #
    # --------------------------------------------------------------------- #
    def positions(self, t: float | np.ndarray) -> np.ndarray:
        """Satellite Cartesian positions at time ``t`` seconds.

        Returns array of shape ``(M, 3)`` if ``t`` is scalar, otherwise
        ``(len(t), M, 3)``.  Implements Eq. (1):

            s_m^t = a_s * [ cos(psi) cos(Om) - sin(psi) sin(Om) cos(alpha),
                            cos(psi) sin(Om) + sin(psi) cos(Om) cos(alpha),
                            sin(psi) sin(alpha) ]
            psi_m^t = Phi_m + omega t + f_0
        """
        t_arr = np.atleast_1d(np.asarray(t, dtype=float))              # [T]
        # psi: [T, M]
        psi = self.phase0[None, :] + self.mean_motion * t_arr[:, None]
        Om = self.raan[None, :]
        cpsi, spsi = np.cos(psi), np.sin(psi)
        cOm, sOm = np.cos(Om), np.sin(Om)
        ci = np.cos(self.inc)
        si = np.sin(self.inc)

        x = self.a * (cpsi * cOm - spsi * sOm * ci)
        y = self.a * (cpsi * sOm + spsi * cOm * ci)
        z = self.a * (spsi * si) * np.ones_like(cOm)
        pos = np.stack([x, y, z], axis=-1)                             # [T, M, 3]
        if np.isscalar(t) or (np.ndim(t) == 0):
            return pos[0]
        return pos

    # --------------------------------------------------------------------- #
    # Lemma 2                                                              #
    # --------------------------------------------------------------------- #
    @staticmethod
    def elevation(sat_pos: np.ndarray, ue_pos: np.ndarray) -> np.ndarray:
        """Elevation angle [rad] of satellites as seen from UEs.

        Eq. (4):  psi = pi/2 - arccos( u . (s - u) / (|u| |s - u|) )

        ``sat_pos`` : ``(..., M, 3)``
        ``ue_pos``  : ``(K, 3)``
        returns     : ``(..., K, M)``
        """
        s = sat_pos[..., None, :, :]                     # (..., 1, M, 3)
        u = ue_pos[:, None, :]                           # (K, 1, 3)
        rel = s - u                                      # (..., K, M, 3)
        num = np.sum(u * rel, axis=-1)                   # (..., K, M)
        den = np.linalg.norm(u, axis=-1) * np.linalg.norm(rel, axis=-1)
        cos_zenith = np.clip(num / np.maximum(den, 1e-9), -1.0, 1.0)
        return np.pi / 2.0 - np.arccos(cos_zenith)

    @staticmethod
    def slant_range(sat_pos: np.ndarray, ue_pos: np.ndarray) -> np.ndarray:
        """Euclidean UE-satellite distance [m].  ``(..., K, M)``  (Eq. 3)."""
        s = sat_pos[..., None, :, :]
        u = ue_pos[:, None, :]
        return np.linalg.norm(s - u, axis=-1)

    def access_matrix(
        self, sat_pos: np.ndarray, ue_pos: np.ndarray, min_elev_deg: float
    ) -> np.ndarray:
        """Boolean accessibility mask ``(..., K, M)`` — Lemma 2 condition."""
        elev = self.elevation(sat_pos, ue_pos)
        return elev >= np.deg2rad(min_elev_deg)


class CombinedConstellation:
    """Union of several Walker-Delta shells (e.g. the paper's *hybrid*
    Starlink Phase 1-a + Phase 2-a scenario, Fig. 10).

    Exposes the subset of the :class:`Constellation` interface used by the
    environment (``M`` and ``positions``) plus the accessibility helpers.
    """

    def __init__(self, cfgs: list[ConstellationConfig]):
        self.shells = [Constellation(c) for c in cfgs]
        self.M = sum(s.M for s in self.shells)
        # per-satellite shell label, for reporting
        self.shell_of = np.concatenate(
            [np.full(s.M, i, np.int32) for i, s in enumerate(self.shells)]
        )
        self.cfg = cfgs[0]

    def positions(self, t):
        parts = [s.positions(t) for s in self.shells]
        return np.concatenate(parts, axis=-2)          # concat on the M axis

    # delegate the static geometry helpers
    elevation = staticmethod(Constellation.elevation)
    slant_range = staticmethod(Constellation.slant_range)

    def access_matrix(self, sat_pos, ue_pos, min_elev_deg):
        elev = self.elevation(sat_pos, ue_pos)
        return elev >= np.deg2rad(min_elev_deg)


def make_constellation(spec):
    """Factory: accepts a :class:`Constellation`/:class:`CombinedConstellation`,
    a single :class:`ConstellationConfig`, or a list of configs (hybrid)."""
    if isinstance(spec, (Constellation, CombinedConstellation)):
        return spec
    if isinstance(spec, (list, tuple)):
        return CombinedConstellation(list(spec))
    return Constellation(spec)


def latlon_to_ecef(lat_deg: np.ndarray, lon_deg: np.ndarray) -> np.ndarray:
    """UE position on a spherical Earth — Eq. (2).

    u_k = R_E [cos(phi) cos(delta), cos(phi) sin(delta), sin(phi)]
    """
    lat = np.deg2rad(np.asarray(lat_deg, dtype=float))
    lon = np.deg2rad(np.asarray(lon_deg, dtype=float))
    return R_EARTH * np.stack(
        [np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)],
        axis=-1,
    )


def sample_ue_positions(
    region_deg: tuple[float, float, float, float], k: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Randomly place ``k`` fixed VSAT UEs inside the lat/lon region."""
    lat_min, lat_max, lon_min, lon_max = region_deg
    lat = rng.uniform(lat_min, lat_max, size=k)
    lon = rng.uniform(lon_min, lon_max, size=k)
    return latlon_to_ecef(lat, lon), np.stack([lat, lon], axis=-1)


def remaining_visible_time(
    access_ts: np.ndarray, t_idx: int, dt: float
) -> np.ndarray:
    """Remaining visible time (RVT) per (UE, sat) at time index ``t_idx``.

    ``access_ts`` : boolean ``(T, K, M)`` accessibility time series.
    Returns ``(K, M)`` seconds until the satellite first becomes inaccessible
    (0 if not currently accessible).  Because the geometry is deterministic
    (Lemma 1) this look-ahead is exact, matching the paper's use of ephemeris
    pre-computation.
    """
    T = access_ts.shape[0]
    cur = access_ts[t_idx]                                    # (K, M)
    # For every future step, is it *continuously* visible up to there?
    future = access_ts[t_idx:]                                # (Tf, K, M)
    cont = np.cumprod(future, axis=0).astype(bool)            # (Tf, K, M)
    rvt = cont.sum(axis=0).astype(float) * dt                 # (K, M)
    return np.where(cur, rvt, 0.0)
