"""
unittest 单元测试基础
====================

unittest 是 Python 内置的单元测试框架。
"""

print("=" * 50)
print("1. 基础测试用例")
print("=" * 50)

import unittest

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

class TestMathFunctions(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(1, 2), 3)
    
    def test_add_negative(self):
        self.assertEqual(add(-1, -2), -3)
    
    def test_add_mixed(self):
        self.assertEqual(add(-1, 2), 1)
    
    def test_divide_normal(self):
        self.assertEqual(divide(10, 2), 5)
    
    def test_divide_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

print("定义测试类: TestMathFunctions")
print("包含 5 个测试方法")

print()
print("=" * 50)
print("2. 断言方法")
print("=" * 50)

class TestAssertions(unittest.TestCase):
    def test_assert_equal(self):
        self.assertEqual(1 + 1, 2)
    
    def test_assert_not_equal(self):
        self.assertNotEqual(1 + 1, 3)
    
    def test_assert_true(self):
        self.assertTrue(1 < 2)
    
    def test_assert_false(self):
        self.assertFalse(1 > 2)
    
    def test_assert_is_none(self):
        self.assertIsNone(None)
    
    def test_assert_is_not_none(self):
        self.assertIsNotNone("hello")
    
    def test_assert_in(self):
        self.assertIn(1, [1, 2, 3])
    
    def test_assert_not_in(self):
        self.assertNotIn(5, [1, 2, 3])
    
    def test_assert_is_instance(self):
        self.assertIsInstance("hello", str)
    
    def test_assert_raises(self):
        with self.assertRaises(ValueError):
            int("abc")

print("常用断言方法:")
print("  assertEqual(a, b)       - a == b")
print("  assertTrue(x)           - x is True")
print("  assertIsNone(x)        - x is None")
print("  assertIn(a, b)         - a in b")
print("  assertIsInstance(a, b) - isinstance(a, b)")
print("  assertRaises(e)        - 抛出异常 e")

print()
print("=" * 50)
print("3. setUp 和 tearDown")
print("=" * 50)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        print("setUp: 初始化数据库连接...")
        self.data = []
    
    def tearDown(self):
        print("tearDown: 关闭数据库连接...")
    
    def test_insert(self):
        self.data.append("record1")
        self.assertEqual(len(self.data), 1)
        print("插入记录成功")
    
    def test_delete(self):
        self.data.append("record1")
        self.data.pop()
        self.assertEqual(len(self.data), 0)
        print("删除记录成功")

print("setUp: 每个测试方法前执行")
print("tearDown: 每个测试方法后执行")

print()
print("=" * 50)
print("4. 测试跳过和预期失败")
print("=" * 50)

class TestSkips(unittest.TestCase):
    @unittest.skip("跳过此测试")
    def test_skipped(self):
        self.fail("不应该执行")
    
    @unittest.skipIf(True, "条件为真时跳过")
    def test_skip_if(self):
        pass
    
    @unittest.skipUnless(False, "条件为假时跳过")
    def test_skip_unless(self):
        pass
    
    @unittest.expectedFailure
    def test_expected_fail(self):
        self.assertEqual(1, 2)

print("跳过装饰器:")
print("  @unittest.skip(reason)        - 无条件跳过")
print("  @unittest.skipIf(cond, reason) - 条件为真时跳过")
print("  @unittest.skipUnless(cond)    - 条件为假时跳过")
print("  @unittest.expectedFailure     - 预期失败")

print()
print("=" * 50)
print("5. 测试套件")
print("=" * 50)

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")
    
    def test_lower(self):
        self.assertEqual("HELLO".lower(), "hello")
    
    def test_strip(self):
        self.assertEqual("  hello  ".strip(), "hello")
    
    def test_split(self):
        self.assertEqual("a,b,c".split(","), ["a", "b", "c"])

print("创建测试套件:")
print("  suite = unittest.TestSuite()")
print("  suite.addTest(TestStringMethods('test_upper'))")
print("  unittest.TextTestRunner(verbosity=2).run(suite)")

print()
print("=" * 50)
print("6. 运行测试")
print("=" * 50)

print("运行方式:")
print("  1. 直接运行: python -m unittest test_module.py")
print("  2. 运行所有: python -m unittest discover")
print("  3. 指定文件: python -m unittest test_file.TestClass.test_method")
print("  4. 详细输出: python -m unittest -v test_module.py")

print("\n实际运行示例:")
loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestMathFunctions)
runner = unittest.TextTestRunner(verbosity=0)
runner.run(suite)
