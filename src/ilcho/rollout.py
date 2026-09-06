"""Episode rollout helpers shared by training and evaluation."""
from __future__ import annotations

import numpy as np

from .environment import CHOEnv
from .qmix import EpisodeBatch, MARLController


def run_learning_episode(
    env: CHOEnv, ctrl: MARLController, episode: int, ue_seed: int | None = None
) -> tuple[EpisodeBatch, dict, float]:
    """Roll one episode with epsilon-greedy exploration and return a batch."""
    obs, avail = env.reset(ue_seed=ue_seed)
    ctrl.reset_hidden(env.K)
    eps = ctrl.epsilon(episode)
    T = env.T
    K = env.K

    # obs/avail stored as float16 to keep the replay buffer small at large K
    # (the global mixing "state" is just obs reshaped, so it is not stored).
    obs_buf = np.zeros((T + 1, K, env.obs_dim), np.float16)
    avail_buf = np.zeros((T + 1, K, env.n_actions), np.bool_)
    act_buf = np.zeros((T, K), np.int64)
    rew_buf = np.zeros(T, np.float32)
    rewk_buf = np.zeros((T, K), np.float32)
    mask_buf = np.zeros(T, np.float32)

    total_r = 0.0
    for t in range(T):
        obs_buf[t] = obs
        avail_buf[t] = avail > 0
        actions = ctrl.act(obs, avail, eps)
        act_buf[t] = actions
        obs, avail, rewards, done, _ = env.step(actions)
        rew_buf[t] = rewards.mean()
        rewk_buf[t] = rewards
        mask_buf[t] = 1.0
        total_r += float(rewards.mean())
        if done:
            obs_buf[t + 1] = obs
            avail_buf[t + 1] = avail > 0
            break

    batch = EpisodeBatch(
        obs=obs_buf, actions=act_buf, avail=avail_buf,
        reward=rew_buf, reward_k=rewk_buf, mask=mask_buf,
    )
    return batch, env.episode_metrics(), total_r


def run_policy_episode(env: CHOEnv, policy, ue_seed: int | None = None,
                       greedy_ctrl: MARLController | None = None) -> dict:
    """Roll one episode with a fixed policy (baseline) or a greedy controller."""
    obs, avail = env.reset(ue_seed=ue_seed)
    if greedy_ctrl is not None:
        greedy_ctrl.reset_hidden(env.K)
    for _ in range(env.T):
        if greedy_ctrl is not None:
            actions = greedy_ctrl.act(obs, avail, eps=0.0)
        else:
            actions = policy.act(obs, avail)
        obs, avail, _, done, _ = env.step(np.asarray(actions))
        if done:
            break
    return env.episode_metrics()
