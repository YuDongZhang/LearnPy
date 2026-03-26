# 2. Pandas基础操作

## 什么是Pandas

Pandas是Python最强大的数据分析库，提供DataFrame和Series两种核心数据结构，可以轻松处理表格数据。

## 核心数据结构

### Series
一维带标签的数组，类似带索引的列表。

### DataFrame
二维表格数据，类似Excel表或SQL表。每列是一个Series。

## 创建DataFrame

```python
# 从字典创建
df = pd.DataFrame({"name": ["张三", "李四"], "age": [25, 30]})

# 从CSV读取
df = pd.read_csv("data.csv")

# 从Excel读取
df = pd.read_excel("data.xlsx")
```

## 基础操作

| 操作 | 方法 |
|------|------|
| 查看前N行 | `df.head(n)` |
| 基本信息 | `df.info()`, `df.describe()` |
| 选择列 | `df["col"]`, `df[["col1","col2"]]` |
| 选择行 | `df.loc[标签]`, `df.iloc[位置]` |
| 条件筛选 | `df[df["age"] > 25]` |
| 排序 | `df.sort_values("col")` |
| 去重 | `df.drop_duplicates()` |
| 缺失值 | `df.isna()`, `df.fillna()`, `df.dropna()` |

## 数据修改

```python
df["new_col"] = df["a"] + df["b"]  # 新增列
df.rename(columns={"old": "new"})   # 重命名
df.drop("col", axis=1)              # 删除列
df.apply(func)                      # 应用函数
```

## 统计分析

```python
df.mean()          # 均值
df.std()           # 标准差
df.corr()          # 相关系数矩阵
df.value_counts()  # 频次统计
```

## 数据IO

| 格式 | 读取 | 写入 |
|------|------|------|
| CSV | `read_csv()` | `to_csv()` |
| Excel | `read_excel()` | `to_excel()` |
| JSON | `read_json()` | `to_json()` |
| SQL | `read_sql()` | `to_sql()` |
