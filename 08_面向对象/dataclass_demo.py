"""
数据类 (dataclass)
=================

Python 3.7+ 引入的数据类，用于简化数据存储类的定义。
自动生成 __init__、__repr__、__eq__ 等方法。
"""

from dataclasses import dataclass, field, asdict, astuple
from typing import List, ClassVar

print("=" * 50)
print("1. 基础 dataclass")
print("=" * 50)

@dataclass
class Person:
    name: str
    age: int
    city: str = "北京"

p1 = Person("张三", 25)
p2 = Person("李四", 30, "上海")
p3 = Person("张三", 25)

print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"p1 == p3 = {p1 == p3}")

print()
print("=" * 50)
print("2. 默认值与可变默认值")
print("=" * 50)

@dataclass
class Student:
    name: str
    grades: List[int] = field(default_factory=list)
    
    def add_grade(self, grade):
        self.grades.append(grade)
    
    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

s1 = Student("张三")
s1.add_grade(85)
s1.add_grade(92)
s1.add_grade(78)

s2 = Student("李四")
s2.add_grade(90)

print(f"{s1.name} 的成绩: {s1.grades}, 平均分: {s1.average():.1f}")
print(f"{s2.name} 的成绩: {s2.grades}, 平均分: {s2.average():.1f}")

print()
print("=" * 50)
print("3. field() 高级用法")
print("=" * 50)

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 1
    tags: List[str] = field(default_factory=list)
    _internal_id: int = field(default=0, repr=False)
    description: str = field(default="", compare=False)
    
    @property
    def total(self):
        return self.price * self.quantity

p = Product("笔记本电脑", 5999.0, 2, tags=["电子产品", "办公"])
p.description = "高性能商务笔记本"
print(f"商品: {p}")
print(f"总价: {p.total}")

print()
print("=" * 50)
print("4. 不可变数据类")
print("=" * 50)

@dataclass(frozen=True)
class Point:
    x: float
    y: float
    
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

p1 = Point(0, 0)
p2 = Point(3, 4)
print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"距离: {p1.distance_to(p2)}")

try:
    p1.x = 10
except AttributeError as e:
    print(f"\n尝试修改不可变数据类: {e}")

print()
print("=" * 50)
print("5. 类变量与实例变量")
print("=" * 50)

@dataclass
class Employee:
    name: str
    salary: float
    company: ClassVar[str] = "Python公司"
    employee_count: ClassVar[int] = 0
    
    def __post_init__(self):
        Employee.employee_count += 1

e1 = Employee("张三", 10000)
e2 = Employee("李四", 15000)

print(f"员工: {e1.name}, {e2.name}")
print(f"公司: {Employee.company}")
print(f"员工数: {Employee.employee_count}")

print()
print("=" * 50)
print("6. __post_init__ 后处理")
print("=" * 50)

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    perimeter: float = field(init=False)
    
    def __post_init__(self):
        self.area = self.width * self.height
        self.perimeter = 2 * (self.width + self.height)

rect = Rectangle(5, 3)
print(f"矩形: {rect.width} x {rect.height}")
print(f"面积: {rect.area}")
print(f"周长: {rect.perimeter}")

print()
print("=" * 50)
print("7. 继承 dataclass")
print("=" * 50)

@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str = "未知"

dog = Dog("旺财", 3, "金毛")
print(f"狗: {dog}")

print()
print("=" * 50)
print("8. 转换为字典和元组")
print("=" * 50)

@dataclass
class Book:
    title: str
    author: str
    price: float

book = Book("Python编程", "张三", 59.9)

print(f"字典: {asdict(book)}")
print(f"元组: {astuple(book)}")

print()
print("=" * 50)
print("9. 排序支持")
print("=" * 50)

@dataclass(order=True)
class StudentRecord:
    grade: float
    name: str = field(compare=False)
    student_id: int = field(compare=False)

students = [
    StudentRecord(85.5, "张三", 101),
    StudentRecord(92.0, "李四", 102),
    StudentRecord(78.5, "王五", 103),
    StudentRecord(92.0, "赵六", 104),
]

print("按成绩排序:")
for s in sorted(students, reverse=True):
    print(f"  {s.name}: {s.grade}")

print()
print("=" * 50)
print("10. 实际应用：配置类")
print("=" * 50)

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306
    username: str = "root"
    password: str = ""
    database: str = "test"
    charset: str = "utf8mb4"
    
    @property
    def connection_string(self):
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

config = DatabaseConfig(
    host="192.168.1.100",
    username="admin",
    password="secret",
    database="myapp"
)

print(f"数据库配置:")
print(f"  主机: {config.host}:{config.port}")
print(f"  数据库: {config.database}")
print(f"  连接字符串: {config.connection_string}")

print()
print("=" * 50)
print("11. dataclass vs 普通类对比")
print("=" * 50)

print("普通类写法:")
print("""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"
    
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age
""")

print("dataclass 写法:")
print("""
@dataclass
class Person:
    name: str
    age: int
""")

print("\ndataclass 优势:")
print("  1. 代码简洁，减少样板代码")
print("  2. 自动生成 __init__、__repr__、__eq__")
print("  3. 类型注解提高可读性")
print("  4. 支持不可变、排序等特性")
