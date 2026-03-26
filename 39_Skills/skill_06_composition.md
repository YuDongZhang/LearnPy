# 第6节：Skill组合使用

本节介绍如何组合多个Skill来解决复杂问题，这是Skill强大功能的核心。

---

## 为什么要组合Skill？

单个Skill只能做一件事，但现实问题往往需要多个步骤。

```
场景：分析用户评论情感
┌─────────────────────────────────────────────────────┐
│  步骤1: 清洗数据    →  步骤2: 分词    →  步骤3: 情感分析 │
│  (DataCleaner)    →  (Tokenizer)  →  (Sentiment)     │
└─────────────────────────────────────────────────────┘
```

---

## 组合模式

### 模式1：管道模式 (Pipeline)

数据像水流一样依次通过各个Skill。

```python
# skill_pipeline.py
"""
管道模式：数据依次通过多个Skill
特点：上一个输出作为下一个输入
"""

class SkillPipeline:
    """
    Skill管道类
    
    用途：将多个Skill串联起来，数据依次处理
    
    示例：
        pipeline = Pipeline()
        pipeline.add(cleaner)
        pipeline.add(tokenizer)
        pipeline.add(analyzer)
        result = pipeline.run(data)
    """
    
    def __init__(self, name="Unnamed Pipeline"):
        """
        初始化管道
        
        参数:
            name: 管道名称（用于日志）
        """
        self.name = name
        self.steps = []  # 存储步骤：[(skill_name, handler), ...]
    
    def add(self, skill_name, handler):
        """
        添加一个步骤到管道
        
        参数:
            skill_name: Skill名称
            handler: 处理函数
        
        返回:
            self，支持链式调用
        """
        self.steps.append((skill_name, handler))
        return self
    
    def run(self, initial_data):
        """
        执行管道
        
        参数:
            initial_data: 初始输入数据
        
        返回:
            最终结果
        """
        print(f"\n=== 执行管道: {self.name} ===")
        
        # 从第一个数据开始
        current_data = initial_data
        step_results = []  # 记录每步结果
        
        # 依次执行每个步骤
        for i, (skill_name, handler) in enumerate(self.steps):
            print(f"\n步骤 {i+1}: {skill_name}")
            print(f"  输入: {str(current_data)[:50]}...")
            
            # 调用Skill处理
            result = handler(current_data)
            
            # 记录结果
            step_results.append({
                "step": i + 1,
                "skill": skill_name,
                "output": result
            })
            
            # 准备下一步的输入
            # 如果返回是字典，提取 'result' 字段
            if isinstance(result, dict):
                current_data = result.get("result", result)
            else:
                current_data = result
            
            print(f"  输出: {str(current_data)[:50]}...")
        
        print(f"\n=== 管道执行完成 ===")
        
        return {
            "final_result": current_data,
            "step_results": step_results,
            "total_steps": len(self.steps)
        }


# ==================== 示例：文本处理管道 ====================

print("=" * 50)
print("示例1: 文本处理管道")
print("=" * 50)

# Step 1: 文本清洗
def clean_text(text):
    """清洗文本：去除多余空格、转小写"""
    # 去除首尾空格
    text = text.strip()
    # 多个空格合并为一个
    import re
    text = re.sub(r'\s+', ' ', text)
    # 转小写
    text = text.lower()
    return {"result": text, "original": text}

# Step 2: 分词
def tokenize(text):
    """分词：按空格分割"""
    words = text.split()
    return {"result": words, "count": len(words)}

# Step 3: 词性标注（简化版）
def tag_pos(words):
    """词性标注：简单规则"""
    # 简化规则：常见单词标记为名词/动词
    pos_tags = []
    for word in words:
        if word in ['the', 'a', 'an', 'is', 'are', 'was', 'were']:
            pos_tags.append((word, 'article'))
        elif word in ['run', 'eat', 'walk', 'jump']:
            pos_tags.append((word, 'verb'))
        else:
            pos_tags.append((word, 'noun'))
    return {"result": pos_tags}

# Step 4: 统计
def count_words(words):
    """统计词频"""
    from collections import Counter
    freq = Counter(words)
    return {"result": dict(freq)}

# 创建并执行管道
pipeline = SkillPipeline("文本分析管道")
pipeline.add("clean", clean_text)
pipeline.add("tokenize", tokenize)
pipeline.add("pos_tag", tag_pos)
pipeline.add("count", count_words)

result = pipeline.run("  The  cat   runs  fast  ")

print(f"\n最终结果: {result['final_result']}")
```

---

### 模式2：分支模式 (Router)

根据条件选择不同的Skill执行。

