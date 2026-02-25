"""
强化学习概述
==========

介绍强化学习的基本概念、发展历程和应用领域。
"""

print("=" * 60)
print("1. 强化学习简介")
print("=" * 60)

print("""
强化学习 (Reinforcement Learning, RL):

核心思想:
  • 智能体 (Agent) 与环境 (Environment) 交互
  • 通过试错学习最优策略
  • 最大化累计奖励

与监督学习的区别:
  • 监督学习: 需要标注数据
  • 强化学习: 通过与环境交互获取反馈

基本要素:
  1. 智能体 (Agent): 学习者
  2. 环境 (Environment): 智能体所处的世界
  3. 状态 (State): 环境的描述
  4. 动作 (Action): 智能体可以采取的行动
  5. 奖励 (Reward): 反馈信号
  6. 策略 (Policy): 状态到动作的映射
""")

print()
print("=" * 60)
print("2. 强化学习基本框架")
print("=" * 60)

print("""
强化学习交互流程:

  智能体 ──动作(A)──> 环境
                   │
                   ▼
              状态(S') + 奖励(R)
                   │
                   ▼
              智能体 <──

核心问题:
  • 探索 (Exploration): 尝试新的动作
  • 利用 (Exploitation): 使用已知的最优策略

平衡: ε-greedy 策略
  • 以 ε 概率随机选择动作 (探索)
  • 以 1-ε 概率选择最优动作 (利用)
""")

print()
print("=" * 60)
print("3. 马尔可夫决策过程")
print("=" * 60)

print("""
马尔可夫决策过程 (MDP):

五元组 (S, A, P, R, γ):
  • S: 状态空间
  • A: 动作空间
  • P: 状态转移概率 P(s'|s, a)
  • R: 奖励函数 R(s, a, s')
  • γ: 折扣因子 (0 < γ < 1)

马尔可夫性:
  P(s_{t+1} | s_t, a_t, s_{t-1}, ...) = P(s_{t+1} | s_t, a_t)

状态值函数 V(s):
  V(s) = E[G_t | s_t = s]
  G_t = R_t + γR_{t+1} + γ²R_{t+2} + ...

状态-动作值函数 Q(s, a):
  Q(s, a) = E[G_t | s_t = s, a_t = a]
""")

print()
print("=" * 60)
print("4. 贝尔曼方程")
print("=" * 60)

print("""
贝尔曼方程 (Bellman Equation):

值函数的递归关系:

  V(s) = max_a [ R(s, a) + γ Σ P(s'|s, a) V(s') ]

  Q(s, a) = R(s, a) + γ Σ P(s'|s, a) max_{a'} Q(s', a')

最优值函数:
  V*(s) = max_a Q*(s, a)

  Q*(s, a) = R(s, a) + γ Σ P(s'|s, a) V*(s')

最优策略:
  π*(s) = argmax_a [ R(s, a) + γ Σ P(s'|s, a) V*(s') ]
""")

print()
print("=" * 60)
print("5. 发展历程")
print("=" * 60)

print("""
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
""")

print()
print("=" * 60)
print("6. 主要算法分类")
print("=" * 60)

print("""
6.1 基于值函数 (Value-Based)

  • Q-Learning
  • SARSA
  • DQN (Deep Q-Network)
  • Double DQN
  • Dueling DQN
  • Rainbow DQN

6.2 基于策略 (Policy-Based)

  • Policy Gradient
  • REINFORCE
  • Actor-Critic
  • A2C/A3C
  • PPO (Proximal Policy Optimization)
  • SAC (Soft Actor-Critic)

6.3 模型基 (Model-Based)

  • Dyna-Q
  • AlphaZero
  • MuZero
""")

print()
print("=" * 60)
print("7. 应用领域")
print("=" * 60)

print("""
| 领域 | 应用 |
|------|------|
| 游戏 | Atari, AlphaGo, Dota2 |
| 机器人 | 运动控制, 抓取 |
| 推荐系统 | 个性化推荐 |
| 自动驾驶 | 决策控制 |
| 资源调度 | 数据中心节能 |
| 金融 | 交易策略 |
| NLP | 对话系统, RLHF |

经典案例:
  • AlphaGo: 围棋
  • OpenAI Five: Dota2
  • AlphaStar: 星际争霸
  • Tesla Autopilot: 自动驾驶
""")

