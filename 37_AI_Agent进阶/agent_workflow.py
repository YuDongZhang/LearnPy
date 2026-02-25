"""
Agent工作流
==========

介绍Agent工作流的设计和实现。
"""

print("=" * 60)
print("1. Agent工作流概述")
print("=" * 60)

print("Agent工作流:")
print("  - 预定义的执行流程")
print("  - 结构化的任务处理")
print("  - 可视化的流程控制")
print()
print("与普通Agent的区别:")
print("  - 普通Agent: 动态决策")
print("  - 工作流: 固定流程+动态决策")

print()
print("=" * 60)
print("2. 工作流模式")
print("=" * 60)

print("2.1 顺序工作流")
print("  Step1 -> Step2 -> Step3 -> Result")
print()
print("2.2 并行工作流")
print("       / Step1 \\")
print("  Input -> - Step2 -> Merge -> Output")
print("       \\ Step3 /")
print()
print("2.3 条件工作流")
print("  Input -> 判断 -> True -> StepA")
print("            |")
print("           False -> StepB")
print()
print("2.4 循环工作流")
print("  Step1 -> 判断 -> 满足? -> Yes -> Step2 -> Step1")
print("           |")
print("          No")
print("           |")
print("         Output")

print()
print("=" * 60)
print("3. 工作流设计原则")
print("=" * 60)

print("3.1 单一职责")
print("  - 每个步骤只做一件事")
print("  - 易于理解和维护")
print()
print("3.2 清晰接口")
print("  - 步骤之间数据格式明确")
print("  - 便于组合和替换")
print()
print("3.3 可观测性")
print("  - 记录每个步骤的输入输出")
print("  - 便于调试和优化")
print()
print("3.4 错误处理")
print("  - 每个步骤有错误处理")
print("  - 支持重试和降级")

print()
print("=" * 60)
print("4. 简单工作流实现")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 定义工具
search_tool = Tool(name="搜索", func=lambda x: f"搜索结果: {x}", description="搜索")
analyze_tool = Tool(name="分析", func=lambda x: f"分析: {x}", description="分析")
write_tool = Tool(name="写作", func=lambda x: f"写作: {x}", description="写作")

def simple_workflow(task):
    # Step 1: 搜索
    search_result = search_tool.run(task)

    # Step 2: 分析
    analysis = analyze_tool.run(search_result)

    # Step 3: 写作
    result = write_tool.run(analysis)

    return result

# 使用
result = simple_workflow("AI发展趋势")
''')

print()
print("=" * 60)
print("5. 条件分支工作流")
print("=" * 60)

print('''
def conditional_workflow(task):
    # 判断任务类型
    task_type = classify_task(task)

    if task_type == "research":
        # 研究任务
        return research_workflow(task)
    elif task_type == "coding":
        # 编程任务
        return coding_workflow(task)
    elif task_type == "writing":
        # 写作任务
        return writing_workflow(task)
    else:
        return general_workflow(task)

def classify_task(task):
    # 使用LLM判断任务类型
    prompt = f"判断以下任务类型: {task}"
    return llm.predict(prompt)
''')

print()
print("=" * 60)
print("6. 并行工作流")
print("=" * 60)

print('''
import asyncio
from concurrent.futures import ThreadPoolExecutor

def parallel_workflow(task):
    # 分解任务
    subtasks = decompose_task(task)

    # 并行执行
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(execute_subtask, subtasks))

    # 合并结果
    final_result = merge_results(results)

    return final_result

def decompose_task(task):
    # 分解为子任务
    return ["子任务1", "子任务2", "子任务3"]

def execute_subtask(subtask):
    return f"完成: {subtask}"

def merge_results(results):
    return " | ".join(results)
''')

print()
print("=" * 60)
print("7. 循环工作流")
print("=" * 60)

print('''
def iterative_workflow(task, max_iterations=5):
    result = None

    for i in range(max_iterations):
        # 生成解决方案
        solution = generate_solution(task, result)

        # 检查是否满足要求
        if check_quality(solution):
            return solution

        # 反馈改进
        feedback = get_feedback(solution)
        result = f"{feedback}"

    return solution

def generate_solution(task, feedback):
    prompt = f"任务: {task}"
    if feedback:
        prompt += f"\\n反馈: {feedback}"
    return llm.predict(prompt)

def check_quality(solution):
    # 检查质量
    return len(solution) > 100

