"""
CSV 文件处理
============

CSV (Comma-Separated Values) 是一种表格数据格式。
Python 使用 csv 模块处理 CSV 文件。
"""

import csv
import os

demo_dir = "d:\\project\\LearnPy\\06_文件操作"

print("=" * 40)
print("1. 写入 CSV 文件")
print("=" * 40)

file_path = os.path.join(demo_dir, "students.csv")

students = [
    ["姓名", "年龄", "城市", "分数"],
    ["张三", 18, "北京", 85],
    ["李四", 19, "上海", 92],
    ["王五", 18, "广州", 78]
]

with open(file_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)

print(f"CSV 文件已保存: {file_path}")

print()
print("=" * 40)
print("2. 读取 CSV 文件")
print("=" * 40)

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

print()
print("=" * 40)
print("3. 使用 DictWriter 和 DictReader")
print("=" * 40)

file_path = os.path.join(demo_dir, "employees.csv")

employees = [
    {"name": "张三", "department": "技术部", "salary": 10000},
    {"name": "李四", "department": "市场部", "salary": 8000},
    {"name": "王五", "department": "财务部", "salary": 9000}
]

with open(file_path, "w", encoding="utf-8", newline="") as f:
    fieldnames = ["name", "department", "salary"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(employees)

print("使用 DictWriter 写入完成")

print("-" * 40)

print("使用 DictReader 读取:")
with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']} - {row['department']} - {row['salary']}元")

print()
print("=" * 40)
print("4. 追加数据")
print("=" * 40)

with open(file_path, "a", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
    writer.writerow({"name": "赵六", "department": "人事部", "salary": 8500})

print("已追加一条记录")

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("当前所有记录:")
    for row in reader:
        print(f"  {row['name']} - {row['department']}")

print()
print("=" * 40)
print("5. 自定义分隔符")
print("=" * 40)

file_path = os.path.join(demo_dir, "data.tsv")

data = [
    ["姓名", "年龄"],
    ["张三", 25],
    ["李四", 30]
]

with open(file_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(data)

print("TSV 文件（制表符分隔）已保存")

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        print(f"  {row}")

print()
print("=" * 40)
print("6. 处理特殊字符")
print("=" * 40)

file_path = os.path.join(demo_dir, "special.csv")

data = [
    ["描述", "备注"],
    ["包含,逗号", "正常"],
    ["包含\"引号\"", "正常"],
    ["包含\n换行", "正常"]
]

with open(file_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerows(data)

print("包含特殊字符的数据已保存（自动处理引号和转义）")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print("文件内容:")
    print(content)

print()
print("=" * 40)
print("7. 实用示例：数据分析")
print("=" * 40)

file_path = os.path.join(demo_dir, "sales.csv")

sales_data = [
    ["日期", "产品", "数量", "单价"],
    ["2024-01-01", "苹果", 100, 5.0],
    ["2024-01-01", "香蕉", 150, 3.0],
    ["2024-01-02", "苹果", 80, 5.0],
    ["2024-01-02", "橙子", 200, 4.0],
    ["2024-01-03", "香蕉", 120, 3.0]
]

with open(file_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(sales_data)

print("销售数据已保存")

total_revenue = 0
with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("销售记录:")
    for row in reader:
        revenue = int(row["数量"]) * float(row["单价"])
        total_revenue += revenue
        print(f"  {row['日期']} - {row['产品']}: {row['数量']}个 x {row['单价']}元 = {revenue}元")

print(f"\n总销售额: {total_revenue}元")

print()
print("=" * 40)
print("8. 清理演示文件")
print("=" * 40)

for filename in ["students.csv", "employees.csv", "data.tsv", "special.csv", "sales.csv"]:
    file_path = os.path.join(demo_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"已删除: {filename}")
