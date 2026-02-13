"""
条件判断示例
============

if 语句用于根据条件执行不同的代码。
条件为 True 时执行，为 False 时跳过。
"""

print("=" * 40)
print("1. 基本 if 语句")
print("=" * 40)

age = 20

if age >= 18:
    print("你已经成年了")

print("-" * 40)

temperature = 35

if temperature > 30:
    print("天气很热")
    print("记得多喝水")

print()
print("=" * 40)
print("2. if-else 语句")
print("=" * 40)

score = 55

if score >= 60:
    print("及格")
else:
    print("不及格")

print("-" * 40)

is_raining = True

if is_raining:
    print("带伞出门")
else:
    print("不用带伞")

print()
print("=" * 40)
print("3. if-elif-else 语句")
print("=" * 40)

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数 {score} 的等级是 {grade}")

print("-" * 40)

day = 3

if day == 1:
    day_name = "星期一"
elif day == 2:
    day_name = "星期二"
elif day == 3:
    day_name = "星期三"
elif day == 4:
    day_name = "星期四"
elif day == 5:
    day_name = "星期五"
elif day == 6:
    day_name = "星期六"
elif day == 7:
    day_name = "星期日"
else:
    day_name = "无效的日期"

print(f"数字 {day} 对应 {day_name}")

print()
print("=" * 40)
print("4. 条件嵌套")
print("=" * 40)

age = 25
has_license = True

if age >= 18:
    if has_license:
        print("可以开车")
    else:
        print("需要先考驾照")
else:
    print("年龄不够，不能开车")

print("-" * 40)

score = 75
attendance = 90

if score >= 60:
    if attendance >= 80:
        print("通过课程")
    else:
        print("出勤率不足")
else:
    print("分数不够")

print()
print("=" * 40)
print("5. 逻辑运算符组合条件")
print("=" * 40)

age = 25
income = 5000

if age >= 18 and income >= 3000:
    print("符合贷款条件")

print("-" * 40)

has_card = False
has_cash = True

if has_card or has_cash:
    print("可以支付")

print("-" * 40)

is_weekend = True

if not is_weekend:
    print("工作日")
else:
    print("休息日")

print()
print("=" * 40)
print("6. 三元表达式")
print("=" * 40)

age = 20

status = "成年" if age >= 18 else "未成年"
print(f"状态: {status}")

print("-" * 40)

a, b = 10, 20
max_value = a if a > b else b
print(f"较大的值是: {max_value}")
