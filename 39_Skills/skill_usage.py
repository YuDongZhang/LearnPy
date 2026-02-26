"""
Skill使用场景
=============

本文件介绍Skill的各种使用场景：
- 单独使用
- 组合使用
- 工作流编排
- 与AI Agent结合
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
import json

# ============================================================================
# 第一部分：单独使用Skill
# ============================================================================

class SkillInvoker:
    """Skill调用器"""
    
    def __init__(self):
        self.skills = {}
    
    def register(self, name: str, handler: Callable):
        """注册Skill"""
        self.skills[name] = handler
    
    def invoke(self, name: str, params: Dict) -> Any:
        """调用Skill"""
        if name not in self.skills:
            raise ValueError(f"Skill不存在: {name}")
        return self.skills[name](params)


def demonstrate_single_usage():
    """演示单独使用"""
    
    print("=" * 60)
    print("单独使用Skill")
    print("=" * 60)
    
    invoker = SkillInvoker()
    
    # 注册简单Skill
    invoker.register("uppercase", lambda p: p["text"].upper())
    invoker.register("lowercase", lambda p: p["text"].lower())
    invoker.register("reverse", lambda p: p["text"][::-1])
    invoker.register("word_count", lambda p: len(p["text"].split()))
    
    # 调用Skill
    print("\n调用uppercase Skill:")
    result = invoker.invoke("uppercase", {"text": "hello world"})
    print(f"  输入: 'hello world'")
    print(f"  输出: '{result}'")
    
    print("\n调用word_count Skill:")
    result = invoker.invoke("word_count", {"text": "hello world from python"})
    print(f"  输入: 'hello world from python'")
    print(f"  输出: {result} 个单词")


# ============================================================================
# 第二部分：组合使用Skill
# ============================================================================

class SkillPipeline:
    """Skill管道（组合多个Skill）"""
    
    def __init__(self):
        self.steps: List[tuple[str, Dict]] = []
    
    def add(self, skill_name: str, params: Dict = None) -> 'SkillPipeline':
        """添加Skill到管道"""
        self.steps.append((skill_name, params or {}))
        return self
    
    def execute(self, invoker: SkillInvoker, initial_data: Any = None) -> List[Any]:
        """执行管道"""
        results = []
        data = initial_data
        
        for skill_name, params in self.steps:
            params = params.copy() if params else {}
            if data is not None:
                params["input"] = data
            
            result = invoker.invoke(skill_name, params)
            results.append(result)
            data = result
        
        return results


def demonstrate_pipeline_usage():
    """演示管道使用"""
    
    print("\n" + "=" * 60)
    print("组合使用Skill - 管道模式")
    print("=" * 60)
    
    invoker = SkillInvoker()
    
    # 注册处理Skill
    invoker.register("clean", lambda p: p["input"].strip().lower())
    invoker.register("tokenize", lambda p: p["input"].split())
    invoker.register("count", lambda p: len(p["input"]))
    invoker.register("deduplicate", lambda p: list(set(p["input"])))
    
    # 创建管道
    pipeline = (
        SkillPipeline()
        .add("clean")
        .add("tokenize")
        .add("deduplicate")
        .add("count")
    )
    
    print("\n处理文本: 'Hello world hello Python WORLD python'")
    print("\n管道步骤:")
    print("  1. clean - 清理和转小写")
    print("  2. tokenize - 分词")
    print("  3. deduplicate - 去重")
    print("  4. count - 计数")
    
    results = pipeline.execute(invoker, "Hello world hello Python WORLD python")
    
    print("\n中间结果:")
    print(f"  清理后: '{results[0]}'")
    print(f"  分词后: {results[1]}")
    print(f"  去重后: {results[2]}")
    print(f"  最终计数: {results[3]}")


# ============================================================================
# 第三部分：条件分支
# ============================================================================

class ConditionalSkillRunner:
    """条件Skill运行器"""
    
    def __init__(self):
        self.skills: Dict[str, Callable] = {}
        self.conditions: Dict[str, Callable] = {}
    
    def register_skill(self, name: str, handler: Callable):
        """注册Skill"""
        self.skills[name] = handler
    
    def register_condition(self, name: str, condition: Callable):
        """注册条件"""
        self.conditions[name] = condition
    
    def run(self, rules: List[Dict], context: Dict) -> Any:
        """根据条件执行"""
        for rule in rules:
            condition_name = rule.get("condition")
            skill_name = rule.get("skill")
            
            if condition_name and skill_name:
                condition = self.conditions.get(condition_name)
                if condition and condition(context):
                    skill = self.skills.get(skill_name)
                    if skill:
                        return skill(context)
            
            elif skill_name:
                skill = self.skills.get(skill_name)
                if skill:
                    return skill(context)
        
        return None


def demonstrate_conditional_usage():
    """演示条件分支"""
    
    print("\n" + "=" * 60)
    print("条件分支使用Skill")
    print("=" * 60)
    
    runner = ConditionalSkillRunner()
    
    # 注册Skills
    runner.register_skill("process_text", lambda c: f"处理文本: {c['data']}")
    runner.register_skill("process_json", lambda c: f"处理JSON: {json.dumps(c['data'])}")
    runner.register_skill("process_csv", lambda c: f"处理CSV: {len(c['data'])}行")
    runner.register_skill("unknown_type", lambda c: "未知数据类型")
    
    # 注册条件
    runner.register_condition("is_text", lambda c: isinstance(c.get("data"), str))
    runner.register_condition("is_list", lambda c: isinstance(c.get("data"), list))
    runner.register_condition("is_dict", lambda c: isinstance(c.get("data"), dict))
    
    # 定义规则
    rules = [
        {"condition": "is_text", "skill": "process_text"},
        {"condition": "is_list", "skill": "process_csv"},
        {"condition": "is_dict", "skill": "process_json"},
        {"skill": "unknown_type"}
    ]
    
    # 测试不同数据类型
    test_cases = [
        {"data": "Hello World"},
        {"data": [1, 2, 3, 4, 5]},
        {"data": {"name": "test", "value": 100}}
    ]
    
    print("\n测试条件路由:")
    for context in test_cases:
        result = runner.run(rules, context)
        print(f"  数据: {context['data']}")
        print(f"  结果: {result}\n")


# ============================================================================
# 第四部分：工作流编排
# ============================================================================

@dataclass
class WorkflowStep:
    """工作流步骤"""
    skill: str
    params: Dict
    depends_on: List[str] = None
    condition: str = None


class SkillWorkflow:
    """Skill工作流"""
    
    def __init__(self):
        self.steps: List[WorkflowStep] = []
        self.invoker = SkillInvoker()
    
    def register_skill(self, name: str, handler: Callable):
        """注册Skill"""
        self.invoker.register(name, handler)
    
    def add_step(self, skill: str, params: Dict = None, 
                 depends_on: List[str] = None, condition: str = None):
        """添加步骤"""
        self.steps.append(WorkflowStep(
            skill=skill,
            params=params or {},
            depends_on=depends_on or [],
            condition=condition
        ))
    
    def execute(self, initial_data: Dict) -> Dict:
        """执行工作流"""
        results = {}
        data = initial_data.copy()
        
        for i, step in enumerate(self.steps):
            step_params = step.params.copy()
            
            # 处理依赖
            for dep in step.depends_on:
                if dep in results:
                    step_params[f"from_{dep}"] = results[dep]
            
            # 处理条件
            if step.condition:
                if not self._evaluate_condition(step.condition, data):
                    continue
            
            # 执行Skill
            step_params["data"] = data
            result = self.invoker.invoke(step.skill, step_params)
            
            results[f"step_{i}"] = result
            data = result
        
        return {
            "results": results,
            "final_output": data
        }
    
    def _evaluate_condition(self, condition: str, data: Dict) -> bool:
        """评估条件"""
        if condition == "has_data":
            return bool(data)
        if condition == "has_error":
            return data.get("error") is not None
        return True


def demonstrate_workflow_usage():
    """演示工作流"""
    
    print("\n" + "=" * 60)
    print("工作流编排Skill")
    print("=" * 60)
    
    workflow = SkillWorkflow()
    
    # 注册处理Skill
    workflow.register_skill("fetch", lambda p: {"raw": "原始数据 from API"})
    workflow.register_skill("validate", lambda p: {
        "valid": True,
        "data": p["data"].get("raw", "")
    })
    workflow.register_skill("transform", lambda p: {
        "transformed": p["data"]["data"].upper()
    })
    workflow.register_skill("save", lambda p: {
        "saved": True,
        "path": "/output/data.txt"
    })
    workflow.register_skill("notify", lambda p: {
        "notified": True,
        "message": "处理完成"
    })
    
    # 构建工作流
    workflow.add_step("fetch")
    workflow.add_step("validate", depends_on=["step_0"])
    workflow.add_step("transform", depends_on=["step_1"], 
                     condition="has_data")
    workflow.add_step("save", depends_on=["step_2"])
    workflow.add_step("notify", depends_on=["step_3"])
    
    print("\n工作流步骤:")
    for i, step in enumerate(workflow.steps):
        deps = f" (依赖: {', '.join(step.depends_on)})" if step.depends_on else ""
        cond = f" [条件: {step.condition}]" if step.condition else ""
        print(f"  {i+1}. {step.skill}{deps}{cond}")
    
    # 执行工作流
    result = workflow.execute({})
    
    print("\n执行结果:")
    print(json.dumps(result["results"], indent=2, ensure_ascii=False))


# ============================================================================
# 第五部分：与AI Agent结合
# ============================================================================

class AIAgentWithSkills:
    """集成Skill的AI Agent"""
    
    def __init__(self):
        self.skills: Dict[str, Callable] = {}
        self.conversation_history: List[Dict] = []
    
    def register_skill(self, name: str, description: str, handler: Callable):
        """注册Skill"""
        self.skills[name] = {
            "description": description,
            "handler": handler
        }
    
    def get_available_skills(self) -> List[Dict]:
        """获取可用Skills"""
        return [
            {"name": name, "description": info["description"]}
            for name, info in self.skills.items()
        ]
    
    def select_skill(self, user_request: str) -> Optional[tuple[str, Dict]]:
        """根据用户请求选择Skill"""
        request_lower = user_request.lower()
        
        skill_mapping = [
            ("review", "code_review", "代码审查"),
            ("文档", "generate_doc", "文档生成"),
            ("测试", "generate_test", "测试生成"),
            ("分析", "analyze", "数据分析"),
            ("翻译", "translate", "翻译"),
            ("总结", "summarize", "摘要生成")
        ]
        
        for keyword, skill_name, skill_desc in skill_mapping:
            if keyword in request_lower:
                return skill_name, {}
        
        return None
    
    def process_request(self, user_request: str, context: Dict = None) -> str:
        """处理用户请求"""
        self.conversation_history.append({
            "role": "user",
            "content": user_request
        })
        
        skill_info = self.select_skill(user_request)
        
        if skill_info:
            skill_name, params = skill_info
            skill = self.skills.get(skill_name)
            
            if skill and context:
                result = skill["handler"](params)
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": f"使用Skill [{skill_name}] 处理完成",
                    "result": result
                })
                
                return f"处理完成，结果: {result}"
        
        return "无法理解请求，建议尝试其他操作"


def demonstrate_ai_agent_usage():
    """演示AI Agent结合"""
    
    print("\n" + "=" * 60)
    print("AI Agent结合Skill")
    print("=" * 60)
    
    agent = AIAgentWithSkills()
    
    # 注册Skills
    agent.register_skill(
        "code_review",
        "审查代码质量和安全问题",
        lambda p: "代码评分: 85/100，发现2个警告"
    )
    
    agent.register_skill(
        "generate_doc",
        "生成代码文档",
        lambda p: "生成的文档:\n```\ndef foo():\n    '''函数说明'''\n```"
    )
    
    agent.register_skill(
        "generate_test",
        "生成单元测试",
        lambda p: "生成的测试:\n```\ndef test_foo():\n    assert foo()\n```"
    )
    
    print("\n可用Skills:")
    for skill in agent.get_available_skills():
        print(f"  - {skill['name']}: {skill['description']}")
    
    # 处理请求
    print("\n处理用户请求:")
    
    requests = [
        "请帮我审查这段代码",
        "生成一下文档",
        "写点测试"
    ]
    
    for request in requests:
        print(f"\n用户: {request}")
        result = agent.process_request(request, {"code": "def test(): pass"})
        print(f"Agent: {result}")


# ============================================================================
# 第六部分：Skill缓存和优化
# ============================================================================

class CachedSkillInvoker:
    """带缓存的Skill调用器"""
    
    def __init__(self):
        self.skills: Dict[str, Callable] = {}
        self.cache: Dict[str, Any] = {}
        self.cache_enabled = True
    
    def register(self, name: str, handler: Callable):
        """注册Skill"""
        self.skills[name] = handler
    
    def invoke(self, name: str, params: Dict) -> Any:
        """调用Skill（带缓存）"""
        if not self.cache_enabled:
            return self._execute(name, params)
        
        cache_key = self._make_key(name, params)
        
        if cache_key in self.cache:
            print(f"  [缓存命中] {name}")
            return self.cache[cache_key]
        
        result = self._execute(name, params)
        self.cache[cache_key] = result
        
        return result
    
    def _execute(self, name: str, params: Dict) -> Any:
        """执行Skill"""
        if name not in self.skills:
            raise ValueError(f"Skill不存在: {name}")
        return self.skills[name](params)
    
    def _make_key(self, name: str, params: Dict) -> str:
        """生成缓存键"""
        return f"{name}:{json.dumps(params, sort_keys=True)}"
    
    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()
        print("缓存已清除")


def demonstrate_cached_usage():
    """演示缓存"""
    
    print("\n" + "=" * 60)
    print("Skill缓存优化")
    print("=" * 60)
    
    invoker = CachedSkillInvoker()
    
    call_count = 0
    
    def expensive_operation(params: Dict) -> str:
        nonlocal call_count
        call_count += 1
        return f"处理: {params['text']} (第{call_count}次调用)"
    
    invoker.register("process", expensive_operation)
    
    # 第一次调用
    print("\n第一次调用:")
    result = invoker.invoke("process", {"text": "hello"})
    print(f"  结果: {result}")
    
    # 第二次调用（相同参数，应命中缓存）
    print("\n第二次调用（相同参数）:")
    result = invoker.invoke("process", {"text": "hello"})
    print(f"  结果: {result}")
    
    # 第三次调用（不同参数）
    print("\n第三次调用（不同参数）:")
    result = invoker.invoke("process", {"text": "world"})
    print(f"  结果: {result}")
    
    # 清除缓存后再调用
    print("\n清除缓存后调用:")
    invoker.clear_cache()
    result = invoker.invoke("process", {"text": "hello"})
    print(f"  结果: {result}")
    
    print(f"\n总调用次数: {call_count}")


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    demonstrate_single_usage()
    demonstrate_pipeline_usage()
    demonstrate_conditional_usage()
    demonstrate_workflow_usage()
    demonstrate_ai_agent_usage()
    demonstrate_cached_usage()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
Skill使用场景:

1. 单独使用
   - 简单直接
   - 适合单一任务
   - 易于理解和维护

2. 管道组合
   - 多个Skill串联
   - 数据流式处理
   - 适合批处理

3. 条件分支
   - 根据条件选择Skill
   - 动态路由
   - 适合复杂逻辑

4. 工作流编排
   - 步骤依赖管理
   - 状态传递
   - 适合完整业务流程

5. AI Agent结合
   - 意图识别
   - Skill自动选择
   - 增强AI能力

6. 缓存优化
   - 减少重复计算
   - 提高性能
   - 节省资源
""")
