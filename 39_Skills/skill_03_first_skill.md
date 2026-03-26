# 第3节：编写第一个简单Skill

本节手把手教你编写第一个Skill，从简单到复杂，逐步掌握Skill的写法。

---

## 最简单的Skill

### 场景
让AI学会把文字转成大写。

### 步骤1：定义Skill结构

```yaml
# skill_to_uppercase.yaml
name: "to_uppercase"
description: "将文本转换为大写"
parameters:
  - name: text
    type: string
    description: "要转换的文本"
    required: true
output:
  type: string
  description: "大写文本"
```

### 步骤2：实现处理逻辑

```python
def to_uppercase_handler(params):
    """
    处理函数：接收参数，返回结果
    
    参数:
        params: 字典，包含输入参数
            - text: 要转换的文本
    
    返回:
        大写后的文本
    """
    # 从params中获取text参数
    text = params.get("text", "")
    
    # 执行转换
    result = text.upper()
    
    # 返回结果
    return result
```

### 步骤3：测试

```python
# 测试用例
params = {"text": "hello world"}
result = to_uppercase_handler(params)
print(result)  # 输出: "HELLO WORLD"
```

---

## 进阶Skill：带验证和错误处理

### 场景
计算两个数的加减乘除。

### 代码实现

```python
# skill_calculator.py
"""
计算器Skill
功能：加减乘除四则运算
"""

def calculator_handler(params):
    """
    计算器处理函数
    
    参数说明:
        params 字典包含:
            - a: 第一个数字 (必需)
            - b: 第二个数字 (必需)
            - operation: 操作类型 (必需)
                可选值: "add", "subtract", "multiply", "divide"
    
    返回:
        字典，包含:
            - result: 计算结果
            - error: 错误信息(如果有)
    """
    
    # ==================== 第1步：获取参数 ====================
    # 使用params.get()安全获取参数，第二个参数是默认值
    a = params.get("a")
    b = params.get("b")
    operation = params.get("operation")
    
    # ==================== 第2步：验证参数 ====================
    # 检查必需参数是否存在
    errors = []
    
    if a is None:
        errors.append("缺少参数 'a'")
    
    if b is None:
        errors.append("缺少参数 'b'")
    
    if operation is None:
        errors.append("缺少参数 'operation'")
    
    # 如果有错误，提前返回
    if errors:
        return {
            "success": False,
            "error": "; ".join(errors)
        }
    
    # ==================== 第3步：类型验证 ====================
    # 确保a和b是数字
    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return {
            "success": False,
            "error": "参数 'a' 和 'b' 必须是数字"
        }
    
    # ==================== 第4步：执行计算 ====================
    result = None
    
    if operation == "add":
        # 加法
        result = a + b
    elif operation == "subtract":
        # 减法
        result = a - b
    elif operation == "multiply":
        # 乘法
        result = a * b
    elif operation == "divide":
        # 除法（注意除零错误）
        if b == 0:
            return {
                "success": False,
                "error": "除数不能为零"
            }
        result = a / b
    else:
        # 未知操作
        return {
            "success": False,
            "error": f"未知操作: {operation}"
        }
    
    # ==================== 第5步：返回结果 ====================
    return {
        "success": True,
        "result": result,
        "operation": operation,
        "a": a,
        "b": b
    }
```

### 测试代码

```python
# 测试各种情况
print("=== 测试加法 ===")
result = calculator_handler({"a": 10, "b": 5, "operation": "add"})
print(result)  # {'success': True, 'result': 15.0, ...}

print("\n=== 测试除法 ===")
result = calculator_handler({"a": 10, "b": 3, "operation": "divide"})
print(result)  # {'success': True, 'result': 3.333..., ...}

print("\n=== 测试除零 ===")
result = calculator_handler({"a": 10, "b": 0, "operation": "divide"})
print(result)  # {'success': False, 'error': '除数不能为零'}

print("\n=== 测试缺少参数 ===")
result = calculator_handler({"a": 10, "operation": "add"})
print(result)  # {'success': False, 'error': '缺少参数 b'}
```

---

## 总结：Skill编写要点

### 核心步骤

```
1. 获取参数 → params.get("参数名")
2. 验证参数 → 检查必需参数、类型、范围
3. 处理业务 → 执行具体逻辑
4. 返回结果 → 统一格式的字典
```

### 错误处理模式

```python
# 标准返回格式
return {
    "success": True/False,
    "result": ...,        # 成功时返回
    "error": ...          # 失败时返回
}
```

### 最佳实践

| 做法 | 说明 |
|------|------|
| 参数验证 | 确保必需参数存在 |
| 类型检查 | 确保类型正确 |
| 错误处理 | 优雅处理异常情况 |
| 清晰返回 | 统一返回格式 |

---

## 下一节

[第4节：Skill的注册和使用](skill_04_registration.md)
