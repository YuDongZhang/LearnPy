"""
迭代器工具
=========
"""

print("=" * 40)
print("1. enumerate - 带索引迭代")
print("=" * 40)

fruits = ["苹果", "香蕉", "橙子"]
print("带索引遍历:")
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

print()
print("指定起始索引:")
for index, fruit in enumerate(fruits, start=1):
    print(f"  {index}: {fruit}")

print()
print("=" * 40)
print("2. zip - 并行迭代")
print("=" * 40)

names = ["张三", "李四", "王五"]
ages = [25, 30, 28]
cities = ["北京", "上海", "广州"]

print("并行遍历:")
for name, age, city in zip(names, ages, cities):
    print(f"  {name}, {age}岁, {city}")

print()
print("创建字典:")
person_dict = dict(zip(names, ages))
print(f"  {person_dict}")

print()
print("=" * 40)
print("3. map - 映射")
print("=" * 40)

numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x**2, numbers))
print(f"平方: {squares}")

words = ["hello", "world", "python"]
upper_words = list(map(str.upper, words))
print(f"大写: {upper_words}")

print()
print("=" * 40)
print("4. filter - 过滤")
print("=" * 40)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

greater_than_5 = list(filter(lambda x: x > 5, numbers))
print(f"大于5: {greater_than_5}")

print()
print("=" * 40)
print("5. itertools 模块")
print("=" * 40)

import itertools

print("count - 无限计数:")
for i, num in enumerate(itertools.count(start=10, step=2)):
    if i >= 5:
        break
    print(f"  {num}")

print()
print("cycle - 无限循环:")
for i, item in enumerate(itertools.cycle(["A", "B", "C"])):
    if i >= 7:
        break
    print(f"  {item}")

print()
print("repeat - 重复:")
repeated = list(itertools.repeat("Hello", 3))
print(f"重复3次: {repeated}")

print()
print("chain - 链接迭代:")
list1 = [1, 2, 3]
list2 = [4, 5, 6]
chained = list(itertools.chain(list1, list2))
print(f"链接: {chained}")

print()
print("islice - 切片迭代:")
numbers = range(100)
sliced = list(itertools.islice(numbers, 5, 10))
print(f"切片[5:10]: {sliced}")

print()
print("=" * 40)
print("6. 组合迭代器")
print("=" * 40)

print("product - 笛卡尔积:")
for pair in itertools.product(['A', 'B'], [1, 2]):
    print(f"  {pair}")

print()
print("permutations - 排列:")
for perm in itertools.permutations([1, 2, 3], 2):
    print(f"  {perm}")

print()
print("combinations - 组合:")
for comb in itertools.combinations([1, 2, 3, 4], 2):
    print(f"  {comb}")
