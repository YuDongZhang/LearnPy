# 2. NumPy数值计算基础

## NumPy简介

NumPy (Numerical Python) 是 Python AI 开发的基础库：

- 提供高性能的多维数组对象 ndarray
- 提供大量的数学函数
- 是 Pandas、TensorFlow 等库的基础

## 创建数组

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])      # 一维数组
arr2 = np.array([[1, 2, 3], [4, 5, 6]]) # 二维数组
arr3 = np.zeros((3, 4))               # 全零数组
arr4 = np.ones((2, 3))                # 全一数组
arr5 = np.arange(0, 10, 2)            # 类似 range: [0, 2, 4, 6, 8]
arr6 = np.linspace(0, 1, 5)           # 均匀分割: [0, 0.25, 0.5, 0.75, 1]
```

## 数组基本操作

向量化运算，无需写循环：

```python
arr = np.array([1, 2, 3, 4, 5])
arr + 1     # [2, 3, 4, 5, 6]
arr * 2     # [2, 4, 6, 8, 10]
arr ** 2    # [1, 4, 9, 16, 25]

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a + b       # [5, 7, 9]  逐元素相加
a * b       # [4, 10, 18] 逐元素相乘
```

## 索引和切片

```python
arr = np.array([10, 20, 30, 40, 50])
arr[0]      # 10
arr[-1]     # 50
arr[1:4]    # [20, 30, 40]
arr[::2]    # [10, 30, 50] 步长为2

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr2d[0]     # [1, 2, 3]      第一行
arr2d[0, 1]  # 2              第0行第1列
arr2d[:, 1]  # [2, 5, 8]      第1列
```

## 形状操作

```python
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])  # 形状 (2, 4)
arr.reshape(4, 2)   # 重塑为 (4, 2)
arr.flatten()       # 展平为一维
arr.T               # 转置，形状变为 (4, 2)
```

## 常用统计函数

```python
arr = np.array([1, 2, 3, 4, 5])
arr.sum(), arr.mean(), arr.std(), arr.min(), arr.max()
arr.argmin(), arr.argmax()  # 最小/最大值的索引

arr2d = np.array([[1, 2, 3], [4, 5, 6]])
arr2d.sum(axis=0)  # [5, 7, 9]  按列求和
arr2d.sum(axis=1)  # [6, 15]    按行求和
```

## 广播机制

Broadcasting 允许不同形状的数组进行运算，规则是从右向左比较维度：

- 维度相同，或
- 其中一个维度为 1

```python
a = np.array([[1], [2], [3]])   # 形状 (3, 1)
b = np.array([10, 20, 30])      # 形状 (3,)
a + b    # 广播为 (3, 3)
```

## 随机数生成

| 函数 | 说明 |
|------|------|
| `np.random.rand(5)` | 0-1 均匀分布 |
| `np.random.randn(5)` | 正态分布 |
| `np.random.randint(1, 10, 5)` | 随机整数 |
| `np.random.choice(...)` | 随机选择 |
| `np.random.seed(42)` | 固定随机种子，保证可复现 |

## 逻辑运算与掩码

```python
arr = np.array([1, 2, 3, 4, 5])
arr > 3    # [False, False, False, True, True]

mask = arr > 3
arr[mask]   # [4, 5]  布尔索引筛选

np.where(arr > 3, '大', '小')  # 条件选择
```

## 矩阵运算

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A + B      # 矩阵加法
A * B      # 逐元素乘法（注意！）
A @ B      # 矩阵乘法
A.dot(B)   # 矩阵乘法（等价）

np.linalg.inv(A)   # 矩阵的逆
np.linalg.det(A)   # 行列式
```

`A * B` 和 `A @ B` 的区别是 NumPy 最常见的坑之一。

## 代码

讲解对应的示例代码见 `2_numpy_basics.py`。
