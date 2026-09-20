"""
Pandas 数据处理基础
==================

Pandas 是 Python 中最流行的数据处理库，用于数据分析。
"""

print("=" * 60)
print("1. Pandas 简介")
print("=" * 60)

print("""
Pandas 提供两种主要数据结构:
  • Series   - 一维带标签的数组
  • DataFrame - 二维表格数据（类似 Excel）

核心功能:
  • 数据读取/写入 (CSV, Excel, JSON, SQL)
  • 数据清洗和预处理
  • 数据分析
  • 数据可视化
""")

print()
print("=" * 60)
print("2. Series 创建")
print("=" * 60)

import pandas as pd

s = pd.Series([10, 20, 30, 40])
print(f"简单 Series:\n{s}")
print(f"\n索引: {s.index.tolist()}")
print(f"值: {s.values}")

s2 = pd.Series([100, 200, 300], index=['a', 'b', 'c'])
print(f"\n带索引的 Series:\n{s2}")

print()
print("=" * 60)
print("3. DataFrame 创建")
print("=" * 60)

data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳']
}

df = pd.DataFrame(data)
print(f"DataFrame:\n{df}")

df2 = pd.DataFrame([
    [1, '北京'],
    [2, '上海'],
    [3, '广州']
], columns=['编号', '城市'])

print(f"\n从列表创建:\n{df2}")

print()
print("=" * 60)
print("4. 数据读取")
print("=" * 60)

print("常见数据读取方法:")
print("""
df = pd.read_csv('file.csv')       # 读取 CSV
df = pd.read_excel('file.xlsx')    # 读取 Excel
df = pd.read_json('file.json')     # 读取 JSON
df = pd.read_sql(query, connection) # 读取 SQL
""")

print()
print("=" * 60)
print("5. 数据选择")
print("=" * 60)

df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳']
})

print(f"DataFrame:\n{df}")

print(f"\n选择单列: df['姓名']\n{df['姓名'].tolist()}")

print(f"\n选择多列: df[['姓名', '城市']]")
print(df[['姓名', '城市']])

print(f"\n按位置选择 iloc[0:2]:")
print(df.iloc[0:2])

print(f"\n按标签选择 loc['0':'2']:")
df_with_idx = df.copy()
df_with_idx.index = ['a', 'b', 'c', 'd']
print(df_with_idx.loc['a':'c'])

print()
print("=" * 60)
print("6. 数据过滤")
print("=" * 60)

df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳']
})

print("过滤年龄大于28的行:")
print(df[df['年龄'] > 28])

print("\n多条件过滤 (年龄>25 且 在北京):")
print(df[(df['年龄'] > 25) & (df['城市'] == '北京')])

print()
print("=" * 60)
print("7. 数据增删改查")
print("=" * 60)

df = pd.DataFrame({
    '姓名': ['张三', '李四'],
    '年龄': [25, 30]
})

print("初始 DataFrame:")
print(df)

df.loc[2] = ['王五', 35]
print("\n添加行:")
print(df)

df['城市'] = ['北京', '上海', '广州']
print("\n添加列:")
print(df)

df.loc[0, '年龄'] = 26
print("\n修改值:")
print(df)

df = df.drop(0)
print("\n删除行:")
print(df)

print()
print("=" * 60)
print("8. 数据统计")
print("=" * 60)

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50]
})

print(f"DataFrame:\n{df}")

print(f"\ndescribe():")
print(df.describe())

print(f"\nsum(): {df.sum().tolist()}")
print(f"mean(): {df.mean().tolist()}")
print(f"std(): {df.std().tolist()}")
print(f"min(): {df.min().tolist()}")
print(f"max(): {df.max().tolist()}")

print()
print("=" * 60)
print("9. 分组聚合")
print("=" * 60)

df = pd.DataFrame({
    '部门': ['销售', '销售', '技术', '技术', '行政'],
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '薪资': [5000, 6000, 8000, 9000, 4000]
})

print(f"DataFrame:\n{df}")

print("\n按部门分组求平均薪资:")
print(df.groupby('部门')['薪资'].mean())

print("\n按部门分组统计:")
print(df.groupby('部门').agg({
    '姓名': 'count',
    '薪资': ['sum', 'mean']
}))

print()
print("=" * 60)
print("10. 缺失值处理")
print("=" * 60)

df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [5, None, None, 8],
    'C': [9, 10, 11, 12]
})

print(f"包含缺失值的 DataFrame:\n{df}")

print(f"\n检测缺失值:\n{df.isnull()}")

print(f"\n填充缺失值:")
print(df.fillna(0))

print(f"\n删除缺失值:")
print(df.dropna())

print()
print("=" * 60)
print("11. 数据合并")
print("=" * 60)

df1 = pd.DataFrame({'key': ['a', 'b'], 'value': [1, 2]})
df2 = pd.DataFrame({'key': ['a', 'b'], 'value': [3, 4]})

print(f"df1:\n{df1}")
print(f"df2:\n{df2}")

print("\nconcat 合并:")
print(pd.concat([df1, df2], ignore_index=True))

df3 = pd.DataFrame({'key': ['a', 'b'], 'value2': [5, 6]})
print(f"\ndf3:\n{df3}")

print("\nmerge 合并:")
print(pd.merge(df1, df3, on='key'))

print()
print("=" * 60)
print("12. 数据导出")
print("=" * 60)

print("常见数据导出方法:")
print("""
df.to_csv('file.csv', index=False)    # 导出 CSV
df.to_excel('file.xlsx', index=False) # 导出 Excel
df.to_json('file.json')              # 导出 JSON
df.to_sql('table', connection)        # 导出 SQL
""")
