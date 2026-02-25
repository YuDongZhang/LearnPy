# 第十八章：测试与调试

## 本章目标
- 掌握 Python 单元测试 (unittest)
- 学会使用 pytest 测试框架
- 掌握代码调试技巧
- 了解代码质量工具

---

## 1. 为什么需要测试

- 确保代码正确性
- 防止回归（修改代码后不影响原有功能）
- 提高代码可维护性
- 文档化代码行为

---

## 2. unittest 单元测试

Python 内置的单元测试框架：

```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
    
    def test_divide(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0
```

---

## 3. pytest 测试框架

更简洁、功能更强大的测试框架：

```python
def test_add():
    assert 1 + 1 == 2

def test_list():
    assert len([1, 2, 3]) == 3
```

---

## 4. 调试技巧

- print 调试法
- logging 日志
- pdb 交互式调试
- IDE 调试器

---

## 5. 示例文件

| 文件 | 内容 |
|------|------|
| `unittest_demo.py` | unittest 单元测试基础 |
| `pytest_demo.py` | pytest 框架使用 |
| `debug_tips.py` | 调试技巧与工具 |

---

## 上一章 | 下一章

[第十七章：异步编程](../17_异步编程/README.md) | [第十九章：项目实战](../19_项目实战/README.md)
