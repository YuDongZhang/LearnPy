"""
特殊方法（魔术方法）
==================

特殊方法以双下划线开头和结尾，用于定义类的特殊行为。
"""

print("=" * 50)
print("1. 构造和初始化")
print("=" * 50)

class Person:
    def __new__(cls, name):
        print(f"__new__ 被调用，创建对象")
        return super().__new__(cls)
    
    def __init__(self, name):
        print(f"__init__ 被调用，初始化对象")
        self.name = name

p = Person("张三")

print()
print("=" * 50)
print("2. 字符串表示")
print("=" * 50)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"Person: {self.name}, {self.age}岁"
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"

p = Person("张三", 25)

print(f"str(p): {str(p)}")
print(f"repr(p): {repr(p)}")
print(f"p: {p}")

print()
print("=" * 50)
print("3. 运算符重载")
print("=" * 50)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __len__(self):
        return 2
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return abs(self) < abs(other)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}, v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 3 = {v1 * 3}")
print(f"v1 / 2 = {v1 / 2}")
print(f"-v1 = {-v1}")
print(f"abs(v1) = {abs(v1)}")
print(f"len(v1) = {len(v1)}")
print(f"v1 == Vector(3, 4) = {v1 == Vector(3, 4)}")
print(f"v1 < v2 = {v1 < v2}")

print()
print("=" * 50)
print("4. 容器类型方法")
print("=" * 50)

class MyList:
    def __init__(self, items=None):
        self.items = items if items else []
    
    def __getitem__(self, index):
        return self.items[index]
    
    def __setitem__(self, index, value):
        self.items[index] = value
    
    def __delitem__(self, index):
        del self.items[index]
    
    def __contains__(self, item):
        return item in self.items
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)
    
    def __str__(self):
        return str(self.items)

my_list = MyList([1, 2, 3, 4, 5])

print(f"my_list = {my_list}")
print(f"my_list[0] = {my_list[0]}")
print(f"my_list[2:4] = {my_list[2:4]}")
print(f"3 in my_list = {3 in my_list}")
print(f"10 in my_list = {10 in my_list}")
print(f"len(my_list) = {len(my_list)}")

my_list[0] = 10
print(f"修改后: my_list = {my_list}")

del my_list[1]
print(f"删除后: my_list = {my_list}")

print()
print("=" * 50)
print("5. 可调用对象")
print("=" * 50)

class Counter:
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(f"counter() = {counter()}")
print(f"counter() = {counter()}")
print(f"counter() = {counter()}")
print(f"调用次数: {counter.count}")

print()
print("=" * 50)
print("6. 比较方法")
print("=" * 50)

class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch
    
    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
    
    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
    
    def __le__(self, other):
        return self == other or self < other
    
    def __gt__(self, other):
        return other < self
    
    def __ge__(self, other):
        return self > other or self == other
    
    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

v1 = Version(1, 2, 0)
v2 = Version(1, 2, 1)
v3 = Version(2, 0, 0)

print(f"v1 = {v1}, v2 = {v2}, v3 = {v3}")
print(f"v1 == v2 = {v1 == v2}")
print(f"v1 < v2 = {v1 < v2}")
print(f"v2 < v3 = {v2 < v3}")
print(f"v1 <= v2 = {v1 <= v2}")
print(f"v3 > v2 = {v3 > v2}")

print()
print("=" * 50)
print("7. 上下文管理器")
print("=" * 50)

class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"打开文件: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"关闭文件: {self.filename}")
        if self.file:
            self.file.close()
        return False

with FileManager("test.txt", "w") as fm:
    fm.file.write("Hello, World!")
    print("正在写入文件...")

print()
print("=" * 50)
print("8. 属性访问控制")
print("=" * 50)

class PrivateExample:
    def __init__(self, value):
        self.__private_value = value
    
    def __getattr__(self, name):
        print(f"访问属性: {name}")
        if name.startswith("_"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return f"默认值"
    
    def __setattr__(self, name, value):
        print(f"设置属性: {name} = {value}")
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        print(f"删除属性: {name}")
        super().__delattr__(name)

obj = PrivateExample(100)
print(f"obj.__private_value = {obj._PrivateExample__private_value}")
print(f"obj.nonexistent = {obj.nonexistent}")

print()
print("=" * 50)
print("9. 哈希和布尔值")
print("=" * 50)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __hash__(self):
        return hash((self.suit, self.rank))
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
    def __bool__(self):
        return self.rank != "Joker"
    
    def __str__(self):
        return f"{self.rank}{self.suit}"

card1 = Card("♠", "A")
card2 = Card("♠", "A")
card3 = Card("♥", "A")

print(f"card1 = {card1}")
print(f"hash(card1) = {hash(card1)}")
print(f"card1 == card2 = {card1 == card2}")
print(f"card1 == card3 = {card1 == card3}")

joker = Card("♠", "Joker")
normal_card = Card("♥", "K")
print(f"\nbool(joker) = {bool(joker)}")
print(f"bool(normal_card) = {bool(normal_card)}")

print()
print("=" * 50)
print("10. 完整示例：分数类")
print("=" * 50)

from math import gcd

class Fraction:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("分母不能为零")
        sign = -1 if numerator * denominator < 0 else 1
        numerator = abs(numerator)
        denominator = abs(denominator)
        g = gcd(numerator, denominator)
        self.numerator = sign * (numerator // g)
        self.denominator = denominator // g
    
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
    
    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"
    
    def __add__(self, other):
        n = self.numerator * other.denominator + other.numerator * self.denominator
        d = self.denominator * other.denominator
        return Fraction(n, d)
    
    def __sub__(self, other):
        n = self.numerator * other.denominator - other.numerator * self.denominator
        d = self.denominator * other.denominator
        return Fraction(n, d)
    
    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
    
    def __truediv__(self, other):
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
    
    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator
    
    def __lt__(self, other):
        return self.numerator * other.denominator < other.numerator * self.denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __int__(self):
        return self.numerator // self.denominator

f1 = Fraction(1, 2)
f2 = Fraction(1, 3)
f3 = Fraction(2, 4)

print(f"f1 = {f1}, f2 = {f2}, f3 = {f3}")
print(f"f1 + f2 = {f1 + f2}")
print(f"f1 - f2 = {f1 - f2}")
print(f"f1 * f2 = {f1 * f2}")
print(f"f1 / f2 = {f1 / f2}")
print(f"f1 == f3 = {f1 == f3}")
print(f"f1 < f2 = {f1 < f2}")
print(f"float(f1) = {float(f1)}")
