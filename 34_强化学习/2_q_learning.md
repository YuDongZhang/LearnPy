# 2. Q-Learning 算法

## 核心思想

Q-Learning (1989) 是最经典的强化学习算法：

- 学习**状态-动作对的价值 Q(s, a)**：在状态 s 下采取动作 a 的期望累计奖励
- 通过迭代更新 Q 值，逐步逼近最优 Q 表
- **Off-policy**：可以从过去的经验中学习，不依赖当前执行策略
- **TD 学习**：用时序差分更新

## 更新公式

```
Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]
```

| 符号 | 含义 |
|------|------|
| α | 学习率 |
| γ | 折扣因子 |
| r | 奖励 |
| s' | 下一个状态 |
| max_{a'} Q(s', a') | 下一个状态的最大 Q 值 |

动作选择用 **ε-greedy** 策略：

```python
if random.random() < ε:
    action = random_action      # 探索
else:
    action = argmax Q(s, :)     # 利用
```

## 简单实现

创建 Q 表、选择动作、更新 Q 表三个核心函数：

```python
import numpy as np

def create_q_table(n_states, n_actions):
    return np.zeros((n_states, n_actions))

def choose_action(state, q_table, epsilon=0.1):
    if np.random.random() < epsilon:
        return np.random.randint(q_table.shape[1])
    else:
        return np.argmax(q_table[state])

def update_q_table(q_table, state, action, reward, next_state,
                   alpha=0.1, gamma=0.95):
    old_value = q_table[state, action]
    next_max = np.max(q_table[next_state])
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    q_table[state, action] = new_value
    return q_table
```

训练循环：每个 episode 用 ε-greedy 选动作、执行、更新 Q 表，并对 ε 做衰减：

```python
for episode in range(n_episodes):
    state = env.reset()
    while True:
        action = choose_action(state, q_table, epsilon)
        next_state, reward, done, _ = env.step(action)
        q_table = update_q_table(q_table, state, action,
                                  reward, next_state, alpha, gamma)
        state = next_state
        if done:
            break
    epsilon = max(0.01, epsilon * 0.995)  # 探索率衰减
```

也可以把 Q 表、选动作、更新封装成 `QLearningAgent` 类，在 `FrozenLake-v1`、`Taxi-v3` 等离散环境上训练。

## SARSA：On-policy 的孪生兄弟

SARSA (State-Action-Reward-State-Action) 与 Q-Learning 更新公式几乎一样，区别在于目标项：

| 对比 | Q-Learning | SARSA |
|------|-----------|-------|
| 类型 | Off-policy | On-policy |
| 目标 | max_{a'} Q(s', a')（最大 Q 值） | Q(s', a')（实际执行的下一个动作） |
| 风格 | 激进，学最优策略 | 保守，考虑探索的影响 |

经典例证是**悬崖行走 (Cliff Walking)** 问题（4×12 网格，底部是悬崖，掉入扣 100 分）：

- Q-Learning 学到最优但危险的路径（贴着悬崖走，探索时可能掉下去）
- SARSA 学到次优但安全的路径（远离悬崖）

## 实用技巧

**学习率衰减**：α = α₀ / (1 + decay × episode)。

**折扣因子**：
- γ 接近 1：考虑长远奖励
- γ 接近 0：重视即时奖励
- 通常取 0.9 ~ 0.99

**探索衰减**：线性衰减、指数衰减、定期重置。

**奖励设计**：
- 正奖励：达成目标
- 负奖励：失败/惩罚
- 小负奖励：鼓励快速完成任务（如迷宫每步 -0.1）

## 与动态规划的区别

| 对比 | Q-Learning | 动态规划（策略迭代/值迭代） |
|------|-----------|--------------------------|
| 模型 | 无模型 (Model-free) | 需要模型（知道转移概率 P） |
| 学习方式 | 在线试错 | 已知环境模型直接计算 |

动态规划适合已知环境模型的小规模问题；Q-Learning 适合未知环境的在线学习。

## 进阶方向

| 技术 | 解决的问题 |
|------|-----------|
| Double Q-Learning | Q 值过高估计（两个 Q 表交替更新） |
| Dueling DQN | 分离 V(s) 和优势 A(s,a) |
| 优先经验回放 | TD 误差大的经验优先回放 |
| Noisy Networks | 用噪声代替 ε-greedy 探索 |

## 优缺点与适用场景

- ✓ 简单易实现，收敛性好
- ✗ 只能处理**离散状态/动作**，状态空间大时难以扩展
- 改进方向：用神经网络做函数近似（→ DQN）
- 适用：离散状态/动作、状态空间较小、需要快速原型

## 代码

讲解对应的示例代码见 `2_q_learning.py`。
