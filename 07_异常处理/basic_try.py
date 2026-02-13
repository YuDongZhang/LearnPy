"""
基本异常处理
============

使用 try/except 捕获和处理异常。
防止程序因错误而崩溃。
"""

print("=" * 40)
print("1. 没有异常处理的情况")
print("=" * 40)

print("以下代码会崩溃:")
print("print(10 / 0)  # ZeroDivisionError")

print()
print("=" * 40)
print("2. 基本异常处理")
print("=" * 40)

try:
    result = 10 / 0
except ZeroDivisionError:
    print("捕获到异常：除数不能为零")

print("程序继续执行...")

print()
print("=" * 40)
print("3. 获取异常信息")
print("=" * 40)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"异常类型: {type(e).__name__}")
    print(f"异常信息: {e}")

print()
print("=" * 40)
print("4. 常见异常类型")
print("=" * 40)

print("ValueError - 值错误:")
try:
    num = int("abc")
except ValueError as e:
    print(f"  捕获: {e}")

print()
print("TypeError - 类型错误:")
try:
    result = "hello" + 123
except TypeError as e:
    print(f"  捕获: {e}")

print()
print("IndexError - 索引越界:")
try:
    items = [1, 2, 3]
    print(items[10])
except IndexError as e:
    print(f"  捕获: {e}")

print()
print("KeyError - 键不存在:")
try:
    person = {"name": "张三"}
    print(person["age"])
except KeyError as e:
    print(f"  捕获: 键 {e} 不存在")

print()
print("=" * 40)
print("5. 使用 else 子句")
print("=" * 40)

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "除数不能为零"
    else:
        return f"结果是 {result}"

print(f"safe_divide(10, 2): {safe_divide(10, 2)}")
print(f"safe_divide(10, 0): {safe_divide(10, 0)}")

print()
print("=" * 40)
print("6. 使用 finally 子句")
print("=" * 40)

print("finally 始终执行，无论是否发生异常:")

def test_finally():
    try:
        print("  try 块执行")
        return "从 try 返回"
    finally:
        print("  finally 块执行")

result = test_finally()
print(f"  返回值: {result}")

print()
print("=" * 40)
print("7. 实际应用示例")
print("=" * 40)

def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("请输入有效的数字！")

print("模拟用户输入:")
inputs = ["abc", "12.5", "25"]
for inp in inputs:
    print(f"  输入: {inp}")
    try:
        num = int(inp)
        print(f"  转换成功: {num}")
    except ValueError:
        print(f"  转换失败: 不是有效整数")

print()
print("=" * 40)
print("8. 异常链")
print("=" * 40)

try:
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        raise RuntimeError("计算错误") from e
except RuntimeError as e:
    print(f"外层捕获: {e}")
    print(f"原始异常: {e.__cause__}")
