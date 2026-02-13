"""
返回值
======

函数使用 return 返回结果。
一个函数可以返回多个值。
"""

print("=" * 40)
print("1. 基本返回值")
print("=" * 40)

def add(a, b):
    return a + b

result = add(3, 5)
print(f"add(3, 5) = {result}")

print("-" * 40)

def is_even(n):
    return n % 2 == 0

print("判断奇偶:")
print(f"is_even(4) = {is_even(4)}")
print(f"is_even(7) = {is_even(7)}")

print()
print("=" * 40)
print("2. 没有返回值")
print("=" * 40)

def greet(name):
    print(f"你好，{name}！")

result = greet("张三")
print(f"没有return的函数返回: {result}")
print(f"类型: {type(result)}")

print()
print("=" * 40)
print("3. 多个返回值")
print("=" * 40)

def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"最小值: {minimum}, 最大值: {maximum}")

print("-" * 40)

def divide(a, b):
    if b == 0:
        return None, "除数不能为0"
    return a / b, None

result, error = divide(10, 2)
if error:
    print(f"错误: {error}")
else:
    print(f"结果: {result}")

result, error = divide(10, 0)
if error:
    print(f"错误: {error}")
else:
    print(f"结果: {result}")

print()
print("=" * 40)
print("4. 返回字典")
print("=" * 40)

def build_person(name, age, city="未知"):
    return {
        "name": name,
        "age": age,
        "city": city
    }

person = build_person("张三", 25, "北京")
print("返回的字典:")
for key, value in person.items():
    print(f"  {key}: {value}")

print()
print("=" * 40)
print("5. 返回列表")
print("=" * 40)

def get_even_numbers(max_num):
    evens = []
    for i in range(2, max_num + 1, 2):
        evens.append(i)
    return evens

even_list = get_even_numbers(10)
print(f"1-10的偶数: {even_list}")

print()
print("=" * 40)
print("6. 返回函数")
print("=" * 40)

def get_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = get_multiplier(2)
triple = get_multiplier(3)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

print()
print("=" * 40)
print("7. 提前返回")
print("=" * 40)

def check_age(age):
    if age < 0:
        return "年龄不能为负数"
    if age < 18:
        return "未成年"
    if age < 60:
        return "成年人"
    return "老年人"

print("使用提前返回简化代码:")
print(f"check_age(-5) = {check_age(-5)}")
print(f"check_age(15) = {check_age(15)}")
print(f"check_age(30) = {check_age(30)}")
print(f"check_age(70) = {check_age(70)}")

print()
print("=" * 40)
print("8. 实际应用示例")
print("=" * 40)

def calculate_circle(radius):
    """
    计算圆的周长和面积
    """
    import math
    circumference = 2 * math.pi * radius
    area = math.pi * radius ** 2
    return circumference, area

r = 5
c, a = calculate_circle(r)
print(f"半径为{r}的圆:")
print(f"  周长: {c:.2f}")
print(f"  面积: {a:.2f}")
