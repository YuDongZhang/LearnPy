"""
7. 进阶实战 - AI研究团队
用LangGraph构建：研究 → 写作 → 审核 → (不通过则修订) 的完整工作流。
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ============================================================
# 1. 定义状态
# ============================================================
class ResearchState(TypedDict):
    topic: str
    research: str
    article: str
    review: str
    iteration: int
    max_iterations: int


# ============================================================
# 2. 定义Agent链
# ============================================================
researcher_chain = (
    ChatPromptTemplate.from_template(
        "你是一个专业研究员。请搜索和分析以下主题的关键信息，提供简要研究报告（200字内）。\n主题: {topic}"
    ) | llm | StrOutputParser()
)

writer_chain = (
    ChatPromptTemplate.from_template(
        "你是一个技术作家。基于以下研究资料撰写一篇结构清晰的短文（300字内）。\n"
        "研究资料: {research}\n"
        "{feedback}"
    ) | llm | StrOutputParser()
)

reviewer_chain = (
    ChatPromptTemplate.from_template(
        "你是一个严格的审核员。审核以下文章，如果质量合格回复'通过'，"
        "否则回复'需要修改: '加上具体修改意见。\n文章: {article}"
    ) | llm | StrOutputParser()
)


# ============================================================
# 3. 定义节点
# ============================================================
def research_node(state: ResearchState) -> dict:
    print(f"\n[研究员] 正在研究: {state['topic']}")
    research = researcher_chain.invoke({"topic": state["topic"]})
    print(f"[研究员] 完成研究")
    return {"research": research, "iteration": 1}


def write_node(state: ResearchState) -> dict:
    feedback = ""
    if state.get("review") and "需要修改" in state["review"]:
        feedback = f"上次审核反馈: {state['review']}，请据此改进。"
    print(f"\n[写手] 正在撰写（第{state.get('iteration', 1)}版）")
    article = writer_chain.invoke({"research": state["research"], "feedback": feedback})
    print(f"[写手] 完成撰写")
    return {"article": article}


def review_node(state: ResearchState) -> dict:
    print(f"\n[审核员] 正在审核第{state['iteration']}版")
    review = reviewer_chain.invoke({"article": state["article"]})
    print(f"[审核员] 审核结果: {review[:50]}...")
    return {"review": review, "iteration": state["iteration"] + 1}


def should_revise(state: ResearchState) -> str:
    if "通过" in state["review"] and "需要修改" not in state["review"]:
        print("\n[流程] 审核通过，结束")
        return "end"
    if state["iteration"] > state.get("max_iterations", 3):
        print(f"\n[流程] 达到最大迭代次数，结束")
        return "end"
    print(f"\n[流程] 需要修订，进入第{state['iteration']}轮")
    return "revise"


# ============================================================
# 4. 构建图
# ============================================================
def build_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("review", review_node)

    workflow.set_entry_point("research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "review")
    workflow.add_conditional_edges(
        "review", should_revise,
        {"revise": "write", "end": END}
    )

    return workflow.compile()


# ============================================================
# 5. 运行
# ============================================================
if __name__ == "__main__":
    graph = build_graph()

    topic = input("输入研究主题（回车使用默认）: ").strip()
    if not topic:
        topic = "LLM Agent的最新发展趋势"

    print(f"\n{'='*60}")
    print(f"AI研究团队启动 | 主题: {topic}")
    print(f"{'='*60}")

    result = graph.invoke({
        "topic": topic,
        "research": "",
        "article": "",
        "review": "",
        "iteration": 0,
        "max_iterations": 3,
    })

    print(f"\n{'='*60}")
    print("最终文章:")
    print(f"{'='*60}")
    print(result["article"])
    print(f"\n共迭代 {result['iteration'] - 1} 次")
