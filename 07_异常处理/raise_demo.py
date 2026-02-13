"""
抛出异常
========

使用 raise 语句主动抛出异常。
用于验证输入、标记错误条件等。
"""

print("=" * 40)
print("1. 基本抛出异常")
print("=" * 40)

def check_positive(n):
    if n < 0:
        raise ValueError("数值必须为正数")
    return n

print("测试抛出异常:")
try:
    check_positive(10)
    print("  10 是正数，通过")
except ValueError as e:
    print(f"  错误: {e}")

try:
    check_positive(-5)
except ValueError as e:
    print(f"  -5 检查失败: {e}")

print()
print("=" * 40)
print("2. 抛出带参数的异常")
print("=" * 40)

def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"年龄必须是整数，当前类型: {type(age).__name__}")
    if age < 0:
        raise ValueError(f"年龄不能为负数: {age}")
    if age > 150:
        raise ValueError(f"年龄不合理: {age}")
    return age

print("测试不同错误:")
test_cases = ["二十", -5, 200, 25]

for case in test_cases:
    try:
        result = set_age(case)
        print(f"  {case} -> 设置成功")
    except (TypeError, ValueError) as e:
        print(f"  {case} -> 错误: {e}")

print()
print("=" * 40)
print("3. 重新抛出异常")
print("=" * 40)

def process_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print("  文件未找到，记录日志...")
        raise

print("测试重新抛出:")
try:
    process_file("nonexistent.txt")
except FileNotFoundError:
    print("  外层处理文件不存在错误")

print()
print("=" * 40)
print("4. 异常链 (raise from)")
print("=" * 40)

def load_config(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError("配置加载失败") from e

print("测试异常链:")
try:
    load_config("config.txt")
except RuntimeError as e:
    print(f"  捕获: {e}")
    print(f"  原因: {e.__cause__}")

print()
print("=" * 40)
print("5. 条件抛出")
print("=" * 40)

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b

def calculate_average(numbers):
    if not numbers:
        raise ValueError("列表不能为空")
    return sum(numbers) / len(numbers)

print("测试条件抛出:")
try:
    divide(10, 0)
except ZeroDivisionError as e:
    print(f"  {e}")

try:
    calculate_average([])
except ValueError as e:
    print(f"  {e}")

print()
print("=" * 40)
print("6. assert 语句")
print("=" * 40)

def calculate_discount(price, discount):
    assert 0 <= discount <= 1, f"折扣必须在0-1之间: {discount}"
    return price * (1 - discount)

print("使用 assert 进行断言:")
try:
    result = calculate_discount(100, 0.2)
    print(f"  折后价格: {result}")
except AssertionError as e:
    print(f"  断言失败: {e}")

try:
    calculate_discount(100, 1.5)
except AssertionError as e:
    print(f"  断言失败: {e}")

print()
print("注意: assert 可能在优化模式下被禁用")
print("生产代码应使用 raise")

print()
print("=" * 40)
print("7. 实际应用：参数验证")
print("=" * 40)

def create_user(name, age, email):
    if not name:
        raise ValueError("用户名不能为空")
    if not isinstance(age, int) or age < 0:
        raise ValueError("年龄必须是非负整数")
    if "@" not in email:
        raise ValueError("邮箱格式不正确")
    
    return {
        "name": name,
        "age": age,
        "email": email
    }

print("创建用户:")
test_users = [
    ("张三", 25, "zhangsan@example.com"),
    ("", 25, "test@example.com"),
    ("李四", -5, "lisi@example.com"),
    ("王五", 30, "invalid-email")
]

for name, age, email in test_users:
    try:
        user = create_user(name, age, email)
        print(f"  创建成功: {user['name']}")
    except ValueError as e:
        print(f"  创建失败: {e}")

print()
print("=" * 40)
print("8. 最佳实践")
print("=" * 40)

print("1. 在有意义的地方抛出异常")
print("2. 使用描述性的错误信息")
print("3. 选择合适的异常类型")
print("4. 不要过度使用异常替代条件判断")

print("-" * 40)

print("示例：合理的异常使用")
print("def withdraw(balance, amount):")
print("    if amount > balance:")
print("        raise ValueError('余额不足')")
print("    return balance - amount")
