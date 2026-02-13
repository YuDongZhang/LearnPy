"""
装饰器基础
=========
"""

print("=" * 40)
print("1. 函数作为参数")
print("=" * 40)

def greet():
    return "你好！"

def call_func(func):
    print(f"调用函数: {func.__name__}")
    return func()

result = call_func(greet)
print(f"结果: {result}")

print()
print("=" * 40)
print("2. 函数作为返回值")
print("=" * 40)

def get_greeting(name):
    def greet():
        return f"你好，{name}！"
    return greet

greet_zhangsan = get_greeting("张三")
print(f"返回的函数: {greet_zhangsan}")
print(f"调用结果: {greet_zhangsan()}")

print()
print("=" * 40)
print("3. 简单装饰器")
print("=" * 40)

def my_decorator(func):
    def wrapper():
        print("=== 函数执行前 ===")
        func()
        print("=== 函数执行后 ===")
    return wrapper

@my_decorator
def say_hello():
    print("你好，Python！")

say_hello()

print()
print("=" * 40)
print("4. 装饰器语法糖的本质")
print("=" * 40)

def my_decorator(func):
    def wrapper():
        print("执行前")
        func()
        print("执行后")
    return wrapper

def say_hello():
    print("你好！")

print("@语法糖等价于手动赋值:")
say_hello = my_decorator(say_hello)
say_hello()

print()
print("=" * 40)
print("5. 处理函数参数")
print("=" * 40)

def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}，参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回: {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

@log_call
def greet(name, greeting="你好"):
    return f"{greeting}，{name}！"

add(3, 5)
greet("张三")
greet("李四", greeting="早上好")

print()
print("=" * 40)
print("6. 保留函数元信息")
print("=" * 40)

from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example():
    """这是一个示例函数"""
    pass

print(f"函数名: {example.__name__}")
print(f"文档字符串: {example.__doc__}")

print()
print("=" * 40)
print("7. 多个装饰器叠加")
print("=" * 40)

def decorator_a(func):
    def wrapper():
        print("A - 前")
        func()
        print("A - 后")
    return wrapper

def decorator_b(func):
    def wrapper():
        print("B - 前")
        func()
        print("B - 后")
    return wrapper

@decorator_a
@decorator_b
def say_hello():
    print("你好！")

print("装饰器执行顺序（从外到内）:")
say_hello()
