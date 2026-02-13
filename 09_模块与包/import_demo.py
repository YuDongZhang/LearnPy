"""
导入模块示例
============
"""

print("=" * 40)
print("1. 导入整个模块")
print("=" * 40)

import math

print(f"math.sqrt(16) = {math.sqrt(16)}")
print(f"math.pi = {math.pi}")
print(f"math.ceil(3.2) = {math.ceil(3.2)}")
print(f"math.floor(3.8) = {math.floor(3.8)}")

print()
print("=" * 40)
print("2. 导入特定函数")
print("=" * 40)

from math import sqrt, pi, pow

print(f"sqrt(25) = {sqrt(25)}")
print(f"pi = {pi}")
print(f"pow(2, 3) = {pow(2, 3)}")

print()
print("=" * 40)
print("3. 使用别名")
print("=" * 40)

import math as m
from math import factorial as fact

print(f"m.sqrt(9) = {m.sqrt(9)}")
print(f"fact(5) = {fact(5)}")

print()
print("=" * 40)
print("4. 导入所有内容（不推荐）")
print("=" * 40)

from math import *

print(f"sin(0) = {sin(0)}")
print(f"cos(0) = {cos(0)}")

print()
print("=" * 40)
print("5. random 模块")
print("=" * 40)

import random

print(f"random.random() = {random.random()}")
print(f"random.randint(1, 10) = {random.randint(1, 10)}")
print(f"random.choice([1, 2, 3, 4, 5]) = {random.choice([1, 2, 3, 4, 5])}")

numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"random.shuffle([1,2,3,4,5]) = {numbers}")

print()
print("=" * 40)
print("6. datetime 模块")
print("=" * 40)

from datetime import datetime, date, timedelta

now = datetime.now()
print(f"当前时间: {now}")
print(f"格式化: {now.strftime('%Y-%m-%d %H:%M:%S')}")

today = date.today()
print(f"今天日期: {today}")

tomorrow = today + timedelta(days=1)
print(f"明天日期: {tomorrow}")

print()
print("=" * 40)
print("7. os 模块")
print("=" * 40)

import os

print(f"当前目录: {os.getcwd()}")
print(f"环境变量 PATH 存在: {'PATH' in os.environ}")

print()
print("=" * 40)
print("8. sys 模块")
print("=" * 40)

import sys

print(f"Python 版本: {sys.version}")
print(f"模块搜索路径数量: {len(sys.path)}")