def get_feedback(solution):
    return "内容不够详细，请扩充"
''')

print()
print("=" * 60)
print("8. 工作流状态管理")
print("=" * 60)

print("8.1 简单状态")
print('''
class WorkflowState:
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.data = {}

    def add_step(self, name, result):
        self.steps.append({
            "step": name,
            "result": result
        })
        self.current_step += 1

    def get_history(self):
        return self.steps

state = WorkflowState()
state.add_step("搜索", "搜索结果...")
state.add_step("分析", "分析结果...")
''')

print()
print("8.2 持久化状态")
print('''
import json
from datetime import datetime

class PersistentState:
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.state_file = f"state_{workflow_id}.json"
        self.load()

    def load(self):
        try:
            with open(self.state_file, "r") as f:
                self.data = json.load(f)
        except:
            self.data = {"created": datetime.now().isoformat()}

    def save(self):
        with open(self.state_file, "w") as f:
            json.dump(self.data, f)

    def update(self, key, value):
        self.data[key] = value
        self.save()
''')

print()
print("=" * 60)
print("9. 工作流监控")
print("=" * 60)

print("9.1 步骤日志")
print('''
import logging
from datetime import datetime

class WorkflowLogger:
    def __init__(self, workflow_name):
        self.workflow_name = workflow_name
        self.logs = []

    def log_step(self, step_name, input_data, output_data):
        self.logs.append({
            "time": datetime.now().isoformat(),
            "step": step_name,
            "input": input_data,
            "output": output_data
        })

    def get_logs(self):
        return self.logs

logger = WorkflowLogger("research")
logger.log_step("搜索", "AI", "搜索结果...")
''')

print()
print("9.2 性能监控")
print('''
import time
from functools import wraps

def monitor_step(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        print(f"{func.__name__} 执行时间: {duration:.2f}秒")
        return result
    return wrapper
''')

print()
print("=" * 60)
print("10. 工作流错误处理")
print("=" * 60)

print("10.1 重试机制")
print('''
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_with_retry(step_func, *args, **kwargs):
    return step_func(*args, **kwargs)
''')

print()
print("10.2 降级策略")
print('''
def execute_with_fallback(primary_func, fallback_func, *args, **kwargs):
    try:
        return primary_func(*args, **kwargs)
    except Exception as e:
        print(f"主流程失败: {e}, 使用降级方案")
        return fallback_func(*args, **kwargs)
''')

print()
print("=" * 60)
print("11. 工作流编排工具")
print("=" * 60)

print("11.1 Prefect")
print("  - Python原生工作流编排")
print("  - 任务调度和监控")
print()
print("11.2 Airflow")
print("  - 大规模工作流")
print("  - 复杂调度")
print()
print("11.3 Dagster")
print("  - 数据流水线")
print("  - 现代化UI")
print()
print("11.4 LangChain LCEL")
print("  - LLM工作流")
print("  - 链式组合")

print()
print("=" * 60)
print("12. LangChain LCEL工作流")
print("=" * 60)

print('''
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

llm = ChatOpenAI(model="gpt-4o")

# 定义步骤
prompt1 = ChatPromptTemplate.from_template("总结: {topic}")
prompt2 = ChatPromptTemplate.from_template("用诗意的方式改写: {summary}")

# 构建工作流
chain = prompt1 | llm | StrOutputParser() | prompt2 | llm | StrOutputParser()

# 执行
result = chain.invoke({"topic": "人工智能"})
''')

print()
print("=" * 60)
print("13. 工作流最佳实践")
print("=" * 60)

print("设计原则:")
print("  1. 流程简单清晰")
print("  2. 步骤解耦")
print("  3. 状态可追溯")
print("  4. 错误可处理")
print()
print("性能优化:")
print("  1. 减少不必要的步骤")
print("  2. 并行处理独立任务")
print("  3. 缓存中间结果")
print("  4. 监控关键指标")

print()
print("=" * 60)
print("14. 工作流总结")
print("=" * 60)

print("Agent工作流要点:")
print()
print("* 工作流模式:")
print("  - 顺序、并行、条件、循环")
print()
print("* 关键组件:")
print("  - 状态管理、错误处理、监控")
print()
print("* 编排工具:")
print("  - LangChain LCEL、Prefect、Airflow")
print()
print("* 最佳实践:")
print("  - 简单清晰、可观测、可维护")
