"""
1. 多Agent系统 - 代码示例
演示串行协作：研究员 → 写手 → 审核员
"""

from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ============================================================
# 定义三个角色Agent
# ============================================================

# 研究员：负责搜索收集信息
researcher = initialize_agent(
    tools=[
        Tool(name="搜索", func=lambda q: f"搜索'{q}'的结果: 找到3篇相关文章...", description="搜索信息")
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

# 写手：负责撰写内容
writer = initialize_agent(
    tools=[
        Tool(name="写作", func=lambda x: x, description="整理并写作内容")
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

# 审核员：负责审核质量
reviewer = initialize_agent(
    tools=[
        Tool(name="审核", func=lambda x: x, description="审核内容质量")
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)


# ============================================================
# 串行协作流程
# ============================================================
class MultiAgentPipeline:
    """研究员 → 写手 → 审核员 的串行协作"""

    def run(self, topic: str) -> str:
        print(f"\n{'='*50}")
        print(f"主题: {topic}")
        print(f"{'='*50}")

        # Step 1: 研究
        print("\n[1/3] 研究员搜索中...")
        research = researcher.run(f"搜索关于'{topic}'的关键信息和最新进展")

        # Step 2: 写作
        print("\n[2/3] 写手撰写中...")
        draft = writer.run(f"基于以下研究资料写一篇简要报告:\n{research}")

        # Step 3: 审核
        print("\n[3/3] 审核员审核中...")
        final = reviewer.run(f"审核以下报告，指出问题并给出改进建议:\n{draft}")

        return final


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    pipeline = MultiAgentPipeline()
    result = pipeline.run("大语言模型Agent的最新发展")
    print(f"\n最终结果:\n{result}")
