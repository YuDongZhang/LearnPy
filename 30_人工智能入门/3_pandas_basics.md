# 3. Pandas数据处理基础

## Pandas简介

Pandas 是 Python 中最流行的数据处理库，提供两种主要数据结构：

- **Series**：一维带标签的数组
- **DataFrame**：二维表格数据（类似 Excel）

核心功能：数据读取/写入（CSV、Excel、JSON、SQL）、数据清洗和预处理、数据分析、数据可视化。

## Series创建

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40])
s.index.tolist()  # 索引
s.values          # 值

s2 = pd.Series([100, 200, 300], index=['a', 'b', 'c'])  # 带自定义索引
```

## DataFrame创建

```python
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳']
}
df = pd.DataFrame(data)

# 从列表创建
df2 = pd.DataFrame([[1, '北京'], [2, '上海']], columns=['编号', '城市'])
```

## 数据读取

```python
df = pd.read_csv('file.csv')        # 读取 CSV
df = pd.read_excel('file.xlsx')     # 读取 Excel
df = pd.read_json('file.json')      # 读取 JSON
df = pd.read_sql(query, connection) # 读取 SQL
```

## 数据选择

```python
df['姓名']             # 选择单列 → Series
df[['姓名', '城市']]    # 选择多列 → DataFrame
df.iloc[0:2]           # 按位置选择前2行
df.loc['a':'c']        # 按标签选择（含端点）
```

## 数据过滤

```python
df[df['年龄'] > 28]                              # 单条件
df[(df['年龄'] > 25) & (df['城市'] == '北京')]    # 多条件用 & | 连接
```

## 数据增删改查

```python
df.loc[2] = ['王五', 35]       # 添加行
df['城市'] = ['北京', '上海']   # 添加列
df.loc[0, '年龄'] = 26         # 修改值
df = df.drop(0)                # 删除行
```

## 数据统计

```python
df.describe()   # 基本统计摘要（计数、均值、标准差、分位数）
df.sum()        # 求和
df.mean()       # 均值
df.std()        # 标准差
df.min(), df.max()
```

## 分组聚合

```python
df.groupby('部门')['薪资'].mean()

# 多重聚合
df.groupby('部门').agg({
    '姓名': 'count',
    '薪资': ['sum', 'mean']
})
```

SQL 中的 `GROUP BY` 思路，是数据分析的核心操作。

## 缺失值处理

```python
df.isnull()     # 检测缺失值
df.fillna(0)    # 填充缺失值
df.dropna()     # 删除含缺失值的行
```

## 数据合并

```python
pd.concat([df1, df2], ignore_index=True)  # 纵向拼接
pd.merge(df1, df3, on='key')              # 按关键列连接（类似 SQL JOIN）
```

## 数据导出

```python
df.to_csv('file.csv', index=False)
df.to_excel('file.xlsx', index=False)
df.to_json('file.json')
df.to_sql('table', connection)
```

## 代码

讲解对应的示例代码见 `3_pandas_basics.py`。
