"""
组合 vs 继承
============

面向对象设计的核心原则：优先使用组合而非继承。
"""

print("=" * 50)
print("1. 继承的问题")
print("=" * 50)

print("继承的缺点:")
print("  1. 耦合性高：子类依赖父类的实现细节")
print("  2. 脆弱性：父类改动可能破坏子类")
print("  3. 层级过深：继承链过长导致复杂性增加")
print("  4. 限制灵活性：Python 单继承限制")

print("\n示例：继承链过长")
print("""
Animal
  └── Mammal
        └── Dog
              └── ServiceDog
                    └── GuideDog
""")

print()
print("=" * 50)
print("2. 组合示例：图书管理系统")
print("=" * 50)

class Author:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __str__(self):
        return f"{self.name}"

class Publisher:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Book:
    def __init__(self, title, author, publisher, price):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.price = price
    
    def __str__(self):
        return f"《{self.title}》- {self.author}，出版社: {self.publisher.name}，价格: ¥{self.price}"

author = Author("张三", "zhangsan@example.com")
publisher = Publisher("人民邮电出版社", "北京")
book = Book("Python编程", author, publisher, 89.0)

print(book)
print(f"作者邮箱: {book.author.email}")
print(f"出版社地址: {book.publisher.address}")

print()
print("=" * 50)
print("3. 继承示例：员工管理系统（不推荐）")
print("=" * 50)

class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
    
    def work(self):
        print(f"员工 {self.name} 正在工作")

class Manager(Employee):
    def __init__(self, name, employee_id, department):
        super().__init__(name, employee_id)
        self.department = department
        self.team = []
    
    def work(self):
        print(f"经理 {self.name} 正在管理 {self.department} 部门")
    
    def add_team_member(self, employee):
        self.team.append(employee)

class Developer(Employee):
    def __init__(self, name, employee_id, programming_language):
        super().__init__(name, employee_id)
        self.programming_language = programming_language
    
    def work(self):
        print(f"开发者 {self.name} 正在用 {self.programming_language} 写代码")

manager = Manager("张三", "M001", "技术部")
dev1 = Developer("李四", "D001", "Python")
dev2 = Developer("王五", "D002", "Java")

manager.add_team_member(dev1)
manager.add_team_member(dev2)

print("继承方式的问题:")
print("  - Manager 和 Developer 都要继承 Employee")
print("  - 如果加薪逻辑不同，需要覆盖方法")
print("  - 新角色（如 Designer）需要继续继承")

print()
print("=" * 50)
print("4. 组合示例：员工管理系统（推荐）")
print("=" * 50)

class Salary:
    def __init__(self, base_salary, bonus=0):
        self.base_salary = base_salary
        self.bonus = bonus
    
    def calculate(self):
        return self.base_salary + self.bonus

class Department:
    def __init__(self, name):
        self.name = name
        self.members = []
    
    def add_member(self, employee):
        self.members.append(employee)

class Role:
    def __init__(self, title, responsibilities):
        self.title = title
        self.responsibilities = responsibilities
    
    def work(self):
        print(f"  职责: {', '.join(self.responsibilities)}")

class EmployeeV2:
    def __init__(self, name, employee_id, role: Role, salary: Salary):
        self.name = name
        self.employee_id = employee_id
        self.role = role
        self.salary = salary
    
    def work(self):
        print(f"{self.name} ({self.role.title}):")
        self.role.work()
    
    def get_salary(self):
        return self.salary.calculate()

role_manager = Role("技术经理", ["团队管理", "项目规划", "代码评审"])
role_dev = Role("后端开发", ["API开发", "数据库设计", "单元测试"])

salary_manager = Salary(20000, 5000)
salary_dev = Salary(15000, 2000)

emp1 = EmployeeV2("张三", "E001", role_manager, salary_manager)
emp2 = EmployeeV2("李四", "E002", role_dev, salary_dev)

print("组合方式的优势:")
for emp in [emp1, emp2]:
    emp.work()
    print(f"  薪资: ¥{emp.get_salary():,}")
    print()

print("组合的优势:")
print("  - 角色和薪资可以独立变化")
print("  - 新角色只需创建新的 Role 类")
print("  - 薪资计算逻辑可以单独测试")
print("  - 降低了类之间的耦合度")

print()
print("=" * 50)
print("5. 何时使用继承")
print("=" * 50)

print("适合使用继承的情况:")
print("  1. 明确的is-a关系（ Dog is an Animal ）")
print("  2. 不需要改变父类的行为")
print("  3. 继承层级浅（最多 2-3 层）")
print("  4. 子类复用父类的全部功能")

class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError

class Cat(Animal):
    def speak(self):
        return "喵喵喵"

cat = Cat("咪咪")
print(f"{cat.name} 叫: {cat.speak()}")

print("\n解释:")
print("  - Cat is an Animal ✓ 明确的is-a关系")
print("  - Cat 只需要实现 speak 方法，其他功能继承自 Animal")

print()
print("=" * 50)
print("6. 何时使用组合")
print("=" * 50)

print("适合使用组合的情况:")
print("  1. has-a关系（ Book has an Author ）")
print("  2. 需要动态改变行为")
print("  3. 需要复用多个不相关的功能")
print("  4. 想要避免继承的耦合性")

print("\n示例：汽车有引擎和轮子（has-a）")

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        return "引擎启动"

class Wheel:
    def __init__(self, size):
        self.size = size

class Car:
    def __init__(self, brand, engine: Engine):
        self.brand = brand
        self.engine = engine
        self.wheels = [Wheel(18) for _ in range(4)]
    
    def drive(self):
        wheel_count = len(self.wheels)
        print(f"{self.brand} 汽车 ({wheel_count} 个轮子, {self.engine.horsepower}马力)")
        print(f"  {self.engine.start()}")
        print("  行驶中...")

engine = Engine(200)
car = Car("比亚迪", engine)
car.drive()

print("\n组合的优势:")
print("  - 引擎和轮子可以独立替换")
print("  - 可以轻松添加新组件（如空调、音响）")
print("  - 符合'对扩展开放，对修改关闭'原则")

print()
print("=" * 50)
print("7. 设计原则总结")
print("=" * 50)

print("""
┌─────────────────────────────────────────────────────────┐
│                  面向对象设计原则                         │
├─────────────────────────────────────────────────────────┤
│  优先使用组合而非继承                                    │
│                                                         │
│  继承 ✅  组合 ✅                                      │
│  ├─ is-a 关系明确          ├─ has-a 关系               │
│  ├─ 继承层级浅            ├─ 功能可插拔               │
│  ├─ 不需要修改父类行为    ├─ 降低耦合                 │
│  └─ 复用父类全部功能      └─ 灵活应对变化             │
└─────────────────────────────────────────────────────────┘
""")
