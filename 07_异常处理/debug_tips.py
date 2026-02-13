"""
调试技巧
========

Python 提供多种调试工具和技巧。
学会调试是编程的重要技能。
"""

import traceback
import sys

print("=" * 40)
print("1. 打印调试信息")
print("=" * 40)

def calculate(a, b):
    print(f"  [DEBUG] a = {a}, b = {b}")
    result = a / b
    print(f"  [DEBUG] result = {result}")
    return result

print("使用 print 调试:")
calculate(10, 2)

print()
print("=" * 40)
print("2. 使用 logging 模块")
print("=" * 40)

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def process_data(data):
    logging.debug(f"处理数据: {data}")
    result = sum(data) / len(data)
    logging.info(f"计算结果: {result}")
    return result

print("使用 logging:")
process_data([1, 2, 3, 4, 5])

print()
print("=" * 40)
print("3. 获取异常堆栈")
print("=" * 40)

def func_c():
    raise ValueError("在 func_c 中出错")

def func_b():
    func_c()

def func_a():
    func_b()

print("获取完整堆栈信息:")
try:
    func_a()
except ValueError:
    print("  堆栈追踪:")
    traceback.print_exc()

print()
print("=" * 40)
print("4. 使用 traceback 获取堆栈字符串")
print("=" * 40)

try:
    func_a()
except ValueError:
    tb_str = traceback.format_exc()
    print("  堆栈字符串:")
    print(tb_str)

print()
print("=" * 40)
print("5. 获取异常详情")
print("=" * 40)

try:
    func_a()
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"  异常类型: {exc_type.__name__}")
    print(f"  异常值: {exc_value}")
    print(f"  追踪对象: {exc_traceback}")

print()
print("=" * 40)
print("6. 使用 pdb 调试器")
print("=" * 40)

print("pdb 常用命令:")
print("  n (next) - 执行下一行")
print("  s (step) - 进入函数")
print("  c (continue) - 继续执行")
print("  p 变量名 - 打印变量值")
print("  l (list) - 显示代码")
print("  q (quit) - 退出调试")

print("-" * 40)

print("使用方法:")
print("  import pdb; pdb.set_trace()  # 设置断点")
print("  breakpoint()  # Python 3.7+ 推荐方式")

print()
print("=" * 40)
print("7. 使用 breakpoint() (Python 3.7+)")
print("=" * 40)

def debug_example():
    x = 10
    y = 20
    z = x + y
    return z

print("在代码中添加断点:")
print("def debug_example():")
print("    x = 10")
print("    breakpoint()  # 程序会在此暂停")
print("    y = 20")
print("    return x + y")

print()
print("=" * 40)
print("8. 使用 assert 调试")
print("=" * 40)

def calculate_average(numbers):
    assert len(numbers) > 0, "列表不能为空"
    return sum(numbers) / len(numbers)

print("使用 assert 检查条件:")
try:
    calculate_average([])
except AssertionError as e:
    print(f"  断言失败: {e}")

print()
print("=" * 40)
print("9. 使用 vars() 和 dir()")
print("=" * 40)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("张三", 25)

print("vars() - 查看对象属性:")
print(f"  vars(p) = {vars(p)}")

print()
print("dir() - 查看所有属性和方法:")
print(f"  dir(p) = {[x for x in dir(p) if not x.startswith('_')]}")

print()
print("=" * 40)
print("10. 调试技巧总结")
print("=" * 40)

print("常用调试方法:")
print("1. print() - 最简单直接")
print("2. logging - 生产环境推荐")
print("3. pdb/breakpoint() - 交互式调试")
print("4. traceback - 查看错误堆栈")
print("5. assert - 检查假设条件")
print("6. IDE 调试器 - 断点、变量监视")

print("-" * 40)

print("调试流程:")
print("1. 复现问题")
print("2. 定位问题位置")
print("3. 分析原因")
print("4. 修复并验证")
print("5. 添加测试防止回归")
