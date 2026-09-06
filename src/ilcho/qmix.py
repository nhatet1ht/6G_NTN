"""QMIX multi-agent RL controller (the ILCHO learner) + IQL variant (LBSH).

Follows Rashid et al., "QMIX", ICML 2018 (ref. [32] in the paper):

    * per-agent recurrent Q-network (DRQN / GRU)                    -> Q_k
    * monotonic mixing network with hyper-networks on the state     -> Q_tot
    * double-DQN targets, soft target update (eta_QMIX)             (Eq. 19/25)

Setting ``mode="iql"`` disables the mixer and trains each agent on its own TD
error with a load-balancing reward -> this is the LBSH baseline
(He et al., IEEE GLOBECOM 2020, ref. [26] in the paper).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import QMixConfig


# --------------------------------------------------------------------------- #
class RNNAgent(nn.Module):
    """Shared DRQN agent network (Fig. 4).

    Uses ``nn.GRU`` (fused, whole-sequence) rather than a Python ``GRUCell``
    loop: during ``learn`` the 600-step sequence is processed in one optimised
    call, which is the dominant training cost at large agent counts.
    """

    def __init__(self, obs_dim: int, n_actions: int, hidden: int):
        super().__init__()
        self.hidden = hidden
        self.fc1 = nn.Linear(obs_dim, hidden)
        self.gru = nn.GRU(hidden, hidden, batch_first=True)
        self.fc2 = nn.Linear(hidden, n_actions)

    def init_hidden(self, batch: int, device) -> torch.Tensor:
        return torch.zeros(1, batch, self.hidden, device=device)

    def forward_seq(self, obs_seq: torch.Tensor, h0: torch.Tensor | None = None):
        """obs_seq: (N, T, obs_dim) -> q: (N, T, n_actions), hN: (1, N, hidden)."""
        x = F.relu(self.fc1(obs_seq))
        out, hn = self.gru(x, h0)
        return self.fc2(out), hn

    def forward(self, obs: torch.Tensor, h: torch.Tensor):
        """Single-step: obs (N, obs_dim), h (1, N, hidden)."""
        q_seq, hn = self.forward_seq(obs.unsqueeze(1), h)
        return q_seq.squeeze(1), hn


class QMixer(nn.Module):
    """Monotonic mixing network with state-conditioned hyper-networks."""

    def __init__(self, n_agents: int, state_dim: int, embed: int, hyper_hidden: int):
        super().__init__()
        self.n_agents = n_agents
        self.embed = embed
        self.hyper_w1 = nn.Sequential(
            nn.Linear(state_dim, hyper_hidden), nn.ReLU(),
            nn.Linear(hyper_hidden, n_agents * embed),
        )
        self.hyper_w2 = nn.Sequential(
            nn.Linear(state_dim, hyper_hidden), nn.ReLU(),
            nn.Linear(hyper_hidden, embed),
        )
        self.hyper_b1 = nn.Linear(state_dim, embed)
        self.hyper_b2 = nn.Sequential(
            nn.Linear(state_dim, embed), nn.ReLU(), nn.Linear(embed, 1)
        )

    def forward(self, agent_qs: torch.Tensor, state: torch.Tensor) -> torch.Tensor:
        # agent_qs: (B, n_agents)   state: (B, state_dim)
        b = agent_qs.size(0)
        w1 = torch.abs(self.hyper_w1(state)).view(b, self.n_agents, self.embed)
        b1 = self.hyper_b1(state).view(b, 1, self.embed)
        hidden = F.elu(torch.bmm(agent_qs.view(b, 1, self.n_agents), w1) + b1)
        w2 = torch.abs(self.hyper_w2(state)).view(b, self.embed, 1)
        b2 = self.hyper_b2(state).view(b, 1, 1)
        y = torch.bmm(hidden, w2) + b2
        return y.view(b, 1)


# --------------------------------------------------------------------------- #
@dataclass
class EpisodeBatch:
    obs: np.ndarray       # (T+1, K, obs_dim)   float16
    actions: np.ndarray   # (T, K)
    avail: np.ndarray     # (T+1, K, n_actions) bool
    reward: np.ndarray    # (T,)            team reward (mean over agents)
    reward_k: np.ndarray  # (T, K)          per-agent reward (for IQL)
    mask: np.ndarray      # (T,)            1 while episode running
    # the QMIX global "state" is obs flattened over agents -> not stored


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data: list[EpisodeBatch] = []
        self._ptr = 0

    def add(self, ep: EpisodeBatch) -> None:
        if len(self.data) < self.capacity:
            self.data.append(ep)
        else:
            self.data[self._ptr] = ep
        self._ptr = (self._ptr + 1) % self.capacity

    def __len__(self) -> int:
        return len(self.data)

    def sample(self, batch: int, rng: np.random.Generator) -> list[EpisodeBatch]:
        idx = rng.integers(0, len(self.data), size=min(batch, len(self.data)))
        return [self.data[i] for i in idx]


# --------------------------------------------------------------------------- #
class MARLController:
    """Owns the networks, does action selection and learning."""

    def __init__(
        self,
        obs_dim: int,
        state_dim: int,
        n_actions: int,
        n_agents: int,
        cfg: QMixConfig,
        mode: str = "qmix",
        device: str = "cpu",
        seed: int = 0,
    ):
        self.cfg = cfg
        self.mode = mode
        self.device = torch.device(device)
        self.n_actions = n_actions
        self.n_agents = n_agents
        torch.manual_seed(seed)

        self.agent = RNNAgent(obs_dim, n_actions, cfg.rnn_hidden).to(self.device)
        self.target_agent = RNNAgent(obs_dim, n_actions, cfg.rnn_hidden).to(self.device)
        self.target_agent.load_state_dict(self.agent.state_dict())
        params = list(self.agent.parameters())

        self.mixer = self.target_mixer = None
        if mode == "qmix":
            self.mixer = QMixer(n_agents, state_dim, cfg.mix_hidden,
                                cfg.hyper_hidden).to(self.device)
            self.target_mixer = QMixer(n_agents, state_dim, cfg.mix_hidden,
                                       cfg.hyper_hidden).to(self.device)
            self.target_mixer.load_state_dict(self.mixer.state_dict())
            params += list(self.mixer.parameters())

        self.opt = torch.optim.Adam(params, lr=cfg.lr)
        self.rng = np.random.default_rng(seed)
        self._h = None
        self.train_steps = 0

    # ------------------------------------------------------------------ #
    def epsilon(self, episode: int) -> float:
        frac = min(1.0, episode / max(self.cfg.eps_anneal_episodes, 1))
        return self.cfg.eps_start + frac * (self.cfg.eps_end - self.cfg.eps_start)

    def reset_hidden(self, batch: int) -> None:
        self._h = self.agent.init_hidden(batch, self.device)

    @torch.no_grad()
    def act(self, obs: np.ndarray, avail: np.ndarray, eps: float) -> np.ndarray:
        """Epsilon-greedy actions for all agents (obs: (K, obs_dim))."""
        o = torch.as_tensor(obs, dtype=torch.float32, device=self.device)
        q, self._h = self.agent(o, self._h)
        av = torch.as_tensor(avail, dtype=torch.float32, device=self.device)
        q = q.masked_fill(av == 0, -1e9)
        greedy = q.argmax(dim=1).cpu().numpy()
        rand = np.array([
            self.rng.choice(np.flatnonzero(avail[k] > 0)) for k in range(obs.shape[0])
        ])
        explore = self.rng.random(obs.shape[0]) < eps
        return np.where(explore, rand, greedy)

    # ------------------------------------------------------------------ #
    def _batchify(self, eps_list: list[EpisodeBatch]):
        T = min(e.actions.shape[0] for e in eps_list)
        dev = self.device
        stack = lambda arrs: torch.as_tensor(np.stack(arrs), dtype=torch.float32,
                                             device=dev)
        obs = stack([e.obs[: T + 1] for e in eps_list])          # (B,T+1,K,O)
        B, Tp1, K, O = obs.shape
        # compact global state for the mixer: fleet mean + max over agents
        # (2*O dims instead of K*O -> keeps the hyper-networks cheap at large K)
        state = torch.cat([obs.mean(dim=2), obs.amax(dim=2)], dim=-1)  # (B,T+1,2O)
        avail = stack([e.avail[: T + 1] for e in eps_list])      # (B,T+1,K,A)
        actions = torch.as_tensor(np.stack([e.actions[:T] for e in eps_list]),
                                  dtype=torch.long, device=dev)  # (B,T,K)
        reward = stack([e.reward[:T] for e in eps_list])         # (B,T)
        reward_k = stack([e.reward_k[:T] for e in eps_list])     # (B,T,K)
        mask = stack([e.mask[:T] for e in eps_list])             # (B,T)
        return obs, state, avail, actions, reward, reward_k, mask, T

    def learn(self, eps_list: list[EpisodeBatch]) -> float:
        obs, state, avail, actions, reward, reward_k, mask, T = self._batchify(eps_list)
        B, K = actions.shape[0], self.n_agents
        dev = self.device

        # (B, T+1, K, O) -> (B*K, T+1, O) : whole-sequence GRU in one call
        O = obs.shape[-1]
        obs_seq = obs.permute(0, 2, 1, 3).reshape(B * K, T + 1, O)
        A = self.n_actions
        q_online = self.agent.forward_seq(obs_seq)[0].view(B, K, T + 1, A).permute(0, 2, 1, 3)
        with torch.no_grad():
            q_target = self.target_agent.forward_seq(obs_seq)[0].view(
                B, K, T + 1, A).permute(0, 2, 1, 3)                # (B,T+1,K,A)

        chosen = torch.gather(q_online[:, :T], 3, actions.unsqueeze(3)).squeeze(3)

        # double DQN: online picks argmax, target evaluates
        q_online_det = q_online.clone().detach()
        q_online_det[avail == 0] = -1e9
        next_actions = q_online_det[:, 1:].argmax(dim=3, keepdim=True)
        q_tgt_next = torch.gather(q_target[:, 1:], 3, next_actions).squeeze(3)

        if self.mode == "qmix":
            q_tot = self.mixer(chosen.reshape(B * T, K),
                               state[:, :T].reshape(B * T, -1)).view(B, T)
            q_tot_next = self.target_mixer(
                q_tgt_next.reshape(B * T, K), state[:, 1:].reshape(B * T, -1)
            ).view(B, T)
            target = reward + self.cfg.gamma * q_tot_next
            td = (q_tot - target.detach()) * mask
        else:  # iql -- per-agent TD on individual rewards
            target_k = reward_k + self.cfg.gamma * q_tgt_next
            td = (chosen - target_k.detach()) * mask.unsqueeze(2)

        loss = (td ** 2).sum() / mask.sum().clamp(min=1) / (K if self.mode == "iql" else 1)
        self.opt.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(
            list(self.agent.parameters())
            + (list(self.mixer.parameters()) if self.mixer else []),
            self.cfg.grad_clip,
        )
        self.opt.step()
        self.train_steps += 1
        self._soft_update()
        return float(loss.item())

    def _soft_update(self) -> None:
        tau = self.cfg.tau
        for tp, p in zip(self.target_agent.parameters(), self.agent.parameters()):
            tp.data.mul_(1 - tau).add_(tau * p.data)
        if self.mixer is not None:
            for tp, p in zip(self.target_mixer.parameters(), self.mixer.parameters()):
                tp.data.mul_(1 - tau).add_(tau * p.data)

    # ------------------------------------------------------------------ #
    def save(self, path: str) -> None:
        blob = {"agent": self.agent.state_dict(), "mode": self.mode}
        if self.mixer is not None:
            blob["mixer"] = self.mixer.state_dict()
        torch.save(blob, path)

    def load(self, path: str) -> None:
        blob = torch.load(path, map_location=self.device)
        self.agent.load_state_dict(blob["agent"])
        self.target_agent.load_state_dict(blob["agent"])
        if self.mixer is not None and "mixer" in blob:
            try:
                self.mixer.load_state_dict(blob["mixer"])
            except RuntimeError:
                # mixer is only used for centralised training; a size mismatch
                # (different agent count at evaluation) is harmless.
                pass
