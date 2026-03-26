# 1. NumPy数组与运算

## 什么是NumPy

NumPy是Python科学计算的基础库，提供高性能的多维数组对象和数学运算函数。几乎所有AI/数据科学库都依赖NumPy。

## 核心概念：ndarray

NumPy的核心是ndarray（N-dimensional array），比Python列表快10-100倍。

### 创建数组
- `np.array()` — 从列表创建
- `np.zeros()` / `np.ones()` — 全0/全1数组
- `np.arange()` / `np.linspace()` — 等差数组
- `np.random.randn()` — 随机数组

### 数组属性
- `shape` — 形状（如(3,4)表示3行4列）
- `dtype` — 数据类型（float64、int32等）
- `ndim` — 维度数
- `size` — 元素总数

## 数组运算

### 向量化运算
NumPy的运算是逐元素的，不需要写循环：
```python
a + b    # 逐元素加
a * b    # 逐元素乘
a ** 2   # 逐元素平方
```

### 广播机制
不同形状的数组也能运算，NumPy自动扩展：
```python
a = np.array([[1,2,3], [4,5,6]])  # (2,3)
b = np.array([10, 20, 30])        # (3,)
a + b  # b自动广播为(2,3)
```

## 常用操作

| 操作 | 函数 |
|------|------|
| 索引切片 | `a[0]`, `a[1:3]`, `a[:, 0]` |
| 变形 | `reshape()`, `flatten()`, `T` |
| 聚合 | `sum()`, `mean()`, `max()`, `min()` |
| 拼接 | `concatenate()`, `vstack()`, `hstack()` |
| 排序 | `sort()`, `argsort()` |
| 条件 | `where()`, 布尔索引 |

## 线性代数

```python
np.dot(a, b)      # 矩阵乘法
np.linalg.inv(a)  # 逆矩阵
np.linalg.det(a)  # 行列式
np.linalg.eig(a)  # 特征值分解
```
