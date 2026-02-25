"""
LangGraph入门
==========

详细介绍LangGraph框架的使用。
"""

print("=" * 60)
print("1. LangGraph概述")
print("=" * 60)

print("LangGraph:")
print("  - LangChain推出的图结构工作流框架")
print("  - 用于构建Agent和多步骤工作流")
print("  - 基于状态图的设计")
print("  - 支持循环和条件分支")
print()
print("核心概念:")
print("  - Node: 执行单元")
print("  - Edge: 连接关系")
print("  - State: 共享状态")
print("  - Graph: 整体流程")

print()
print("=" * 60)
print("2. 核心概念")
print("=" * 60)

print("2.1 State (状态)")
print('''
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_step: str
    result: str
''')

print()
print("2.2 Node (节点)")
print('''
def my_node(state: AgentState) -> AgentState:
    # 处理逻辑
    state["current_step"] = "node1"
    state["result"] = "处理完成"
    return state
''')

print()
print("2.3 Edge (边)")
print('''
# 边类型
# 1. 正常边: node1 -> node2
# 2. 条件边: node1 -> (if) node2 / (else) node3
# 3. START和END
''')

print()
print("=" * 60)
print("3. 简单LangGraph示例")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. 定义状态
class GraphState(TypedDict):
    task: str
    result: str

# 2. 定义节点
def search_node(state):
    task = state["task"]
    result = f"搜索完成: {task}"
    return {"result": result}

def write_node(state):
    result = state["result"]
    return {"result": result + " | 写作完成"}

# 3. 创建图
workflow = StateGraph(GraphState)

# 4. 添加节点
workflow.add_node("search", search_node)
workflow.add_node("write", write_node)

# 5. 添加边
workflow.set_entry_point("search")
workflow.add_edge("search", "write")
workflow.add_edge("write", END)

# 6. 编译
graph = workflow.compile()

# 7. 执行
result = graph.invoke({"task": "AI发展"})
''')

print()
print("=" * 60)
print("4. 条件边")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END

class ConditionalState(TypedDict):
    task: str
    task_type: str
    result: str

def classify_node(state):
    task = state["task"]
    task_type = "research" if "研究" in task else "general"
    return {"task_type": task_type}

def research_node(state):
    return {"result": "研究完成"}

def general_node(state):
    return {"result": "处理完成"}

def route_decision(state):
    if state["task_type"] == "research":
        return "research"
    return "general"

workflow = StateGraph(ConditionalState)

workflow.add_node("classify", classify_node)
workflow.add_node("research", research_node)
workflow.add_node("general", general_node)

workflow.set_entry_point("classify")
workflow.add_conditional_edges(
    "classify",
    route_decision,
    {"research": "research", "general": "general"}
)
workflow.add_edge("research", END)
workflow.add_edge("general", END)

graph = workflow.compile()
''')

print()
print("=" * 60)
print("5. 循环工作流")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END

class LoopState(TypedDict):
    iteration: int
    result: str

def generate_node(state):
    return {
        "iteration": state["iteration"] + 1,
        "result": f"生成版本{state['iteration'] + 1}"
    }

def check_node(state):
    if state["iteration"] >= 3:
        return "accept"
    return "continue"

workflow = StateGraph(LoopState)

workflow.add_node("generate", generate_node)
workflow.add_node("check", check_node)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "check")
workflow.add_conditional_edges(
    "check",
    lambda x: "generate" if x["result"] else END,
    {"continue": "generate", "accept": END}
)

graph = workflow.compile()
''')

print()
print("=" * 60)
print("6. 多Agent协作")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END

class MultiAgentState(TypedDict):
    task: str
    researcher_result: str
    writer_result: str
    reviewer_result: str

def researcher_node(state):
    task = state["task"]
    return {"researcher_result": f"研究: {task}"}

def writer_node(state):
    research = state["researcher_result"]
    return {"writer_result": f"写作基于: {research}"}

def reviewer_node(state):
    draft = state["writer_result"]
    return {"reviewer_result": f"审核: {draft}"}

workflow = StateGraph(MultiAgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")
workflow.add_edge("reviewer", END)

graph = workflow.compile()
result = graph.invoke({"task": "AI发展"})
''')

