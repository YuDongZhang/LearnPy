"""
2. Pandas基础操作 - 代码示例
"""

import pandas as pd
import numpy as np

# ========== 1. 创建DataFrame ==========
df = pd.DataFrame({
    "name": ["张三", "李四", "王五", "赵六", "钱七"],
    "age": [25, 30, 28, 35, 22],
    "city": ["北京", "上海", "广州", "北京", "上海"],
    "salary": [15000, 25000, 18000, 30000, 12000],
})
print("DataFrame:")
print(df)

# ========== 2. 基本信息 ==========
print(f"\n基本信息:")
print(f"  形状: {df.shape}")
print(f"  列名: {list(df.columns)}")
print(f"  数据类型:\n{df.dtypes}")
print(f"\n统计摘要:\n{df.describe()}")

# ========== 3. 选择数据 ==========
print(f"\n选择列: {df['name'].tolist()}")
print(f"选择行(iloc): {df.iloc[0].tolist()}")
print(f"条件筛选(age>25):\n{df[df['age'] > 25]}")

# ========== 4. 数据修改 ==========
df["bonus"] = df["salary"] * 0.1
df["level"] = df["salary"].apply(lambda x: "高" if x > 20000 else "中" if x > 15000 else "低")
print(f"\n新增列后:\n{df}")

# ========== 5. 排序 ==========
print(f"\n按薪资降序:\n{df.sort_values('salary', ascending=False)}")

# ========== 6. 统计 ==========
print(f"\n城市分布:\n{df['city'].value_counts()}")
print(f"平均薪资: {df['salary'].mean():.0f}")
print(f"薪资中位数: {df['salary'].median():.0f}")

# ========== 7. 缺失值处理 ==========
df_missing = df.copy()
df_missing.loc[1, "salary"] = np.nan
print(f"\n缺失值:\n{df_missing.isna().sum()}")
df_filled = df_missing.fillna(df_missing["salary"].mean())
print(f"填充后:\n{df_filled}")
