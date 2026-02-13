"""
函数参数详解
============

Python 函数支持多种参数类型：
- 位置参数
- 默认参数
- 关键字参数
- 可变参数
"""

print("=" * 40)
print("1. 位置参数")
print("=" * 40)

def add(a, b):
    return a + b

result = add(3, 5)
print(f"add(3, 5) = {result}")

print("-" * 40)

print("位置参数必须按顺序传递:")
def describe_person(name, age, city):
    return f"{name}, {age}岁, 来自{city}"

info = describe_person("张三", 25, "北京")
print(info)

print()
print("=" * 40)
print("2. 默认参数")
print("=" * 40)

def greet(name, greeting="你好"):
    return f"{greeting}, {name}！"

print("使用默认值:")
print(greet("张三"))

print("-" * 40)

print("覆盖默认值:")
print(greet("李四", "早上好"))

print("-" * 40)

def create_user(name, age=18, city="未知"):
    return {"name": name, "age": age, "city": city}

print("多个默认参数:")
print(create_user("张三"))
print(create_user("李四", 25))
print(create_user("王五", 30, "上海"))

print()
print("=" * 40)
print("3. 关键字参数")
print("=" * 40)

def info(name, age, city):
    print(f"姓名: {name}")
    print(f"年龄: {age}")
    print(f"城市: {city}")

print("使用关键字参数（顺序可以改变）:")
info(age=25, city="北京", name="张三")

print("-" * 40)

print("混合使用位置参数和关键字参数:")
info("李四", city="上海", age=30)

print()
print("=" * 40)
print("4. 可变位置参数 (*args)")
print("=" * 40)

def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print("传递任意数量的参数:")
print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
print(f"sum_all() = {sum_all()}")

print("-" * 40)

def print_info(name, *hobbies):
    print(f"{name}的爱好:")
    for hobby in hobbies:
        print(f"  - {hobby}")

print_info("张三", "读书", "游泳", "编程")

print()
print("=" * 40)
print("5. 可变关键字参数 (**kwargs)")
print("=" * 40)

def create_profile(**info):
    print("用户信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")

print("传递任意数量的关键字参数:")
create_profile(name="张三", age=25, city="北京", job="工程师")

print("-" * 40)

def configure(**settings):
    print("配置:")
    for key, value in settings.items():
        print(f"  {key} = {value}")

configure(debug=True, port=8080, host="localhost")

print()
print("=" * 40)
print("6. 参数组合")
print("=" * 40)

def func(a, b, c=10, *args, **kwargs):
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}")
    print(f"args = {args}")
    print(f"kwargs = {kwargs}")

print("参数顺序: 位置参数 -> 默认参数 -> *args -> **kwargs")
print("-" * 40)
func(1, 2)
print("-" * 40)
func(1, 2, 3)
print("-" * 40)
func(1, 2, 3, 4, 5)
print("-" * 40)
func(1, 2, 3, 4, 5, x=100, y=200)

print()
print("=" * 40)
print("7. 强制关键字参数")
print("=" * 40)

def person(name, *, age, city):
    print(f"{name}, {age}岁, {city}")

print("* 后面的参数必须使用关键字:")
person("张三", age=25, city="北京")
