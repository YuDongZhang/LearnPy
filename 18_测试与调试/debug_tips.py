"""
调试技巧与工具
==============

Python 调试的多种方法和工具。
"""

print("=" * 50)
print("1. print 调试法")
print("=" * 50)

def buggy_function(x, y):
    result = x + y
    print(f"DEBUG: x = {x}, y = {y}, result = {result}")
    return result * 2

result = buggy_function(3, 5)
print(f"最终结果: {result}")

print("\nprint 调试的优点:")
print("  - 简单直观")
print("  - 适合快速定位问题")
print("\n缺点:")
print("  - 需要手动添加和删除")
print("  - 代码混乱")

print()
print("=" * 50)
print("2. logging 日志")
print("=" * 50)

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def calculate(a, b):
    logger.debug(f"输入: a={a}, b={b}")
    result = a + b
    logger.info(f"计算结果: {result}")
    return result

print("logging 优点:")
print("  - 可控制日志级别")
print("  - 可以输出到文件")
print("  - 可格式化和过滤")

print()
print("=" * 50)
print("3. pdb 交互式调试")
print("=" * 50)

print("pdb 命令:")
print("  n (next)       - 执行下一行")
print("  s (step)       - 进入函数")
print("  c (continue)   - 继续执行到断点")
print("  p var          - 打印变量值")
print("  l (list)       - 查看当前代码")
print("  q (quit)       - 退出调试")

print("\npdb 使用方式:")
print("  1. import pdb; pdb.set_trace()")
print("  2. python -m pdb script.py")

print()
print("=" * 50)
print("4. breakpoint() (Python 3.7+)")
print("=" * 50)

def calculate_sum(numbers):
    total = 0
    breakpoint()
    for n in numbers:
        total += n
    return total

print("breakpoint() 优点:")
print("  - 简单易用")
print("  - 默认调用 pdb")
print("  - 可自定义调试器 (PYTHONBREAKPOINT)")

print("\n使用方法:")
print("  breakpoint()  # 在代码中设置断点")
print("  python script.py  # 运行后会自动进入调试器")

print()
print("=" * 50)
print("5. IDE 调试器")
print("=" * 50)

print("VS Code 调试:")
print("  1. 安装 Python 扩展")
print("  2. 设置断点（点击代码行号左侧）")
print("  3. 按 F5 开始调试")
print("  4. 使用调试工具栏: 继续、单步执行、进入函数等")

print("\nPyCharm 调试:")
print("  1. 设置断点")
print("  2. 右键选择 Debug")
print("  3. 使用调试窗口查看变量")

print()
print("=" * 50)
print("6. 常见错误类型")
print("=" * 50)

errors = [
    ("SyntaxError", "语法错误", "代码拼写或格式错误"),
    ("IndentationError", "缩进错误", "缩进不一致"),
    ("NameError", "名称错误", "使用了未定义的变量"),
    ("TypeError", "类型错误", "类型不匹配的操作"),
    ("IndexError", "索引错误", "列表/元组索引越界"),
    ("KeyError", "键错误", "字典中不存在的键"),
    ("ValueError", "值错误", "传入无效的参数值"),
    ("AttributeError", "属性错误", "对象没有该属性"),
    ("IOError", "输入输出错误", "文件操作失败"),
    ("ZeroDivisionError", "除零错误", "除数为零"),
]

print("常见错误及原因:")
for err_type, name, reason in errors:
    print(f"  {err_type:20s} - {name}: {reason}")

print()
print("=" * 50)
print("7. 调试策略")
print("=" * 50)

print("二分查找法:")
print("  1. 在代码中间添加断点")
print("  2. 确定问题在前半部分还是后半部分")
print("  3. 重复直到定位到具体行")

print("\n最小复现法:")
print("  1. 简化代码，删除无关部分")
print("  2. 找到能复现问题的最小代码")
print("  3. 逐步添加代码直到发现问题")

print("\n橡皮鸭调试法:")
print("  1. 向同事或橡皮鸭解释代码")
print("  2. 详细说明每一步在做什么")
print("  3. 往往在解释过程中发现bug")

print()
print("=" * 50)
print("8. 错误堆栈分析")
print("=" * 50)

def function_c():
    return 1 / 0

def function_b():
    return function_c()

def function_a():
    return function_b()

try:
    function_a()
except ZeroDivisionError as e:
    print("错误堆栈:")
    import traceback
    traceback.print_exc()

print("\n分析堆栈:")
print("  - 最内层（最后一行）是错误发生地")
print("  - 从下往上阅读，找到问题根源")
print("  - 注意箭头指向的代码行")

print()
print("=" * 50)
print("9. 调试工具推荐")
print("=" * 50)

tools = [
    ("pdb", "Python 内置交互式调试器"),
    ("ipdb", "增强版 pdb，支持 IPython"),
    ("pudb", "全屏 curses 界面调试器"),
    ("pytest", "测试框架内置调试功能"),
    ("sentry", "线上错误监控和追踪"),
    ("pyrasite", "运行时注入代码到进程"),
]

print("调试工具:")
for tool, desc in tools:
    print(f"  {tool:15s} - {desc}")

print()
print("=" * 50)
print("10. 良好调试习惯")
print("=" * 50)

habits = [
    "先读错误信息，理解问题再动手",
    "使用版本控制，方便回退",
    "每次只修改一个变量",
    "修改后立即测试",
    "记录调试过程，避免重复工作",
    "完成后清理调试代码",
]

print("调试习惯:")
for i, habit in enumerate(habits, 1):
    print(f"  {i}. {habit}")
