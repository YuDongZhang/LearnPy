"""
break 和 continue 示例
======================

break: 跳出整个循环
continue: 跳过本次循环，继续下一次
"""

print("=" * 40)
print("1. break 示例")
print("=" * 40)

print("找到第一个能被7整除的数就停止:")
for i in range(1, 20):
    if i % 7 == 0:
        print(f"  找到了: {i}")
        break
    print(f"  检查 {i}...")

print("-" * 40)

print("模拟查找用户:")
users = ["张三", "李四", "王五", "赵六"]
target = "王五"

for user in users:
    print(f"  检查用户: {user}")
    if user == target:
        print(f"  找到目标用户: {user}")
        break

print()
print("=" * 40)
print("2. continue 示例")
print("=" * 40)

print("打印1-10中的奇数:")
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(f"  {i}")

print("-" * 40)

print("跳过空字符串:")
items = ["苹果", "", "香蕉", None, "橙子", ""]

for item in items:
    if not item:
        continue
    print(f"  处理: {item}")

print()
print("=" * 40)
print("3. break 和 continue 对比")
print("=" * 40)

print("使用break:")
for i in range(5):
    if i == 3:
        break
    print(f"  i = {i}")
print("  循环结束")

print("-" * 40)

print("使用continue:")
for i in range(5):
    if i == 3:
        continue
    print(f"  i = {i}")
print("  循环结束")

print()
print("=" * 40)
print("4. 在嵌套循环中使用")
print("=" * 40)

print("break只跳出内层循环:")
for i in range(3):
    print(f"外层循环 i = {i}")
    for j in range(5):
        if j == 2:
            break
        print(f"  内层循环 j = {j}")

print("-" * 40)

print("使用标志变量跳出外层循环:")
found = False
for i in range(3):
    print(f"外层循环 i = {i}")
    for j in range(5):
        if j == 2 and i == 1:
            found = True
            break
        print(f"  内层循环 j = {j}")
    if found:
        print("  跳出外层循环")
        break

print()
print("=" * 40)
print("5. 实际应用场景")
print("=" * 40)

print("场景1: 验证数据直到有效")
valid_data = [False, False, True]
index = 0

while True:
    is_valid = valid_data[index]
    print(f"  检查数据 {index}: {'有效' if is_valid else '无效'}")
    if is_valid:
        print("  数据验证通过！")
        break
    index += 1

print("-" * 40)

print("场景2: 过滤并处理数据")
numbers = [1, -2, 3, -4, 5, -6, 7]
positive_sum = 0

for num in numbers:
    if num < 0:
        continue
    positive_sum += num
    print(f"  正数 {num}，当前总和: {positive_sum}")

print(f"正数总和: {positive_sum}")

print("-" * 40)

print("场景3: 查找并提前退出")
scores = [85, 92, 78, 95, 88]
target_score = 95
found_index = -1

for i, score in enumerate(scores):
    print(f"  检查第{i+1}个分数: {score}")
    if score == target_score:
        found_index = i
        print(f"  找到目标分数 {target_score} 在位置 {i}")
        break

if found_index == -1:
    print("  未找到目标分数")

print()
print("=" * 40)
print("6. 注意事项")
print("=" * 40)

print("break 和 continue 只能用在循环中")
print("break: 完全退出循环")
print("continue: 跳过本次迭代，继续下一次")
print()
print("合理使用可以让代码更简洁高效")
