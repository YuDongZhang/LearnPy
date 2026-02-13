"""
JSON 文件处理
=============

JSON (JavaScript Object Notation) 是一种轻量级数据交换格式。
Python 使用 json 模块处理 JSON 数据。
"""

import json
import os

demo_dir = "d:\\project\\LearnPy\\06_文件操作"

print("=" * 40)
print("1. Python 对象转 JSON 字符串")
print("=" * 40)

data = {
    "name": "张三",
    "age": 25,
    "city": "北京",
    "hobbies": ["读书", "游泳", "编程"],
    "is_student": False
}

json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("Python 字典转 JSON 字符串:")
print(json_str)

print("-" * 40)

print("参数说明:")
print("  ensure_ascii=False - 支持中文")
print("  indent=2 - 缩进格式化")

print()
print("=" * 40)
print("2. JSON 字符串转 Python 对象")
print("=" * 40)

json_str = '{"name": "李四", "age": 30, "city": "上海"}'

python_obj = json.loads(json_str)
print(f"JSON 字符串: {json_str}")
print(f"Python 对象: {python_obj}")
print(f"类型: {type(python_obj)}")

print()
print("=" * 40)
print("3. 写入 JSON 文件")
print("=" * 40)

file_path = os.path.join(demo_dir, "data.json")

students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78}
]

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

print(f"JSON 文件已保存: {file_path}")

print()
print("=" * 40)
print("4. 读取 JSON 文件")
print("=" * 40)

with open(file_path, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print("从文件读取的数据:")
for student in loaded_data:
    print(f"  {student['name']}: {student['score']}分")

print()
print("=" * 40)
print("5. 处理复杂嵌套结构")
print("=" * 40)

complex_data = {
    "company": "ABC公司",
    "employees": [
        {
            "id": 1,
            "name": "张三",
            "department": "技术部",
            "skills": ["Python", "Java", "SQL"]
        },
        {
            "id": 2,
            "name": "李四",
            "department": "市场部",
            "skills": ["营销", "数据分析"]
        }
    ],
    "founded": 2020,
    "active": True
}

file_path = os.path.join(demo_dir, "company.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(complex_data, f, ensure_ascii=False, indent=2)

print("复杂嵌套数据已保存")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"公司: {data['company']}")
print("员工:")
for emp in data['employees']:
    print(f"  {emp['name']} - {emp['department']}")

print()
print("=" * 40)
print("6. JSON 格式化输出")
print("=" * 40)

data = {"name": "测试", "values": [1, 2, 3]}

print("紧凑格式:")
print(json.dumps(data, ensure_ascii=False))

print()
print("美化格式 (indent=2):")
print(json.dumps(data, ensure_ascii=False, indent=2))

print()
print("排序键 (sort_keys=True):")
data = {"c": 3, "a": 1, "b": 2}
print(json.dumps(data, sort_keys=True, indent=2))

print()
print("=" * 40)
print("7. 错误处理")
print("=" * 40)

invalid_json = '{"name": "test", "age": }'

try:
    data = json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")

print()
print("=" * 40)
print("8. 类型对应关系")
print("=" * 40)

print("Python -> JSON:")
print("  dict  -> object")
print("  list  -> array")
print("  str   -> string")
print("  int   -> number")
print("  float -> number")
print("  True  -> true")
print("  False -> false")
print("  None  -> null")

print()
print("=" * 40)
print("9. 清理演示文件")
print("=" * 40)

for filename in ["data.json", "company.json"]:
    file_path = os.path.join(demo_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"已删除: {filename}")
