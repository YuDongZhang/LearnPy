"""
自定义异常
==========

创建自己的异常类，用于特定的错误场景。
继承 Exception 或其子类。
"""

print("=" * 40)
print("1. 创建自定义异常")
print("=" * 40)

class MyError(Exception):
    pass

try:
    raise MyError("这是一个自定义错误")
except MyError as e:
    print(f"捕获自定义异常: {e}")

print()
print("=" * 40)
print("2. 添加属性的异常")
print("=" * 40)

class InsufficientBalanceError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.message = f"余额不足: 当前余额 {balance}, 需要 {amount}"
        super().__init__(self.message)

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(balance, amount)
    return balance - amount

print("测试自定义异常:")
try:
    withdraw(100, 150)
except InsufficientBalanceError as e:
    print(f"  错误: {e}")
    print(f"  当前余额: {e.balance}")
    print(f"  需要金额: {e.amount}")

print()
print("=" * 40)
print("3. 异常层级")
print("=" * 40)

class AppError(Exception):
    """应用程序基础异常"""
    pass

class DatabaseError(AppError):
    """数据库相关异常"""
    pass

class ConnectionError(DatabaseError):
    """连接异常"""
    pass

class QueryError(DatabaseError):
    """查询异常"""
    pass

print("异常层级结构:")
print("  Exception")
print("    └── AppError")
print("          └── DatabaseError")
print("                ├── ConnectionError")
print("                └── QueryError")

print("-" * 40)

print("测试异常层级:")
try:
    raise ConnectionError("无法连接数据库")
except DatabaseError as e:
    print(f"  作为 DatabaseError 捕获: {e}")

try:
    raise QueryError("SQL 语法错误")
except AppError as e:
    print(f"  作为 AppError 捕获: {e}")

print()
print("=" * 40)
print("4. 实际应用：用户管理")
print("=" * 40)

class UserError(Exception):
    """用户相关异常基类"""
    pass

class UserNotFoundError(UserError):
    """用户不存在"""
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"用户不存在: {user_id}")

class UserAlreadyExistsError(UserError):
    """用户已存在"""
    def __init__(self, username):
        self.username = username
        super().__init__(f"用户名已存在: {username}")

class InvalidPasswordError(UserError):
    """密码无效"""
    def __init__(self, reason="密码不符合要求"):
        super().__init__(reason)

users = {}

def register(username, password):
    if username in users:
        raise UserAlreadyExistsError(username)
    if len(password) < 6:
        raise InvalidPasswordError("密码长度至少6位")
    users[username] = password
    return True

def login(username, password):
    if username not in users:
        raise UserNotFoundError(username)
    if users[username] != password:
        raise InvalidPasswordError("密码错误")
    return True

print("测试用户管理:")
test_cases = [
    ("register", "张三", "123456"),
    ("register", "张三", "abcdef"),
    ("register", "李四", "abc"),
    ("login", "王五", "123456"),
    ("login", "张三", "wrong"),
    ("login", "张三", "123456"),
]

for action, username, password in test_cases:
    try:
        if action == "register":
            register(username, password)
            print(f"  注册成功: {username}")
        else:
            login(username, password)
            print(f"  登录成功: {username}")
    except UserError as e:
        print(f"  操作失败: {e}")

print()
print("=" * 40)
print("5. 实际应用：文件处理")
print("=" * 40)

class FileProcessingError(Exception):
    """文件处理异常"""
    def __init__(self, filename, reason):
        self.filename = filename
        self.reason = reason
        super().__init__(f"处理文件 {filename} 失败: {reason}")

class InvalidFormatError(FileProcessingError):
    """格式无效"""
    def __init__(self, filename, expected_format):
        super().__init__(filename, f"期望格式: {expected_format}")

class FileTooLargeError(FileProcessingError):
    """文件过大"""
    def __init__(self, filename, size, max_size):
        super().__init__(filename, f"文件大小 {size} 超过限制 {max_size}")

def process_file(filename, size, format_type):
    if size > 1000:
        raise FileTooLargeError(filename, size, 1000)
    if format_type != "json":
        raise InvalidFormatError(filename, "json")
    return True

print("测试文件处理:")
test_files = [
    ("data.json", 500, "json"),
    ("data.xml", 500, "xml"),
    ("large.json", 2000, "json"),
]

for filename, size, fmt in test_files:
    try:
        process_file(filename, size, fmt)
        print(f"  处理成功: {filename}")
    except FileProcessingError as e:
        print(f"  处理失败: {e}")

print()
print("=" * 40)
print("6. 最佳实践")
print("=" * 40)

print("1. 异常类名以 Error 结尾")
print("2. 继承合适的父类")
print("3. 添加有意义的属性和方法")
print("4. 提供清晰的错误信息")
print("5. 保持异常层级简单")

print("-" * 40)

print("好的示例:")
print("class PaymentError(Exception):")
print("    def __init__(self, order_id, reason):")
print("        self.order_id = order_id")
print("        super().__init__(f'订单 {order_id} 支付失败: {reason}')")
