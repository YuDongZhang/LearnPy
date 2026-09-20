# 1. 强化学习概述

## 什么是强化学习

**强化学习 (Reinforcement Learning, RL)** 是机器学习的一个重要分支，智能体通过与环境交互、不断试错来学习最优策略，目标是最大化累计奖励。

与监督学习的区别：

| 对比 | 监督学习 | 强化学习 |
|------|---------|---------|
| 数据 | 需要标注数据 | 通过与环境交互获取反馈 |
| 反馈 | 每个样本有正确答案 | 只有延迟的奖励信号 |
| 目标 | 拟合输入输出映射 | 最大化累计奖励 |

## 基本要素

| 要素 | 含义 |
|------|------|
| 智能体 (Agent) | 学习者、决策者 |
| 环境 (Environment) | 智能体所处的世界 |
| 状态 (State) | 环境的描述 |
| 动作 (Action) | 智能体可以采取的行动 |
| 奖励 (Reward) | 环境的反馈信号 |
| 策略 (Policy) | 状态到动作的映射 |

交互流程：

```
智能体 ──动作(A)──> 环境
                   │
                   ▼
              状态(S') + 奖励(R)
                   │
                   ▼
              智能体 <──
```

## 探索与利用

- **探索 (Exploration)**：尝试新的动作，发现可能更好的策略
- **利用 (Exploitation)**：使用已知的最优策略

平衡二者的经典方法是 **ε-greedy**：

```
以 ε 概率随机选择动作 (探索)
以 1-ε 概率选择最优动作 (利用)
```

其他探索策略：Boltzmann 概率探索、UCB、Thompson Sampling。

## 马尔可夫决策过程 (MDP)

MDP 用五元组 (S, A, P, R, γ) 描述强化学习问题：

| 符号 | 含义 |
|------|------|
| S | 状态空间 |
| A | 动作空间 |
| P | 状态转移概率 P(s'\|s, a) |
| R | 奖励函数 R(s, a, s') |
| γ | 折扣因子 (0 < γ < 1) |

**马尔可夫性**：下一个状态只依赖当前状态和动作，与历史无关：

```
P(s_{t+1} | s_t, a_t, s_{t-1}, ...) = P(s_{t+1} | s_t, a_t)
```

## 值函数与贝尔曼方程

累计回报（从时刻 t 开始）：

```
G_t = R_t + γR_{t+1} + γ²R_{t+2} + ...
```

- **状态值函数**：V(s) = E[G_t | s_t = s]
- **状态-动作值函数**：Q(s, a) = E[G_t | s_t = s, a_t = a]

贝尔曼方程给出值函数的递归关系：

```
V(s) = max_a [ R(s, a) + γ Σ P(s'|s, a) V(s') ]
Q(s, a) = R(s, a) + γ Σ P(s'|s, a) max_{a'} Q(s', a')
```

最优策略：π*(s) = argmax_a Q*(s, a)。

## 发展历程

| 年份 | 里程碑 |
|------|--------|
| 1956 | Bellman 提出动态规划 |
| 1989 | Q-Learning 算法提出 |
| 1992 | TD 学习 |
| 2013 | DQN (Deep Q-Network) |
| 2015 | DeepMind Atari 游戏 |
| 2016 | AlphaGo 战胜李世石 |
| 2017 | AlphaGo Zero |
| 2018 | AlphaStar (星际争霸) |
| 2019 | OpenAI Five (Dota2) |
| 2022 | ChatGPT (RLHF) |

## 算法分类

| 类别 | 代表算法 | 特点 |
|------|---------|------|
| 基于值函数 | Q-Learning, SARSA, DQN, Double DQN, Dueling DQN, Rainbow | 学习值函数，间接得到策略 |
| 基于策略 | REINFORCE, Actor-Critic, A2C/A3C, PPO, SAC | 直接学习策略 |
| 模型基 | Dyna-Q, AlphaZero, MuZero | 学习环境模型 |

## 应用领域

| 领域 | 应用 |
|------|------|
| 游戏 | Atari, AlphaGo, Dota2 |
| 机器人 | 运动控制, 抓取 |
| 推荐系统 | 个性化推荐 |
| 自动驾驶 | 决策控制 |
| 资源调度 | 数据中心节能 |
| 金融 | 交易策略 |
| NLP | 对话系统, RLHF |

## 常用环境

最常用的是 OpenAI Gym（新版本为 Gymnasium）：

```bash
pip install gymnasium
pip install stable-baselines3
pip install ale-py  # Atari 环境
pip install pygame  # 可视化
```

常见环境：CartPole（倒立摆）、MountainCar（爬山车）、Pendulum（摆）、Atari 游戏、MuJoCo 物理模拟。

其他环境平台：DeepMind Lab、Unity ML-Agents、StarCraft II Learning Environment。

## 第一个 RL 程序

```python
import gym

env = gym.make("CartPole-v1")
state = env.reset()

for step in range(1000):
    action = env.action_space.sample()  # 随机动作
    state, reward, done, info = env.step(action)
    env.render()
    if done:
        break

env.close()
print(f"动作空间: {env.action_space}")
print(f"状态空间: {env.observation_space}")
```

## 评估指标

- **累计奖励 (Total Reward)**：一个 episode 的所有奖励之和
- **回合成功率 (Success Rate)**：达到目标的回合比例
- **收敛速度**：达到指定性能所需的步数/回合数
- **泛化能力**：在未见过的环境中的表现

## 学习路径建议

1. 强化学习基础概念（MDP、贝尔曼方程）
2. Q-Learning / SARSA
3. DQN 及改进算法
4. Policy Gradient / Actor-Critic
5. 实战项目（CartPole 平衡、Atari 游戏、迷宫探索）

## 代码

讲解对应的示例代码见 `1_rl_overview.py`。
