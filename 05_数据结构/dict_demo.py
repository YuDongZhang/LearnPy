"""
字典详解
========

字典是键值对的集合。
使用花括号 {} 创建字典。
"""

print("=" * 40)
print("1. 创建字典")
print("=" * 40)

person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

print(f"person = {person}")

print("-" * 40)

empty_dict = {}
print(f"空字典: {empty_dict}")

dict_from_list = dict([("a", 1), ("b", 2)])
print(f"从列表创建: {dict_from_list}")

print()
print("=" * 40)
print("2. 访问元素")
print("=" * 40)

person = {"name": "张三", "age": 25, "city": "北京"}
print(f"person = {person}")

print(f"person['name'] = {person['name']}")
print(f"person['age'] = {person['age']}")

print("-" * 40)

print("使用 get() 方法（更安全）:")
print(f"person.get('name') = {person.get('name')}")
print(f"person.get('job') = {person.get('job')}")
print(f"person.get('job', '未知') = {person.get('job', '未知')}")

print()
print("=" * 40)
print("3. 修改元素")
print("=" * 40)

person = {"name": "张三", "age": 25}
print(f"原始: {person}")

person["age"] = 26
print(f"修改年龄: {person}")

person["job"] = "工程师"
print(f"添加职业: {person}")

print()
print("=" * 40)
print("4. 删除元素")
print("=" * 40)

person = {"name": "张三", "age": 25, "city": "北京", "job": "工程师"}
print(f"原始: {person}")

del person["job"]
print(f"del person['job']: {person}")

age = person.pop("age")
print(f"pop('age') 返回: {age}, 结果: {person}")

city = person.pop("city", "未知")
print(f"pop('city', '未知'): {person}")

person.clear()
print(f"clear(): {person}")

print()
print("=" * 40)
print("5. 遍历字典")
print("=" * 40)

person = {"name": "张三", "age": 25, "city": "北京"}

print("遍历键:")
for key in person:
    print(f"  {key}")

print("-" * 40)

print("遍历值:")
for value in person.values():
    print(f"  {value}")

print("-" * 40)

print("遍历键值对:")
for key, value in person.items():
    print(f"  {key}: {value}")

print()
print("=" * 40)
print("6. 字典方法")
print("=" * 40)

person = {"name": "张三", "age": 25}

print(f"keys(): {list(person.keys())}")
print(f"values(): {list(person.values())}")
print(f"items(): {list(person.items())}")

print("-" * 40)

print("setdefault() - 如果键不存在则添加:")
person.setdefault("city", "未知")
print(f"setdefault('city', '未知'): {person}")

person.setdefault("city", "上海")
print(f"setdefault('city', '上海'): {person}")

print("-" * 40)

print("update() - 更新字典:")
person.update({"age": 26, "job": "工程师"})
print(f"update({{'age': 26, 'job': '工程师'}}): {person}")

print()
print("=" * 40)
print("7. 字典推导式")
print("=" * 40)

squares = {x: x ** 2 for x in range(1, 6)}
print(f"1-5的平方: {squares}")

print("-" * 40)

scores = {"张三": 85, "李四": 92, "王五": 78}
passed = {name: score for name, score in scores.items() if score >= 80}
print(f"及格的学生: {passed}")

print()
print("=" * 40)
print("8. 嵌套字典")
print("=" * 40)

students = {
    "张三": {"math": 90, "english": 85},
    "李四": {"math": 88, "english": 92},
    "王五": {"math": 75, "english": 80}
}

print("学生成绩:")
for name, scores in students.items():
    print(f"  {name}: 数学{scores['math']}, 英语{scores['english']}")

print()
print("=" * 40)
print("9. 字典合并")
print("=" * 40)

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

merged = {**dict1, **dict2}
print(f"使用 ** 合并: {merged}")

dict1.update(dict2)
print(f"使用 update(): {dict1}")

print()
print("=" * 40)
print("10. 实际应用示例")
print("=" * 40)

print("学生信息管理:")
students = {}

def add_student(name, age, score):
    students[name] = {"age": age, "score": score}

def get_student(name):
    return students.get(name, "未找到")

add_student("张三", 18, 85)
add_student("李四", 19, 92)
add_student("王五", 18, 78)

print(f"所有学生: {students}")
print(f"查找张三: {get_student('张三')}")
print(f"查找赵六: {get_student('赵六')}")

print("-" * 40)

print("单词计数:")
text = "hello world hello python world hello"
word_count = {}

for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1

print(f"单词出现次数: {word_count}")
