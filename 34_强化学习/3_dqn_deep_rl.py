"""
DQN 深度强化学习
==============

介绍 DQN (Deep Q-Network) 算法的原理和实现。
"""

print("=" * 60)
print("1. DQN 简介")
print("=" * 60)

print("""
DQN (Deep Q-Network) - 2013:

背景:
  • Q-Learning 无法处理高维状态空间
  • 深度神经网络可以处理图像等高维输入

核心创新:
  • 用神经网络近似 Q 函数
  • 经验回放 (Experience Replay)
  • 目标网络 (Target Network)

DQN 论文:
  "Playing Atari with Deep Reinforcement Learning" (2013)
  - DeepMind
""")

print()
print("=" * 60)
print("2. DQN 原理")
print("=" * 60)

print("""
2.1 函数近似

  用神经网络 Q(s, a; θ) 近似 Q*(s, a)

  输入: 状态 s (可以是图像)
  输出: 每个动作的 Q 值

2.2 损失函数

  L(θ) = E[(r + γ max_{a'} Q(s', a'; θ⁻) - Q(s, a; θ))²]

  θ⁻: 目标网络参数 (固定)

2.3 经验回放

  存储: (s, a, r, s', done)
  优点:
    • 打乱数据相关性
    • 提高数据利用率
    • 稳定训练

2.4 目标网络

    固定目标网络参数 θ⁻
    每隔 N 步更新
    解决训练不稳定问题
""")

print()
print("=" * 60)
print("3. DQN 算法")
print("=" * 60)

print("""
DQN 训练步骤:

1. 初始化:
   - Q 网络参数 θ
   - 目标网络参数 θ⁻ = θ
   - 经验回放池 D

2. 每回合:
   a) 收集经验:
      - ε-greedy 选择动作
      - 执行动作存储到 D

   b) 从 D 随机采样 mini-batch

   c) 计算损失:
      y_i = r_i + γ max_{a'} Q(s'_i, a'; θ⁻)
      L = (y_i - Q(s_i, a_i; θ))²

   d) 更新 Q 网络

   e) 定期更新目标网络

3. 重复直到收敛
""")

print()
print("=" * 60)
print("4. PyTorch DQN 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym

# 4.1 Q 网络
class DQN(nn.Module):
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

# 4.2 经验回放
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = []
        self.capacity = capacity
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        batch = np.random.choice(len(self.buffer), batch_size, replace=False)
        states, actions, rewards, next_states, dones = [], [], [], [], []

        for i in batch:
            s, a, r, ns, d = self.buffer[i]
            states.append(s)
            actions.append(a)
            rewards.append(r)
            next_states.append(ns)
            dones.append(d)

        return (
            torch.FloatTensor(np.array(states)),
            torch.LongTensor(actions),
            torch.FloatTensor(rewards),
            torch.FloatTensor(np.array(next_states)),
            torch.FloatTensor(dones)
        )

    def __len__(self):
        return len(self.buffer)
''')

print()
print("=" * 60)
print("5. DQN 训练")
print("=" * 60)

print('''
# 5.1 超参数
BATCH_SIZE = 64
GAMMA = 0.99
LR = 0.001
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
TARGET_UPDATE = 10
N_EPISODES = 500

# 5.2 初始化
env = gym.make("CartPole-v1")
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

q_network = DQN(state_dim, action_dim)
target_network = DQN(state_dim, action_dim)
target_network.load_state_dict(q_network.state_dict())

optimizer = optim.Adam(q_network.parameters(), lr=LR)
replay_buffer = ReplayBuffer()

# 5.3 选择动作
def choose_action(state, epsilon):
    if np.random.random() < epsilon:
        return np.random.randint(action_dim)
    else:
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = q_network(state)
            return q_values.argmax(1).item()

# 5.4 训练循环
epsilon = EPSILON_START
rewards_history = []

for episode in range(N_EPISODES):
    state = env.reset()
    total_reward = 0

    while True:
        # 选择动作
        action = choose_action(state, epsilon)

        # 执行动作
        next_state, reward, done, _ = env.step(action)

        # 存储经验
        replay_buffer.push(state, action, reward, next_state, done)

        state = next_state
        total_reward += reward

        # 训练
        if len(replay_buffer) >= BATCH_SIZE:
            states, actions, rewards, next_states, dones = replay_buffer.sample(BATCH_SIZE)

            # 计算目标 Q 值
            with torch.no_grad():
                next_q = target_network(next_states).max(1)[0]
                target_q = rewards + (1 - dones) * GAMMA * next_q

            # 计算当前 Q 值
            current_q = q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)

            # 更新
            loss = nn.MSELoss()(current_q, target_q)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if done:
            break

    # 更新目标网络
    if episode % TARGET_UPDATE == 0:
        target_network.load_state_dict(q_network.state_dict())

    # 衰减探索率
    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
    rewards_history.append(total_reward)

    if episode % 50 == 0:
        avg_reward = np.mean(rewards_history[-50:])
        print(f"Episode {episode}: Avg Reward = {avg_reward:.2f}, Epsilon = {epsilon:.3f}")
''')

print()
print("=" * 60)
print("6. 使用 CNN 的 DQN")
print("=" * 60)

print('''
import torch.nn as nn

