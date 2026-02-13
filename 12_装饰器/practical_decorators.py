"""
实用装饰器示例
=============
"""

import time
from functools import wraps

print("=" * 40)
print("1. 计时装饰器")
print("=" * 40)

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行耗时: {end - start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "完成"

slow_function()

print()
print("=" * 40)
print("2. 日志装饰器")
print("=" * 40)

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用函数: {func.__name__}")
        print(f"[LOG] 参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] 返回值: {result}")
        return result
    return wrapper

@log
def divide(a, b):
    return a / b

divide(10, 2)

print()
print("=" * 40)
print("3. 缓存装饰器")
print("=" * 40)

def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"从缓存获取: {args}")
            return cache[args]
        print(f"计算并缓存: {args}")
        result = func(*args)
        cache[args] = result
        return result
    
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("计算 fibonacci(5):")
print(f"结果: {fibonacci(5)}")

print()
print("=" * 40)
print("4. 重试装饰器")
print("=" * 40)

def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第 {attempt + 1} 次尝试失败: {e}")
                    if attempt == max_attempts - 1:
                        print("所有尝试均失败")
                        raise
            return None
        return wrapper
    return decorator

import random

@retry(3)
def unstable_function():
    if random.random() < 0.7:
        raise ValueError("随机失败")
    return "成功！"

try:
    result = unstable_function()
    print(f"最终结果: {result}")
except Exception as e:
    print(f"最终异常: {e}")

print()
print("=" * 40)
print("5. 权限验证装饰器")
print("=" * 40)

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get('user', {'is_admin': False})
        if not user.get('is_admin', False):
            print("权限不足：需要管理员权限")
            return None
        return func(*args, **kwargs)
    return wrapper

@require_auth
def delete_database(user):
    print("数据库已删除")
    return True

print("普通用户尝试:")
delete_database(user={'is_admin': False})

print()
print("管理员尝试:")
delete_database(user={'is_admin': True})

print()
print("=" * 40)
print("6. 类型检查装饰器")
print("=" * 40)

def validate_types(**types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for param, value in kwargs.items():
                if param in types and not isinstance(value, types[param]):
                    raise TypeError(f"参数 {param} 应该是 {types[param]} 类型，实际是 {type(value)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_user(name, age):
    return {"name": name, "age": age}

print("正确类型:")
user1 = create_user(name="张三", age=25)
print(f"  {user1}")

print()
print("错误类型:")
try:
    user2 = create_user(name="李四", age="二十五")
except TypeError as e:
    print(f"  错误: {e}")
