"""
变量定义与使用
==============

变量是存储数据的容器。
Python 中定义变量不需要声明类型，直接赋值即可。
"""

print("=" * 40)
print("变量定义示例")
print("=" * 40)

name = "Python"
age = 30
price = 3.14
is_active = True

print("name =", name)
print("age =", age)
print("price =", price)
print("is_active =", is_active)

print("-" * 40)

print("查看变量类型：")
print("name 的类型是：", type(name))
print("age 的类型是：", type(age))
print("price 的类型是：", type(price))
print("is_active 的类型是：", type(is_active))

print("-" * 40)

print("变量可以重新赋值：")
x = 10
print("x =", x, "类型：", type(x))

x = "hello"
print("x =", x, "类型：", type(x))

print("-" * 40)

print("多个变量赋值：")
a = b = c = 100
print("a =", a, "b =", b, "c =", c)

x, y, z = 1, 2, 3
print("x =", x, "y =", y, "z =", z)

print("-" * 40)

print("变量命名规则：")
my_name = "张三"
myAge = 20
_private = "私有变量"

print("my_name =", my_name)
print("myAge =", myAge)
print("_private =", _private)

print("-" * 40)

print("命名错误示例（这些会报错）：")
print("1name = 1  # 不能以数字开头")
print("my-name = 1  # 不能包含连字符")
print("class = 1  # 不能使用关键字")
