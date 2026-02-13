"""
高级装饰器
=========
"""

from functools import wraps

print("=" * 40)
print("1. 带参数的装饰器")
print("=" * 40)

def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(n):
                print(f"第 {i + 1} 次执行")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f"你好，{name}！")

say_hello("张三")

print()
print("=" * 40)
print("2. 类装饰器")
print("=" * 40)

class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("你好！")

say_hello()
say_hello()
say_hello()

print()
print("=" * 40)
print("3. 类方法装饰器")
print("=" * 40)

def log_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"调用 {self.__class__.__name__}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class Person:
    def __init__(self, name):
        self.name = name
    
    @log_method
    def say_hello(self):
        print(f"你好，我是{self.name}")
    
    @log_method
    def get_name(self):
        return self.name

p = Person("张三")
p.say_hello()
print(f"名字: {p.get_name()}")

print()
print("=" * 40)
print("4. 装饰器工厂")
print("=" * 40)

def create_decorator(before=None, after=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if before:
                before(func.__name__, *args, **kwargs)
            result = func(*args, **kwargs)
            if after:
                after(func.__name__, result)
            return result
        return wrapper
    return decorator

def log_before(name, *args, **kwargs):
    print(f"[前] 调用 {name}")

def log_after(name, result):
    print(f"[后] {name} 返回 {result}")

@create_decorator(before=log_before, after=log_after)
def add(a, b):
    return a + b

add(3, 5)

print()
print("=" * 40)
print("5. 上下文管理装饰器")
print("=" * 40)

from contextlib import contextmanager

@contextmanager
def timer_context(name):
    import time
    start = time.time()
    print(f"[{name}] 开始")
    yield
    end = time.time()
    print(f"[{name}] 结束，耗时: {end - start:.4f} 秒")

print("使用上下文管理器:")
with timer_context("处理任务"):
    import time
    time.sleep(0.3)
    print("正在处理...")

print()
print("=" * 40)
print("6. 属性装饰器")
print("=" * 40)

class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value
    
    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self):
        import math
        return 2 * math.pi * self._radius

c = Circle(5)
print(f"半径: {c.radius}")
print(f"面积: {c.area:.2f}")
print(f"周长: {c.circumference:.2f}")

c.radius = 10
print(f"新半径: {c.radius}")
print(f"新面积: {c.area:.2f}")

print()
print("=" * 40)
print("7. 静态方法和类方法装饰器")
print("=" * 40)

class MathUtils:
    PI = 3.14159
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @classmethod
    def circle_area(cls, radius):
        return cls.PI * radius ** 2

print(f"静态方法: MathUtils.add(3, 5) = {MathUtils.add(3, 5)}")
print(f"类方法: MathUtils.circle_area(5) = {MathUtils.circle_area(5):.2f}")
