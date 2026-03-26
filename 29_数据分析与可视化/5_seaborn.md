# 5. Seaborn统计可视化

## 什么是Seaborn

基于Matplotlib的高级可视化库，专注统计图表，默认样式更美观。

## 常用图表

| 图表 | 函数 | 适用场景 |
|------|------|---------|
| 分布图 | `sns.histplot()` / `sns.kdeplot()` | 数据分布 |
| 箱线图 | `sns.boxplot()` | 分布+异常值 |
| 小提琴图 | `sns.violinplot()` | 分布形状 |
| 散点图 | `sns.scatterplot()` | 相关性 |
| 热力图 | `sns.heatmap()` | 相关系数矩阵 |
| 计数图 | `sns.countplot()` | 分类计数 |
| 配对图 | `sns.pairplot()` | 多变量关系 |
| 回归图 | `sns.regplot()` | 线性关系 |

## 与Pandas配合

Seaborn直接接受DataFrame，用列名指定x/y：
```python
sns.scatterplot(data=df, x="age", y="salary", hue="department")
```

## 样式设置

```python
sns.set_theme(style="whitegrid")  # 主题
sns.set_palette("husl")           # 调色板
```
