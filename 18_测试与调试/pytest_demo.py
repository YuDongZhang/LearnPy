"""
pytest 测试框架
==============

pytest 是更简洁、功能更强大的 Python 测试框架。
需要先安装: pip install pytest
"""

print("=" * 50)
print("1. 基础测试")
print("=" * 50)

def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_strings():
    assert add("hello", "world") == "helloworld"

print("pytest 特点:")
print("  - 不需要继承任何类")
print("  - 测试函数以 test_ 开头")
print("  - 使用 assert 语句而不是 assertEqual")

print()
print("=" * 50)
print("2. 断言")
print("=" * 50)

def test_assertions():
    assert 1 + 1 == 2
    assert 1 + 1 != 3
    assert "hello" in "hello world"
    assert [1, 2] == [1, 2]
    assert {"a": 1} == {"a": 1}

def test_assert_with_message():
    x = 1
    y = 2
    assert x == y, f"期望 {x} == {y}"

print("断言特点:")
print("  - 使用原生 assert 语句")
print("  - 失败时自动显示详细信息")
print("  - 支持自定义错误消息")

print()
print("=" * 50)
print("3. fixture (夹具)")
print("=" * 50)

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, n):
        self.result += n
        return self
    
    def subtract(self, n):
        self.result -= n
        return self
    
    def get_result(self):
        return self.result

print("fixture 示例:")
print("""
import pytest

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    calculator.add(5)
    assert calculator.get_result() == 5

def test_chained(calculator):
    calculator.add(10).subtract(3)
    assert calculator.get_result() == 7
""")

print()
print("=" * 50)
print("4. 参数化测试")
print("=" * 50)

print("参数化示例:")
print("""
import pytest

@pytest.mark.parametrize('a,b,expected', [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
""")

def add(a, b):
    return a + b

test_cases = [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, 20, 30),
]

print("手动模拟参数化测试:")
for a, b, expected in test_cases:
    result = add(a, b)
    status = "✓" if result == expected else "✗"
    print(f"  {status} add({a}, {b}) = {result}, expected = {expected}")

print()
print("=" * 50)
print("5. 标记 (markers)")
print("=" * 50)

print("常用标记:")
print("  @pytest.mark.skip      - 跳过测试")
print("  @pytest.mark.skipif   - 条件跳过")
print("  @pytest.mark.xfail    - 预期失败")
print("  @pytest.mark.slow     - 慢速测试")
print("  @pytest.mark.unit     - 单元测试")
print("  @pytest.mark.integration - 集成测试")

print()
print("=" * 50)
print("6. 模拟对象 (mock)")
print("=" * 50)

print("Mock 示例:")
print("""
from unittest.mock import Mock, patch

def get_user(user_id):
    # 模拟 API 调用
    return {'id': user_id, 'name': '张三'}

def test_get_user():
    mock_api = Mock(return_value={'id': 1, 'name': '李四'})
    result = mock_api(1)
    assert result['name'] == '李四'
""")

print()
print("=" * 50)
print("7. 断言异常")
print("=" * 50)

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)

print("断言异常方式:")
print("  with pytest.raises(ExceptionType):")
print("      code_that_raises_exception()")

print("\n手动测试:")
try:
    divide(10, 0)
except ValueError as e:
    print(f"  ✓ 正确抛出异常: {e}")

print()
print("=" * 50)
print("8. 断言警告")
print("=" * 50)

import warnings

def deprecated_function():
    warnings.warn("此函数已弃用", DeprecationWarning)
    return "结果"

print("断言警告:")
print("  import pytest")
print("  with pytest.warns(WarningType):")
print("      function_that_warns()")

print("\n手动测试:")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    deprecated_function()
    if len(w) == 1:
        print(f"  ✓ 捕获到警告: {w[0].message}")

print()
print("=" * 50)
print("9. 测试覆盖率")
print("=" * 50)

print("覆盖率工具: pytest-cov")
print("  安装: pip install pytest-cov")
print("  运行: pytest --cov=myapp tests/")
print("  报告: pytest --cov=myapp --cov-report=html")

print()
print("=" * 50)
print("10. pytest 配置文件")
print("=" * 50)

print("pytest.ini 或 pyproject.toml:")
print("""
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
""")

print()
print("=" * 50)
print("11. 运行命令")
print("=" * 50)

print("常用命令:")
print("  pytest              - 运行当前目录所有测试")
print("  pytest file.py     - 运行指定文件")
print("  pytest -v          - 详细输出")
print("  pytest -k 'test_name' - 按名称过滤")
print("  pytest --collect-only - 只收集测试，不运行")
print("  pytest -x           - 遇到第一个失败就停止")
print("  pytest --lf         - 只运行上次失败的测试")
