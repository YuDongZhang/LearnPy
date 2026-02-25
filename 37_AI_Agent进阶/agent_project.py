"""
Agent进阶实战
==========

通过实际项目练习Agent进阶开发。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("项目: AI研究团队")
print()
print("功能:")
print("  - 自动研究主题")
print("  - 协作撰写报告")
print("  - 多轮审核改进")
print()
print("技术栈:")
print("  - LangGraph")
print("  - 多Agent协作")
print("  - 工作流编排")

print()
print("=" * 60)
print("2. 项目结构")
print("=" * 60)

print("research_team/")
print("├── agents/")
print("│   ├── __init__.py")
print("│   ├── researcher.py")
print("│   ├── writer.py")
print("│   └── reviewer.py")
print("├── graph/")
print("│   ├── __init__.py")
print("│   └── research_graph.py")
print("├── main.py")
print("└── requirements.txt")

print()
print("=" * 60)
print("3. 定义Agent角色")
print("=" * 60)

print('''
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 研究员Agent
researcher_prompt = ChatPromptTemplate.from_template("""你是一个专业的研究员。
任务: 研究以下主题
主题: {topic}

请搜索和分析相关信息，提供详细的研究报告。""")

# 写作者Agent
writer_prompt = ChatPromptTemplate.from_template("""你是一个专业的技术作家。
任务: 基于研究报告撰写文章
研究内容: {research}

请撰写一篇结构清晰、内容丰富的文章。""")

# 审核员Agent
reviewer_prompt = ChatPromptTemplate.from_template("""你是一个严格的内容审核员。
任务: 审核以下文章
文章: {article}

