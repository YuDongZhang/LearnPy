# 第5节：真实世界Skill示例

本节展示几个真实可用的Skill示例，帮助你理解如何编写实用的Skill。

---

## Skill 1：文本摘要

### 场景
让AI学会 summarizing 长文本为短摘要。

### 代码实现

```python
# skill_text_summarizer.py
"""
文本摘要Skill
功能：将长文本压缩成简短摘要
"""

def summarize_handler(params):
    """
    文本摘要处理函数
    
    参数:
        params 字典:
            - text: 要摘要的文本 (必需)
            - max_length: 最大长度，默认 100 字符
            - style: 摘要风格 ("brief" 简短 | "detailed" 详细)
    
    返回:
        字典:
            - success: 是否成功
            - summary: 摘要文本
            - original_length: 原文长度
            - summary_length: 摘要长度
    """
    
    # ==================== 第1步：获取参数 ====================
    text = params.get("text", "")
    max_length = params.get("max_length", 100)
    style = params.get("style", "brief")
    
    # ==================== 第2步：验证参数 ====================
    if not text:
        return {
            "success": False,
            "error": "文本不能为空"
        }
    
    # ==================== 第3步：处理逻辑 ====================
    # 简单的摘要逻辑：
    # 1. 按句子分割
    # 2. 提取关键词
    # 3. 组合摘要
    
    # 清理文本
    text = text.strip()
    original_length = len(text)
    
    # 简单分句（按句号、问号、感叹号分割）
    sentences = []
    current = ""
    for char in text:
        current += char
        if char in "。.!?！?":
            if current.strip():
                sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    
    # 根据风格选择句子
    if style == "brief":
        # 简短模式：只取第一句和最后一句
        if len(sentences) >= 2:
            summary_sentences = [sentences[0], sentences[-1]]
        else:
            summary_sentences = sentences[:1]
    else:
        # 详细模式：取前几句
        summary_sentences = sentences[:3]
    
    # 组合摘要
    summary = "，".join(summary_sentences)
    
    # 截断到最大长度
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."
    
    # ==================== 第4步：返回结果 ====================
    return {
        "success": True,
        "summary": summary,
        "original_length": original_length,
        "summary_length": len(summary),
        "sentence_count": len(sentences),
        "style": style
    }


# ==================== 测试 ====================

# 测试用例
test_cases = [
    {
        "name": "简短摘要",
        "params": {
            "text": "今天天气很好。阳光明媚。适合外出游玩。我去了公园。",
            "style": "brief"
        }
    },
    {
        "name": "详细摘要",
        "params": {
            "text": "今天天气很好。阳光明媚。适合外出游玩。我去了公园。",
            "style": "detailed"
        }
    },
    {
        "name": "自定义长度",
        "params": {
            "text": "Python是一种高级编程语言。它简单易学。功能强大。应用广泛。",
            "max_length": 30
        }
    }
]

print("=== 文本摘要Skill测试 ===\n")
for case in test_cases:
    print(f"测试: {case['name']}")
    print(f"输入: {case['params']['text'][:50]}...")
    result = summarize_handler(case["params"])
    print(f"输出: {result['summary']}")
    print(f"原文长度: {result['original_length']} → 摘要长度: {result['summary_length']}")
    print("-" * 40)
```

---

## Skill 2：代码审查

### 场景
自动审查代码质量问题。

