"""
函数基础
========

函数是一段可重复使用的代码块。
使用 def 关键字定义函数。
"""

print("=" * 40)
print("1. 定义和调用函数")
print("=" * 40)

def say_hello():
    print("你好！")

print("调用函数:")
say_hello()
say_hello()

print("-" * 40)

def greet(name):
    print(f"你好，{name}！")

print("带参数的函数:")
greet("张三")
greet("李四")

print()
print("=" * 40)
print("2. 函数文档字符串")
print("=" * 40)

def calculate_area(width, height):
    """
    计算矩形面积
    
    参数:
        width: 宽度
        height: 高度
    
    返回:
        面积
    """
    return width * height

print("查看函数文档:")
print(calculate_area.__doc__)

print("-" * 40)

area = calculate_area(5, 3)
print(f"矩形面积: {area}")

print()
print("=" * 40)
print("3. 空函数")
print("=" * 40)

def do_nothing():
    pass

print("空函数使用 pass 占位")
do_nothing()
print("执行完毕")

print()
print("=" * 40)
print("4. 函数作为对象")
print("=" * 40)

def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

print("函数可以赋值给变量:")
func = shout
print(func("hello"))

func = whisper
print(func("HELLO"))

print("-" * 40)

print("函数可以作为参数:")
def apply_func(func, text):
    return func(text)

print(apply_func(shout, "hello"))
print(apply_func(whisper, "HELLO"))

print()
print("=" * 40)
print("5. 函数命名规范")
print("=" * 40)

print("函数名应该:")
print("- 使用小写字母")
print("- 单词之间用下划线分隔")
print("- 名称要有意义，描述函数的功能")

print("-" * 40)

print("好的命名示例:")
print("  calculate_area()")
print("  get_user_info()")
print("  is_valid_email()")

print()
print("不好的命名示例:")
print("  ca()  # 太短，不清楚")
print("  CalculateArea()  # 不推荐驼峰命名")
print("  func1()  # 没有意义")
