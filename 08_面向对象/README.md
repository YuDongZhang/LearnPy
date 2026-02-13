# 第八章：面向对象

## 本章目标
- 理解面向对象编程思想
- 掌握类和对象的定义
- 理解继承、封装、多态
- 掌握特殊方法（魔术方法）

---

## 1. 什么是面向对象

面向对象编程（OOP）是一种编程范式，将数据和操作数据的方法封装在一起。

**核心概念：**
- **类 (Class)**：对象的模板/蓝图
- **对象 (Object)**：类的实例
- **属性 (Attribute)**：对象的数据
- **方法 (Method)**：对象的行为

---

## 2. 定义类

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def say_hello(self):
        print(f"你好，我是{self.name}")

p = Person("张三", 25)
p.say_hello()
```

---

## 3. 三大特性

| 特性 | 说明 |
|------|------|
| **封装** | 隐藏内部实现细节 |
| **继承** | 子类继承父类的属性和方法 |
| **多态** | 同一方法在不同对象有不同表现 |

---

## 4. 示例文件

- `basic_class.py` - 类的基础
- `init_and_self.py` - 构造方法和 self
- `inheritance.py` - 继承
- `encapsulation.py` - 封装
- `polymorphism.py` - 多态
- `special_methods.py` - 特殊方法

---

## 上一章 | 下一章

[第七章：异常处理](../07_异常处理/README.md) | [第九章：模块与包](../09_模块与包/README.md)
