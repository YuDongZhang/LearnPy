"""
继承
==

继承允许子类获得父类的属性和方法，并可以扩展或重写。
"""

print("=" * 50)
print("1. 基础继承")
print("=" * 50)

class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("子类必须实现此方法")
    
    def introduce(self):
        print(f"我是{self.name}")

class Dog(Animal):
    def speak(self):
        return f"{self.name}说：汪汪汪！"

class Cat(Animal):
    def speak(self):
        return f"{self.name}说：喵喵喵！"

dog = Dog("旺财")
cat = Cat("咪咪")

print(dog.speak())
print(cat.speak())
dog.introduce()

print()
print("=" * 50)
print("2. 调用父类方法 - super()")
print("=" * 50)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"Person.__init__ 被调用")
    
    def introduce(self):
        print(f"我叫{self.name}，今年{self.age}岁")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        print(f"Student.__init__ 被调用")
    
    def introduce(self):
        super().introduce()
        print(f"我的学号是：{self.student_id}")

s = Student("张三", 20, "S001")
s.introduce()

print()
print("=" * 50)
print("3. 多重继承")
print("=" * 50)

class Flyable:
    def fly(self):
        print(f"{self.name}在飞翔")

class Swimmable:
    def swim(self):
        print(f"{self.name}在游泳")

class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return f"{self.name}说：嘎嘎嘎！"

duck = Duck("唐老鸭")
print(duck.speak())
duck.fly()
duck.swim()

print()
print("=" * 50)
print("4. 方法解析顺序 (MRO)")
print("=" * 50)

print("Duck 的 MRO:")
for i, cls in enumerate(Duck.__mro__, 1):
    print(f"  {i}. {cls.__name__}")

print()
print("=" * 50)
print("5. 方法重写与扩展")
print("=" * 50)

class Vehicle:
    def __init__(self, brand):
        self.brand = brand
    
    def info(self):
        print(f"品牌: {self.brand}")
    
    def move(self):
        print("交通工具在移动")

class Car(Vehicle):
    def __init__(self, brand, seats):
        super().__init__(brand)
        self.seats = seats
    
    def info(self):
        super().info()
        print(f"座位数: {self.seats}")
    
    def move(self):
        print(f"{self.brand}汽车在公路上行驶")

class Bicycle(Vehicle):
    def move(self):
        print(f"{self.brand}自行车在骑行")

car = Car("宝马", 5)
bike = Bicycle("永久")

print("汽车信息:")
car.info()
car.move()

print()
print("自行车信息:")
bike.info()
bike.move()

print()
print("=" * 50)
print("6. 继承中的类属性")
print("=" * 50)

class Parent:
    family_name = "张家"
    
    def show_family(self):
        print(f"家族: {self.family_name}")

class Child(Parent):
    pass

p = Parent()
c = Child()

p.show_family()
c.show_family()

print(f"\n通过类访问:")
print(f"Parent.family_name = {Parent.family_name}")
print(f"Child.family_name = {Child.family_name}")

print()
print("=" * 50)
print("7. isinstance() 和 issubclass()")
print("=" * 50)

dog = Dog("旺财")

print(f"isinstance(dog, Dog) = {isinstance(dog, Dog)}")
print(f"isinstance(dog, Animal) = {isinstance(dog, Animal)}")
print(f"isinstance(dog, object) = {isinstance(dog, object)}")

print()
print(f"issubclass(Dog, Animal) = {issubclass(Dog, Animal)}")
print(f"issubclass(Dog, object) = {issubclass(Dog, object)}")
print(f"issubclass(Animal, Dog) = {issubclass(Animal, Dog)}")
