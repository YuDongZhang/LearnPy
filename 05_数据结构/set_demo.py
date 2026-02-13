"""
集合详解
========

集合是无序、不重复元素的集合。
使用花括号 {} 或 set() 创建集合。
"""

print("=" * 40)
print("1. 创建集合")
print("=" * 40)

numbers = {1, 2, 3, 4, 5}
fruits = {"苹果", "香蕉", "橙子"}
empty = set()

print(f"numbers = {numbers}")
print(f"fruits = {fruits}")
print(f"empty = {empty}")

print("-" * 40)

print("从列表创建集合（自动去重）:")
numbers = set([1, 2, 2, 3, 3, 3, 4])
print(f"set([1, 2, 2, 3, 3, 3, 4]) = {numbers}")

print("-" * 40)

print("从字符串创建集合:")
chars = set("hello")
print(f"set('hello') = {chars}")

print()
print("=" * 40)
print("2. 集合特点")
print("=" * 40)

print("1. 无序 - 不能通过索引访问")
print("2. 不重复 - 自动去重")
print("3. 元素必须是不可变类型")

print("-" * 40)

print("自动去重:")
s = {1, 2, 2, 3, 3, 3}
print(f"{1, 2, 2, 3, 3, 3} = {s}")

print()
print("=" * 40)
print("3. 添加元素")
print("=" * 40)

fruits = {"苹果", "香蕉"}
print(f"原始: {fruits}")

fruits.add("橙子")
print(f"add('橙子'): {fruits}")

fruits.add("苹果")
print(f"add('苹果') (重复不添加): {fruits}")

print()
print("=" * 40)
print("4. 删除元素")
print("=" * 40)

numbers = {1, 2, 3, 4, 5}
print(f"原始: {numbers}")

numbers.remove(3)
print(f"remove(3): {numbers}")

numbers.discard(10)
print(f"discard(10) (不存在不报错): {numbers}")

removed = numbers.pop()
print(f"pop() 移除: {removed}, 结果: {numbers}")

numbers.clear()
print(f"clear(): {numbers}")

print()
print("=" * 40)
print("5. 集合运算")
print("=" * 40)

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(f"a = {a}")
print(f"b = {b}")

print("-" * 40)

print("并集 (| 或 union):")
print(f"a | b = {a | b}")
print(f"a.union(b) = {a.union(b)}")

print("-" * 40)

print("交集 (& 或 intersection):")
print(f"a & b = {a & b}")
print(f"a.intersection(b) = {a.intersection(b)}")

print("-" * 40)

print("差集 (- 或 difference):")
print(f"a - b = {a - b}")
print(f"a.difference(b) = {a.difference(b)}")

print("-" * 40)

print("对称差集 (^ 或 symmetric_difference):")
print(f"a ^ b = {a ^ b}")
print(f"a.symmetric_difference(b) = {a.symmetric_difference(b)}")

print()
print("=" * 40)
print("6. 集合比较")
print("=" * 40)

a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
c = {1, 2, 3}

print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")

print("-" * 40)

print(f"a == c: {a == c}")
print(f"a == b: {a == b}")

print("-" * 40)

print("子集 (issubset):")
print(f"a <= b: {a <= b}")
print(f"a.issubset(b): {a.issubset(b)}")

print("-" * 40)

print("超集 (issuperset):")
print(f"b >= a: {b >= a}")
print(f"b.issuperset(a): {b.issuperset(a)}")

print("-" * 40)

print("无交集 (isdisjoint):")
d = {6, 7, 8}
print(f"d = {d}")
print(f"a.isdisjoint(d): {a.isdisjoint(d)}")

print()
print("=" * 40)
print("7. 集合方法")
print("=" * 40)

a = {1, 2, 3}
b = {3, 4, 5}

print(f"a = {a}, b = {b}")

a.update(b)
print(f"a.update(b): {a}")

print("-" * 40)

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7}

a.intersection_update(b)
print(f"a.intersection_update(b): {a}")

print("-" * 40)

a = {1, 2, 3, 4, 5}
b = {4, 5}

a.difference_update(b)
print(f"a.difference_update(b): {a}")

print()
print("=" * 40)
print("8. 不可变集合")
print("=" * 40)

frozen = frozenset([1, 2, 3, 4, 5])
print(f"frozenset: {frozen}")

print("frozenset 是不可变的，可以作为字典的键或集合的元素")

print()
print("=" * 40)
print("9. 集合推导式")
print("=" * 40)

squares = {x ** 2 for x in range(1, 6)}
print(f"1-5的平方: {squares}")

print("-" * 40)

numbers = [1, 2, 2, 3, 3, 4, 5, 5]
unique_evens = {x for x in numbers if x % 2 == 0}
print(f"不重复的偶数: {unique_evens}")

print()
print("=" * 40)
print("10. 实际应用示例")
print("=" * 40)

print("去重:")
items = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(items))
print(f"原始: {items}")
print(f"去重: {unique}")

print("-" * 40)

print("找出共同好友:")
my_friends = {"张三", "李四", "王五"}
your_friends = {"李四", "王五", "赵六"}
common = my_friends & your_friends
print(f"我的好友: {my_friends}")
print(f"你的好友: {your_friends}")
print(f"共同好友: {common}")

print("-" * 40)

print("检查元素是否存在 (比列表快):")
valid_ids = {1001, 1002, 1003, 1004, 1005}
user_id = 1003
if user_id in valid_ids:
    print(f"ID {user_id} 有效")
else:
    print(f"ID {user_id} 无效")
