"""
Policy Gradient 方法
=================

介绍 Policy Gradient (策略梯度) 和 Actor-Critic 算法。
"""

print("=" * 60)
print("1. Policy Gradient 简介")
print("=" * 60)

print("""
Policy Gradient (策略梯度):

为什么需要 Policy Gradient?

  • DQN 只适用于离散动作
  • 有些问题动作是连续的
  • 直接学习策略比学习值函数更直接
  • 策略可以随机 ( stochastic )

核心思想:
  • 直接学习策略 π(a|s)
  • 优化目标: 期望累计奖励
  • 使用梯度上升更新策略
""")

print()
print("=" * 60)
print("2. 策略梯度定理")
print("=" * 60)

print("""
策略梯度定理:

目标: 最大化期望奖励
  J(θ) = E_πθ [R]

梯度:
  ∇θ J(θ) = E_πθ [∇θ log πθ(a|s) · Q^π(s, a)]

简化:
  ∇θ J(θ) ≈ E[∇θ log πθ(a|s) · G_t]

其中:
  • πθ(a|s): 策略网络输出的概率
  • G_t: 累计奖励
  • ∇θ log πθ(a|s): 得分函数 (Score function)

直觉:
  • 增加出现好结果的策略的概率
  • 减少出现坏结果的策略的概率
""")

print()
print("=" * 60)
print("3. REINFORCE 算法")
print("=" * 60)

print("""
REINFORCE (1992):

步骤:
  1. 用当前策略采样轨迹
  2. 计算每个状态的回报 G_t
  3. 用梯度上升更新策略参数

更新公式:
  θ ← θ + α · ∇θ log πθ(a_t|s_t) · G_t

优点:
  • 简单直观
  • 可以处理连续动作

缺点:
  • 方差大
  • 收敛慢
""")

print()
print("=" * 60)
print("4. PyTorch REINFORCE 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym

# 4.1 策略网络
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)

# 4.2 采样动作
def select_action(state, policy_net):
    state = torch.FloatTensor(state).unsqueeze(0)
    probs = policy_net(state)
    action_dist = torch.distributions.Categorical(probs)
    action = action_dist.sample()
    log_prob = action_dist.log_prob(action)
    return action.item(), log_prob

# 4.3 计算回报
def compute_returns(rewards, gamma=0.99):
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    return torch.FloatTensor(returns)

# 4.4 训练
env = gym.make("CartPole-v1")
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

policy_net = PolicyNetwork(state_dim, action_dim)
optimizer = optim.Adam(policy_net.parameters(), lr=0.01)

n_episodes = 500

for episode in range(n_episodes):
    log_probs = []
    rewards = []
    state = env.reset()

    while True:
        action, log_prob = select_action(state, policy_net)
        next_state, reward, done, _ = env.step(action)

        log_probs.append(log_prob)
        rewards.append(reward)

        if done:
            break

        state = next_state

    # 计算回报
    returns = compute_returns(rewards)
    returns = (returns - returns.mean()) / (returns.std() + 1e-8)

    # 策略梯度更新
    policy_loss = []
    for log_prob, G in zip(log_probs, returns):
        policy_loss.append(-log_prob * G)

    optimizer.zero_grad()
    torch.cat(policy_loss).sum().backward()
    optimizer.step()

    if episode % 50 == 0:
        print(f"Episode {episode}: Reward = {sum(rewards)}")
''')

print()
print("=" * 60)
print("5. Actor-Critic")
print("=" * 60)

print("""
Actor-Critic (1999):

结合值函数和策略梯度:

  • Actor: 策略网络, 选择动作
  • Critic: 值网络, 评估动作

优势函数:
  A(s, a) = Q(s, a) - V(s)

  • 减少方差
  • 更快收敛

更新:
  • Actor: ∇θ log πθ(a|s) · A(s, a)
  • Critic: (R + γV(s') - V(s))²
""")

print()
print("=" * 60)
print("6. Actor-Critic 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym

# 6.1 Actor 网络
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Actor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)

# 6.2 Critic 网络
class Critic(nn.Module):
    def __init__(self, state_dim):
        super(Critic, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.network(x)

# 6.3 训练
actor = Actor(4, 2)
critic = Critic(4)

actor_optimizer = optim.Adam(actor.parameters(), lr=0.001)
critic_optimizer = optim.Adam(critic.parameters(), lr=0.001)

n_episodes = 500

for episode in range(n_episodes):
    state = env.reset()
    total_reward = 0

    while True:
        state_tensor = torch.FloatTensor(state).unsqueeze(0)

        # Actor 选择动作
        probs = actor(state_tensor)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()

        # 执行动作
        next_state, reward, done, _ = env.step(action.item())

        # 计算 TD 目标
        with torch.no_grad():
            target = reward + 0.99 * critic(torch.FloatTensor(next_state).unsqueeze(0))

        # Critic 更新
        current_value = critic(state_tensor)
        critic_loss = nn.MSELoss()(current_value, target)

        critic_optimizer.zero_grad()
        critic_loss.backward()
        critic_optimizer.step()

        # Actor 更新
        advantage = target - current_value
        log_prob = dist.log_prob(action)
        actor_loss = -log_prob * advantage.detach()

        actor_optimizer.zero_grad()
        actor_loss.backward()
        actor_optimizer.step()

        total_reward += reward
        state = next_state

        if done:
            break

    if episode % 50 == 0:
        print(f"Episode {episode}: Reward = {total_reward}")
''')

