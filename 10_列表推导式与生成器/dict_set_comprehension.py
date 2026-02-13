"""
字典和集合推导式示例
==================
"""

print("=" * 40)
print("1. 字典推导式")
print("=" * 40)

names = ["张三", "李四", "王五"]
name_length = {name: len(name) for name in names}
print(f"名字长度: {name_length}")

numbers = [1, 2, 3, 4, 5]
squares_dict = {x: x**2 for x in numbers}
print(f"平方字典: {squares_dict}")

print()
print("=" * 40)
print("2. 带条件的字典推导式")
print("=" * 40)

scores = {"张三": 85, "李四": 92, "王五": 78, "赵六": 95}
passed = {name: score for name, score in scores.items() if score >= 80}
print(f"80分以上: {passed}")

print()
print("=" * 40)
print("3. 键值互换")
print("=" * 40)

original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"原字典: {original}")
print(f"互换后: {swapped}")

print()
print("=" * 40)
print("4. 集合推导式")
print("=" * 40)

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = {x for x in numbers}
print(f"原列表: {numbers}")
print(f"去重集合: {unique}")

words = ["Hello", "World", "Python"]
first_letters = {word[0] for word in words}
print(f"首字母集合: {first_letters}")

print()
print("=" * 40)
print("5. 带条件的集合推导式")
print("=" * 40)

numbers = [-3, -1, 0, 2, 5, -4, 3]
positive_unique = {x for x in numbers if x > 0}
print(f"正数集合: {positive_unique}")

print()
print("=" * 40)
print("6. 实际应用示例")
print("=" * 40)

words = ["apple", "banana", "cherry", "date", "elderberry"]
word_info = {word: {"length": len(word), "upper": word.upper()} for word in words}
for word, info in word_info.items():
    print(f"  {word}: {info}")

print()
text = "hello world python programming"
char_count = {char: text.count(char) for char in set(text) if char != ' '}
print(f"字符计数: {char_count}")
