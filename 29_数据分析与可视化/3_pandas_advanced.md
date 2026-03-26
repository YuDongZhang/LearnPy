# 3. Pandas进阶

## 分组聚合（GroupBy）

SQL中的GROUP BY在Pandas中的实现：

```python
df.groupby("category")["sales"].sum()
df.groupby(["year", "month"]).agg({"sales": "sum", "count": "mean"})
```

## 数据合并

| 方法 | 说明 | 类似SQL |
|------|------|---------|
| `merge()` | 按键合并 | JOIN |
| `concat()` | 拼接 | UNION |
| `join()` | 按索引合并 | JOIN ON index |

## 透视表

```python
pd.pivot_table(df, values="sales", index="product", columns="month", aggfunc="sum")
```

## 时间序列

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df.resample("M").sum()  # 按月汇总
df.rolling(7).mean()    # 7日滚动均值
```

## 字符串操作

```python
df["name"].str.lower()
df["name"].str.contains("张")
df["name"].str.split("_")
df["name"].str.replace("old", "new")
```

## 性能优化

1. 用`category`类型替代字符串列
2. 用`read_csv`的`usecols`只读需要的列
3. 用`chunksize`分块读取大文件
4. 避免逐行循环，用向量化操作
