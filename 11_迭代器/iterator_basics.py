"""
迭代器基础
=========
"""

print("=" * 40)
print("1. 可迭代对象 vs 迭代器")
print("=" * 40)

my_list = [1, 2, 3]
print(f"列表是可迭代对象: {hasattr(my_list, '__iter__')}")
print(f"列表不是迭代器: {hasattr(my_list, '__next__')}")

my_iter = iter(my_list)
print(f"iter(list) 是迭代器: {hasattr(my_iter, '__next__')}")

print()
print("=" * 40)
print("2. 手动使用迭代器")
print("=" * 40)

my_list = [1, 2, 3]
my_iter = iter(my_list)

print(f"第一个值: {next(my_iter)}")
print(f"第二个值: {next(my_iter)}")
print(f"第三个值: {next(my_iter)}")

try:
    print(f"第四个值: {next(my_iter)}")
except StopIteration:
    print("迭代结束，抛出 StopIteration")

print()
print("=" * 40)
print("3. for 循环的原理")
print("=" * 40)

my_list = [1, 2, 3]

print("for 循环内部实现:")
it = iter(my_list)
while True:
    try:
        value = next(it)
        print(f"  值: {value}")
    except StopIteration:
        print("  循环结束")
        break

print()
print("=" * 40)
print("4. 字符串迭代器")
print("=" * 40)

text = "Python"
char_iter = iter(text)
print("遍历字符串:")
for char in char_iter:
    print(f"  '{char}'")

print()
print("=" * 40)
print("5. 字典迭代器")
print("=" * 40)

person = {"name": "张三", "age": 25, "city": "北京"}

print("遍历键:")
for key in person:
    print(f"  {key}")

print()
print("遍历键值对:")
for key, value in person.items():
    print(f"  {key}: {value}")

print()
print("=" * 40)
print("6. 迭代器只能遍历一次")
print("=" * 40)

numbers = [1, 2, 3]
my_iter = iter(numbers)

print("第一次遍历:")
for num in my_iter:
    print(f"  {num}")

print("第二次遍历（无输出）:")
for num in my_iter:
    print(f"  {num}")

print("需要重新获取迭代器:")
my_iter = iter(numbers)
for num in my_iter:
    print(f"  {num}")
