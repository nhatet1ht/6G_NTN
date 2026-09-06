"""3GPP TR 38.811 / 38.821 link budget and Shannon throughput.

Implements Eqs. (8)-(13) of Choi et al., IEEE TMC 2026:

    P_loss   = P_loss,b + P_loss,g + P_loss,s + P_loss,e            (8)
    P_loss,b = FSPL(d, f_c) + S_F + C_L(alpha_CL, f_c)             (9)
    FSPL     = 32.45 + 20 log10(f_c[GHz]) + 20 log10(d[m])        (10)
    P_loss,m,k = P_LoS * P_loss + (1 - P_LoS) * P_loss,NLoS       (11)
    gamma_m,k  = E_EIRP + G_T - K_B - P_loss,m,k - B_W            (12)
    R_m,k      = B_W * log2(1 + gamma_m,k)   [linear SNR]         (13)
"""
from __future__ import annotations

import numpy as np

from .config import ChannelConfig, BOLTZMANN_DBW


class LinkBudget:
    def __init__(self, cfg: ChannelConfig):
        self.cfg = cfg
        elevs = np.array(sorted(cfg.los_prob_table.keys()), dtype=float)
        probs = np.array([cfg.los_prob_table[int(e)] for e in elevs])
        self._elev_grid = elevs
        self._los_grid = probs

    # ------------------------------------------------------------------ #
    def los_probability(self, elev_deg: np.ndarray) -> np.ndarray:
        """Interpolated rural LOS probability (TR 38.811 Table 6.6.1-1)."""
        return np.interp(elev_deg, self._elev_grid, self._los_grid)

    # ------------------------------------------------------------------ #
    def fspl_db(self, dist_m: np.ndarray) -> np.ndarray:
        """Free-space path loss, Eq. (10)."""
        return (
            32.45
            + 20.0 * np.log10(self.cfg.carrier_ghz)
            + 20.0 * np.log10(np.maximum(dist_m, 1.0))
        )

    def atmospheric_db(self, elev_deg: np.ndarray) -> np.ndarray:
        """Gaseous attenuation  P_loss,g = L_zenith / sin(elevation)."""
        sin_e = np.sin(np.deg2rad(np.clip(elev_deg, 1.0, 90.0)))
        return self.cfg.zenith_atten_db / sin_e

    # ------------------------------------------------------------------ #
    def path_loss_db(
        self,
        dist_m: np.ndarray,
        elev_deg: np.ndarray,
        rng: np.random.Generator | None = None,
    ) -> np.ndarray:
        """Composite path loss, Eqs. (8)-(11).

        Shadow fading S_F ~ N(0, sigma_SF^2) is drawn per call when ``rng`` is
        given (frozen to its mean, 0 dB, otherwise so that geometry-only
        sanity checks are deterministic).
        """
        fspl = self.fspl_db(dist_m)
        atmo = self.atmospheric_db(elev_deg)

        if rng is not None:
            sf_los = rng.normal(0.0, self.cfg.sigma_sf_los_db, size=dist_m.shape)
            sf_nlos = rng.normal(0.0, self.cfg.sigma_sf_nlos_db, size=dist_m.shape)
        else:
            sf_los = np.zeros_like(dist_m)
            sf_nlos = np.zeros_like(dist_m)

        pl_los = fspl + atmo + sf_los
        pl_nlos = fspl + atmo + sf_nlos + self.cfg.clutter_loss_nlos_db

        p_los = self.los_probability(elev_deg)
        return p_los * pl_los + (1.0 - p_los) * pl_nlos             # Eq. (11)

    # ------------------------------------------------------------------ #
    def snr_db(self, path_loss_db: np.ndarray) -> np.ndarray:
        """Downlink SNR, Eq. (12).

        E_EIRP is given as a density (dBW/MHz); total EIRP over the channel is
        E_EIRP + 10 log10(B_MHz).  The noise term B_W is 10 log10(B_Hz).
        """
        b_hz = self.cfg.bandwidth_hz
        eirp_total_dbw = self.cfg.eirp_dbw_per_mhz + 10.0 * np.log10(b_hz / 1e6)
        noise_dbw = BOLTZMANN_DBW + 10.0 * np.log10(b_hz)  # K_B(dBW/K/Hz)+B_W(dBHz)
        return (
            eirp_total_dbw
            + self.cfg.g_over_t_db
            - noise_dbw
            - path_loss_db
        )

    def spectral_efficiency(self, snr_db: np.ndarray) -> np.ndarray:
        """Shannon spectral efficiency R/B = log2(1 + SNR_lin)  (Eq. 13)."""
        snr_lin = 10.0 ** (snr_db / 10.0)
        return np.log2(1.0 + snr_lin)

    def throughput_bps(self, snr_db: np.ndarray) -> np.ndarray:
        return self.cfg.bandwidth_hz * self.spectral_efficiency(snr_db)
