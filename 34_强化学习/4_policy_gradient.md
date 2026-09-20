# 4. Policy Gradient 策略梯度

## 为什么需要策略梯度

值函数方法（DQN）的局限：

- 只适用于离散动作，无法处理连续动作（如机器人关节角度）
- 通过值函数间接得到策略，有时不如直接学策略高效
- 策略梯度可以学习**随机策略 (stochastic policy)**

核心思想：直接学习策略 π(a|s)，以期望累计奖励为目标，用**梯度上升**更新策略参数。

## 策略梯度定理

目标是最大化期望奖励 J(θ) = E_πθ[R]，其梯度：

```
∇θ J(θ) = E_πθ [∇θ log πθ(a|s) · Q^π(s, a)]
       ≈ E[∇θ log πθ(a|s) · G_t]
```

- πθ(a|s)：策略网络输出的动作概率
- G_t：累计奖励
- ∇θ log πθ(a|s)：得分函数 (Score function)

直觉：**增加带来好结果的动作概率，减少带来坏结果的动作概率**。

## REINFORCE 算法

REINFORCE (1992) 是最简单的策略梯度算法：

1. 用当前策略采样一条完整轨迹
2. 计算每个状态的回报 G_t
3. 按更新公式做梯度上升：θ ← θ + α · ∇θ log πθ(a_t|s_t) · G_t

优点：简单直观、可处理连续动作；缺点：**方差大、收敛慢**。

PyTorch 实现（CartPole）：

```python
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, action_dim), nn.Softmax(dim=-1)
        )

# 采样动作并记录 log_prob
def select_action(state, policy_net):
    state = torch.FloatTensor(state).unsqueeze(0)
    probs = policy_net(state)
    dist = torch.distributions.Categorical(probs)
    action = dist.sample()
    return action.item(), dist.log_prob(action)

# 反向计算回报: G_t = r_t + γ·G_{t+1}
def compute_returns(rewards, gamma=0.99):
    returns, G = [], 0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    return torch.FloatTensor(returns)
```

训练时用回报标准化 `(returns - mean) / std` 减小方差，损失为 `-log_prob × G` 的和。

## Actor-Critic

Actor-Critic (1999) 结合值函数与策略梯度，用两个网络：

| 角色 | 网络 | 职责 |
|------|------|------|
| Actor | 策略网络 | 选择动作 |
| Critic | 值网络 | 评估动作好坏 |

用**优势函数** A(s, a) = Q(s, a) − V(s) 代替 G_t：

- Actor 更新：∇θ log πθ(a|s) · A(s, a)
- Critic 更新：最小化 (R + γV(s') − V(s))²（TD 误差）

优势函数能显著**减少方差、加快收敛**。

## A2C / A3C

- **A2C (Advantage Actor-Critic)**：使用优势函数 + 并行环境采样
- **A3C (Asynchronous A3C)**：多个 worker 异步并行收集数据、更新参数

## PPO 算法

PPO (Proximal Policy Optimization, 2017) 是目前最常用的 RL 算法：

- 核心思想：**限制每次策略更新的幅度**（信任域思想），防止策略突变
- 目标函数：

```
L^CLIP(θ) = E[min(r(θ)·A, clip(r(θ), 1-ε, 1+ε)·A)]
其中 r(θ) = πθ(a|s) / πθ_old(a|s)
```

- 特点：稳定、高效、易于实现，OpenAI 默认算法
- 实现要点：先收集一批数据，再用 clip 损失重复更新 k 个 epoch

## SAC 算法

SAC (Soft Actor-Critic, 2018) 面向**连续动作**：

- 最大熵强化学习：J(π) = E[Q(s,a) + α·H(π(·|s))]，熵项鼓励探索
- 适合机器人控制等连续控制任务

## 连续动作的处理方式

1. **高斯策略**：π(a|s) = N(μ(s), σ(s)²)，网络输出均值和标准差，从分布采样
2. **方差缩减**：基线 (baseline)、优势函数
3. **确定性策略**：直接输出动作值（DPG、DDPG）

## 算法选择建议

| 场景 | 推荐算法 |
|------|---------|
| 离散动作 | PPO |
| 连续动作 | SAC, PPO |
| 入门学习 | REINFORCE |

优缺点：✓ 支持连续动作和随机策略；✗ 方差大、收敛慢（需靠 Actor-Critic / PPO 等改进）。

## 代码

讲解对应的示例代码见 `4_policy_gradient.py`。
