# 3. DQN 深度强化学习

## 为什么需要 DQN

Q-Learning 用表格存储 Q 值，无法处理高维状态空间（如游戏图像）。DQN (Deep Q-Network, 2013, DeepMind) 的思路：**用神经网络近似 Q 函数**。

- 输入：状态 s（可以是图像）
- 输出：每个动作的 Q 值

论文：《Playing Atari with Deep Reinforcement Learning》(2013)。

## 两大核心创新

### 经验回放 (Experience Replay)

把交互数据 (s, a, r, s', done) 存入记忆库，训练时随机采样：

- 打乱数据相关性（序列数据高度相关，直接训练不稳定）
- 提高数据利用率（一条经验可多次使用）

### 目标网络 (Target Network)

另建一个参数固定的目标网络 θ⁻ 来计算 TD 目标：

- 每隔 N 步才把 Q 网络参数复制过来
- 避免"追逐移动目标"导致的训练不稳定

## 损失函数

```
L(θ) = E[(r + γ max_{a'} Q(s', a'; θ⁻) - Q(s, a; θ))²]
```

θ⁻ 是目标网络参数（固定），γ 通常取 0.99。

## 训练流程

```
1. 初始化 Q 网络 θ、目标网络 θ⁻ = θ、经验回放池 D
2. 每回合:
   a) ε-greedy 选择动作，执行并存储经验到 D
   b) 从 D 随机采样 mini-batch
   c) 计算目标: y_i = r_i + γ max_{a'} Q(s'_i, a'; θ⁻)
   d) 最小化 L = (y_i - Q(s_i, a_i; θ))² 更新 Q 网络
   e) 定期同步目标网络
3. 重复直到收敛
```

## PyTorch 实现

Q 网络（低维状态用 MLP）与经验回放：

```python
import torch
import torch.nn as nn

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
        # 随机采样并转为 Tensor
        ...
```

训练核心：用目标网络算 TD 目标，Q 网络拟合当前值，MSE 损失反向传播：

```python
with torch.no_grad():
    next_q = target_network(next_states).max(1)[0]
    target_q = rewards + (1 - dones) * GAMMA * next_q

current_q = q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
loss = nn.MSELoss()(current_q, target_q)
```

典型超参数：

| 超参数 | 取值 |
|--------|------|
| 学习率 | 0.00025 ~ 0.001 |
| 折扣因子 γ | 0.99 |
| 回放池大小 | 10000 ~ 1M |
| Batch size | 32 ~ 128 |
| 目标网络更新间隔 | 每 10 回合 |
| ε 衰减 | 0.995（从 1.0 衰减到 0.01） |

## 图像输入：CNN DQN

处理 Atari 游戏画面时用 CNN：堆叠 4 帧灰度图 (84×84) 作为输入，经卷积层提取特征后输出各动作 Q 值。图像预处理：灰度化 → 缩放到 84×84 → 归一化。

## 改进版本

| 算法 | 年份 | 核心改进 |
|------|------|---------|
| Double DQN | 2015 | 在线网络选动作、目标网络算价值，缓解 Q 值高估 |
| Dueling DQN | 2016 | Q(s,a) = V(s) + A(s,a)，分别估计状态值和优势 |
| Rainbow DQN | 2017 | 集成 Double、Dueling、优先回放、多步学习、分布式RL、噪声网络 |

## 使用 Stable-Baselines3

实际项目中通常直接用现成库，几行代码即可训练 DQN：

```python
from stable_baselines3 import DQN

model = DQN("MlpPolicy", "CartPole-v1", verbose=1,
            learning_rate=0.0001, buffer_size=10000,
            learning_starts=1000, batch_size=64, gamma=0.99,
            train_freq=4, target_update_interval=1000,
            exploration_fraction=0.1, exploration_final_eps=0.05)
model.learn(total_timesteps=100000)
model.save("dqn_cartpole")
```

## 优缺点

- ✓ 处理高维状态空间（图像输入）
- ✓ 经验回放支持离线学习
- ✗ 只能处理离散动作
- ✗ 训练不稳定，需要技巧调参

## 代码

讲解对应的示例代码见 `3_dqn_deep_rl.py`。
