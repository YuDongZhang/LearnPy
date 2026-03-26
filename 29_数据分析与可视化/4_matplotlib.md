# 4. Matplotlib可视化

## 什么是Matplotlib

Python最基础的绑图库，几乎所有可视化库都基于它。

## 基础用法

```python
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.title("标题")
plt.xlabel("X轴")
plt.ylabel("Y轴")
plt.show()
```

## 常用图表

| 图表 | 函数 | 适用场景 |
|------|------|---------|
| 折线图 | `plt.plot()` | 趋势变化 |
| 柱状图 | `plt.bar()` | 分类对比 |
| 散点图 | `plt.scatter()` | 相关性分析 |
| 直方图 | `plt.hist()` | 分布情况 |
| 饼图 | `plt.pie()` | 占比分析 |
| 箱线图 | `plt.boxplot()` | 异常值检测 |
| 热力图 | `plt.imshow()` | 矩阵/相关性 |

## 子图

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 1].bar(x, y)
```

## 样式美化

```python
plt.style.use("seaborn-v0_8")  # 使用预设样式
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 中文支持
plt.rcParams["axes.unicode_minus"] = False
```

## 保存图片

```python
plt.savefig("chart.png", dpi=300, bbox_inches="tight")
```
