"""
列表推导式示例
=============
"""

print("=" * 40)
print("1. 基本列表推导式")
print("=" * 40)

squares = [x**2 for x in range(5)]
print(f"平方数: {squares}")

doubles = [x * 2 for x in range(5)]
print(f"两倍数: {doubles}")

words = ["hello", "world", "python"]
upper_words = [word.upper() for word in words]
print(f"大写: {upper_words}")

print()
print("=" * 40)
print("2. 带条件的列表推导式")
print("=" * 40)

evens = [x for x in range(10) if x % 2 == 0]
print(f"偶数: {evens}")

odds = [x for x in range(10) if x % 2 != 0]
print(f"奇数: {odds}")

positive = [x for x in [-3, -1, 0, 2, 5, -4] if x > 0]
print(f"正数: {positive}")

print()
print("=" * 40)
print("3. 带 if-else 的列表推导式")
print("=" * 40)

labels = ["偶数" if x % 2 == 0 else "奇数" for x in range(5)]
print(f"标签: {labels}")

abs_values = [x if x >= 0 else -x for x in [-3, 2, -1, 5, -4]]
print(f"绝对值: {abs_values}")

print()
print("=" * 40)
print("4. 嵌套列表推导式")
print("=" * 40)

matrix = [[j for j in range(3)] for i in range(3)]
print(f"矩阵: {matrix}")

flat = [x for row in matrix for x in row]
print(f"展平: {flat}")

pairs = [(x, y) for x in range(3) for y in range(3)]
print(f"坐标对: {pairs}")

print()
print("=" * 40)
print("5. 实际应用示例")
print("=" * 40)

words = ["Python", "is", "awesome", "and", "powerful"]
long_words = [word for word in words if len(word) > 5]
print(f"长单词(>5字符): {long_words}")

word_lengths = [len(word) for word in words]
print(f"单词长度: {word_lengths}")

scores = [85, 92, 78, 90, 65, 88]
passed = [score for score in scores if score >= 60]
print(f"及格分数: {passed}")

grades = ["优秀" if s >= 90 else "良好" if s >= 80 else "及格" if s >= 60 else "不及格" for s in scores]
print(f"等级: {grades}")

print()
print("=" * 40)
print("6. 性能对比")
print("=" * 40)

import time

start = time.time()
result1 = []
for i in range(100000):
    result1.append(i ** 2)
time1 = time.time() - start

start = time.time()
result2 = [i ** 2 for i in range(100000)]
time2 = time.time() - start

print(f"for 循环耗时: {time1:.4f} 秒")
print(f"列表推导式耗时: {time2:.4f} 秒")
print(f"列表推导式更快: {time1 > time2}")
