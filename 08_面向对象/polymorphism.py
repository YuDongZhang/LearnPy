"""
多态
==

多态是指同一方法在不同对象上有不同的表现。
Python 是动态类型语言，天然支持多态。
"""

print("=" * 50)
print("1. 多态基础概念")
print("=" * 50)

class Animal:
    def speak(self):
        raise NotImplementedError("子类必须实现此方法")

class Dog(Animal):
    def speak(self):
        return "汪汪汪！"

class Cat(Animal):
    def speak(self):
        return "喵喵喵！"

class Duck(Animal):
    def speak(self):
        return "嘎嘎嘎！"

def animal_sound(animal):
    """多态函数：接受任何 Animal 类型的对象"""
    print(f"{animal.__class__.__name__} 发出声音: {animal.speak()}")

animals = [Dog(), Cat(), Duck()]

print("遍历不同的动物，调用相同的方法:")
for animal in animals:
    animal_sound(animal)

print()
print("=" * 50)
print("2. 鸭子类型 (Duck Typing)")
print("=" * 50)

class Person:
    def speak(self):
        return "你好！"

class Robot:
    def speak(self):
        return "哔哔哔！"

def make_it_speak(obj):
    """不需要继承关系，只要有 speak 方法即可"""
    print(f"{obj.__class__.__name__} 说: {obj.speak()}")

print("鸭子类型示例：")
make_it_speak(Dog())
make_it_speak(Person())
make_it_speak(Robot())

print()
print("=" * 50)
print("3. 运算符多态（运算符重载）")
print("=" * 50)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """重载 + 运算符"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """重载 - 运算符"""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """重载 * 运算符（与标量相乘）"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        """重载 == 运算符"""
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(4, 5)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 3 = {v1 * 3}")
print(f"v1 == Vector(2, 3) = {v1 == Vector(2, 3)}")

print()
print("=" * 50)
print("4. 函数重载的替代方案")
print("=" * 50)

class Calculator:
    def calculate(self, a, b=None):
        """通过默认参数实现类似重载的效果"""
        if b is None:
            return a * a
        else:
            return a + b

calc = Calculator()
print(f"calculate(5) = {calc.calculate(5)}")
print(f"calculate(3, 4) = {calc.calculate(3, 4)}")

print()
print("=" * 50)
print("5. 实际应用：图形绘制系统")
print("=" * 50)

import math

class Shape:
    def area(self):
        pass
    
    def perimeter(self):
        pass
    
    def describe(self):
        print(f"{self.__class__.__name__}:")
        print(f"  面积: {self.area():.2f}")
        print(f"  周长: {self.perimeter():.2f}")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self):
        return self.a + self.b + self.c

shapes = [
    Rectangle(5, 3),
    Circle(4),
    Triangle(3, 4, 5)
]

print("统一处理不同类型的图形:")
for shape in shapes:
    shape.describe()
    print()

print("=" * 50)
print("6. 多态与抽象基类")
print("=" * 50)

from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass
    
    @abstractmethod
    def refund(self, amount):
        pass

class Alipay(Payment):
    def pay(self, amount):
        print(f"支付宝支付 {amount} 元")
    
    def refund(self, amount):
        print(f"支付宝退款 {amount} 元")

class WeChatPay(Payment):
    def pay(self, amount):
        print(f"微信支付 {amount} 元")
    
    def refund(self, amount):
        print(f"微信退款 {amount} 元")

def process_payment(payment_method: Payment, amount):
    """使用抽象基类确保传入的对象实现了必要的方法"""
    payment_method.pay(amount)

print("支付方式多态:")
process_payment(Alipay(), 100)
process_payment(WeChatPay(), 200)
