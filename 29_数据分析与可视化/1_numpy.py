"""
1. NumPy数组与运算 - 代码示例
"""

import numpy as np

# ========== 1. 创建数组 ==========
print("创建数组:")
a = np.array([1, 2, 3, 4, 5])
print(f"  从列表: {a}")
print(f"  全0: {np.zeros((2, 3))}")
print(f"  全1: {np.ones((2, 3))}")
print(f"  等差: {np.arange(0, 10, 2)}")
print(f"  等分: {np.linspace(0, 1, 5)}")
print(f"  随机: {np.random.randn(3)}")

# ========== 2. 数组属性 ==========
b = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n数组属性:")
print(f"  shape: {b.shape}, dtype: {b.dtype}, ndim: {b.ndim}, size: {b.size}")

# ========== 3. 向量化运算 ==========
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print(f"\n向量化运算:")
print(f"  x + y = {x + y}")
print(f"  x * y = {x * y}")
print(f"  x ** 2 = {x ** 2}")
print(f"  np.sqrt(x) = {np.sqrt(x)}")

# ========== 4. 广播 ==========
matrix = np.array([[1, 2, 3], [4, 5, 6]])
vector = np.array([10, 20, 30])
print(f"\n广播: (2,3) + (3,) = \n{matrix + vector}")

# ========== 5. 索引与切片 ==========
a = np.arange(12).reshape(3, 4)
print(f"\n索引切片:")
print(f"  原数组:\n{a}")
print(f"  第1行: {a[0]}")
print(f"  第2列: {a[:, 1]}")
print(f"  条件筛选(>5): {a[a > 5]}")

# ========== 6. 聚合运算 ==========
data = np.random.randn(100)
print(f"\n聚合运算:")
print(f"  均值: {data.mean():.4f}")
print(f"  标准差: {data.std():.4f}")
print(f"  最大: {data.max():.4f}, 最小: {data.min():.4f}")
print(f"  求和: {data.sum():.4f}")