```python
# skill_router.py
"""
分支模式：根据条件选择不同的Skill
特点：根据输入类型/内容决定走哪个分支
"""

class SkillRouter:
    """
    Skill路由器类
    
    用途：根据条件选择要执行的Skill
    
    示例：
        router = Router()
        router.add_route("is_text", text_handler)
        router.add_route("is_number", number_handler)
        result = router.route(data)
    """
    
    def __init__(self):
        """初始化路由器"""
        self.routes = {}  # 条件名称 -> 处理函数
        self.conditions = {}  # 条件名称 -> 条件函数
    
    def add_condition(self, name, condition_func):
        """
        添加条件函数
        
        参数:
            name: 条件名称
            condition_func: 返回True/False的函数
        """
        self.conditions[name] = condition_func
    
    def add_route(self, condition_name, handler, description=""):
        """
        添加路由
        
        参数:
            condition_name: 条件名称（匹配哪个条件）
            handler: 处理函数
            description: 路由描述
        """
        self.routes[condition_name] = {
            "handler": handler,
            "description": description
        }
    
    def route(self, data):
        """
        根据条件路由
        
        参数:
            data: 输入数据
        
        返回:
            处理结果
        """
        # 遍历所有条件，找到第一个匹配的
        for condition_name, condition_func in self.conditions.items():
            if condition_func(data):
                # 找到匹配的路由
                handler = self.routes[condition_name]["handler"]
                print(f"路由到: {condition_name}")
                return handler(data)
        
        # 没有匹配的路由
        return {"error": "没有匹配的路由"}


# ==================== 示例：数据处理路由 ====================

print("=" * 50)
print("示例2: 数据处理路由")
print("=" * 50)

# 创建路由器
router = SkillRouter()

# 定义条件
router.add_condition("is_text", lambda d: isinstance(d, str))
router.add_condition("is_number", lambda d: isinstance(d, (int, float)))
router.add_condition("is_list", lambda d: isinstance(d, list))
router.add_condition("is_dict", lambda d: isinstance(d, dict))

# 定义处理函数
def handle_text(data):
    """处理文本：统计字符和单词"""
    return {
        "result": f"文本长度={len(data)}, 单词数={len(data.split())}"
    }

def handle_number(data):
    """处理数字：判断奇偶、绝对值"""
    return {
        "result": f"数字={data}, 绝对值={abs(data)}, {'偶数' if data % 2 == 0 else '奇数'}"
    }

def handle_list(data):
    """处理列表：统计元素"""
    return {
        "result": f"列表长度={len(data)}, 元素={data}"
    }

def handle_dict(data):
    """处理字典：统计键值对"""
    return {
        "result": f"字典键数={len(data)}, 键={list(data.keys())}"
    }

# 注册路由
router.add_route("is_text", handle_text, "文本处理")
router.add_route("is_number", handle_number, "数字处理")
router.add_route("is_list", handle_list, "列表处理")
router.add_route("is_dict", handle_dict, "字典处理")

# 测试各种数据类型
test_data = [
    "Hello World",      # 文本
    42,                # 数字
    [1, 2, 3, 4, 5],   # 列表
    {"name": "Tom", "age": 20}  # 字典
]

for data in test_data:
    print(f"\n输入: {data}")
    result = router.route(data)
    print(f"输出: {result}")
```

---

### 模式3：工作流模式 (Workflow)

多个有依赖关系的步骤，按顺序执行。

