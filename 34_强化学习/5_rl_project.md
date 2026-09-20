# 5. RL实战：游戏 AI

## 项目概述

项目目标：训练智能体在游戏环境中生存并获得尽可能高的分数。

| 环境 | 特点 |
|------|------|
| CartPole | 倒立摆，状态 4 维、动作 2 个，入门首选 |
| LunarLander | 月球着陆，状态 8 维、动作 4 个 |
| Atari | 图像输入，需 CNN |

## CartPole 环境

| 项目 | 内容 |
|------|------|
| 状态 | 小车位置、小车速度、杆角度、杆角速度 |
| 动作 | 0: 向左推, 1: 向右推 |
| 奖励 | 每步 +1；杆倒下/小车出界则结束 |
| 目标 | 坚持尽可能长时间（最高 500 步） |

## DQN 解决方案

完整流程 = 经验回放 + 目标网络 + ε-greedy：

```python
def train_dqn(env, n_episodes=500):
    q_net, target_net = DQN(state_dim, action_dim), DQN(state_dim, action_dim)
    target_net.load_state_dict(q_net.state_dict())
    optimizer = optim.Adam(q_net.parameters(), lr=0.001)

    for episode in range(n_episodes):
        state = env.reset()
        while True:
            # 1. ε-greedy 选动作
            if random.random() < epsilon:
                action = random.randint(0, action_dim - 1)
            else:
                with torch.no_grad():
                    action = q_net(torch.FloatTensor(state)).argmax().item()

            next_state, reward, done, _ = env.step(action)

            # 2. 存储经验
            buffer.push(state, action, reward, next_state, done)

            # 3. 采样 + 计算 TD 目标 + 更新
            if len(buffer) >= batch_size:
                ...

            state = next_state
            if done:
                break

        # 4. 定期同步目标网络、衰减 ε
        if episode % target_update == 0:
            target_net.load_state_dict(q_net.state_dict())
        epsilon = max(epsilon_min, epsilon * epsilon_decay)
```

## PPO 解决方案

Actor-Critic 结构 + clip 损失 + **GAE 优势估计**：

- 用 `compute_gae(rewards, values, next_values, dones, gamma, lam)` 计算广义优势：δ_t = r_t + γ·V(s_{t+1}) − V(s_t)，gae = δ_t + γλ·gae
- 一个 episode 的数据收集完后，用 `agent.update(...)` 重复更新 k_epochs 次（PPO2 风格）

## 使用 Stable-Baselines3 的完整流程

实际项目推荐直接用 SB3，训练 + 评估 + 保存一条龙：

```python
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.evaluation import evaluate_policy

# 训练
model = PPO("MlpPolicy", "CartPole-v1", verbose=0)
model.learn(total_timesteps=50000)

# 评估（多次评估取平均）
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)

# 保存 / 加载
model.save("rl_model")
model = PPO.load("rl_model")
```

## 自定义环境

继承 `gym.Env` 并实现 `reset` / `step` / `render`，注册后即可像内置环境一样使用：

```python
class CustomEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(4,), dtype=np.float32)

    def reset(self):
        self.state = np.random.randn(4).astype(np.float32)
        return self.state

    def step(self, action):
        ...
        return self.state, reward, done, {}

gym.register("CustomEnv-v0", CustomEnv)
env = gym.make("CustomEnv-v0")
```

## 训练技巧

| 技巧 | 说明 |
|------|------|
| 奖励塑形 | 设计及时反馈的奖励函数，避免稀疏奖励 |
| 课程学习 | 从简单到复杂，逐步增加难度 |
| 多环境并行 | A2C/PPO 支持并行采样，加速训练 |
| 超参数调优 | 学习率、折扣因子、探索率 |

## 评估与可视化

```python
# 绘制训练曲线 + 移动平均
def plot_training(rewards, window=50):
    plt.plot(rewards, alpha=0.3)
    avg = np.convolve(rewards, np.ones(window)/window, mode="valid")
    plt.plot(avg, label=f"{window}-episode moving average")
    plt.xlabel("Episode"); plt.ylabel("Reward")
    plt.savefig("training.png")
```

## 模型部署

```python
model.save("my_model")                    # 保存
torch.onnx.export(model.policy, dummy_input, "model.onnx")  # 导出 ONNX
# 也可封装为 Flask API：接收 observation，返回 action
```

## 项目总结

1. **环境选择**：合适的 Gym 环境
2. **算法选择**：DQN / PPO / SAC
3. **训练优化**：奖励设计、超参数
4. **评估**：多次评估取平均
5. **部署**：ONNX、API

下一步可以尝试：Atari 游戏、机器人控制、多智能体协作。

## 代码

讲解对应的示例代码见 `5_rl_project.py`。
