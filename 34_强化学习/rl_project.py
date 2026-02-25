"""
RL 实战：游戏 AI 项目
==================

使用强化学习实现游戏 AI。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("""
项目: 游戏 AI

任务:
  • 控制智能体在环境中生存
  • 获得尽可能高的分数

环境:
  • CartPole: 倒立摆
  • LunarLander: 月球着陆
  • Atari: 游戏

目标:
  • 学会保持平衡
  • 获得高分
""")

print()
print("=" * 60)
print("2. CartPole 问题")
print("=" * 60)

print("""
CartPole 环境:

状态:
  • 小车位置
  • 小车速度
  • 杆角度
  • 杆角速度

动作:
  • 0: 向左推
  • 1: 向右推

奖励:
  • 每步 +1
  • 结束时 (角度过大/位置超出) 0

目标:
  • 坚持尽可能长时间
""")

print()
print("=" * 60)
print("3. DQN 解决方案")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym
from collections import deque
import random

# 经验回放
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards),
            np.array(next_states),
            np.array(dones)
        )

    def __len__(self):
        return len(self.buffer)

# Q 网络
class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.network(x)

# 训练函数
def train_dqn(env, n_episodes=500):
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    q_net = DQN(state_dim, action_dim)
    target_net = DQN(state_dim, action_dim)
    target_net.load_state_dict(q_net.state_dict())

    optimizer = optim.Adam(q_net.parameters(), lr=0.001)
    buffer = ReplayBuffer()

    gamma = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995
    epsilon_min = 0.01
    batch_size = 64
    target_update = 10

    rewards_history = []

    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0

        while True:
            # ε-greedy
            if random.random() < epsilon:
                action = random.randint(0, action_dim - 1)
            else:
                with torch.no_grad():
                    action = q_net(torch.FloatTensor(state)).argmax().item()

            next_state, reward, done, _ = env.step(action)

            buffer.push(state, action, reward, next_state, done)

            if len(buffer) >= batch_size:
                # 训练
                states, actions, rewards, next_states, dones = buffer.sample(batch_size)

                states = torch.FloatTensor(states)
                actions = torch.LongTensor(actions)
                rewards = torch.FloatTensor(rewards)
                next_states = torch.FloatTensor(next_states)
                dones = torch.FloatTensor(dones)

                with torch.no_grad():
                    target = rewards + (1 - dones) * gamma * target_net(next_states).max(1)[0]

                current = q_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)

                loss = nn.MSELoss()(current, target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            total_reward += reward
            state = next_state

            if done:
                break

        if episode % target_update == 0:
            target_net.load_state_dict(q_net.state_dict())

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        rewards_history.append(total_reward)

        if episode % 50 == 0:
            print(f"Episode {episode}: Reward = {total_reward}, Epsilon = {epsilon:.3f}")

    return q_net, rewards_history

# 运行
env = gym.make("CartPole-v1")
model, rewards = train_dqn(env)
''')

print()
print("=" * 60)
print("4. PPO 解决方案")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym
from torch.distributions import Categorical

class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=0.0003):
        self.gamma = 0.99
        self.eps_clip = 0.2
        self.k_epochs = 4

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
        probs = self.actor(torch.FloatTensor(state))
        dist = Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

    def update(self, states, actions, old_log_probs, returns, advantages):
        for _ in range(self.k_epochs):
            probs = self.actor(states)
            dist = Categorical(probs)
            new_log_probs = dist.log_prob(actions)

            ratio = torch.exp(new_log_probs - old_log_probs)
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1-self.eps_clip, 1+self.eps_clip) * advantages

            actor_loss = -torch.min(surr1, surr2).mean()
            values = self.critic(states)
            critic_loss = nn.MSELoss()(values, returns)

            self.actor_opt.zero_grad()
            actor_loss.backward()
            self.actor_opt.step()

            self.critic_opt.zero_grad()
            critic_loss.backward()
            self.critic_opt.step()

def compute_gae(rewards, values, next_values, dones, gamma=0.99, lam=0.95):
    advantages = []
    gae = 0

    for t in reversed(range(len(rewards))):
        if t == len(rewards) - 1:
            next_value = 0
        else:
            next_value = next_values[t + 1]

        delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
        gae = delta + gamma * lam * (1 - dones[t]) * gae
        advantages.insert(0, gae)

    return torch.FloatTensor(advantages)

# 训练
env = gym.make("CartPole-v1")
agent = PPOAgent(4, 2)

for episode in range(500):
    states, actions, rewards, log_probs = [], [], [], []
    state = env.reset()

    while True:
        action, log_prob = agent.get_action(state)
        next_state, reward, done, _ = env.step(action)

        states.append(torch.FloatTensor(state))
        actions.append(torch.tensor(action))
        rewards.append(reward)
        log_probs.append(log_prob)

        if done:
            break
        state = next_state

    # 更新
    states = torch.stack(states)
    actions = torch.stack(actions)
    log_probs = torch.stack(log_probs)

    values = agent.critic(states).squeeze()
    next_values = torch.cat([values[1:], torch.tensor([0.0])])
    returns = compute_gae(rewards, values.detach(), next_values.detach(), [0] * len(rewards))
    advantages = returns - values.detach()

    agent.update(states, actions, log_probs.detach(), returns, advantages)

    if episode % 50 == 0:
        print(f"Episode {episode}: Reward = {sum(rewards)}")
''')

print()
print("=" * 60)
print("5. LunarLander 问题")
print("=" * 60)

print("""
LunarLander 环境:

