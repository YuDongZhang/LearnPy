"""
变量作用域
==========

变量的可见范围称为作用域。
- 局部变量：函数内部定义，只能在函数内使用
- 全局变量：函数外部定义，可以在任何地方使用
"""

print("=" * 40)
print("1. 局部变量")
print("=" * 40)

def my_function():
    local_var = 100
    print(f"函数内部: local_var = {local_var}")

my_function()

print("-" * 40)

print("函数外部无法访问局部变量:")
print("print(local_var)  # 这会报错！")

print()
print("=" * 40)
print("2. 全局变量")
print("=" * 40)

global_var = "我是全局变量"

def print_global():
    print(f"函数内访问全局变量: {global_var}")

print_global()
print(f"函数外访问全局变量: {global_var}")

print()
print("=" * 40)
print("3. 局部变量与全局变量同名")
print("=" * 40)

x = 10

def func():
    x = 20
    print(f"函数内 x = {x}")

func()
print(f"函数外 x = {x}")

print()
print("=" * 40)
print("4. global 关键字")
print("=" * 40)

count = 0

def increment():
    global count
    count += 1
    print(f"函数内 count = {count}")

print(f"初始 count = {count}")
increment()
increment()
increment()
print(f"最终 count = {count}")

print()
print("=" * 40)
print("5. nonlocal 关键字")
print("=" * 40)

def outer():
    x = "外层变量"
    
    def inner():
        nonlocal x
        x = "内层修改后的变量"
        print(f"内层函数: {x}")
    
    print(f"调用内层前: {x}")
    inner()
    print(f"调用内层后: {x}")

outer()

print()
print("=" * 40)
print("6. 作用域规则 (LEGB)")
print("=" * 40)

print("Python 查找变量的顺序 (LEGB):")
print("1. L (Local) - 局部作用域")
print("2. E (Enclosing) - 嵌套作用域")
print("3. G (Global) - 全局作用域")
print("4. B (Built-in) - 内置作用域")

print("-" * 40)

x = "全局"

def outer_func():
    x = "嵌套"
    
    def inner_func():
        x = "局部"
        print(f"内层函数 x = {x}")
    
    inner_func()
    print(f"外层函数 x = {x}")

outer_func()
print(f"全局 x = {x}")

print()
print("=" * 40)
print("7. 实际应用示例")
print("=" * 40)

total_score = 0
count = 0

def add_score(score):
    global total_score, count
    total_score += score
    count += 1

def get_average():
    global total_score, count
    if count == 0:
        return 0
    return total_score / count

print("计算平均分:")
add_score(85)
add_score(92)
add_score(78)

print(f"总分: {total_score}")
print(f"人数: {count}")
print(f"平均分: {get_average():.1f}")

print()
print("=" * 40)
print("8. 最佳实践")
print("=" * 40)

print("建议:")
print("1. 尽量避免使用全局变量")
print("2. 函数应该通过参数接收数据，通过返回值输出结果")
print("3. 保持函数的独立性和可测试性")

print("-" * 40)

print("不推荐:")
print("total = 0")
print("def add(x):")
print("    global total")
print("    total += x")

print()
print("推荐:")
print("def add(x, total):")
print("    return total + x")