print()
print("=" * 60)
print("8. 常用环境")
print("=" * 60)

print("""
8.1 OpenAI Gym

pip install gym

环境类型:
  • CartPole: 倒立摆
  • MountainCar: 爬山车
  • Pendulum: 摆
  • Atari: 雅达利游戏
  • MuJoCo: 物理模拟

8.2 DeepMind Lab

8.3 Unity ML-Agents

8.4 StarCraft II Learning Environment
""")

print()
print("=" * 60)
print("9. 核心概念")
print("=" * 60)

print("""
9.1 探索策略

  • ε-greedy: 随机探索
  • Boltzmann: 概率探索
  • UCB (Upper Confidence Bound)
  • Thompson Sampling

9.2 经验回放 (Experience Replay)

  • 存储 (s, a, r, s', done) 到记忆库
  • 随机采样打破数据相关性
  • DQN 核心技术

9.3 目标网络 (Target Network)

  • 固定目标网络参数
  • 稳定训练
  • 每隔 N 步更新

9.4 优势函数

  A(s, a) = Q(s, a) - V(s)
  表示采取动作 a 相对于平均水平的优势
""")

print()
print("=" * 60)
print("10. 安装库")
print("=" * 60)

print("""
pip install gym
pip install gymnasium  # 新的 Gym 版本
pip install stable-baselines3
pip install torch
pip install ale-py  # Atari 环境

# 可视化
pip install pygame
pip install pyglet
""")

print()
print("=" * 60)
print("11. 第一个 RL 程序")
print("=" * 60)

print('''
import gym

# 创建环境
env = gym.make("CartPole-v1")

# 重置环境
state = env.reset()

# 运行一个 episode
for step in range(1000):
    # 随机选择一个动作
    action = env.action_space.sample()

    # 执行动作
    state, reward, done, info = env.step(action)

    # 渲染环境
    env.render()

    if done:
        break

env.close()

# 查看环境信息
print(f"动作空间: {env.action_space}")
print(f"状态空间: {env.observation_space}")
print(f"状态边界: {env.observation_space.low} - {env.observation_space.high}")
''')

print()
print("=" * 60)
print("12. 学习路径")
print("=" * 60)

print("""
推荐学习路线:

阶段1: 基础
  • 理解 MDP 和贝尔曼方程
  • 实现 Q-Learning
  • 理解探索-利用平衡

阶段2: 深度 RL
  • DQN 原理
  • 经验回放
  • 目标网络
  • 实现 DQN

阶段3: 策略梯度
  • Policy Gradient 原理
  • Actor-Critic
  • PPO 算法

阶段4: 进阶
  • 多智能体 RL
  • 元学习
  • 离线 RL

实战项目:
  • CartPole 平衡
  • Atari 游戏
  • 迷宫探索
  • 简单游戏 AI
""")

print()
print("=" * 60)
print("13. 评估指标")
print("=" * 60)

print("""
13.1 累计奖励 (Total Reward)

  一个 episode 的所有奖励之和

13.2 回合成功率 (Success Rate)

  达到目标的回合比例

13.3 收敛速度

  达到指定性能所需的步数/回合数

13.4 泛化能力

  在未见过的环境中的表现
""")

print()
print("=" * 60)
print("14. 强化学习总结")
print("=" * 60)

print("""
强化学习要点:

✓ 核心要素:
  • 智能体、环境、状态、动作、奖励、策略

✓ 主要算法:
  • 值函数: Q-Learning, DQN
  • 策略梯度: PPO, Actor-Critic

✓ 关键技术:
  • 探索-利用平衡
  • 经验回放
  • 目标网络
  • 优势估计

✓ 应用:
  • 游戏 AI
  • 机器人控制
  • 自动驾驶
  • 推荐系统

✓ 学习建议:
  • 先理解基础概念
  • 实现经典算法
  • 多调试参数
""")
