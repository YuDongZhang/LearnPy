"""
列表详解
========

列表是有序、可变的集合。
使用方括号 [] 创建列表。
"""

print("=" * 40)
print("1. 创建列表")
print("=" * 40)

fruits = ["苹果", "香蕉", "橙子"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []

print(f"fruits = {fruits}")
print(f"numbers = {numbers}")
print(f"mixed = {mixed}")
print(f"empty = {empty}")

print()
print("=" * 40)
print("2. 访问元素")
print("=" * 40)

fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]

print(f"fruits = {fruits}")
print(f"fruits[0] = {fruits[0]}")
print(f"fruits[2] = {fruits[2]}")
print(f"fruits[-1] = {fruits[-1]}")
print(f"fruits[-2] = {fruits[-2]}")

print("-" * 40)

print("切片操作:")
print(f"fruits[1:3] = {fruits[1:3]}")
print(f"fruits[:3] = {fruits[:3]}")
print(f"fruits[2:] = {fruits[2:]}")
print(f"fruits[::2] = {fruits[::2]}")
print(f"fruits[::-1] = {fruits[::-1]}")

print()
print("=" * 40)
print("3. 修改元素")
print("=" * 40)

numbers = [1, 2, 3, 4, 5]
print(f"原始列表: {numbers}")

numbers[0] = 10
print(f"修改第一个元素: {numbers}")

numbers[1:3] = [20, 30]
print(f"修改多个元素: {numbers}")

print()
print("=" * 40)
print("4. 添加元素")
print("=" * 40)

fruits = ["苹果", "香蕉"]
print(f"原始列表: {fruits}")

fruits.append("橙子")
print(f"append('橙子'): {fruits}")

fruits.insert(1, "葡萄")
print(f"insert(1, '葡萄'): {fruits}")

more_fruits = ["西瓜", "草莓"]
fruits.extend(more_fruits)
print(f"extend(['西瓜', '草莓']): {fruits}")

print()
print("=" * 40)
print("5. 删除元素")
print("=" * 40)

numbers = [1, 2, 3, 4, 5, 3, 6]
print(f"原始列表: {numbers}")

del numbers[0]
print(f"del numbers[0]: {numbers}")

removed = numbers.pop()
print(f"pop() 移除的元素: {removed}, 结果: {numbers}")

removed = numbers.pop(1)
print(f"pop(1) 移除的元素: {removed}, 结果: {numbers}")

numbers.remove(3)
print(f"remove(3) 移除第一个3: {numbers}")

print()
print("=" * 40)
print("6. 查找和统计")
print("=" * 40)

numbers = [1, 2, 3, 4, 3, 5, 3]
print(f"numbers = {numbers}")

print(f"index(3) = {numbers.index(3)}")
print(f"count(3) = {numbers.count(3)}")
print(f"3 in numbers = {3 in numbers}")
print(f"10 in numbers = {10 in numbers}")

print()
print("=" * 40)
print("7. 排序和反转")
print("=" * 40)

numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"原始列表: {numbers}")

numbers.sort()
print(f"sort() 升序: {numbers}")

numbers.sort(reverse=True)
print(f"sort(reverse=True) 降序: {numbers}")

numbers.reverse()
print(f"reverse() 反转: {numbers}")

print("-" * 40)

numbers = [3, 1, 4, 1, 5]
sorted_list = sorted(numbers)
print(f"sorted() 返回新列表: {sorted_list}")
print(f"原列表不变: {numbers}")

print()
print("=" * 40)
print("8. 其他常用操作")
print("=" * 40)

numbers = [1, 2, 3, 4, 5]
print(f"numbers = {numbers}")

print(f"len(numbers) = {len(numbers)}")
print(f"sum(numbers) = {sum(numbers)}")
print(f"min(numbers) = {min(numbers)}")
print(f"max(numbers) = {max(numbers)}")

print("-" * 40)

numbers.clear()
print(f"clear() 清空列表: {numbers}")

numbers = [1, 2, 3]
numbers_copy = numbers.copy()
print(f"copy() 复制列表: {numbers_copy}")

print()
print("=" * 40)
print("9. 列表推导式")
print("=" * 40)

squares = [x ** 2 for x in range(1, 6)]
print(f"1-5的平方: {squares}")

evens = [x for x in range(1, 11) if x % 2 == 0]
print(f"1-10的偶数: {evens}")

words = ["hello", "world", "python"]
upper_words = [w.upper() for w in words]
print(f"转大写: {upper_words}")

print()
print("=" * 40)
print("10. 实际应用示例")
print("=" * 40)

print("学生成绩管理:")
scores = [85, 92, 78, 95, 88]

print(f"成绩列表: {scores}")
print(f"平均分: {sum(scores) / len(scores):.1f}")
print(f"最高分: {max(scores)}")
print(f"最低分: {min(scores)}")

scores.sort(reverse=True)
print(f"排名: {scores}")

print("-" * 40)

print("购物清单:")
shopping_list = []

shopping_list.append("牛奶")
shopping_list.append("面包")
shopping_list.append("鸡蛋")
print(f"购物清单: {shopping_list}")

shopping_list.remove("面包")
print(f"买了面包后: {shopping_list}")

shopping_list.append("苹果")
print(f"添加苹果: {shopping_list}")
