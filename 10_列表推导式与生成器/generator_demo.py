"""
生成器示例
=========
"""

print("=" * 40)
print("1. 生成器表达式")
print("=" * 40)

gen = (x**2 for x in range(5))
print(f"生成器对象: {gen}")
print(f"类型: {type(gen)}")

print("遍历生成器:")
for value in gen:
    print(f"  {value}")

print()
print("=" * 40)
print("2. 生成器函数与 yield")
print("=" * 40)

def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

gen = count_up(5)
print(f"生成器: {gen}")
print(f"第一个值: {next(gen)}")
print(f"第二个值: {next(gen)}")
print("剩余值:")
for value in gen:
    print(f"  {value}")

print()
print("=" * 40)
print("3. 斐波那契数列生成器")
print("=" * 40)

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print("前10个斐波那契数:")
for num in fibonacci(10):
    print(f"  {num}", end="")
print()

print()
print("=" * 40)
print("4. 无限生成器")
print("=" * 40)

def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1

counter = infinite_counter()
print("获取前5个值:")
for _ in range(5):
    print(f"  {next(counter)}")

print()
print("=" * 40)
print("5. 生成器 vs 列表（内存对比）")
print("=" * 40)

import sys

big_list = [x for x in range(10000)]
big_gen = (x for x in range(10000))

print(f"列表大小: {sys.getsizeof(big_list)} 字节")
print(f"生成器大小: {sys.getsizeof(big_gen)} 字节")

print()
print("=" * 40)
print("6. 生成器管道")
print("=" * 40)

def generate_numbers(n):
    for i in range(n):
        yield i

def filter_even(gen):
    for num in gen:
        if num % 2 == 0:
            yield num

def square_numbers(gen):
    for num in gen:
        yield num ** 2

numbers = generate_numbers(10)
evens = filter_even(numbers)
squares = square_numbers(evens)

print("偶数的平方:")
for num in squares:
    print(f"  {num}")

print()
print("=" * 40)
print("7. 读取大文件示例")
print("=" * 40)

def read_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

def filter_lines(lines, keyword):
    for line in lines:
        if keyword in line:
            yield line

print("生成器可以逐行处理大文件，不会一次性加载到内存")

print()
print("=" * 40)
print("8. yield from 语法")
print("=" * 40)

def sub_generator():
    yield 1
    yield 2

def main_generator():
    yield from sub_generator()
    yield 3

print("yield from 示例:")
for value in main_generator():
    print(f"  {value}")