```python
# skill_workflow.py
"""
工作流模式：步骤有依赖关系
特点：步骤之间有依赖，必须按顺序执行
"""

class SkillWorkflow:
    """
    Skill工作流类
    
    用途：管理有依赖关系的步骤
    
    示例：
        workflow = Workflow()
        workflow.add_step("step1", handler1)      # 无依赖
        workflow.add_step("step2", handler2, ["step1"])  # 依赖step1
        result = workflow.run(data)
    """
    
    def __init__(self, name="Workflow"):
        """初始化工作流"""
        self.name = name
        self.steps = {}  # step_id -> {handler, depends_on}
        self.results = {}  # step_id -> result
    
    def add_step(self, step_id, handler, depends_on=None):
        """
        添加步骤
        
        参数:
            step_id: 步骤ID（唯一标识）
            handler: 处理函数
            depends_on: 依赖的步骤ID列表
        """
        self.steps[step_id] = {
            "handler": handler,
            "depends_on": depends_on or []
        }
    
    def run(self, initial_data):
        """
        执行工作流
        
        参数:
            initial_data: 初始数据
        
        返回:
            所有步骤的结果
        """
        print(f"\n=== 执行工作流: {self.name} ===")
        
        self.results = {}
        
        # 记录已执行的步骤
        executed = set()
        
        # 按依赖顺序执行
        # 简单实现：循环直到所有步骤完成
        max_iterations = len(self.steps) + 1
        iteration = 0
        
        while len(executed) < len(self.steps) and iteration < max_iterations:
            iteration += 1
            
            for step_id, step_info in self.steps.items():
                # 已跳过，跳过
                if step_id in executed:
                    continue
                
                # 检查依赖是否满足
                deps = step_info["depends_on"]
                deps_ready = all(dep in executed for dep in deps)
                
                if not deps_ready:
                    continue
                
                # 准备输入数据
                # 合并所有依赖步骤的输出作为输入
                input_data = initial_data.copy() if isinstance(initial_data, dict) else {}
                for dep in deps:
                    if dep in self.results:
                        input_data[f"_{dep}_output"] = self.results[dep]
                
                # 执行步骤
                print(f"\n步骤 {step_id} (依赖: {deps})")
                handler = step_info["handler"]
                result = handler(input_data)
                
                # 保存结果
                self.results[step_id] = result
                executed.add(step_id)
                
                print(f"  完成")
        
        print(f"\n=== 工作流完成: {len(executed)}/{len(self.steps)} 步骤 ===")
        
        return {
            "results": self.results,
            "executed_steps": list(executed)
        }


# ==================== 示例：数据处理工作流 ====================

print("=" * 50)
print("示例3: 数据处理工作流")
print("=" * 50)

# 创建工作流
workflow = SkillWorkflow("数据处理工作流")

# Step 1: 获取数据（无依赖）
def fetch_data(input_data):
    """模拟获取数据"""
    # 模拟从API获取
    return {"raw_data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

# Step 2: 清洗数据（依赖 Step 1）
def clean_data(input_data):
    """清洗数据：过滤负数和零"""
    raw = input_data.get("_step1_output", {}).get("raw_data", [])
    cleaned = [x for x in raw if x > 0]
    return {"cleaned_data": cleaned}

# Step 3: 转换数据（依赖 Step 2）
def transform_data(input_data):
    """转换数据：每个元素乘以2"""
    cleaned = input_data.get("_step2_output", {}).get("cleaned_data", [])
    transformed = [x * 2 for x in cleaned]
    return {"transformed_data": transformed}

# Step 4: 统计（依赖 Step 3）
def calculate_stats(input_data):
    """计算统计信息"""
    transformed = input_data.get("_step3_output", {}).get("transformed_data", [])
    stats = {
        "count": len(transformed),
        "sum": sum(transformed),
        "avg": sum(transformed) / len(transformed) if transformed else 0,
        "max": max(transformed) if transformed else 0,
        "min": min(transformed) if transformed else 0
    }
    return {"stats": stats}

# Step 5: 生成报告（依赖 Step 3 和 Step 4）
def generate_report(input_data):
    """生成报告"""
    transformed = input_data.get("_step3_output", {}).get("transformed_data", [])
    stats = input_data.get("_step4_output", {}).get("stats", {})
    
    report = f"""
    ===================
    数据处理报告
    ===================
    
    处理后数据: {transformed}
    数据条数: {stats.get('count', 0)}
    总和: {stats.get('sum', 0)}
    平均值: {stats.get('avg', 0):.2f}
    最大值: {stats.get('max', 0)}
    最小值: {stats.get('min', 0)}
    
    ===================
    """
    return {"report": report}

# 添加步骤
workflow.add_step("step1", fetch_data)  # 无依赖
workflow.add_step("step2", clean_data, ["step1"])  # 依赖step1
workflow.add_step("step3", transform_data, ["step2"])  # 依赖step2
workflow.add_step("step4", calculate_stats, ["step3"])  # 依赖step3
workflow.add_step("step5", generate_report, ["step3", "step4"])  # 依赖step3和step4

# 执行工作流
result = workflow.run({})

print("\n" + result["results"]["step5"]["report"])
```

---

## 总结

### 三种组合模式

| 模式 | 特点 | 适用场景 |
|------|------|---------|
| 管道 | 串联，数据流式 | ETL、文本处理 |
| 分支 | 根据条件选择 | 类型处理、路由 |
| 工作流 | 有依赖关系 | 复杂业务流程 |

### 组合的好处

```
1. 模块化：每个Skill独立，易于维护
2. 复用：一套Skill，多处使用
3. 灵活：可以自由组合
4. 可扩展：添加新步骤不影响现有流程
```

---

## 下一节

[第7节：高级Topic](skill_07_advanced.md)
