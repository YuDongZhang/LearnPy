"""
Q-Learning 算法
============

介绍 Q-Learning 算法的原理和实现。
"""

print("=" * 60)
print("1. Q-Learning 简介")
print("=" * 60)

print("""
Q-Learning (1989):

核心思想:
  • 学习状态-动作对的价值 (Q值)
  • 通过迭代更新 Q 值
  • 最终得到最优 Q 表

Q(s, a): 在状态 s 下采取动作 a 的期望累计奖励

算法特点:
  • Off-policy: 可以从过去的经验中学习
  • TD 学习: 时序差分
  • 值迭代: 逐步逼近最优值
""")

print()
print("=" * 60)
print("2. Q-Learning 算法")
print("=" * 60)

print("""
Q-Learning 更新公式:

  Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]

  α: 学习率
  γ: 折扣因子
  r: 奖励
  s': 下一个状态
  max_{a'} Q(s', a'): 下一个状态的最大 Q 值

ε-greedy 策略:

  if random.random() < ε:
      action = random action  # 探索
  else:
      action = argmax Q(s, :)  # 利用
""")

print()
print("=" * 60)
print("3. 简单 Q-Learning 实现")
print("=" * 60)

print('''
import numpy as np
import gym

# 3.1 创建 Q 表
def create_q_table(n_states, n_actions):
    return np.zeros((n_states, n_actions))

# 3.2 选择动作 (ε-greedy)
def choose_action(state, q_table, epsilon=0.1):
    if np.random.random() < epsilon:
        return np.random.randint(q_table.shape[1])
    else:
        return np.argmax(q_table[state])

# 3.3 更新 Q 表
def update_q_table(q_table, state, action, reward, next_state, alpha=0.1, gamma=0.95):
    old_value = q_table[state, action]
    next_max = np.max(q_table[next_state])
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    q_table[state, action] = new_value
    return q_table

# 3.4 完整训练
def train_q_learning(env, n_episodes=500, epsilon=0.1, alpha=0.1, gamma=0.95):
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q_table = create_q_table(n_states, n_actions)

    rewards = []

    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0

        while True:
            # 选择动作
            action = choose_action(state, q_table, epsilon)

            # 执行动作
            next_state, reward, done, _ = env.step(action)

            # 更新 Q 表
            q_table = update_q_table(q_table, state, action, reward, next_state, alpha, gamma)

            total_reward += reward
            state = next_state

            if done:
                break

        rewards.append(total_reward)

        # 衰减 epsilon
        epsilon = max(0.01, epsilon * 0.995)

    return q_table, rewards

# 使用
env = gym.make("FrozenLake-v1")
q_table, rewards = train_q_learning(env)
''')

print()
print("=" * 60)
print("4. SARSA 算法")
print("=" * 60)

print("""
SARSA (State-Action-Reward-State-Action):

与 Q-Learning 的区别:
  • On-policy: 必须按照当前策略执行
  • SARSA: 使用实际执行的下一个动作的 Q 值
  • Q-Learning: 使用最大 Q 值

SARSA 更新:

  Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]

其中 a' 是实际采取的动作

特点:
  • 更保守, 考虑探索的影响
  • 适合在线学习
""")

print()
print("=" * 60)
print("5. 迷宫环境示例")
print("=" * 60)

print('''
import numpy as np

# 5.1 定义迷宫环境
class MazeEnv:
    def __init__(self):
        self.maze = np.array([
            [0, 0, 0, 0],
            [0, -1, 0, -1],
            [0, 0, 0, 1],  # 1 是目标
        ])
        self.n_rows, self.n_cols = self.maze.shape
        self.start = (0, 0)
        self.goal = (2, 3)
        self.state = self.start

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        # 动作: 0=上, 1=下, 2=左, 3=右
        row, col = self.state

        if action == 0 and row > 0:
            row -= 1
        elif action == 1 and row < self.n_rows - 1:
            row += 1
        elif action == 2 and col > 0:
            col -= 1
        elif action == 3 and col < self.n_cols - 1:
            col += 1

        self.state = (row, col)

        if self.state == self.goal:
            return self.state, 1, True
        elif self.maze[row, col] == -1:
            return self.state, -1, True
        else:
            return self.state, -0.1, False

    def render(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if (i, j) == self.state:
                    print("A", end=" ")
                elif (i, j) == self.goal:
                    print("G", end=" ")
                elif self.maze[i, j] == -1:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()

# 5.2 在迷宫上训练
env = MazeEnv()
q_table = create_q_table(9, 4)  # 9个状态, 4个动作

# 训练
for episode in range(1000):
    state = env.reset()
    state_idx = state[0] * 3 + state[1]

    while True:
        action = choose_action(state_idx, q_table, epsilon=0.1)
        next_state, reward, done = env.step(action)
        next_state_idx = next_state[0] * 3 + next_state[1]

        q_table = update_q_table(q_table, state_idx, action, reward, next_state_idx)

        state_idx = next_state_idx
        if done:
            break
''')

