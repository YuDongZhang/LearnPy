"""
神经网络基础与原理
================

从零实现一个神经网络 (仅用 numpy), 并真实训练观察损失下降。
概念讲解见 2_neural_network.md, 本文件专注于"能跑起来"。
"""

import numpy as np

print("=" * 60)
print("1. 单个神经元: 手算一次前向传播")
print("=" * 60)

x = np.array([1.0, 2.0, 3.0])
w = np.array([0.5, -0.3, 0.8])
b = 0.1

z = np.dot(w, x) + b
print(f"输入 x = {x.tolist()}")
print(f"权重 w = {w.tolist()}, 偏置 b = {b}")
print(f"线性输出 z = w·x + b = {z:.2f}")
print(f"过 ReLU    = {max(0.0, z):.2f}")
print(f"过 Sigmoid = {1 / (1 + np.exp(-z)):.4f}")

print()
print("=" * 60)
print("2. 激活函数对比")
print("=" * 60)

xs = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
print(f"输入:    {xs.tolist()}")
print(f"Sigmoid: {np.round(1 / (1 + np.exp(-xs)), 4).tolist()}")
print(f"Tanh:    {np.round(np.tanh(xs), 4).tolist()}")
print(f"ReLU:    {np.maximum(0, xs).tolist()}")
softmax = np.exp(xs) / np.exp(xs).sum()
print(f"Softmax: {np.round(softmax, 4).tolist()}  (相加 = {softmax.sum():.1f})")

print()
print("=" * 60)
print("3. 损失函数")
print("=" * 60)

y_pred = np.array([0.7, 0.2, 0.1])
y_true = np.array([1, 0, 0])
print(f"预测: {y_pred.tolist()}, 真实: {y_true.tolist()}")
print(f"MSE      = {np.mean((y_pred - y_true) ** 2):.4f}")
print(f"交叉熵   = {-np.mean(y_true * np.log(y_pred + 1e-12)):.4f}")

print()
print("=" * 60)
print("4. 从零实现神经网络 (真实训练)")
print("=" * 60)

np.random.seed(42)

# 构造二分类数据: 两类点分别围绕 (2,2) 和 (-2,-2) 分布
n = 200
X = np.vstack([np.random.randn(n // 2, 2) + 2, np.random.randn(n // 2, 2) - 2])
y = np.hstack([np.ones(n // 2), np.zeros(n // 2)]).reshape(-1, 1)
print(f"数据形状: X={X.shape}, y={y.shape} (二分类)")


class NeuralNetwork:
    """2 层 MLP: 输入 -> 隐藏层(ReLU) -> 输出(Sigmoid)"""

    def __init__(self, n_in, n_hidden):
        # He 初始化: 防止深层网络梯度消失
        self.W1 = np.random.randn(n_in, n_hidden) * np.sqrt(2.0 / n_in)
        self.b1 = np.zeros((1, n_hidden))
        self.W2 = np.random.randn(n_hidden, 1) * np.sqrt(2.0 / n_hidden)
        self.b2 = np.zeros((1, 1))

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = np.maximum(0, self.z1)              # ReLU
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = 1 / (1 + np.exp(-self.z2))          # Sigmoid
        return self.a2

    def backward(self, X, y, lr):
        """链式法则逐层求梯度, 再按负梯度更新参数"""
        m = X.shape[0]
        dz2 = (self.a2 - y) / m                       # 输出层梯度
        dW2 = self.a1.T @ dz2
        db2 = dz2.sum(axis=0, keepdims=True)
        dz1 = (dz2 @ self.W2.T) * (self.z1 > 0)       # ReLU 导数: 正数处为 1
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0, keepdims=True)

        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2

    def loss(self, y):
        eps = 1e-12
        return -np.mean(y * np.log(self.a2 + eps) + (1 - y) * np.log(1 - self.a2 + eps))


nn = NeuralNetwork(2, 8)
print("\n训练过程 (交叉熵损失):")
for epoch in range(1, 1001):
    nn.forward(X)
    loss = nn.loss(y)
    acc = ((nn.a2 > 0.5).astype(float) == y).mean()
    nn.backward(X, y, lr=0.5)
    if epoch in (1, 100, 500, 1000):
        print(f"  epoch {epoch:4d}: loss = {loss:.4f}, 准确率 = {acc:.2%}")

print()
print("=" * 60)
print("5. 小结")
print("=" * 60)

print("""
关键结论:
  - 反向传播 = 链式法则逐层求梯度 (dz2 -> dW2 -> dz1 -> dW1)
  - 优化器只做一件事: 参数 -= 学习率 * 梯度
  - 损失持续下降、准确率上升, 说明网络真的学到了决策边界

激活函数/损失函数/优化器/正则化的完整讲解见 2_neural_network.md
""")