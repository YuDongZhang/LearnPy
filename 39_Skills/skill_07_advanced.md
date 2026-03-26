# 第7节：高级话题

本节介绍Skill的高级话题，包括真实Skill文件格式、Skill商店、Agent与Skill的结合等。

---

## 真实的Skill文件格式

### Claude/Trae使用的SKILL.md格式

当你创建真实的Skill时，需要按照特定格式编写。

```markdown
# Skill名称

## 描述
简要说明这个Skill做什么

## 参数
- param1: 参数1说明
- param2: 参数2说明

## 返回
说明返回什么

## 示例
```
输入: xxx
输出: yyy
```

## 内部提示
（可选）给AI的额外指导
```

### 完整示例：代码审查Skill

```markdown
# code-reviewer

## 描述
审查代码质量，发现潜在问题，提供改进建议。支持Python、JavaScript、Java等语言。

## 参数
- code: 要审查的代码（必需）
- language: 编程语言，默认 "python"（可选）
- strictness: 审查严格程度，可选 "strict", "normal", "lenient"（可选）

## 返回
- score: 代码评分 (0-100)
- issues: 发现的问题列表
- suggestions: 改进建议列表

## 示例
```
输入:
```python
def add(a, b):
    return a + b
```

输出:
{
    "score": 95,
    "issues": [],
    "suggestions": ["建议添加文档字符串"]
}
```

## 内部提示
1. 首先分析代码结构
2. 检查常见安全问题（SQL注入、XSS等）
3. 检查代码风格
4. 给出具体的改进建议
```

---

## Skill商店

### 概念

Skill商店类似于"应用商店"，用户可以：
- 浏览可用的Skills
- 安装需要的Skills
- 评价和分享Skills

### 示例架构

```python
"""
Skill商店系统
"""

class SkillStore:
    """
    Skill商店类
    
    功能：
    - 上传Skill
    - 浏览Skill
    - 下载/安装Skill
    - 评价Skill
    """
    
    def __init__(self):
        """初始化商店"""
        self.skills = {}  # skill_id -> skill_info
        self.ratings = {}  # skill_id -> [rating1, rating2, ...]
    
    def upload(self, skill_id, skill_data, author):
        """
        上传Skill到商店
        
        参数:
            skill_id: Skill唯一ID
            skill_data: Skill定义和数据
            author: 作者名称
        """
        self.skills[skill_id] = {
            **skill_data,
            "author": author,
            "downloads": 0,
            "rating": 0.0,
            "upload_time": "当前时间"
        }
        print(f"✓ Skill '{skill_id}' 已上传到商店")
    
    def browse(self, category=None, sort_by="rating"):
        """
        浏览Skills
        
        参数:
            category: 分类筛选
            sort_by: 排序方式 ("rating", "downloads", "newest")
        
        返回:
            符合条件的Skill列表
        """
        results = list(self.skills.values())
        
        # 分类筛选
        if category:
            results = [s for s in results if s.get("category") == category]
        
        # 排序
        if sort_by == "rating":
            results.sort(key=lambda x: x.get("rating", 0), reverse=True)
        elif sort_by == "downloads":
            results.sort(key=lambda x: x.get("downloads", 0), reverse=True)
        
        return results
    
    def download(self, skill_id):
        """
        下载Skill
        
        参数:
            skill_id: Skill ID
        
        返回:
            Skill数据
        """
        if skill_id not in self.skills:
            raise ValueError(f"Skill不存在: {skill_id}")
        
        # 增加下载计数
        self.skills[skill_id]["downloads"] += 1
        
        return self.skills[skill_id]
    
    def rate(self, skill_id, rating):
        """
        评价Skill
        
        参数:
            skill_id: Skill ID
            rating: 评分 (1-5)
        """
        if skill_id not in self.skills:
            raise ValueError(f"Skill不存在: {skill_id}")
        
        if not (1 <= rating <= 5):
            raise ValueError("评分必须是1-5之间的数字")
        
        # 记录评价
        if skill_id not in self.ratings:
            self.ratings[skill_id] = []
        self.ratings[skill_id].append(rating)
        
        # 计算平均评分
        avg = sum(self.ratings[skill_id]) / len(self.ratings[skill_id])
        self.skills[skill_id]["rating"] = round(avg, 1)
        
        print(f"✓ 已为 '{skill_id}' 评分 {rating} 星")


# ==================== 使用示例 ====================

print("=== Skill商店示例 ===\n")

# 创建商店
store = SkillStore()

# 上传Skills
store.upload("text-uppercase", {
    "name": "text-uppercase",
    "description": "将文本转换为大写",
    "category": "text",
    "handler": "..."
}, "张三")

store.upload("code-reviewer", {
    "name": "code-reviewer", 
    "description": "代码审查工具",
    "category": "code",
    "handler": "..."
}, "李四")

store.upload("data-analyzer", {
    "name": "data-analyzer",
    "description": "数据分析工具",
    "category": "data", 
    "handler": "..."
}, "王五")

# 模拟评价
store.rate("text-uppercase", 5)
store.rate("text-uppercase", 4)
store.rate("code-reviewer", 5)

# 浏览
print("\n按评分排序:")
for skill in store.browse(sort_by="rating"):
    print(f"  - {skill['name']}: {skill['rating']}★ ({skill['downloads']}次下载)")
    print(f"    {skill['description']}")
```

