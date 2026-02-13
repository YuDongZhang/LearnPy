"""
数据类型详解
============

Python 的基本数据类型：
- int    整数
- float  浮点数
- str    字符串
- bool   布尔值
"""

print("=" * 40)
print("1. 整数类型 (int)")
print("=" * 40)

a = 100
b = -50
c = 0

print("a =", a, "类型：", type(a))
print("b =", b, "类型：", type(b))
print("c =", c, "类型：", type(c))

print("-" * 40)

print("整数可以是任意大小：")
big_number = 10 ** 100
print("10的100次方 =", big_number)

print()
print("=" * 40)
print("2. 浮点数类型 (float)")
print("=" * 40)

pi = 3.14159
e = 2.718
negative = -0.5

print("pi =", pi, "类型：", type(pi))
print("e =", e, "类型：", type(e))
print("negative =", negative, "类型：", type(negative))

print("-" * 40)

print("科学计数法：")
big_float = 1.5e10
small_float = 2.5e-3
print("1.5e10 =", big_float)
print("2.5e-3 =", small_float)

print()
print("=" * 40)
print("3. 字符串类型 (str)")
print("=" * 40)

str1 = "Hello"
str2 = 'World'
str3 = """多行
字符串"""

print("str1 =", str1, "类型：", type(str1))
print("str2 =", str2, "类型：", type(str2))
print("str3 =", str3)

print("-" * 40)

print("字符串操作：")
s = "Python"
print("s =", s)
print("s[0] =", s[0])
print("s[-1] =", s[-1])
print("s[0:3] =", s[0:3])
print("len(s) =", len(s))

print()
print("=" * 40)
print("4. 布尔类型 (bool)")
print("=" * 40)

flag1 = True
flag2 = False

print("flag1 =", flag1, "类型：", type(flag1))
print("flag2 =", flag2, "类型：", type(flag2))

print("-" * 40)

print("布尔值常用于条件判断：")
print("True and False =", True and False)
print("True or False =", True or False)
print("not True =", not True)

print()
print("=" * 40)
print("5. 类型转换")
print("=" * 40)

print("字符串转数字：")
s1 = "123"
n1 = int(s1)
f1 = float(s1)
print("int('123') =", n1, "类型：", type(n1))
print("float('123') =", f1, "类型：", type(f1))

print("-" * 40)

print("数字转字符串：")
n2 = 456
s2 = str(n2)
print("str(456) =", s2, "类型：", type(s2))

print("-" * 40)

print("其他转换：")
print("int(3.9) =", int(3.9))
print("float(10) =", float(10))
print("bool(1) =", bool(1))
print("bool(0) =", bool(0))
print("bool('') =", bool(""))
print("bool('hello') =", bool("hello"))
