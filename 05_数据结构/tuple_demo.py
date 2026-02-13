"""
元组详解
========

元组是有序、不可变的集合。
使用圆括号 () 创建元组。
"""

print("=" * 40)
print("1. 创建元组")
print("=" * 40)

point = (3, 4)
colors = ("红", "绿", "蓝")
single = (1,)
empty = ()

print(f"point = {point}")
print(f"colors = {colors}")
print(f"single = {single}")
print(f"empty = {empty}")

print("-" * 40)

print("注意：单个元素需要加逗号")
print("(1,) 是元组")
print("(1) 是整数")

print()
print("=" * 40)
print("2. 访问元素")
print("=" * 40)

colors = ("红", "绿", "蓝", "黄", "紫")
print(f"colors = {colors}")

print(f"colors[0] = {colors[0]}")
print(f"colors[2] = {colors[2]}")
print(f"colors[-1] = {colors[-1]}")

print("-" * 40)

print("切片:")
print(f"colors[1:3] = {colors[1:3]}")
print(f"colors[:3] = {colors[:3]}")
print(f"colors[2:] = {colors[2:]}")

print()
print("=" * 40)
print("3. 元组不可变")
print("=" * 40)

numbers = (1, 2, 3)
print(f"numbers = {numbers}")

print("元组创建后不能修改:")
print("numbers[0] = 10  # 这会报错！")

print("-" * 40)

print("但可以重新赋值:")
numbers = (4, 5, 6)
print(f"重新赋值后: {numbers}")

print()
print("=" * 40)
print("4. 元组解包")
print("=" * 40)

point = (3, 4)
x, y = point
print(f"point = {point}")
print(f"x = {x}, y = {y}")

print("-" * 40)

person = ("张三", 25, "北京")
name, age, city = person
print(f"name = {name}, age = {age}, city = {city}")

print("-" * 40)

print("使用 * 接收多余元素:")
scores = (85, 92, 78, 95, 88)
first, *rest = scores
print(f"first = {first}")
print(f"rest = {rest}")

first, *middle, last = scores
print(f"first = {first}, middle = {middle}, last = {last}")

print()
print("=" * 40)
print("5. 元组操作")
print("=" * 40)

t1 = (1, 2, 3)
t2 = (4, 5, 6)

print(f"t1 = {t1}")
print(f"t2 = {t2}")

print(f"t1 + t2 = {t1 + t2}")
print(f"t1 * 2 = {t1 * 2}")

print("-" * 40)

print(f"len(t1) = {len(t1)}")
print(f"max(t1) = {max(t1)}")
print(f"min(t1) = {min(t1)}")
print(f"sum(t1) = {sum(t1)}")

print()
print("=" * 40)
print("6. 元组方法")
print("=" * 40)

numbers = (1, 2, 3, 2, 4, 2, 5)
print(f"numbers = {numbers}")

print(f"count(2) = {numbers.count(2)}")
print(f"index(3) = {numbers.index(3)}")

print()
print("=" * 40)
print("7. 元组与列表转换")
print("=" * 40)

my_list = [1, 2, 3, 4, 5]
my_tuple = tuple(my_list)
print(f"列表转元组: {my_tuple}")

my_tuple = (1, 2, 3, 4, 5)
my_list = list(my_tuple)
print(f"元组转列表: {my_list}")

print()
print("=" * 40)
print("8. 元组的优势")
print("=" * 40)

print("1. 不可变性 - 数据安全")
print("2. 作为字典的键")
print("3. 性能比列表更好")

print("-" * 40)

print("元组可以作为字典的键:")
locations = {
    (0, 0): "原点",
    (1, 0): "x轴上",
    (0, 1): "y轴上"
}
print(f"locations[(0, 0)] = {locations[(0, 0)]}")

print()
print("=" * 40)
print("9. 命名元组")
print("=" * 40)

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)

print(f"Point: {p}")
print(f"p.x = {p.x}, p.y = {p.y}")
print(f"p[0] = {p[0]}, p[1] = {p[1]}")

print()
print("=" * 40)
print("10. 实际应用示例")
print("=" * 40)

print("表示坐标:")
points = [(0, 0), (1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"  点({x}, {y})")

print("-" * 40)

print("函数返回多个值:")
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

minimum, maximum, average = get_stats([1, 2, 3, 4, 5])
print(f"最小值: {minimum}, 最大值: {maximum}, 平均值: {average}")
