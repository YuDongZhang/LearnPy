"""
while 循环示例
==============

while 循环在条件为真时重复执行代码块。
"""

print("=" * 40)
print("1. 基本while循环")
print("=" * 40)

count = 0

print("从0数到4:")
while count < 5:
    print(f"  count = {count}")
    count += 1

print("-" * 40)

num = 1

print("计算1到5的累加:")
total = 0
while num <= 5:
    total += num
    print(f"  加上{num}，当前总和: {total}")
    num += 1

print(f"最终结果: {total}")

print()
print("=" * 40)
print("2. while循环与用户输入")
print("=" * 40)

print("模拟密码验证（演示用，不实际输入）:")
password = ""
correct_password = "123456"
attempts = 0
max_attempts = 3

print(f"正确密码: {correct_password}")
print(f"最多尝试次数: {max_attempts}")

print()
print("=" * 40)
print("3. 无限循环")
print("=" * 40)

print("使用while True创建无限循环:")
print("while True:")
print("    # 需要用break跳出")
print("    break")

print("-" * 40)

print("示例：模拟简单菜单")
choice = ""
demo_choices = ["1", "2", "3", "q"]
choice_index = 0

while True:
    print("\n--- 菜单 ---")
    print("1. 选项一")
    print("2. 选项二")
    print("3. 选项三")
    print("q. 退出")
    
    choice = demo_choices[choice_index]
    print(f"\n模拟输入: {choice}")
    
    if choice == "q":
        print("退出程序")
        break
    else:
        print(f"你选择了选项 {choice}")
        choice_index += 1

print()
print("=" * 40)
print("4. while-else")
print("=" * 40)

print("while循环正常结束时执行else:")
n = 0
while n < 3:
    print(f"  n = {n}")
    n += 1
else:
    print("  循环正常结束")

print("-" * 40)

print("while循环被break时，else不执行:")
n = 0
while n < 5:
    if n == 2:
        print(f"  在n={n}时break")
        break
    print(f"  n = {n}")
    n += 1
else:
    print("  这行不会执行")

print()
print("=" * 40)
print("5. 实际应用示例")
print("=" * 40)

print("猜数字游戏（演示版）:")
target = 7
guess = 0
attempts = 0

demo_guesses = [3, 5, 7]

while guess != target:
    guess = demo_guesses[attempts]
    attempts += 1
    print(f"  第{attempts}次猜测: {guess}")
    
    if guess < target:
        print("  太小了！")
    elif guess > target:
        print("  太大了！")
    else:
        print(f"  恭喜！猜对了！用了{attempts}次")

print()
print("=" * 40)
print("6. 注意事项")
print("=" * 40)

print("while循环常见错误：")
print("1. 忘记更新条件变量 -> 无限循环")
print("2. 条件永远为真 -> 无限循环")
print("3. 条件永远为假 -> 循环不执行")

print("-" * 40)

print("正确示例:")
i = 0
while i < 3:
    print(f"  i = {i}")
    i += 1

print("-" * 40)

print("错误示例（会无限循环）:")
print("i = 0")
print("while i < 3:")
print("    print(i)  # 忘记 i += 1")