print()
print("=" * 60)
print("7. 工具集成")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent

llm = ChatOpenAI(model="gpt-4o")

# 定义工具
tools = [...]

# 创建Agent
agent = create_tool_calling_agent(llm, tools)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# 定义节点
def agent_node(state):
    result = agent_executor.invoke({"input": state["task"]})
    return {"result": result["output"]}

# 构建图
workflow = StateGraph(GraphState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

graph = workflow.compile()
''')

print()
print("=" * 60)
print("8. 状态持久化")
print("=" * 60)

print("8.1 内存状态")
print('''
from langgraph.checkpoint.memory import MemorySaver

# 创建检查点
checkpointer = MemorySaver()

# 编译时添加
graph = workflow.compile(checkpointer=checkpointer)

# 执行并保存状态
config = {"configurable": {"thread_id": "user_123"}}
graph.invoke({"task": "任务1"}, config)
graph.invoke({"task": "任务2"}, config)  # 继续同一会话
''')

print()
print("8.2 文件状态")
print('''
from langgraph.checkpoint.sqlite import SqliteSaver

# SQLite持久化
checkpointer = SqliteSaver.from_conn_string(":memory:")

graph = workflow.compile(checkpointer=checkpointer)
''')

print()
print("=" * 60)
print("9. 人类交互")
print("=" * 60)

print('''
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# 批准节点
def approval_node(state):
    user_input = input("是否批准? (yes/no): ")
    return {"approved": user_input.lower() == "yes"}

# 条件判断
def should_continue(state):
    if state.get("approved"):
        return "approved"
    return "rejected"

workflow = StateGraph(GraphState)
workflow.add_node("agent", agent_node)
workflow.add_node("approval", approval_node)

workflow.set_entry_point("agent")
workflow.add_edge("agent", "approval")
workflow.add_conditional_edges(
    "approval",
    should_continue,
    {"approved": END, "rejected": "agent"}
)
''')

print()
print("=" * 60)
print("10. 流式输出")
print("=" * 60)

print('''
# 流式执行
for chunk in graph.stream({"task": "AI"}):
    print(chunk)

# 流式消息
from langchain.schema import HumanMessage

for event in graph.stream(
    {"messages": [HumanMessage(content="Hello")]},
    stream_mode="values"
):
    if "messages" in event:
        print(event["messages"][-1].content)
''')

print()
print("=" * 60)
print("11. LangGraph vs LangChain Agent")
print("=" * 60)

print("| 特性 | LangChain Agent | LangGraph |")
print("|------|-----------------|-----------|")
print("| 灵活性 | 高 | 更高 |")
print("| 控制力 | 中 | 细粒度 |")
print("| 循环支持 | 有限 | 完全支持 |")
print("| 可视化 | 无 | 有 |")
print("| 适用场景 | 简单任务 | 复杂工作流 |")

print()
print("=" * 60)
print("12. LangGraph最佳实践")
print("=" * 60)

print("1. 状态设计")
print("  - 只保留必要字段")
print("  - 避免状态膨胀")
print()
print("2. 节点设计")
print("  - 单一职责")
print("  - 清晰的输入输出")
print()
print("3. 边设计")
print("  - 避免过于复杂")
print("  - 条件边要清晰")
print()
print("4. 错误处理")
print("  - 节点内try-except")
print("  - 重试机制")

print()
print("=" * 60)
print("13. LangGraph总结")
print("=" * 60)

print("LangGraph要点:")
print()
print("* 核心概念:")
print("  - State、Node、Edge、Graph")
print()
print("* 特点:")
print("  - 图结构工作流")
print("  - 支持循环和条件")
print("  - 状态持久化")
print("  - 人类交互")
print()
print("* 适用场景:")
print("  - 多Agent协作")
print("  - 复杂工作流")
print("  - 需要细粒度控制的场景")