```python
# skill_code_reviewer.py
"""
代码审查Skill
功能：检查代码质量、安全问题、风格问题
"""

def code_review_handler(params):
    """
    代码审查处理函数
    
    参数:
        params 字典:
            - code: 要审查的代码 (必需)
            - language: 编程语言，默认 "python"
            - strictness: 严格程度 "strict" | "normal" | "lenient"
    
    返回:
        字典:
            - success: 是否成功
            - score: 评分 0-100
            - issues: 问题列表
            - suggestions: 建议列表
    """
    
    # ==================== 第1步：获取参数 ====================
    code = params.get("code", "")
    language = params.get("language", "python")
    strictness = params.get("strictness", "normal")
    
    # ==================== 第2步：验证参数 ====================
    if not code:
        return {
            "success": False,
            "error": "代码不能为空"
        }
    
    # ==================== 第3步：审查逻辑 ====================
    issues = []      # 发现的问题
    suggestions = [] # 改进建议
    score = 100      # 初始分数
    
    # Python代码审查规则
    if language == "python":
        
        # 规则1：检查裸except
        if "except:" in code:
            issues.append({
                "type": "error",
                "line": "unknown",
                "message": "使用裸 except 语句",
                "rule": "PEP 8 - E722"
            })
            score -= 10
        
        # 规则2：检查硬编码密码
        import re
        if re.search(r'password\s*=\s*["\']', code, re.IGNORECASE):
            issues.append({
                "type": "error",
                "line": "unknown",
                "message": "检测到硬编码密码",
                "rule": "安全最佳实践"
            })
            score -= 15
        
        # 规则3：检查魔法数字
        if re.search(r'\s+=\s+\d+', code):
            issues.append({
                "type": "warning",
                "line": "unknown",
                "message": "检测到魔法数字，建议使用常量",
                "rule": "PEP 8 - E225"
            })
            score -= 5
        
        # 规则4：检查 eval() 使用
        if "eval(" in code:
            issues.append({
                "type": "error",
                "line": "unknown",
                "message": "使用 eval() 存在安全风险",
                "rule": "安全最佳实践"
            })
            score -= 15
        
        # 规则5：检查过长的函数
        lines = code.split('\n')
        if len(lines) > 100:
            issues.append({
                "type": "warning",
                "line": "unknown",
                "message": f"函数过长 ({len(lines)} 行)，建议拆分",
                "rule": "代码可读性"
            })
            score -= 5
        
        # 规则6：检查缺少文档字符串
        if '"""' not in code and "'''" not in code:
            if strictness == "strict" or strictness == "normal":
                suggestions.append("建议添加文档字符串 (docstring)")
    
    # JavaScript代码审查规则
    elif language == "javascript":
        
        # 检查 console.log
        if "console.log" in code:
            issues.append({
                "type": "warning",
                "line": "unknown",
                "message": "检测到 console.log，生产环境应移除",
                "rule": "最佳实践"
            })
            score -= 3
        
        # 检查 innerHTML
        if "innerHTML" in code:
            issues.append({
                "type": "error",
                "line": "unknown",
                "message": "innerHTML 可能导致 XSS 攻击",
                "rule": "安全最佳实践"
            })
            score -= 15
        
        # 检查 var
        if "var " in code:
            suggestions.append("建议使用 let 或 const 代替 var")
    
    # ==================== 第4步：限制分数范围 ====================
    score = max(0, min(100, score))
    
    # ==================== 第5步：返回结果 ====================
    return {
        "success": True,
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "language": language,
        "strictness": strictness,
        "total_lines": len(code.split('\n'))
    }


# ==================== 测试 ====================

print("=== 代码审查Skill测试 ===\n")

# 测试有问题的代码
bad_code = '''
def process_data(items):
    try:
        eval(items)
    except:
        pass
    
    password = "secret123"
    
    result = 0
    for i in range(100):
        result = result + i * 7
'''

print("审查有问题的代码:")
result = code_review_handler({"code": bad_code, "language": "python"})
print(f"评分: {result['score']}/100")
print(f"发现 {len(result['issues'])} 个问题:")
for issue in result['issues']:
    print(f"  [{issue['type']}] {issue['message']}")
print(f"建议: {result['suggestions']}")

print("\n" + "="*40 + "\n")

# 测试好的代码
good_code = '''
def calculate_sum(numbers):
    """计算数字列表的总和"""
    total = 0
    for num in numbers:
        total += num
    return total
'''

print("审查好的代码:")
result = code_review_handler({"code": good_code, "language": "python"})
print(f"评分: {result['score']}/100")
print(f"发现 {len(result['issues'])} 个问题")
print(f"建议: {result['suggestions']}")
```

---

## Skill 3：数据处理

### 场景
处理和分析数据。

