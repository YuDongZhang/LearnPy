"""
3. Pandas进阶 - 代码示例
分组聚合、数据合并、透视表、时间序列。
"""

import pandas as pd
import numpy as np

# ========== 1. 分组聚合 ==========
df = pd.DataFrame({
    "product": ["A", "B", "A", "B", "A", "B"],
    "region": ["北", "北", "南", "南", "北", "南"],
    "sales": [100, 200, 150, 300, 120, 250],
    "quantity": [10, 20, 15, 30, 12, 25],
})

print("分组聚合:")
print(df.groupby("product")["sales"].sum())
print()
print(df.groupby(["product", "region"]).agg({"sales": "sum", "quantity": "mean"}))

# ========== 2. 数据合并 ==========
df1 = pd.DataFrame({"id": [1, 2, 3], "name": ["张三", "李四", "王五"]})
df2 = pd.DataFrame({"id": [1, 2, 4], "score": [90, 85, 78]})

print(f"\nmerge (inner join):\n{pd.merge(df1, df2, on='id', how='inner')}")
print(f"\nmerge (left join):\n{pd.merge(df1, df2, on='id', how='left')}")

# concat拼接
df_top = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
df_bottom = pd.DataFrame({"a": [5, 6], "b": [7, 8]})
print(f"\nconcat:\n{pd.concat([df_top, df_bottom], ignore_index=True)}")

# ========== 3. 透视表 ==========
print(f"\n透视表:")
pivot = pd.pivot_table(df, values="sales", index="product", columns="region", aggfunc="sum")
print(pivot)

# ========== 4. 时间序列 ==========
dates = pd.date_range("2024-01-01", periods=12, freq="M")
ts = pd.DataFrame({"date": dates, "value": np.random.randint(100, 500, 12)})
ts.set_index("date", inplace=True)

print(f"\n时间序列:")
print(ts)
print(f"\n季度汇总:\n{ts.resample('Q').sum()}")
print(f"\n3月滚动均值:\n{ts.rolling(3).mean()}")
