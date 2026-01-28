---
name: reinforcement-learning
description: Q-learning, DQN, PPO, A3C, policy gradient methods, multi-agent systems, and Gym environments. Use for training agents, game AI, robotics, or decision-making systems.
sasmp_version: "1.3.0"
bonded_agent: 04-machine-learning-ai
bond_type: PRIMARY_BOND
---

# Reinforcement Learning

Train intelligent agents that learn optimal behavior through interaction with environments.

## Quick Start

### OpenAI Gymnasium Setup
```python
import gymnasium as gym
import numpy as np

# Create environment
env = gym.make('CartPole-v1')

# Environment info
print(f"Observation space: {env.observation_space}")
print(f"Action space: {env.action_space}")

# Basic interaction loop
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # Random action
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

### Q-Learning (Tabular)
```python
import numpy as np

class QLearning:
    """Tabular Q-Learning for discrete state/action spaces"""

    def __init__(self, n_states, n_actions, lr=0.1, gamma=0.99, epsilon=1.0):
        self.q_table = np.zeros((n_states, n_actions))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def get_action(self, state):
        """Epsilon-greedy action selection"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.q_table.shape[1])
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state, done):
        """Update Q-value using Bellman equation"""
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])

        self.q_table[state, action] += self.lr * (target - self.q_table[state, action])

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Training loop
env = gym.make('FrozenLake-v1')
agent = QLearning(n_states=16, n_actions=4)

for episode in range(10000):
    state, _ = env.reset()
    total_reward = 0

    while True:
        action = agent.get_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        agent.update(state, action, reward, next_state, terminated)

        total_reward += reward
        state = next_state

        if terminated or truncated:
            break
```

## Deep Q-Network (DQN)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

class DQN(nn.Module):
    """Deep Q-Network"""

    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, x):
        return self.network(x)


class ReplayBuffer:
    """Experience replay buffer"""

    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.FloatTensor(states),
            torch.LongTensor(actions),
            torch.FloatTensor(rewards),
            torch.FloatTensor(next_states),
            torch.FloatTensor(dones)
        )

    def __len__(self):
        return len(self.buffer)


class DQNAgent:
    """DQN Agent with target network and experience replay"""

    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99,
                 epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        # Networks
        self.policy_net = DQN(state_dim, action_dim)
        self.target_net = DQN(state_dim, action_dim)
        self.target_net.load_state_dict(self.policy_net.state_dict())

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.buffer = ReplayBuffer()

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)

        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.policy_net(state)
            return q_values.argmax().item()

    def train(self, batch_size=64):
        if len(self.buffer) < batch_size:
            return

        states, actions, rewards, next_states, dones = self.buffer.sample(batch_size)

        # Current Q values
        current_q = self.policy_net(states).gather(1, actions.unsqueeze(1))

        # Target Q values
        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0]
            target_q = rewards + self.gamma * next_q * (1 - dones)

        # Loss
        loss = nn.MSELoss()(current_q.squeeze(), target_q)

        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target(self):
        """Update target network"""
        self.target_net.load_state_dict(self.policy_net.state_dict())
```

## Policy Gradient Methods

### REINFORCE
```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

class PolicyNetwork(nn.Module):
    """Policy network for REINFORCE"""

    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)

    def get_action(self, state):
        probs = self.forward(torch.FloatTensor(state))
        dist = Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)


class REINFORCE:
    """REINFORCE with baseline"""

    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99):
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma

    def compute_returns(self, rewards):
        """Compute discounted returns"""
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns)
        # Normalize for stable training
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        return returns

    def update(self, log_probs, rewards):
        returns = self.compute_returns(rewards)
        log_probs = torch.stack(log_probs)

        # Policy gradient loss
        loss = -(log_probs * returns).mean()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

# Training
agent = REINFORCE(state_dim=4, action_dim=2)

for episode in range(1000):
    state, _ = env.reset()
    log_probs = []
    rewards = []

    while True:
        action, log_prob = agent.policy.get_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)

        log_probs.append(log_prob)
        rewards.append(reward)

        state = next_state
        if terminated or truncated:
            break

    agent.update(log_probs, rewards)
```

### Proximal Policy Optimization (PPO)
```python
import torch
import torch.nn as nn
import torch.optim as optim

class ActorCritic(nn.Module):
    """Actor-Critic network for PPO"""

    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()

        # Shared feature extractor
        self.features = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU()
        )

        # Actor (policy)
        self.actor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )

        # Critic (value function)
        self.critic = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        features = self.features(x)
        return self.actor(features), self.critic(features)


class PPO:
    """Proximal Policy Optimization"""

    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99,
                 clip_ratio=0.2, epochs=10, batch_size=64):
        self.model = ActorCritic(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = gamma
        self.clip_ratio = clip_ratio
        self.epochs = epochs
        self.batch_size = batch_size

    def compute_gae(self, rewards, values, dones, gamma=0.99, lam=0.95):
        """Generalized Advantage Estimation"""
        advantages = []
        gae = 0

        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]

            delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
            gae = delta + gamma * lam * (1 - dones[t]) * gae
            advantages.insert(0, gae)

        return torch.tensor(advantages)

    def update(self, states, actions, old_log_probs, returns, advantages):
        """PPO update with clipping"""

        for _ in range(self.epochs):
            # Get current policy outputs
            probs, values = self.model(states)
            dist = Categorical(probs)
            log_probs = dist.log_prob(actions)
            entropy = dist.entropy().mean()

            # Ratio for PPO clipping
            ratio = torch.exp(log_probs - old_log_probs)

            # Clipped surrogate loss
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.clip_ratio,
                               1 + self.clip_ratio) * advantages
            actor_loss = -torch.min(surr1, surr2).mean()

            # Critic loss
            critic_loss = nn.MSELoss()(values.squeeze(), returns)

            # Total loss with entropy bonus
            loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy

            self.optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(self.model.parameters(), 0.5)
            self.optimizer.step()
```

## Multi-Agent RL

```python
class MultiAgentEnv:
    """Simple multi-agent environment wrapper"""

    def __init__(self, n_agents, env_fn):
        self.n_agents = n_agents
        self.envs = [env_fn() for _ in range(n_agents)]

    def reset(self):
        return [env.reset()[0] for env in self.envs]

    def step(self, actions):
        results = [env.step(a) for env, a in zip(self.envs, actions)]
        observations = [r[0] for r in results]
        rewards = [r[1] for r in results]
        dones = [r[2] or r[3] for r in results]
        return observations, rewards, dones


class IndependentLearners:
    """Independent Q-learning agents"""

    def __init__(self, n_agents, state_dim, action_dim):
        self.agents = [
            DQNAgent(state_dim, action_dim)
            for _ in range(n_agents)
        ]

    def get_actions(self, observations):
        return [agent.get_action(obs)
                for agent, obs in zip(self.agents, observations)]

    def train(self):
        for agent in self.agents:
            agent.train()
```

## Reward Shaping

```python
def shape_reward(reward, state, next_state, done, info):
    """Design better reward signals"""

    shaped_reward = reward

    # Progress reward (encourage forward movement)
    if 'x_position' in info:
        progress = info['x_position'] - info.get('prev_x', 0)
        shaped_reward += 0.1 * progress

    # Survival bonus
    if not done:
        shaped_reward += 0.01

    # Penalty for dangerous states
    if 'danger_zone' in info and info['danger_zone']:
        shaped_reward -= 0.5

    # Goal proximity reward
    if 'goal_distance' in info:
        shaped_reward += 0.1 * (1.0 / (info['goal_distance'] + 1))

    return shaped_reward


# Curriculum learning
class CurriculumEnv:
    """Environment with difficulty progression"""

    def __init__(self, base_env, difficulty_schedule):
        self.env = base_env
        self.schedule = difficulty_schedule
        self.current_level = 0
        self.episode_count = 0

    def reset(self):
        self.episode_count += 1

        # Increase difficulty based on schedule
        if self.episode_count in self.schedule:
            self.current_level += 1
            self._update_difficulty()

        return self.env.reset()

    def _update_difficulty(self):
        # Modify environment parameters
        pass
```

## Stable Baselines3 (Production Ready)

```python
from stable_baselines3 import PPO, DQN, A2C
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import EvalCallback

# Vectorized environments for parallel training
def make_env():
    return gym.make('CartPole-v1')

env = DummyVecEnv([make_env for _ in range(4)])

# Train PPO agent
model = PPO(
    'MlpPolicy',
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    verbose=1,
    tensorboard_log="./ppo_logs/"
)

# Evaluation callback
eval_env = gym.make('CartPole-v1')
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path='./best_model/',
    log_path='./logs/',
    eval_freq=1000,
    n_eval_episodes=10
)

# Train
model.learn(total_timesteps=100000, callback=eval_callback)

# Save and load
model.save("ppo_cartpole")
model = PPO.load("ppo_cartpole")

# Inference
obs = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
```

## Hyperparameter Tuning

```python
# Common hyperparameter ranges
rl_hyperparameters = {
    "learning_rate": [1e-4, 3e-4, 1e-3],
    "gamma": [0.95, 0.99, 0.999],
    "batch_size": [32, 64, 128, 256],
    "n_steps": [128, 256, 512, 2048],
    "clip_range": [0.1, 0.2, 0.3],
    "entropy_coef": [0.0, 0.01, 0.05],
    "hidden_sizes": [(64, 64), (128, 128), (256, 256)]
}

# Optuna tuning
import optuna

def objective(trial):
    lr = trial.suggest_float('lr', 1e-5, 1e-2, log=True)
    gamma = trial.suggest_float('gamma', 0.9, 0.9999)
    n_steps = trial.suggest_int('n_steps', 128, 2048, step=128)

    model = PPO('MlpPolicy', env, learning_rate=lr,
                gamma=gamma, n_steps=n_steps)
    model.learn(total_timesteps=50000)

    # Evaluate
    mean_reward = evaluate_policy(model, eval_env, n_eval_episodes=10)
    return mean_reward

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
```

## Common Issues & Solutions

**Issue: Training instability**
```
Solutions:
- Reduce learning rate
- Increase batch size
- Use gradient clipping
- Normalize observations and rewards
- Use proper random seeds
```

**Issue: Poor exploration**
```
Solutions:
- Increase epsilon/entropy
- Use curiosity-driven exploration
- Add noise to actions (Gaussian, OU)
- Use count-based exploration bonus
```

**Issue: Reward hacking**
```
Solutions:
- Careful reward design
- Use sparse rewards when possible
- Test with adversarial evaluation
- Monitor for unexpected behaviors
```

## Best Practices

1. **Environment**: Verify env correctness before training
2. **Normalization**: Normalize states and rewards
3. **Logging**: Track episode rewards, lengths, losses
4. **Reproducibility**: Set seeds for all random sources
5. **Evaluation**: Separate eval environment, many episodes
6. **Hyperparameters**: Start with known good defaults
7. **Baseline**: Compare against random policy