print()
print("=" * 60)
print("6. 表格型 Q-Learning 完整实现")
print("=" * 60)

print('''
import numpy as np
import gym

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = learning_rate
        self.gamma = discount_factor

        self.q_table = np.zeros((state_size, action_size))
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_size)
        else:
            return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state, action] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def train(self, env, n_episodes):
        scores = []

        for episode in range(n_episodes):
            state = env.reset()
            score = 0

            while True:
                action = self.choose_action(state)
                next_state, reward, done, _ = env.step(action)

                self.learn(state, action, reward, next_state)

                score += reward
                state = next_state

                if done:
                    break

            scores.append(score)
            self.decay_epsilon()

            if episode % 50 == 0:
                avg_score = np.mean(scores[-50:])
                print(f"Episode {episode}: Avg Score = {avg_score:.2f}, Epsilon = {self.epsilon:.3f}")

        return scores

# 使用
env = gym.make("Taxi-v3")
agent = QLearningAgent(state_size=500, action_size=6)
scores = agent.train(env, n_episodes=1000)
''')

print()
print("=" * 60)
print("7. Q-Learning 技巧")
print("=" * 60)

print("""
7.1 学习率衰减

  α = α_0 / (1 + decay * episode)

7.2 折扣因子

  γ 接近 1: 考虑长远奖励
  γ 接近 0: 重视即时奖励
  通常: 0.9 - 0.99

7.3 探索衰减

  ε 衰减策略:
  • 线性衰减
  • 指数衰减
  • 定期重置

7.4 奖励设计

  • 正奖励: 达成目标
  • 负奖励: 失败/惩罚
  • 小负奖励: 鼓励快速完成任务
""")

print()
print("=" * 60)
print("8. 动态规划方法")
print("=" * 60)

print("""
8.1 策略迭代

  1. 策略评估: 计算 V^π(s)
  2. 策略改进: π' = greedy(V^π)
  3. 重复直到收敛

8.2 值迭代

  V(s) = max_a [ R(s,a) + γ Σ P(s'|s,a) V(s') ]

  不需要显式策略

8.3 区别

  Q-Learning:
    • 无模型 (Model-free)
    • 在线学习
    • 试错

  动态规划:
    • 需要模型 (Model-based)
    • 需要知道转移概率
""")

print()
print("=" * 60)
print("9. 悬崖行走问题")
print("=" * 60)

print("""
Cliff Walking 问题:

环境:
  • 4x12 网格
  • 起点: 左下
  • 目标: 右下
  • 悬崖: 底部中间 (掉入扣 100 分)

策略对比:

  • Q-Learning: 最优但危险 (靠近悬崖)
  • SARSA: 次优但安全 (远离悬崖)

  Q-Learning 探索时可能掉入悬崖
  SARSA 会考虑探索的影响
""")

print()
print("=" * 60)
print("10. 进阶技巧")
print("=" * 60)

print("""
10.1 Double Q-Learning

  解决 Q 值过高估计问题
  使用两个 Q 表交替更新

10.2 Dueling DQN

  Q(s,a) = V(s) + A(s,a)
  分别估计状态值和优势函数

10.3 优先经验回放

  TD 误差大的经验优先回放

10.4 Noisy Networks

  用噪声代替 ε-greedy 探索
""")

print()
print("=" * 60)
print("11. Q-Learning 总结")
print("=" * 60)

print("""
Q-Learning 要点:

✓ 核心:
  • Q 表: 状态-动作价值
  • 更新: 贝尔曼方程
  • 探索: ε-greedy

✓ 优缺点:
  ✓ 简单易实现
  ✓ 收敛性好
  ✗ 只能处理离散状态
  ✗ 状态空间大时难以扩展

✓ 改进方向:
  • 函数近似 (DQN)
  • 经验回放
  • 目标网络

✓ 适用场景:
  • 离散状态/动作
  • 状态空间较小
  • 需要快速原型
""")
