"""
多异常处理
==========

处理多种类型的异常。
使用不同的 except 块处理不同错误。
"""

print("=" * 40)
print("1. 多个 except 块")
print("=" * 40)

def process_data(data, index):
    try:
        item = data[index]
        result = int(item)
        return result * 2
    except IndexError:
        print(f"  索引 {index} 超出范围")
    except ValueError:
        print(f"  '{item}' 无法转换为整数")
    return None

print("测试不同的错误:")
print(f"  process_data(['1', '2', '3'], 1) = {process_data(['1', '2', '3'], 1)}")
print(f"  process_data(['1', 'abc', '3'], 1) = {process_data(['1', 'abc', '3'], 1)}")
print(f"  process_data(['1', '2', '3'], 5) = {process_data(['1', '2', '3'], 5)}")

print()
print("=" * 40)
print("2. 捕获多种异常类型")
print("=" * 40)

def safe_operation(a, b, op):
    try:
        if op == "add":
            return a + b
        elif op == "div":
            return a / b
        elif op == "index":
            return a[b]
        else:
            raise ValueError(f"未知操作: {op}")
    except (ZeroDivisionError, TypeError, IndexError) as e:
        print(f"  操作失败: {type(e).__name__} - {e}")
        return None

print("测试多种异常:")
safe_operation(10, 0, "div")
safe_operation("hello", 3, "add")
safe_operation([1, 2], 10, "index")

print()
print("=" * 40)
print("3. 捕获所有异常")
print("=" * 40)

def catch_all(func):
    try:
        return func()
    except Exception as e:
        print(f"  发生异常: {type(e).__name__}: {e}")
        return None

print("捕获所有异常:")
catch_all(lambda: 10 / 0)
catch_all(lambda: int("abc"))
catch_all(lambda: [1, 2, 3][10])

print()
print("注意: 捕获所有异常可能隐藏问题，谨慎使用")

print()
print("=" * 40)
print("4. 异常处理顺序")
print("=" * 40)

print("异常处理按顺序匹配，子类异常应放在前面:")

try:
    raise ValueError("这是一个值错误")
except ValueError:
    print("  ValueError 被捕获")
except Exception:
    print("  Exception 被捕获")

print("-" * 40)

print("错误示例（ValueError 永远不会被捕获）:")
print("try:")
print("    raise ValueError()")
print("except Exception:  # 先捕获了父类")
print("    print('Exception')")
print("except ValueError:  # 永远不会执行")
print("    print('ValueError')")

print()
print("=" * 40)
print("5. 重新抛出异常")
print("=" * 40)

def validate_age(age):
    try:
        age = int(age)
        if age < 0:
            raise ValueError("年龄不能为负数")
        if age > 150:
            raise ValueError("年龄不合理")
        return age
    except ValueError:
        print("  年龄验证失败")
        raise

print("测试重新抛出:")
try:
    validate_age("abc")
except ValueError as e:
    print(f"  外层捕获: {e}")

print()
print("=" * 40)
print("6. 嵌套异常处理")
print("=" * 40)

def nested_handling():
    try:
        print("  外层 try")
        try:
            print("  内层 try")
            result = 10 / 0
        except ZeroDivisionError:
            print("  内层捕获 ZeroDivisionError")
            raise TypeError("转换错误类型")
    except TypeError as e:
        print(f"  外层捕获: {e}")

nested_handling()

print()
print("=" * 40)
print("7. 实际应用：文件操作")
print("=" * 40)

def read_config(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"  配置文件不存在: {filename}")
    except PermissionError:
        print(f"  无权限读取: {filename}")
    except UnicodeDecodeError:
        print(f"  文件编码错误: {filename}")
    except Exception as e:
        print(f"  未知错误: {e}")
    return None

print("尝试读取不存在的文件:")
read_config("nonexistent_config.txt")

print()
print("=" * 40)
print("8. 异常处理最佳实践")
print("=" * 40)

print("1. 只捕获你能处理的异常")
print("2. 不要使用空的 except 块")
print("3. 记录异常信息")
print("4. 使用具体的异常类型")
print("5. 在适当的地方处理异常")

print("-" * 40)

print("不好的做法:")
print("try:")
print("    do_something()")
print("except:  # 太宽泛")
print("    pass  # 静默忽略")

print()
print("好的做法:")
print("try:")
print("    do_something()")
print("except ValueError as e:")
print("    logger.error(f'处理失败: {e}')")
print("    raise")
