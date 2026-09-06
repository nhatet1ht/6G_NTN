"""Configuration objects and physical constants for the ILCHO reproduction.

All values that appear in the paper are annotated with the corresponding
table / equation number.  Values the paper leaves unspecified are marked
``ASSUMPTION`` and are collected here so the report can list them explicitly.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

import yaml

# --------------------------------------------------------------------------- #
# Physical constants                                                           #
# --------------------------------------------------------------------------- #
MU_EARTH = 3.986004418e14  # [m^3/s^2] Earth gravitational parameter (G * M_E)
R_EARTH = 6_371_000.0      # [m] mean Earth radius
C_LIGHT = 299_792_458.0    # [m/s]
BOLTZMANN_DBW = -228.6     # [dBW/K/Hz]  K_B  (Table II)


@dataclass
class ConstellationConfig:
    """Walker-Delta shell parameters.

    Defaults reproduce *Starlink Phase 2-a* (Table I / Table II of the paper):
    altitude 340 km, inclination 53 deg, 48 planes, 110 sats/plane.
    """

    name: str = "starlink_phase_2a"
    altitude_km: float = 340.0        # H_L                       (Table I / II)
    inclination_deg: float = 53.0     # alpha                     (Table I / II)
    num_planes: int = 48              # N_p                       (Table I / II)
    sats_per_plane: int = 110         # N_L                       (Table I / II)
    phasing_factor: int = 1           # F  -- Walker-Delta phasing  (ASSUMPTION;
    #                                   the paper does not publish F for Starlink)
    eccentricity: float = 0.0         # ~0 for Starlink (paper: e = 1.379e-4 ~ 0)

    @property
    def total_sats(self) -> int:
        return self.num_planes * self.sats_per_plane

    @property
    def semi_major_axis_m(self) -> float:
        return R_EARTH + self.altitude_km * 1_000.0


# Named shells taken verbatim from Table I of the paper.
CONSTELLATIONS: dict[str, ConstellationConfig] = {
    "starlink_phase_1a": ConstellationConfig(
        name="starlink_phase_1a", altitude_km=550.0, inclination_deg=53.0,
        num_planes=72, sats_per_plane=22,
    ),
    "starlink_phase_2a": ConstellationConfig(
        name="starlink_phase_2a", altitude_km=340.0, inclination_deg=53.0,
        num_planes=48, sats_per_plane=110,
    ),
    "oneweb_phase_1": ConstellationConfig(
        name="oneweb_phase_1", altitude_km=1200.0, inclination_deg=87.9,
        num_planes=18, sats_per_plane=40,
    ),
}


def resolve_constellation(name: str):
    """Map a CLI name to a config or list of configs.

    ``"hybrid"`` -> Starlink Phase 1-a + Phase 2-a coexisting (paper Fig. 10).
    """
    if name == "hybrid":
        return [CONSTELLATIONS["starlink_phase_1a"],
                CONSTELLATIONS["starlink_phase_2a"]]
    return CONSTELLATIONS[name]


CONSTELLATION_NAMES = list(CONSTELLATIONS) + ["hybrid"]


@dataclass
class ChannelConfig:
    """3GPP TR 38.811 / 38.821 link-budget parameters (Table II)."""

    carrier_ghz: float = 20.0           # Ka-band downlink            (ASSUMPTION:
    #                                     paper only says "Ka-band"; 20 GHz DL)
    bandwidth_hz: float = 250e6         # channel bandwidth B_W       (Table II)
    eirp_dbw_per_mhz: float = -4.0      # E_EIRP                      (Table II)
    g_over_t_db: float = 15.9           # G_T [dB/K]                  (Table II)
    min_elevation_deg: float = 30.0     # psi_min                     (Table II)
    # Rural, Ka-band shadow-fading std [dB]  (TR 38.811 Table 6.6.2-1, ~elevation
    # averaged).  LOS / NLOS.
    sigma_sf_los_db: float = 1.9
    sigma_sf_nlos_db: float = 10.7
    clutter_loss_nlos_db: float = 24.0  # rural Ka NLOS clutter loss  (approx.)
    zenith_atten_db: float = 0.15       # L_zenith(f_c) Ka-band gas    (ASSUMPTION)
    # Rural LOS probability vs. elevation (deg -> prob), TR 38.811 Table 6.6.1-1.
    los_prob_table: dict[int, float] = field(default_factory=lambda: {
        10: 0.782, 20: 0.867, 30: 0.913, 40: 0.937, 50: 0.955,
        60: 0.968, 70: 0.978, 80: 0.985, 90: 0.992,
    })


@dataclass
class EnvConfig:
    """CHO multi-agent environment settings."""

    num_ues: int = 30
    service_duration_s: int = 600     # T_s = 10 min                 (Table II)
    time_step_s: float = 1.0          # 1 s slots                    (paper text)
    max_channels: int = 8             # J  (channels per satellite)  (Table II)
    n_max: int = 16                   # action-space size = max visible sats in
    #                                   the region of interest (Lemma 2).  The
    #                                   global peak over all latitudes is 17
    #                                   (P1a) / ~27 (P2a) -- Fig. 5 -- but inside
    #                                   [39-41 N] the peak is ~11 (P1a) / ~15
    #                                   (P2a), so 16 slots suffice.
    handover_offset_km: float = 50.0  # O_off in Eq. 28              (ASSUMPTION)
    ho_cooldown_s: float = 5.0        # guard time after a HO attempt  (ASSUMPTION:
    #                                   models CHO time-to-trigger + execution
    #                                   latency; prevents 1-Hz re-triggering)
    hof_outage_s: float = 2.0         # data-plane outage after a HO failure
    #                                   (ASSUMPTION: RLF detection + re-establish;
    #                                   makes delivered throughput reflect HOFs)
    # Region of interest [lat_min, lat_max, lon_min, lon_max] deg  (Table II)
    region_deg: tuple[float, float, float, float] = (39.0, 41.0, 39.0, 41.0)
    # Reward parameters -------------------------------------------------------
    reward_type: str = "sigmoid"      # "sigmoid" (Eq. 27) | "linear" (Eq. 30)
    p1_ho_success: float = 0.5        # -p1 penalty on a successful HO (Eq. 27)
    p2_ho_failure: float = 5.0        # -p2 penalty on a HO failure     (Eq. 27)
    # sigmoid cost U_k(x) = c3 / (1 + exp(c1 (x - c2)))            (paper Eq. 27)
    #   throughput term : c1<0, c2>0, c3>0  -> higher SE -> higher reward
    #   RVT term        : c1>0, c2>0, c3<0  -> lower RVT -> penalty
    # c3 scales the term; se_c3=2 keeps the throughput gradient (~1 /bps/Hz)
    # competitive with the HO/HOF penalties so the agent does not over-trade
    # spectral efficiency for stability.
    se_c1: float = -2.0
    se_c2: float = 3.0             # [bps/Hz] centre, on the steep part of the
    #                               operating range (~2.7-3.8 bps/Hz)
    se_c3: float = 2.0
    rvt_c1: float = 0.10
    rvt_c2: float = 18.0           # [s] penalty only bites for near-setting sats
    rvt_c3: float = -1.0
    # linear reward weights (Eq. 30)
    lin_w1_se: float = 0.2
    lin_w2_rvt: float = 0.01


@dataclass
class QMixConfig:
    """QMIX hyper-parameters (Table II: 'Hyper-Parameters of ILCHO')."""

    lr: float = 1e-4                 # beta                        (Table II)
    gamma: float = 0.99             # sigma (discount)            (Table II)
    batch_size: int = 32            # b                           (Table II)
    eps_start: float = 0.9         # epsilon schedule            (Table II)
    eps_end: float = 0.1
    eps_anneal_episodes: int = 800
    num_episodes: int = 1500       # paper: 3000-30000; reduced for CPU repro
    target_update_interval: int = 10   # T_t                     (Table II)
    tau: float = 0.001             # eta_QMIX soft update        (Table II)
    rnn_hidden: int = 64
    mix_hidden: int = 32
    hyper_hidden: int = 64
    buffer_size: int = 5000        # episodes
    grad_clip: float = 10.0
    train_ues: int = 10            # agents used during training


@dataclass
class ExperimentConfig:
    constellation: ConstellationConfig = field(default_factory=ConstellationConfig)
    channel: ChannelConfig = field(default_factory=ChannelConfig)
    env: EnvConfig = field(default_factory=EnvConfig)
    qmix: QMixConfig = field(default_factory=QMixConfig)
    seed: int = 0
    device: str = "cpu"

    # ----------------------------------------------------------------- IO ---- #
    def to_yaml(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(_to_plain(asdict(self)), fh, sort_keys=False)

    @classmethod
    def from_yaml(cls, path: str) -> "ExperimentConfig":
        with open(path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        return cls(
            constellation=ConstellationConfig(**raw.get("constellation", {})),
            channel=ChannelConfig(**raw.get("channel", {})),
            env=EnvConfig(**raw.get("env", {})),
            qmix=QMixConfig(**raw.get("qmix", {})),
            seed=raw.get("seed", 0),
            device=raw.get("device", "cpu"),
        )


def _to_plain(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _to_plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_plain(v) for v in obj]
    return obj
