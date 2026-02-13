"""
for 循环示例
============

for 循环用于遍历序列（列表、元组、字符串等）中的元素。
"""

print("=" * 40)
print("1. 基本for循环")
print("=" * 40)

print("遍历 range(5):")
for i in range(5):
    print(f"  i = {i}")

print("-" * 40)

print("遍历 range(1, 6):")
for i in range(1, 6):
    print(f"  i = {i}")

print("-" * 40)

print("遍历 range(0, 10, 2) (步长为2):")
for i in range(0, 10, 2):
    print(f"  i = {i}")

print()
print("=" * 40)
print("2. 遍历列表")
print("=" * 40)

fruits = ["苹果", "香蕉", "橙子", "葡萄"]

print("遍历水果列表:")
for fruit in fruits:
    print(f"  我喜欢吃{fruit}")

print("-" * 40)

print("使用索引遍历:")
for i in range(len(fruits)):
    print(f"  第{i+1}个水果是: {fruits[i]}")

print("-" * 40)

print("同时获取索引和值 (enumerate):")
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

print()
print("=" * 40)
print("3. 遍历字符串")
print("=" * 40)

text = "Python"

print("遍历字符串的每个字符:")
for char in text:
    print(f"  字符: {char}")

print()
print("=" * 40)
print("4. 遍历字典")
print("=" * 40)

person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

print("遍历字典的键:")
for key in person:
    print(f"  键: {key}")

print("-" * 40)

print("遍历字典的值:")
for value in person.values():
    print(f"  值: {value}")

print("-" * 40)

print("遍历字典的键值对:")
for key, value in person.items():
    print(f"  {key}: {value}")

print()
print("=" * 40)
print("5. 嵌套循环")
print("=" * 40)

print("打印九九乘法表:")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i*j}", end="  ")
    print()

print("-" * 40)

print("打印矩形:")
for i in range(3):
    for j in range(5):
        print("*", end=" ")
    print()

print()
print("=" * 40)
print("6. 循环中的else")
print("=" * 40)

print("for循环正常结束时执行else:")
for i in range(3):
    print(f"  i = {i}")
else:
    print("  循环正常结束")

print("-" * 40)

print("for循环被break时，else不执行:")
for i in range(5):
    if i == 3:
        print(f"  在i={i}时break")
        break
    print(f"  i = {i}")
else:
    print("  这行不会执行")
