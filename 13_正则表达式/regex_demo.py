"""
正则表达式
==========

使用 re 模块进行模式匹配。
"""

import re

print("=" * 40)
print("1. 基本匹配")
print("=" * 40)

pattern = r"hello"
text = "hello world"

match = re.search(pattern, text)
print(f"在 '{text}' 中查找 '{pattern}': {match}")
print(f"匹配内容: {match.group()}")

print()
print("=" * 40)
print("2. 常用元字符")
print("=" * 40)

patterns = [
    (r".", "任意字符"),
    (r"\d", "数字"),
    (r"\w", "字母数字下划线"),
    (r"\s", "空白字符"),
    (r"^abc", "abc开头"),
    (r"xyz$", "xyz结尾"),
]

for pat, desc in patterns:
    print(f"{pat:10} - {desc}")

print()
print("=" * 40)
print("3. 数量词")
print("=" * 40)

text = "ab abc aabc abbc abbbc"

patterns = [
    (r"a*", "0个或多个a"),
    (r"a+", "1个或多个a"),
    (r"a?", "0个或1个a"),
    (r"a{2,4}", "2-4个a"),
]

for pat, desc in patterns:
    matches = re.findall(pat, text)
    print(f"{pat:15} ({desc}): {matches}")

print()
print("=" * 40)
print("4. 字符类")
print("=" * 40)

text = "test1 Test2 TEST3 tEsT4"

patterns = [
    (r"[0-9]", "数字"),
    (r"[a-z]", "小写字母"),
    (r"[A-Z]", "大写字母"),
    (r"[a-zA-Z]+", "所有字母单词"),
]

for pat, desc in patterns:
    matches = re.findall(pat, text)
    print(f"{pat:20} ({desc}): {matches}")

print()
print("=" * 40)
print("5. 分组和捕获")
print("=" * 40)

text = "张三: 25岁, 李四: 30岁"

pattern = r"(\w+): (\d+)岁"
matches = re.findall(pattern, text)
print(f"分组匹配: {matches}")

for name, age in matches:
    print(f"  姓名: {name}, 年龄: {age}")

print()
print("=" * 40)
print("6. 替换")
print("=" * 40)

text = "hello world, python programming"

result = re.sub(r"python", "Python", text)
print(f"替换: {result}")

result = re.sub(r"\b\w+\b", lambda m: m.group().upper(), text)
print(f"大写每个单词: {result}")

print()
print("=" * 40)
print("7. 分割")
print("=" * 40)

text = "apple, banana; orange; grape"

result = re.split(r"[;,]", text)
print(f"按逗号分号分割: {result}")

print()
print("=" * 40)
print("8. 实际应用：邮箱验证")
print("=" * 40)

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

emails = ["test@example.com", "invalid@", "@example.com", "test@"]
for email in emails:
    print(f"{email}: {is_valid_email(email)}")
