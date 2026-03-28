# 1. Java vs Python 语法速查

## 一句话总结

Python = Java去掉大括号、分号、类型声明，缩进代替花括号。

## 基础语法对照

| 特性 | Java | Python |
|------|------|--------|
| 文件后缀 | `.java` | `.py` |
| 入口 | `public static void main(String[] args)` | `if __name__ == "__main__":` |
| 语句结尾 | 分号 `;` | 不需要 |
| 代码块 | `{ }` | 缩进（4空格） |
| 注释 | `//` 和 `/* */` | `#` 和 `"""..."""` |
| 打印 | `System.out.println()` | `print()` |
| 空值 | `null` | `None` |
| 布尔 | `true / false` | `True / False` |

## Hello World

```java
// Java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

```python
# Python
print("Hello World")
```

## 变量

```java
// Java: 必须声明类型
int age = 25;
String name = "张三";
final double PI = 3.14;
```

```python
# Python: 不需要类型声明
age = 25
name = "张三"
PI = 3.14  # 没有真正的常量，约定全大写
```

## 字符串

| 操作 | Java | Python |
|------|------|--------|
| 拼接 | `"a" + "b"` | `"a" + "b"` 或 `f"a{var}b"` |
| 格式化 | `String.format("%s is %d", name, age)` | `f"{name} is {age}"` |
| 长度 | `str.length()` | `len(str)` |
| 包含 | `str.contains("x")` | `"x" in str` |
| 分割 | `str.split(",")` | `str.split(",")` |
| 去空格 | `str.trim()` | `str.strip()` |
| 大小写 | `str.toUpperCase()` | `str.upper()` |
| 多行 | 拼接或Text Block | `"""多行字符串"""` |

## 类型转换

```java
// Java
int a = Integer.parseInt("123");
String s = String.valueOf(123);
double d = (double) a;
```

```python
# Python
a = int("123")
s = str(123)
d = float(a)
```

## 输入

```java
Scanner sc = new Scanner(System.in);
String name = sc.nextLine();
int age = sc.nextInt();
```

```python
name = input("请输入姓名: ")
age = int(input("请输入年龄: "))  # input返回的是字符串
```

## 运算符差异

| 操作 | Java | Python |
|------|------|--------|
| 整除 | `7 / 2` → `3`（int除法） | `7 // 2` → `3` |
| 普通除 | `7.0 / 2` → `3.5` | `7 / 2` → `3.5` |
| 幂运算 | `Math.pow(2, 10)` | `2 ** 10` |
| 逻辑与 | `&&` | `and` |
| 逻辑或 | `\|\|` | `or` |
| 逻辑非 | `!` | `not` |
| 三元 | `a > b ? a : b` | `a if a > b else b` |

## 关键记忆点

1. **没有分号** — 行尾不加 `;`
2. **缩进即代码块** — 4空格代替 `{ }`
3. **没有类型声明** — 直接 `x = 10`
4. **True/False/None** — 首字母大写
5. **and/or/not** — 不是 `&&/||/!`
6. **f-string** — `f"hello {name}"` 比 `String.format` 方便太多
