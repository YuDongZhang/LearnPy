"""
运算符示例
==========

Python 支持多种运算符：
- 算术运算符
- 比较运算符
- 逻辑运算符
- 赋值运算符
"""

print("=" * 40)
print("1. 算术运算符")
print("=" * 40)

a, b = 10, 3

print(f"a = {a}, b = {b}")
print(f"a + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")
print(f"a / b = {a / b}")
print(f"a // b = {a // b}")
print(f"a % b = {a % b}")
print(f"a ** b = {a ** b}")

print("-" * 40)

print("字符串也可以运算：")
s1 = "Hello"
s2 = "World"
print(f"'Hello' + 'World' = {s1 + s2}")
print(f"'Hello' * 3 = {s1 * 3}")

print()
print("=" * 40)
print("2. 比较运算符")
print("=" * 40)

x, y = 5, 10

print(f"x = {x}, y = {y}")
print(f"x == y: {x == y}")
print(f"x != y: {x != y}")
print(f"x > y: {x > y}")
print(f"x < y: {x < y}")
print(f"x >= y: {x >= y}")
print(f"x <= y: {x <= y}")

print("-" * 40)

print("字符串比较：")
print(f"'apple' == 'apple': {'apple' == 'apple'}")
print(f"'apple' < 'banana': {'apple' < 'banana'}")

print()
print("=" * 40)
print("3. 逻辑运算符")
print("=" * 40)

p, q = True, False

print(f"p = {p}, q = {q}")
print(f"p and q: {p and q}")
print(f"p or q: {p or q}")
print(f"not p: {not p}")

print("-" * 40)

print("逻辑运算常用于条件：")
age = 25
has_id = True

can_enter = age >= 18 and has_id
print(f"年龄 >= 18 且有证件: {can_enter}")

print()
print("=" * 40)
print("4. 赋值运算符")
print("=" * 40)

num = 10
print(f"初始值: num = {num}")

num += 5
print(f"num += 5 后: num = {num}")

num -= 3
print(f"num -= 3 后: num = {num}")

num *= 2
print(f"num *= 2 后: num = {num}")

num /= 4
print(f"num /= 4 后: num = {num}")

print()
print("=" * 40)
print("5. 运算优先级")
print("=" * 40)

print("优先级从高到低：")
print("1. ** (幂)")
print("2. * / // %")
print("3. + -")
print("4. 比较运算符")
print("5. 逻辑运算符")

print("-" * 40)

result1 = 2 + 3 * 4
result2 = (2 + 3) * 4
print(f"2 + 3 * 4 = {result1}")
print(f"(2 + 3) * 4 = {result2}")

result3 = 2 ** 3 ** 2
result4 = (2 ** 3) ** 2
print(f"2 ** 3 ** 2 = {result3}")
print(f"(2 ** 3) ** 2 = {result4}")
