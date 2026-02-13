"""
使用自定义模块
=============

演示如何导入和使用自定义模块。
"""

from custom_module import add, subtract, PI, circle_area

print("=" * 40)
print("使用自定义模块")
print("=" * 40)

print(f"PI = {PI}")
print(f"add(10, 20) = {add(10, 20)}")
print(f"subtract(10, 3) = {subtract(10, 3)}")
print(f"circle_area(3) = {circle_area(3):.2f}")

print()
print("=" * 40)
print("导入整个模块")
print("=" * 40)

import custom_module as cm

print(f"cm.VERSION = {cm.VERSION}")
print(f"cm.multiply(4, 5) = {cm.multiply(4, 5)}")
print(f"cm.divide(10, 2) = {cm.divide(10, 2)}")
