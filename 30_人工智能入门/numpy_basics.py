"""
NumPy 数值计算基础
==================

NumPy 是 Python AI 开发的基础库，提供高效的数值计算功能。
"""

print("=" * 60)
print("1. NumPy 简介")
print("=" * 60)

print("""
NumPy (Numerical Python)
  - 提供高性能的多维数组对象 ndarray
  - 提供了大量的数学函数
  - 是 Pandas、TensorFlow 等库的基础
""")

print()
print("=" * 60)
print("2. 创建数组")
print("=" * 60)

import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
print(f"一维数组: {arr1}")
print(f"类型: {type(arr1)}, 形状: {arr1.shape}")

arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n二维数组:\n{arr2}")
print(f"形状: {arr2.shape}")

arr3 = np.zeros((3, 4))
print(f"\n全零数组:\n{arr3}")

arr4 = np.ones((2, 3))
print(f"\n全一数组:\n{arr4}")

arr5 = np.arange(0, 10, 2)
print(f"\narange: {arr5}")

arr6 = np.linspace(0, 1, 5)
print(f"linspace: {arr6}")

print()
print("=" * 60)
print("3. 数组基本操作")
print("=" * 60)

arr = np.array([1, 2, 3, 4, 5])

print(f"数组: {arr}")
print(f"加法: arr + 1 = {arr + 1}")
print(f"乘法: arr * 2 = {arr * 2}")
print(f"平方: arr ** 2 = {arr ** 2}")

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print(f"\n数组相加: {arr1} + {arr2} = {arr1 + arr2}")
print(f"数组相乘: {arr1} * {arr2} = {arr1 * arr2}")

print()
print("=" * 60)
print("4. 数组索引和切片")
print("=" * 60)

arr = np.array([10, 20, 30, 40, 50])

print(f"数组: {arr}")
print(f"索引 [0]: {arr[0]}")
print(f"索引 [-1]: {arr[-1]}")
print(f"切片 [1:4]: {arr[1:4]}")
print(f"步长 [::2]: {arr[::2]}")

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"\n二维数组:\n{arr2d}")
print(f"arr2d[0]: {arr2d[0]}")
print(f"arr2d[0, 1]: {arr2d[0, 1]}")
print(f"arr2d[:, 1]: {arr2d[:, 1]}")

print()
print("=" * 60)
print("5. 数组形状操作")
print("=" * 60)

arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(f"原数组:\n{arr}")
print(f"形状: {arr.shape}")

print(f"\nreshape(4, 2):\n{arr.reshape(4, 2)}")

print(f"\nflatten: {arr.flatten()}")

print(f"\n转置:\n{arr.T}")

print()
print("=" * 60)
print("6. 常用函数")
print("=" * 60)

arr = np.array([1, 2, 3, 4, 5])

print(f"数组: {arr}")
print(f"sum: {arr.sum()}")
print(f"mean: {arr.mean()}")
print(f"std: {arr.std()}")
print(f"min: {arr.min()}")
print(f"max: {arr.max()}")

print(f"\nargmin (最小值索引): {arr.argmin()}")
print(f"argmax (最大值索引): {arr.argmax()}")

arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n二维数组:\n{arr2d}")
print(f"按列求和: {arr2d.sum(axis=0)}")
print(f"按行求和: {arr2d.sum(axis=1)}")

print()
print("=" * 60)
print("7. 广播机制")
print("=" * 60)

print("广播 (Broadcasting): 不同形状数组进行运算")
print("""
规则: 从右向左比较维度
  - 维度相同
  - 或其中一个维度为 1
""")

a = np.array([[1], [2], [3]])
b = np.array([10, 20, 30])

print(f"a (3x1):\n{a}")
print(f"b (3,): {b}")
print(f"a + b:\n{a + b}")

print()
print("=" * 60)
print("8. 随机数生成")
print("=" * 60)

print(f"rand (0-1均匀分布): {np.random.rand(5)}")
print(f"randn (正态分布): {np.random.randn(5)}")
print(f"randint (整数): {np.random.randint(1, 10, 5)}")
print(f"choice (随机选择): {np.random.choice([1,2,3,4,5], 3)}")

np.random.seed(42)
print(f"seed(42) 随机数: {np.random.rand(5)}")

print()
print("=" * 60)
print("9. 逻辑运算")
print("=" * 60)

arr = np.array([1, 2, 3, 4, 5])

print(f"数组: {arr}")
print(f"arr > 3: {arr > 3}")
print(f"arr == 3: {arr == 3}")

mask = arr > 3
print(f"arr[mask] (arr > 3): {arr[mask]}")

print(f"\nnp.where (条件选择):")
print(f"  np.where(arr > 3, '大', '小'): {np.where(arr > 3, '大', '小')}")

print()
print("=" * 60)
print("10. 矩阵运算")
print("=" * 60)

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"A:\n{A}")
print(f"B:\n{B}")
print(f"A + B:\n{A + B}")
print(f"A * B (逐元素):\n{A * B}")
print(f"A @ B (矩阵乘法):\n{A @ B}")
print(f"A.dot(B):\n{A.dot(B)}")

print(f"\n矩阵的逆:")
print(f"np.linalg.inv(A):\n{np.linalg.inv(A)}")

print(f"\n矩阵的行列式:")
print(f"np.linalg.det(A): {np.linalg.det(A)}")