# 6.1 CNN Q 网络 (用于图像输入)
class CNN_DQN(nn.Module):
    def __init__(self, action_dim):
        super(CNN_DQN, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(4, 32, 8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1),
            nn.ReLU()
        )

        self.fc = nn.Sequential(
            nn.Linear(7 * 7 * 64, 512),
            nn.ReLU(),
            nn.Linear(512, action_dim)
        )

    def forward(self, x):
        # x: [batch, 4, 84, 84]
        conv_out = self.conv(x)
        flat = conv_out.view(conv_out.size(0), -1)
        return self.fc(flat)

# 6.2 预处理图像
def preprocess(frame):
    import cv2
    # 灰度化
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # 缩放
    resized = cv2.resize(gray, (84, 84))
    # 归一化
    return resized / 255.0
''')

print()
print("=" * 60)
print("7. Double DQN")
print("=" * 60)

print("""
Double DQN (2015):

问题:
  • Q-Learning 会高估 Q 值
  • 因为使用了相同的 max 操作

解决:
  • 使用两个 Q 网络
  • 在线网络选择动作
  • 目标网络计算价值

更新公式:
  y_i = r_i + γ Q(s'_i, argmax_a Q(s'_i, a; θ); θ⁻)

优势:
  • 减少过度估计
  • 更稳定
  • 效果更好
""")

print()
print("=" * 60)
print("8. Dueling DQN")
print("=" * 60)

print("""
Dueling DQN (2016):

核心思想:
  Q(s, a) = V(s) + A(s, a)

  • V(s): 状态的价值
  • A(s, a): 动作的优势

优势:
  • 分别估计 V 和 A
  • 学习更高效
  • 对价值估计更准确

实现:
  • 两个stream: V 和 A
  • 聚合: Q = V + (A - mean(A))
""")

print()
print("=" * 60)
print("9. Rainbow DQN")
print("=" * 60)

print("""
Rainbow DQN (2017):

结合多种技术:

1. Double DQN - 减少过度估计
2. Dueling DQN - 优势分离
3. Prioritized Experience Replay - 优先回放
4. Multi-step Learning - 多步学习
5. Distributional RL - 分布式 RL
6. Noisy Networks - 噪声网络

效果:
  • 在 Atari 上取得最佳效果
  • 超越人类水平
""")

print()
print("=" * 60)
print("10. 完整 DQN 类")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym
from collections import deque
import random

class DQNAgent:
    def __init__(self, state_dim, action_dim, config):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = config.get("gamma", 0.99)
        self.epsilon = config.get("epsilon_start", 1.0)
        self.epsilon_end = config.get("epsilon_end", 0.01)
        self.epsilon_decay = config.get("epsilon_decay", 0.995)
        self.batch_size = config.get("batch_size", 64)
        self.lr = config.get("lr", 0.001)
        self.target_update = config.get("target_update", 10)

        # 网络
        self.q_network = DQN(state_dim, action_dim)
        self.target_network = DQN(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.lr)
        self.memory = ReplayBuffer(config.get("memory_size", 10000))

    def select_action(self, state, training=True):
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            with torch.no_grad():
                if isinstance(state, np.ndarray):
                    state = torch.FloatTensor(state).unsqueeze(0)
                return self.q_network(state).argmax(1).item()

    def store_transition(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def train(self):
        if len(self.memory) < self.batch_size:
            return None

        # 采样
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        # 目标 Q 值
        with torch.no_grad():
            next_q = self.target_network(next_states).max(1)[0]
            target_q = rewards + (1 - dones) * self.gamma * next_q

        # 当前 Q 值
        current_q = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        # 损失
        loss = nn.MSELoss()(current_q, target_q)

        # 更新
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def update_target(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
''')

print()
print("=" * 60)
print("11. DQN 技巧")
print("=" * 60)

print("""
11.1 预处理

  • 灰度化
  • 缩放到固定大小
  • 帧堆叠 (4帧)
  • 归一化

11.2 网络结构

  • CNN (图像输入)
  • MLP (低维状态)
  • 跳连 (ResNet)

11.3 超参数

  • 学习率: 0.00025 - 0.001
  • 折扣因子: 0.99
  • 经验回放: 100K - 1M
  • Batch size: 32 - 128

11.4 训练技巧

  • 预热 (先随机收集经验)
  • 目标网络更新频率
  • 梯度裁剪
""")

print()
print("=" * 60)
print("12. 使用 Stable-Baselines3")
print("=" * 60)

print('''
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback

# 创建环境
env = gym.make("CartPole-v1")

# 创建模型
model = DQN(
    "MlpPolicy",
    env,
    learning_rate=0.0001,
    buffer_size=10000,
    learning_starts=1000,
    batch_size=64,
    gamma=0.99,
    train_freq=4,
    target_update_interval=1000,
    exploration_fraction=0.1,
    exploration_final_eps=0.05,
    verbose=1
)

# 训练
model.learn(total_timesteps=100000)

# 保存
model.save("dqn_cartpole")

# 加载
model = DQN.load("dqn_cartpole")

# 测试
obs = env.reset()
for i in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _ = env.step(action)
    env.render()
    if done:
        obs = env.reset()
''')

print()
print("=" * 60)
print("13. DQN 总结")
print("""
DQN 要点:

✓ 核心创新:
  • 神经网络函数近似
  • 经验回放
  • 目标网络

✓ 改进版本:
  • Double DQN
  • Dueling DQN
  • Rainbow DQN

✓ 适用场景:
  • 高维状态空间
  • 图像输入
  • 复杂环境

✓ 优缺点:
  ✓ 处理高维输入
  ✓ 离线学习
  ✗ 只能处理离散动作
  ✗ 训练不稳定

✓ 工具:
  • PyTorch 实现
  • Stable-Baselines3
""")
