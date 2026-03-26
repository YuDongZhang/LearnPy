# 第4节：Skill的注册和使用

本节介绍如何注册Skill以及如何在AI助手中使用它。

---

## Skill注册系统

### 什么是注册？

注册就像把Skill"安装"到系统中，让AI能够找到并使用它。

```
┌─────────────────────────────────────────────┐
│              Skill注册表                     │
├─────────────────────────────────────────────┤
│  Skill名称    │ 处理函数    │  描述        │
│  ─────────────────────────────────────────  │
│  to_uppercase │ handler_1   │ 转大写       │
│  calculator   │ handler_2   │ 计算器       │
│  code_review  │ handler_3   │ 代码审查     │
└─────────────────────────────────────────────┘
```

---

## 注册系统实现

```python
# skill_registry.py
"""
Skill注册系统
功能：管理Skill的注册、查找和调用
"""

class SkillRegistry:
    """
    Skill注册表类
    
    负责：
    - 注册新的Skill
    - 查找Skill
    - 调用Skill
    - 列出所有Skill
    """
    
    def __init__(self):
        """
        初始化注册表
        创建两个字典：
        - skills: 存储处理函数 {name: handler}
        - metadata: 存储元数据 {name: info}
        """
        self.skills = {}      # Skill名称 -> 处理函数
        self.metadata = {}    # Skill名称 -> 元数据
    
    def register(self, name, handler, description="", category="general", tags=None):
        """
        注册一个Skill
        
        参数:
            name: Skill名称（唯一标识）
            handler: 处理函数（ callable，接收params，返回结果）
            description: Skill描述
            category: 分类（如 "text", "code", "data"）
            tags: 标签列表
        
        返回:
            无
        
        示例:
            registry.register(
                "to_uppercase",
                to_uppercase_handler,
                "将文本转换为大写",
                "text",
                ["转换", "文本"]
            )
        """
        # 保存处理函数
        self.skills[name] = handler
        
        # 保存元数据
        self.metadata[name] = {
            "name": name,
            "description": description,
            "category": category,
            "tags": tags or []
        }
        
        print(f"✓ 已注册 Skill: {name}")
    
    def get(self, name):
        """
        根据名称获取Skill
        
        参数:
            name: Skill名称
        
        返回:
            处理函数，如果不存在返回None
        """
        return self.skills.get(name)
    
    def invoke(self, name, params):
        """
        调用Skill执行任务
        
        参数:
            name: Skill名称
            params: 参数字典
        
        返回:
            Skill的执行结果
        
        错误:
            如果Skill不存在，抛出异常
        """
        # 查找Skill
        handler = self.get(name)
        
        if handler is None:
            raise ValueError(f"Skill不存在: {name}")
        
        # 调用处理函数
        return handler(params)
    
    def list_skills(self):
        """
        列出所有已注册的Skill
        
        返回:
            元数据列表
        """
        return list(self.metadata.values())
    
    def search(self, keyword):
        """
        搜索Skill
        
        参数:
            keyword: 关键词
        
        返回:
            匹配的Skill列表
        """
        results = []
        for name, meta in self.metadata.items():
            # 在名称、描述、标签中搜索
            if (keyword.lower() in name.lower() or
                keyword.lower() in meta["description"].lower() or
                any(keyword.lower() in tag.lower() for tag in meta["tags"])):
                results.append(meta)
        return results


# ==================== 使用示例 ====================

# 创建注册表实例
registry = SkillRegistry()

# 定义处理函数
def to_uppercase_handler(params):
    text = params.get("text", "")
    return text.upper()

def calculator_handler(params):
    a = params.get("a", 0)
    b = params.get("b", 0)
    op = params.get("operation", "add")
    
    operations = {
        "add": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "mul": lambda x, y: x * y,
        "div": lambda x, y: x / y if y != 0 else None
    }
    
    result = operations.get(op, lambda x, y: None)(a, b)
    return {"result": result}

# 注册Skills
print("=== 注册Skill ===")
registry.register("to_uppercase", to_uppercase_handler, "文本转大写", "text")
registry.register("calculator", calculator_handler, "简单计算器", "tool")

# 列出Skills
print("\n=== 所有Skills ===")
for skill in registry.list_skills():
    print(f"  - {skill['name']}: {skill['description']}")

# 搜索Skills
print("\n=== 搜索 '文本' ===")
results = registry.search("文本")
for r in results:
    print(f"  - {r['name']}")

# 调用Skill
print("\n=== 调用Skill ===")
result = registry.invoke("to_uppercase", {"text": "hello world"})
print(f"to_uppercase: {result}")

result = registry.invoke("calculator", {"a": 10, "b": 5, "operation": "add"})
print(f"calculator: {result}")
```

---

## AI如何使用Skill

### 流程图

```
用户输入
    │
    ▼
┌─────────────────┐
│   AI分析意图    │
│  "帮我转大写"   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  匹配Skill      │
│  → to_uppercase│
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  提取参数       │
│  "hello" → {   │
│    text: "hello"│
│  }              │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  调用处理函数   │
│  handler(params)│
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  返回结果       │
│  "HELLO"        │
└─────────────────┘
```

### AI调用示例

```python
"""
模拟AI调用Skill的过程
"""

def ai_process_request(user_input, registry):
    """
    AI处理用户请求
    
    参数:
        user_input: 用户的自然语言输入
        registry: Skill注册表
    
    返回:
        处理结果
    """
    
    # ==================== 第1步：意图分析 ====================
    # 这里简化为关键词匹配，实际AI会用更复杂的逻辑
    intent_mapping = {
        "大写": {"skill": "to_uppercase", "param_key": "text"},
        "转大写": {"skill": "to_uppercase", "param_key": "text"},
        "计算": {"skill": "calculator", "param_keys": ["a", "b", "operation"]},
    }
    
    matched_intent = None
    for keyword, intent in intent_mapping.items():
        if keyword in user_input:
            matched_intent = intent
            break
    
    if matched_intent is None:
        return "抱歉，我听不懂"
    
    # ==================== 第2步：提取参数 ====================
    # 从用户输入中提取参数（这里简化处理）
    # 实际应用中，AI会理解整个句子的语义
    params = {}
    
    if matched_intent["skill"] == "to_uppercase":
        # 提取要转换的文本
        # 用户说"把hello转大写"，提取"hello"
        text = user_input.replace("大写", "").replace("转", "").strip()
        params = {"text": text}
    
    elif matched_intent["skill"] == "calculator":
        # 提取数字和操作
        params = {"a": 10, "b": 5, "operation": "add"}
    
    # ==================== 第3步：调用Skill ====================
    skill_name = matched_intent["skill"]
    result = registry.invoke(skill_name, params)
    
    return result


# 测试
print("=== AI处理请求 ===")
print(ai_process_request("把hello转大写", registry))
# 输出: "HELLO"

print(ai_process_request("计算10+5", registry))
# 输出: {'result': 15}
```

---

## 总结

### 注册流程

```
1. 定义处理函数
   ↓
2. 创建注册表实例
   ↓
3. 调用 register() 注册
   ↓
4. AI通过 invoke() 调用
```

### 关键方法

| 方法 | 作用 |
|------|------|
| register() | 注册新Skill |
| get() | 获取Skill处理函数 |
| invoke() | 调用Skill执行 |
| list_skills() | 列出所有Skill |
| search() | 搜索Skill |

---

## 下一节

[第5节：真实世界Skill示例](skill_05_real_world.md)
