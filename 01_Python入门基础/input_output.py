"""
输入输出示例
============

input() 函数用于获取用户输入
print() 函数用于输出内容

注意：input() 返回的永远是字符串类型！
"""

print("=" * 40)
print("输入输出示例")
print("=" * 40)

name = input("请输入你的名字：")
print("你好，" + name + "！")

print("-" * 40)

age = input("请输入你的年龄：")
print("你的年龄是：" + age + "岁")

print("-" * 40)

print("注意：input() 返回的是字符串")
print("age 的类型是：", type(age))

print("-" * 40)

print("如果需要数字运算，需要转换类型：")
num1 = input("请输入第一个数字：")
num2 = input("请输入第二个数字：")

result = int(num1) + int(num2)
print("两个数字的和是：" + str(result))

print("-" * 40)

print("更简洁的写法：")
num1 = int(input("请输入第一个数字："))
num2 = int(input("请输入第二个数字："))
print(f"两个数字的和是：{num1 + num2}")