---

## Agent与Skill的结合

### 什么是Agent？

Agent（代理）是一个能自主思考和行动的AI，它可以：
- 理解用户目标
- 规划执行步骤
- 调用各种Skill
- 反思和调整

### Agent架构

```
┌─────────────────────────────────────────────────────────┐
│                     Agent                                │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│  │  理解目标   │ -> │  规划步骤   │ -> │  执行Skill  ││
│  └─────────────┘    └─────────────┘    └─────────────┘│
│         ^                                        │      │
│         │                                        ▼      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│  │  反思结果   │ <- │  评估效果   │    │  Skill注册  ││
│  └─────────────┘    └─────────────┘    └─────────────┘│
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │    用户输入      │
                    │  "帮我审查代码"  │
                    └─────────────────┘
```

### Agent实现示例

```python
"""
Agent与Skill结合示例
"""

class SimpleAgent:
    """
    简单的Agent实现
    
    工作流程：
    1. 理解用户意图
    2. 选择合适的Skill
    3. 调用Skill执行
    4. 返回结果给用户
    """
    
    def __init__(self, name="Assistant"):
        """
        初始化Agent
        
        参数:
            name: Agent名称
        """
        self.name = name
        self.skills = {}  # 注册的Skills
        self.history = []  # 对话历史
    
    def register_skill(self, name, description, handler):
        """
        注册Skill
        
        参数:
            name: Skill名称
            description: Skill描述（用于匹配）
            handler: 处理函数
        """
        self.skills[name] = {
            "description": description,
            "handler": handler
        }
        print(f"✓ Agent已学习新技能: {name}")
    
    def understand_intent(self, user_input):
        """
        理解用户意图
        
        简化版：关键词匹配
        实际应用中会用LLM来理解
        
        参数:
            user_input: 用户输入
        
        返回:
            (skill_name, params) 元组
        """
        user_input_lower = user_input.lower()
        
        # 意图匹配规则
        intent_rules = {
            # 关键词 -> (skill_name, 参数提取函数)
            ("大写", "转大写"): ("to_uppercase", lambda x: {"text": x}),
            ("小写", "转小写"): ("to_lowercase", lambda x: {"text": x}),
            ("审查", "检查"): ("code_reviewer", lambda x: {"code": x, "language": "python"}),
            ("摘要", "总结"): ("summarizer", lambda x: {"text": x}),
            ("计算", "算"): ("calculator", self._extract_math),
        }
        
        for keywords, (skill_name, param_func) in intent_rules.items():
            if any(kw in user_input_lower for kw in keywords):
                # 提取参数
                params = param_func(user_input)
                return skill_name, params
        
        return None, {}
    
    def _extract_math(self, user_input):
        """从数学表达式中提取参数"""
        import re
        # 简单匹配：提取数字和运算符
        numbers = re.findall(r'\d+', user_input)
        op = "add"
        if "减" in user_input or "-" in user_input:
            op = "subtract"
        elif "乘" in user_input or "*" in user_input:
            op = "multiply"
        elif "除" in user_input or "/" in user_input:
            op = "divide"
        
        return {
            "a": int(numbers[0]) if len(numbers) > 0 else 0,
            "b": int(numbers[1]) if len(numbers) > 1 else 0,
            "operation": op
        }
    
    def execute(self, skill_name, params):
        """
        执行Skill
        
        参数:
            skill_name: Skill名称
            params: 参数
        
        返回:
            执行结果
        """
        if skill_name not in self.skills:
            return {"error": f"我不会这个技能: {skill_name}"}
        
        handler = self.skills[skill_name]["handler"]
        return handler(params)
    
    def chat(self, user_input):
        """
        对话接口
        
        参数:
            user_input: 用户输入
        
        返回:
            Agent回复
        """
        print(f"\n用户: {user_input}")
        
        # 1. 理解意图
        skill_name, params = self.understand_intent(user_input)
        
        if skill_name is None:
            response = "抱歉，我不太明白你的意思"
        else:
            # 2. 执行Skill
            result = self.execute(skill_name, params)
            
            # 3. 格式化回复
            response = self._format_response(skill_name, result)
        
        print(f"{self.name}: {response}")
        
        # 记录历史
        self.history.append({
            "user": user_input,
            "response": response,
            "skill": skill_name
        })
        
        return response
    
    def _format_response(self, skill_name, result):
        """格式化响应"""
        if "error" in result:
            return f"出错了: {result['error']}"
        
        if skill_name == "to_uppercase":
            return f"转换结果: {result.get('result', result)}"
        elif skill_name == "code_reviewer":
            return f"代码评分: {result.get('score', 0)}/100\n问题: {len(result.get('issues', []))}个"
        elif skill_name == "summarizer":
            return f"摘要: {result.get('summary', '')}"
        elif skill_name == "calculator":
            return f"计算结果: {result.get('result', '')}"
        
        return str(result)


# ==================== 测试Agent ====================

print("=== Agent与Skill结合示例 ===\n")

# 创建Agent
agent = SimpleAgent("小助手")

# 注册Skills
def to_uppercase_handler(params):
    return {"result": params.get("text", "").upper()}

def to_lowercase_handler(params):
    return {"result": params.get("text", "").lower()}

def code_reviewer_handler(params):
    code = params.get("code", "")
    score = 100
    issues = []
    
    if "except:" in code:
        score -= 10
        issues.append("使用裸except")
    if "eval(" in code:
        score -= 15
        issues.append("使用eval有安全风险")
    
    return {"score": score, "issues": issues}

def summarizer_handler(params):
    text = params.get("text", "")
    sentences = text.split("。")
    summary = sentences[0] if sentences else text
    return {"summary": summary[:50] + "..."}

def calculator_handler(params):
    a = params.get("a", 0)
    b = params.get("b", 0)
    op = params.get("operation", "add")
    
    ops = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else None
    }
    
    return {"result": ops.get(op)}

agent.register_skill("to_uppercase", "文本转大写", to_uppercase_handler)
agent.register_skill("to_lowercase", "文本转小写", to_lowercase_handler)
agent.register_skill("code_reviewer", "代码审查", code_reviewer_handler)
agent.register_skill("summarizer", "文本摘要", summarizer_handler)
agent.register_skill("calculator", "计算器", calculator_handler)

# 对话测试
print("\n--- 开始对话 ---")
agent.chat("把hello转成大写")
agent.chat("审查这段代码: def test(): eval('x')")
agent.chat("总结这段话：今天天气很好。阳光明媚。适合外出。")
agent.chat("计算10乘以5")
```

---

## 最佳实践

### Skill设计原则

| 原则 | 说明 |
|------|------|
| 单一职责 | 一个Skill只做一件事 |
| 清晰接口 | 输入输出要明确 |
| 错误处理 | 要优雅处理异常 |
| 文档完善 | 说明要详细清楚 |
| 可测试 | 逻辑要易于测试 |

### Agent设计原则

| 原则 | 说明 |
|------|------|
| 明确目标 | 让Agent知道要做什么 |
| 适当授权 | 给Agent足够的自主权 |
| 反馈循环 | 让Agent能反思和改进 |
| 安全可控 | 设置边界和限制 |

---

## 总结

### 本章学到的内容

1. **真实Skill格式** - SKILL.md格式
2. **Skill商店** - 上传、下载、评价
3. **Agent结合** - Agent如何调用Skill
4. **最佳实践** - 设计原则

### 进阶学习路径

```
初学者:
  → 理解Skill概念
  → 编写简单Skill
  → 学会注册和使用

进阶:
  → 组合多个Skill
  → 编写真实Skill文件
  → Agent开发

专家:
  → Skill商店开发
  → Agent框架学习
  → 参与开源社区
```

### 下一步

- 阅读官方文档
- 尝试编写自己的Skill
- 参与社区分享