```python
# skill_data_processor.py
"""
数据处理Skill
功能：统计分析、数据转换、数据验证
"""

def data_processor_handler(params):
    """
    数据处理处理函数
    
    参数:
        params 字典:
            - data: 数据 (列表或字典)
            - operation: 操作类型
                - "stats": 统计
                - "validate": 验证
                - "transform": 转换
                - "filter": 过滤
            - options: 操作选项
    
    返回:
        字典:
            - success: 是否成功
            - result: 处理结果
    """
    
    # ==================== 第1步：获取参数 ====================
    data = params.get("data")
    operation = params.get("operation", "stats")
    options = params.get("options", {})
    
    # ==================== 第2步：验证数据 ====================
    if data is None:
        return {
            "success": False,
            "error": "数据不能为空"
        }
    
    # ==================== 第3步：根据操作类型处理 ====================
    
    # ----- 操作1: 统计 (stats) -----
    if operation == "stats":
        if not isinstance(data, list):
            return {
                "success": False,
                "error": "stats操作需要列表类型数据"
            }
        
        if not data:
            return {
                "success": True,
                "result": {"message": "空列表"}
            }
        
        # 计算统计信息
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        
        if not numeric_data:
            return {
                "success": True,
                "result": {"message": "没有数值数据"}
            }
        
        sorted_data = sorted(numeric_data)
        n = len(sorted_data)
        
        result = {
            "count": n,
            "sum": sum(numeric_data),
            "mean": sum(numeric_data) / n,
            "median": sorted_data[n // 2] if n % 2 else 
                     (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2,
            "min": min(numeric_data),
            "max": max(numeric_data),
            "range": max(numeric_data) - min(numeric_data),
            "variance": sum((x - sum(numeric_data)/n) ** 2 for x in numeric_data) / n,
        }
        
        return {"success": True, "result": result}
    
    # ----- 操作2: 验证 (validate) -----
    elif operation == "validate":
        if not isinstance(data, dict):
            return {
                "success": False,
                "error": "validate操作需要字典类型数据"
            }
        
        # 验证规则
        rules = options.get("rules", {})
        errors = []
        
        for field, rule in rules.items():
            if field not in data:
                if rule.get("required", False):
                    errors.append(f"缺少必需字段: {field}")
                continue
            
            value = data[field]
            
            # 类型检查
            expected_type = rule.get("type")
            if expected_type:
                type_map = {
                    "string": str,
                    "number": (int, float),
                    "integer": int,
                    "boolean": bool,
                    "list": list,
                    "dict": dict
                }
                expected = type_map.get(expected_type)
                if expected and not isinstance(value, expected):
                    errors.append(f"字段 {field} 类型错误，期望 {expected_type}")
            
            # 范围检查
            if isinstance(value, (int, float)):
                if "min" in rule and value < rule["min"]:
                    errors.append(f"字段 {field} 小于最小值 {rule['min']}")
                if "max" in rule and value > rule["max"]:
                    errors.append(f"字段 {field} 大于最大值 {rule['max']}")
            
            # 枚举检查
            if "enum" in rule and value not in rule["enum"]:
                errors.append(f"字段 {field} 必须是 {rule['enum']} 之一")
        
        return {
            "success": len(errors) == 0,
            "result": {
                "valid": len(errors) == 0,
                "errors": errors
            }
        }
    
    # ----- 操作3: 转换 (transform) -----
    elif operation == "transform":
        transform_type = options.get("type", "normalize")
        
        if not isinstance(data, list):
            return {
                "success": False,
                "error": "transform操作需要列表类型数据"
            }
        
        if transform_type == "normalize":
            # 归一化：将数据缩放到0-1范围
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            if not numeric_data:
                return {"success": False, "error": "没有数值数据"}
            
            min_val = min(numeric_data)
            max_val = max(numeric_data)
            range_val = max_val - min_val
            
            if range_val == 0:
                return {"success": True, "result": [0.5] * len(data)}
            
            result = []
            for x in data:
                if isinstance(x, (int, float)):
                    result.append((x - min_val) / range_val)
                else:
                    result.append(x)
            
            return {"success": True, "result": result}
        
        elif transform_type == "log":
            # 对数变换
            import math
            result = []
            for x in data:
                if isinstance(x, (int, float)) and x > 0:
                    result.append(math.log(x))
                else:
                    result.append(x)
            return {"success": True, "result": result}
        
        return {"success": False, "error": f"未知转换类型: {transform_type}"}
    
    # ----- 操作4: 过滤 (filter) -----
    elif operation == "filter":
        if not isinstance(data, list):
            return {
                "success": False,
                "error": "filter操作需要列表类型数据"
            }
        
        condition = options.get("condition", "positive")
        
        if condition == "positive":
            # 过滤正数
            result = [x for x in data if isinstance(x, (int, float)) and x > 0]
        elif condition == "negative":
            # 过滤负数
            result = [x for x in data if isinstance(x, (int, float)) and x < 0]
        elif condition == "nonzero":
            # 过滤非零
            result = [x for x in data if x != 0]
        elif condition == "even":
            # 过滤偶数
            result = [x for x in data if isinstance(x, int) and x % 2 == 0]
        else:
            return {"success": False, "error": f"未知过滤条件: {condition}"}
        
        return {
            "success": True,
            "result": result,
            "original_count": len(data),
            "filtered_count": len(result)
        }
    
    # 未知操作
    return {
        "success": False,
        "error": f"未知操作: {operation}"
    }


# ==================== 测试 ====================

print("=== 数据处理Skill测试 ===\n")

# 测试统计
print("1. 统计操作:")
result = data_processor_handler({
    "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "operation": "stats"
})
print(f"   输入: [1-10]")
print(f"   结果: {result['result']}")

print("\n2. 验证操作:")
result = data_processor_handler({
    "data": {"name": "张三", "age": 25, "score": 95},
    "operation": "validate",
    "options": {
        "rules": {
            "name": {"type": "string", "required": True},
            "age": {"type": "number", "min": 0, "max": 150},
            "score": {"type": "number", "min": 0, "max": 100}
        }
    }
})
print(f"   数据: {{name, age, score}}")
print(f"   结果: {result['result']}")

print("\n3. 转换操作:")
result = data_processor_handler({
    "data": [1, 2, 3, 4, 5],
    "operation": "transform",
    "options": {"type": "normalize"}
})
print(f"   输入: [1,2,3,4,5]")
print(f"   归一化: {result['result']}")

print("\n4. 过滤操作:")
result = data_processor_handler({
    "data": [1, -2, 3, -4, 5, -6],
    "operation": "filter",
    "options": {"condition": "positive"}
})
print(f"   输入: [1,-2,3,-4,5,-6]")
print(f"   过滤正数: {result['result']}")
```

---

## 总结

### 本节学的Skill

| Skill | 功能 | 难度 |
|-------|------|------|
| 文本摘要 | 长文本压缩 | ⭐ |
| 代码审查 | 质量检查 | ⭐⭐ |
| 数据处理 | 统计/验证/转换 | ⭐⭐ |

### 编写要点

```
1. 明确输入输出格式
2. 做好参数验证
3. 错误情况要处理
4. 返回结果要统一
```

---

## 下一节

[第6节：Skill组合使用](skill_06_composition.md)
