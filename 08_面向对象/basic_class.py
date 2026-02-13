"""
类的基础
========

类是对象的模板，定义了对象的属性和方法。
对象是类的实例。
"""

print("=" * 40)
print("1. 定义类")
print("=" * 40)

class Person:
    pass

p = Person()
print(f"创建对象: {p}")
print(f"对象类型: {type(p)}")

print()
print("=" * 40)
print("2. 添加属性")
print("=" * 40)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("张三", 25)
p2 = Person("李四", 30)

print(f"p1.name = {p1.name}, p1.age = {p1.age}")
print(f"p2.name = {p2.name}, p2.age = {p2.age}")

print()
print("=" * 40)
print("3. 添加方法")
print("=" * 40)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def say_hello(self):
        print(f"你好，我是{self.name}，今年{self.age}岁")
    
    def have_birthday(self):
        self.age += 1
        print(f"{self.name}过生日了，现在{self.age}岁")

p = Person("张三", 25)
p.say_hello()
p.have_birthday()

print()
print("=" * 40)
print("4. 类属性 vs 实例属性")
print("=" * 40)

class Student:
    school = "Python大学"
    
    def __init__(self, name, score):
        self.name = name
        self.score = score

s1 = Student("张三", 85)
s2 = Student("李四", 92)

print("类属性（所有实例共享）:")
print(f"  s1.school = {s1.school}")
print(f"  s2.school = {s2.school}")

print()
print("实例属性（每个实例独立）:")
print(f"  s1.name = {s1.name}, s1.score = {s1.score}")
print(f"  s2.name = {s2.name}, s2.score = {s2.score}")

print()
print("修改类属性:")
Student.school = "Python学院"
print(f"  s1.school = {s1.school}")
print(f"  s2.school = {s2.school}")

print()
print("=" * 40)
print("5. 类方法")
print("=" * 40)

class Counter:
    count = 0
    
    def __init__(self):
        Counter.count += 1
    
    @classmethod
    def get_count(cls):
        return cls.count

c1 = Counter()
c2 = Counter()
c3 = Counter()

print(f"创建的对象数量: {Counter.get_count()}")

print()
print("=" * 40)
print("6. 静态方法")
print("=" * 40)

class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b

print(f"MathUtils.add(3, 5) = {MathUtils.add(3, 5)}")
print(f"MathUtils.multiply(3, 5) = {MathUtils.multiply(3, 5)}")

print()
print("=" * 40)
print("7. 实际应用：银行账户")
print("=" * 40)

class BankAccount:
    bank_name = "Python银行"
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"存入{amount}元，余额: {self.balance}元")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print(f"余额不足！当前余额: {self.balance}元")
            return False
        self.balance -= amount
        print(f"取出{amount}元，余额: {self.balance}元")
        return True
    
    def get_balance(self):
        return self.balance
    
    @classmethod
    def get_bank_name(cls):
        return cls.bank_name

account = BankAccount("张三", 1000)
print(f"开户: {account.owner}")
print(f"银行: {BankAccount.get_bank_name()}")

account.deposit(500)
account.withdraw(200)
account.withdraw(2000)

print()
print("=" * 40)
print("8. __dict__ 查看属性")
print("=" * 40)

p = Person("王五", 28)
print(f"对象的属性: {p.__dict__}")
print(f"类的属性: {Person.__dict__.keys()}")