print()
print("=" * 60)
print("7. A2C / A3C")
print("=" * 60)

print("""
A2C (Advantage Actor-Critic):

改进:
  • 使用优势函数代替 Q 值
  • 并行环境采样

优势函数:
  A(s, a) = Q(s, a) - V(s)
  A(s, a) = r + γV(s') - V(s)

A3C:
  • Asynchronous A3C
  • 多个 worker 并行收集数据
  • 异步更新
""")

print()
print("=" * 60)
print("8. PPO 算法")
print("=" * 60)

print("""
PPO (Proximal Policy Optimization) - 2017:

核心思想:
  • 信任域方法
  • 限制策略更新幅度

目标函数:
  L^CLIP(θ) = E[min(r(θ)·A, clip(r(θ), 1-ε, 1+ε)·A)]

  r(θ) = πθ(a|s) / πθ_old(a|s)

特点:
  • 稳定
  • 高效
  • 易于实现
  • OpenAI 默认算法
""")

print()
print("=" * 60)
print("9. PPO 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
import gym

class PPO:
    def __init__(self, state_dim, action_dim, lr=0.0003, gamma=0.99, eps_clip=0.2):
        self.gamma = gamma
        self.eps_clip = eps_clip

        self.actor = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )

        self.critic = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 1)
        )

        self.actor_opt = optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_opt = optim.Adam(self.critic.parameters(), lr=lr)

    def get_action(self, state):
        probs = self.actor(state)
        dist = Categorical(probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action, log_prob

    def update(self, states, actions, old_log_probs, returns, advantages):
        # 计算新的策略概率
        probs = self.actor(states)
        dist = Categorical(probs)
        new_log_probs = dist.log_prob(actions)

        # PPO 损失
        ratio = torch.exp(new_log_probs - old_log_probs)
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1-self.eps_clip, 1+self.eps_clip) * advantages

        actor_loss = -torch.min(surr1, surr2).mean()

        # Critic 损失
        values = self.critic(states)
        critic_loss = nn.MSELoss()(values, returns)

        # 更新
        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()

        self.critic_opt.zero_grad()
        critic_loss.backward()
        self.critic_opt.step()

# 使用
env = gym.make("CartPole-v1")
agent = PPO(4, 2)

# 训练循环...
''')

print()
print("=" * 60)
print("10. SAC 算法")
print("=" * 60)

print("""
SAC (Soft Actor-Critic) - 2018:

特点:
  • 最大熵强化学习
  • 熵正则化
  • 连续动作

目标:
  J(π) = E_π[Q(s,a) + α·H(π(·|s))]

  • H: 熵 (鼓励探索)
  • α: 温度参数

优点:
  • 稳定
  • 高效
  • 适合连续动作
""")

print()
print("=" * 60)
print("11. 使用 Stable-Baselines3")
print("=" * 60)

print('''
from stable_baselines3 import PPO, A2C, SAC
from stable_baselines3.common.env_util import make_vec_env

# PPO
model = PPO("MlpPolicy", "CartPole-v1", verbose=1)
model.learn(total_timesteps=100000)

# 测试
obs = env.reset()
for i in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _ = env.step(action)
    env.render()
    if done:
        obs = env.reset()

# A2C
model = A2C("MlpPolicy", "CartPole-v1", verbose=1)
model.learn(total_timesteps=100000)

# SAC (连续动作)
from gym.envs.registration import register
register(id="Pendulum-v2", entry_point="gym.envs.classic_control:PendulumEnv")

model = SAC("MlpPolicy", "Pendulum-v2", verbose=1)
model.learn(total_timesteps=100000)
''')

print()
print("=" * 60)
print("12. 连续动作空间")
print("=" * 60)

print("""
连续动作处理:

1. 高斯策略
  • π(a|s) = N(μ(s), σ(s)²)
  • 输出均值和标准差
  • 从高斯分布采样

2. 方差缩减
  • 使用基线 (baseline)
  • 优势函数
  • 蒙特卡洛 returns

3. 确定性策略
  • 不输出概率
  • 直接输出动作
  • DPG, DDPG 算法
""")

print()
print("=" * 60)
print("13. Policy Gradient 总结")
print("=" * 60)

print("""
Policy Gradient 要点:

✓ 核心思想:
  • 直接学习策略
  • 策略梯度更新
  • 可处理连续动作

✓ 主要算法:
  • REINFORCE: 基础
  • Actor-Critic: 结合值函数
  • A2C/A3C: 并行
  • PPO: 稳定高效
  • SAC: 最大熵

✓ 优缺点:
  ✓ 连续动作
  ✓ 随机策略
  ✗ 方差大
  ✗ 收敛慢

✓ 选择建议:
  • 离散: PPO
  • 连续: SAC, PPO
  • 简单: REINFORCE
""")