请指出问题并提供改进建议。""")

# 创建Agent链
researcher_chain = researcher_prompt | llm
writer_chain = writer_prompt | llm
reviewer_chain = reviewer_prompt | llm
''')

print()
print("=" * 60)
print("4. LangGraph实现")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ResearchState(TypedDict):
    topic: str
    research: str
    article: str
    review: str
    iteration: int

# 研究节点
def research_node(state):
    topic = state["topic"]
    research = researcher_chain.invoke({"topic": topic}).content
    return {"research": research, "iteration": 1}

# 写作节点
def write_node(state):
    research = state["research"]
    article = writer_chain.invoke({"research": research}).content
    return {"article": article, "iteration": state.get("iteration", 0) + 1}

# 审核节点
def review_node(state):
    article = state["article"]
    review = reviewer_chain.invoke({"article": article}).content
    return {"review": review}

# 判断是否需要修改
def should_revise(state):
    review = state.get("review", "")
    if "需要修改" in review or "建议修改" in review:
        return "revise"
    return "accept"

# 修订节点
def revise_node(state):
    article = state["article"]
    review = state["review"]
    new_article = writer_chain.invoke({
        "research": state["research"],
        "feedback": review
    }).content
    return {"article": new_article, "iteration": state["iteration"] + 1}

# 构建图
workflow = StateGraph(ResearchState)

workflow.add_node("research", research_node)
workflow.add_node("write", write_node)
workflow.add_node("review", review_node)
workflow.add_node("revise", revise_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "write")
workflow.add_edge("write", "review")

# 条件边
workflow.add_conditional_edges(
    "review",
    should_revise,
    {"revise": "revise", "accept": END}
)
workflow.add_edge("revise", "review")

# 编译
graph = workflow.compile()
''')

print()
print("=" * 60)
print("5. 执行工作流")
print("=" * 60)

print('''
# 执行研究
result = graph.invoke({
    "topic": "人工智能在医疗领域的应用"
})

print("最终文章:")
print(result["article"])
print()
print(f"修订次数: {result['iteration']}")
''')

print()
print("=" * 60)
print("6. 添加人类审核")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END

# 人类审核节点
def human_review_node(state):
    print("\\n=== 当前文章 ===")
    print(state["article"])
    print("\\n请审核 (输入修改意见或'通过'):")

    feedback = input()
    if feedback in ["通过", "pass", "ok", "y"]:
        return {"human_approved": True}
    return {"human_approved": False, "human_feedback": feedback}

# 修改后的工作流
workflow = StateGraph(ResearchState)
# ... 其他节点 ...

workflow.add_node("human_review", human_review_node)

# 条件边
def after_review(state):
    if state.get("human_approved"):
        return "finish"
    return "revise"

workflow.add_edge("review", "human_review")
workflow.add_conditional_edges(
    "human_review",
    after_review,
    {"revise": "revise", "finish": END}
)
''')

print()
print("=" * 60)
print("7. 多团队协作")
print("=" * 60)

print('''
# 团队1: 技术团队
tech_researcher = ...
tech_writer = ...

# 团队2: 商业团队
biz_researcher = ...
biz_writer = ...

# 综合团队
class TeamCollaboration:
    def __init__(self):
        self.tech_graph = tech_workflow.compile()
        self.biz_graph = biz_workflow.compile()

    def run(self, topic):
        # 并行执行
        tech_result = self.tech_graph.invoke({"topic": f"{topic}技术方面"})
        biz_result = self.biz_graph.invoke({"topic": f"{topic}商业方面"})

        # 综合报告
        final_report = f"""
        # {topic}综合报告

        ## 技术分析
        {tech_result['article']}

        ## 商业分析
        {biz_result['article']}
        """

        return {"article": final_report}
''')

print()
print("=" * 60)
print("8. 状态持久化")
print("=" * 60)

print('''
from langgraph.checkpoint.sqlite import SqliteSaver

# 持久化存储
checkpointer = SqliteSaver.from_conn_string("research.db")

# 编译时添加
graph = workflow.compile(checkpointer=checkpointer)

# 执行并保存状态
config = {"configurable": {"thread_id": "project_001"}}

# 首次执行
result1 = graph.invoke(
    {"topic": "AI发展"},
    config=config
)

# 继续执行
result2 = graph.invoke(
    {"topic": "继续"},
    config=config
)

# 查看历史
history = [state for state in graph.get_state_history(config)]
''')

print()
print("=" * 60)
print("9. 错误处理")
print("=" * 60)

print("9.1 重试机制")
print('''
from langgraph.errors import NodeInterrupt

def safe_node(state):
    try:
        # 正常逻辑
        return process(state)
    except Exception as e:
        print(f"节点执行失败: {e}")
        # 重试或返回默认值
        return {"error": str(e)}
''')

print()
print("9.2 中断处理")
print('''
def review_node(state):
    # 检查是否需要人工介入
    if contains_sensitive_content(state["article"]):
        raise NodeInterrupt("内容包含敏感信息，需要人工审核")

    return {"review": "审核通过"}
''')

print()
print("=" * 60)
print("10. 监控和日志")
print("=" * 60)

print("10.1 步骤日志")
print('''
import logging
from datetime import datetime

class WorkflowMonitor:
    def __init__(self):
        self.steps = []

    def log(self, node, state):
        self.steps.append({
            "time": datetime.now().isoformat(),
            "node": node,
            "state_keys": list(state.keys())
        })

    def get_report(self):
        return f"执行了{len(self.steps)}个步骤"

monitor = WorkflowMonitor()
''')

print()
print("10.2 性能监控")
print('''
import time
from functools import wraps

def time_node(func):
    @wraps(func)
    def wrapper(state):
        start = time.time()
        result = func(state)
        duration = time.time() - start

        print(f"{func.__name__} 耗时: {duration:.2f}秒")
        return result
    return wrapper
''')

print()
print("=" * 60)
print("11. 部署建议")
print("=" * 60)

print("11.1 本地部署")
print("  - 使用Docker容器")
print("  - 配置资源限制")
print("  - 设置日志级别")
print()
print("11.2 云端部署")
print("  - 使用云函数")
print("  - 配置自动扩缩容")
print("  - 设置监控告警")
print()
print("11.3 API服务")
print("  - FastAPI包装")
print("  - 添加认证")
print("  - 限流保护")

print()
print("=" * 60)
print("12. 项目总结")
print("=" * 60)

print("Agent进阶项目要点:")
print()
print("* 项目架构:")
print("  - 多Agent协作")
print("  - LangGraph工作流")
print("  - 人类审核机制")
print()
print("* 核心功能:")
print("  - 自动研究")
print("  - 协作写作")
print("  - 多轮审核")
print("  - 状态持久化")
print()
print("* 扩展方向:")
print("  - 多团队协作")
print("  - 实时数据接入")
print("  - 可视化界面")
print()
print("* 最佳实践:")
print("  - 清晰的Agent角色")
print("  - 完善的工作流")
print("  - 适当的错误处理")
