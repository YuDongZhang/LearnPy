"""
3. LangGraph框架 - 代码示例
演示StateGraph的基本用法：顺序流、条件边、循环。
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# ============================================================
# 示例1: 基础顺序流（搜索 → 写作）
# ============================================================
class BasicState(TypedDict):
    task: str
    search_result: str
    article: str


def search_node(state: BasicState) -> dict:
    task = state["task"]
    return {"search_result": f"关于'{task}'的搜索结果: 找到了3个关键要点..."}


def write_node(state: BasicState) -> dict:
    search = state["search_result"]
    return {"article": f"基于搜索结果撰写的文章:\n{search}\n\n总结: 以上是核心内容。"}


def demo_basic():
    workflow = StateGraph(BasicState)
    workflow.add_node("search", search_node)
    workflow.add_node("write", write_node)
    workflow.set_entry_point("search")
    workflow.add_edge("search", "write")
    workflow.add_edge("write", END)

    graph = workflow.compile()
    result = graph.invoke({"task": "LangGraph入门"})
    print(f"任务: {result['task']}")
    print(f"文章: {result['article']}")


# ============================================================
# 示例2: 条件边（根据任务类型走不同路径）
# ============================================================
class ConditionalState(TypedDict):
    task: str
    task_type: str
    result: str


def classify_node(state: ConditionalState) -> dict:
    task = state["task"]
    if "研究" in task or "调研" in task:
        return {"task_type": "research"}
    elif "代码" in task or "编程" in task:
        return {"task_type": "coding"}
    return {"task_type": "general"}


def research_node(state: ConditionalState) -> dict:
    return {"result": f"[研究模式] 已完成'{state['task']}'的深度调研"}


def coding_node(state: ConditionalState) -> dict:
    return {"result": f"[编程模式] 已完成'{state['task']}'的代码实现"}


def general_node(state: ConditionalState) -> dict:
    return {"result": f"[通用模式] 已完成'{state['task']}'"}


def route(state: ConditionalState) -> str:
    return state["task_type"]


def demo_conditional():
    workflow = StateGraph(ConditionalState)
    workflow.add_node("classify", classify_node)
    workflow.add_node("research", research_node)
    workflow.add_node("coding", coding_node)
    workflow.add_node("general", general_node)

    workflow.set_entry_point("classify")
    workflow.add_conditional_edges(
        "classify", route,
        {"research": "research", "coding": "coding", "general": "general"}
    )
    workflow.add_edge("research", END)
    workflow.add_edge("coding", END)
    workflow.add_edge("general", END)

    graph = workflow.compile()

    for task in ["研究AI趋势", "写一段排序代码", "帮我整理笔记"]:
        result = graph.invoke({"task": task})
        print(f"{task} → {result['result']}")


# ============================================================
# 示例3: 循环（生成 → 检查 → 不满意则重来）
# ============================================================
class LoopState(TypedDict):
    topic: str
    content: str
    iteration: int
    quality_ok: bool


def generate_node(state: LoopState) -> dict:
    iteration = state.get("iteration", 0) + 1
    content = f"第{iteration}版: 关于'{state['topic']}'的内容（质量随迭代提升）"
    return {"content": content, "iteration": iteration}


def check_node(state: LoopState) -> dict:
    # 模拟：第3次迭代才通过
    quality_ok = state["iteration"] >= 3
    status = "通过" if quality_ok else "不通过，需要改进"
    print(f"  检查第{state['iteration']}版: {status}")
    return {"quality_ok": quality_ok}


def should_continue(state: LoopState) -> str:
    return "end" if state["quality_ok"] else "generate"


def demo_loop():
    workflow = StateGraph(LoopState)
    workflow.add_node("generate", generate_node)
    workflow.add_node("check", check_node)

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "check")
    workflow.add_conditional_edges(
        "check", should_continue,
        {"generate": "generate", "end": END}
    )

    graph = workflow.compile()
    result = graph.invoke({"topic": "Agent架构", "iteration": 0, "quality_ok": False})
    print(f"最终结果: {result['content']}（共迭代{result['iteration']}次）")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("示例1: 基础顺序流")
    print("=" * 60)
    demo_basic()

    print("\n" + "=" * 60)
    print("示例2: 条件边")
    print("=" * 60)
    demo_conditional()

    print("\n" + "=" * 60)
    print("示例3: 循环工作流")
    print("=" * 60)
    demo_loop()
