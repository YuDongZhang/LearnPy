"""
封装
====

封装是将数据和操作封装在一起，隐藏内部实现细节，只暴露必要的接口。
"""

print("=" * 50)
print("1. 访问控制级别")
print("=" * 50)

class Person:
    def __init__(self, name, age, salary):
        self.name = name
        self._age = age
        self.__salary = salary
    
    def get_salary(self):
        return self.__salary
    
    def set_salary(self, salary):
        if salary < 0:
            raise ValueError("薪资不能为负数")
        self.__salary = salary

p = Person("张三", 25, 10000)

print(f"公开属性: p.name = {p.name}")
print(f"受保护属性: p._age = {p._age}")
print(f"私有属性（通过方法）: get_salary() = {p.get_salary()}")

p.name = "李四"
p._age = 26
p.set_salary(15000)

print(f"\n修改后:")
print(f"p.name = {p.name}")
print(f"p._age = {p._age}")
print(f"p.get_salary() = {p.get_salary()}")

try:
    p.set_salary(-1000)
except ValueError as e:
    print(f"\n设置负薪资时抛出异常: {e}")

print()
print("=" * 50)
print("2. 属性装饰器 @property")
print("=" * 50)

class Student:
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    
    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, value):
        if value < 0 or value > 100:
            raise ValueError("成绩必须在 0-100 之间")
        self.__score = value
    
    @score.deleter
    def score(self):
        print("不能删除成绩！")

s = Student("张三", 85)

print(f"通过属性访问: s.score = {s.score}")
s.score = 90
print(f"修改后: s.score = {s.score}")

try:
    s.score = 150
except ValueError as e:
    print(f"设置无效成绩: {e}")

s.score = 75

print()
print("=" * 50)
print("3. 只读属性")
print("=" * 50)

class Circle:
    def __init__(self, radius):
        self.__radius = radius
    
    @property
    def radius(self):
        return self.__radius
    
    @property
    def area(self):
        return 3.14 * self.__radius ** 2
    
    @property
    def perimeter(self):
        return 2 * 3.14 * self.__radius

c = Circle(5)

print(f"半径: {c.radius}")
print(f"面积: {c.area:.2f}")
print(f"周长: {c.perimeter:.2f}")

try:
    c.area = 100
except AttributeError as e:
    print(f"\n尝试修改只读属性: {e}")

print()
print("=" * 50)
print("4. 计算属性（缓存）")
print("=" * 50)

class Fibonacci:
    def __init__(self, n):
        self.n = n
        self.__cache = {}
    
    @property
    def sequence(self):
        if self.n not in self.__cache:
            self.__cache[self.n] = self._fib(self.n)
        return self.__cache[self.n]
    
    def _fib(self, n):
        if n <= 1:
            return n
        return self._fib(n - 1) + self._fib(n - 2)

f = Fibonacci(10)
print(f"斐波那契数列前 10 项:")
for i in range(10):
    f_i = Fibonacci(i)
    print(f"  F({i}) = {f_i.sequence}")

print()
print("=" * 50)
print("5. 使用私有变量实现数据验证")
print("=" * 50)

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
    
    @property
    def balance(self):
        return self.__balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于 0")
        self.__balance += amount
        print(f"存入 {amount} 元，余额: {self.__balance} 元")
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于 0")
        if amount > self.__balance:
            raise ValueError("余额不足")
        self.__balance -= amount
        print(f"取出 {amount} 元，余额: {self.__balance} 元")
    
    def transfer(self, to_account, amount):
        self.withdraw(amount)
        to_account.deposit(amount)
        print(f"转账成功: {self.owner} -> {to_account.owner}, 金额: {amount}")

account1 = BankAccount("张三", 1000)
account2 = BankAccount("李四", 500)

account1.deposit(500)
account1.withdraw(300)
account1.transfer(account2, 200)

print(f"\n最终余额:")
print(f"  {account1.owner}: {account1.balance} 元")
print(f"  {account2.owner}: {account2.balance} 元")

print()
print("=" * 50)
print("6. 属性的命名转换")
print("=" * 50)

class Test:
    def __init__(self):
        self.public = "公开"
        self._protected = "受保护"
        self.__private = "私有"

t = Test()

print(f"公开属性: {t.public}")
print(f"受保护属性: {t._protected}")

name_mangled = "_Test__private"
print(f"私有属性（名称改写后）: {getattr(t, name_mangled)}")

print("\n名称改写规则:")
print("  __private -> _类名__private")
print("  目的：防止子类覆盖")

print()
print("=" * 50)
print("7. slots 限制属性")
print("=" * 50)

class Point2D:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point2D(1, 2)
print(f"p.x = {p.x}, p.y = {p.y}")

try:
    p.z = 3
except AttributeError as e:
    print(f"\n添加未定义的 z 属性: {e}")

print("\n使用 __slots__ 的好处:")
print("  1. 限制对象属性，防止意外添加")
print("  2. 节省内存（不创建 __dict__）")
print("  3. 提高属性访问速度")

print()
print("=" * 50)
print("8. 封装实际案例：问卷系统")
print("=" * 50)

class Question:
    def __init__(self, question_text, question_type):
        self.question_text = question_text
        self.question_type = question_type
        self.__options = []
        self.__required = False
    
    @property
    def options(self):
        return self.__options.copy()
    
    def add_option(self, option):
        if self.question_type == "choice":
            self.__options.append(option)
        else:
            raise ValueError("只有选择题才能添加选项")
    
    @property
    def required(self):
        return self.__required
    
    @required.setter
    def required(self, value):
        self.__required = bool(value)
    
    def __str__(self):
        options_str = f", 选项: {', '.join(self.__options)}" if self.__options else ""
        required_str = "（必答）" if self.__required else "（选答）"
        return f"问题: {self.question_text}{options_str} {required_str}"

q1 = Question("请输入您的姓名", "text")
q2 = Question("您喜欢哪种编程语言？", "choice")

q2.add_option("Python")
q2.add_option("Java")
q2.add_option("JavaScript")
q2.required = True

print(q1)
print(q2)

q2.add_option("C++")
print(f"\n获取选项副本: {q2.options}")

try:
    q1.add_option("test")
except ValueError as e:
    print(f"\n文本题添加选项: {e}")
