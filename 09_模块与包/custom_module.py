"""
自定义模块示例
=============

这个文件可以作为模块被其他文件导入使用。
"""

PI = 3.14159
VERSION = "1.0.0"

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def circle_area(radius):
    return PI * radius * radius

def circle_circumference(radius):
    return 2 * PI * radius

def main():
    print("这是一个自定义模块")
    print(f"PI = {PI}")
    print(f"add(3, 5) = {add(3, 5)}")
    print(f"circle_area(5) = {circle_area(5):.2f}")

if __name__ == "__main__":
    main()