状态 (8维):
  • x, y 位置
  • x, y 速度
  • 角度
  • 角速度
  • 左腿触地
  • 右腿触地

动作 (4维):
  • 0: 不操作
  • 1: 左引擎
  • 2: 主引擎
  • 3: 右引擎

奖励:
  • 靠近着陆点: +
  • 保持直立: +
  • 使用燃料: -
  • 坠毁: -
""")

print()
print("=" * 60)
print("6. 完整训练流程")
print("=" * 60)

print('''
import gym
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.evaluation import evaluate_policy

# 方法1: PPO
print("训练 PPO...")
model = PPO("MlpPolicy", "CartPole-v1", verbose=0)
model.learn(total_timesteps=50000)

# 评估
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"PPO: Mean Reward = {mean_reward:.2f} +/- {std_reward:.2f}")

# 方法2: DQN
print("训练 DQN...")
model = DQN("MlpPolicy", "CartPole-v1", verbose=0)
model.learn(total_timesteps=50000)

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"DQN: Mean Reward = {mean_reward:.2f} +/- {std_reward}")

# 保存模型
model.save("rl_model")

# 加载模型
model = PPO.load("rl_model")

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
print("7. 自定义环境")
print("=" * 60)

print('''
import gym
from gym import spaces
import numpy as np

class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(4,), dtype=np.float32
        )
        self.state = None

    def reset(self):
        self.state = np.random.randn(4).astype(np.float32)
        return self.state

    def step(self, action):
        self.state = self.state + np.random.randn(4).astype(np.float32) * 0.1

        reward = 1.0 if action == np.argmax(self.state) else 0.0

        done = np.random.random() < 0.1

        return self.state, reward, done, {}

    def render(self, mode="human"):
        pass

    def close(self):
        pass

# 注册环境
gym.register("CustomEnv-v0", CustomEnv)

# 使用
env = gym.make("CustomEnv-v0")
''')

print()
print("=" * 60)
print("8. 训练技巧")
print("=" * 60)

print("""
8.1 奖励塑形

  • 设计合适的奖励函数
  • 及时反馈
  • 避免稀疏奖励

8.2 课程学习

  • 从简单到复杂
  • 逐步增加难度

8.3 多环境并行

  • A2C / PPO
  • 加速训练

8.4 超参数调优

  • 学习率
  • 折扣因子
  • 探索率
""")

print()
print("=" * 60)
print("9. 评估与可视化")
print("=" * 60)

print('''
from stable_baselines3.common.evaluation import evaluate_policy
import matplotlib.pyplot as plt

# 评估
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
print(f"Mean Reward: {mean_reward:.2f} +/- {std_reward:.2f}")

# 绘制训练曲线
def plot_training(rewards, window=50):
    plt.figure(figsize=(10, 5))
    plt.plot(rewards, alpha=0.3)

    # 移动平均
    if len(rewards) >= window:
        avg = np.convolve(rewards, np.ones(window)/window, mode="valid")
        plt.plot(avg, label=f"{window}-episode moving average")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Training Progress")
    plt.legend()
    plt.savefig("training.png")
    plt.show()

plot_training(rewards_history)
''')

print()
print("=" * 60)
print("10. 模型部署")
print("=" * 60)

print('''
# 保存模型
model.save("my_model")

# 导出 ONNX
import torch
dummy_input = torch.randn(1, 4)
torch.onnx.export(model.policy, dummy_input, "model.onnx")

# 使用导出模型
import onnxruntime as ort
ort_session = ort.InferenceSession("model.onnx")

# Flask API
from flask import Flask, request, jsonify
import gym

app = Flask(__name__)
model = PPO.load("my_model")
env = gym.make("CartPole-v1")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    obs = np.array(data["observation"])
    action, _ = model.predict(obs)
    return jsonify({"action": int(action)})

if __name__ == "__main__":
    app.run(port=5000)
''')

print()
print("=" * 60)
print("11. 项目总结")
print("=" * 60)

print("""
强化学习项目要点:

✓ 1. 环境选择 - 合适的 Gym 环境
✓ 2. 算法选择 - DQN / PPO / SAC
✓ 3. 训练优化 - 奖励设计、超参数
✓ 4. 评估 - 多次评估取平均
✓ 5. 部署 - ONNX、API

下一步可以尝试:
  • Atari 游戏
  • 机器人控制
  • 多智能体协作

推荐资源:
  • OpenAI Gym 文档
  • Stable-Baselines3
  • RL 论文
""")
