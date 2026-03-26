"""
5. Agent实战项目 - 代码示例
项目一: 智能研究助手（搜索+摘要+多轮对话）
项目二: 多Agent协作系统（研究员+写手+审核员）
"""

from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ============================================================
# 项目一: 智能研究助手
# ============================================================
def create_research_assistant():
    """创建一个带搜索和记忆的研究助手Agent"""
    search = DuckDuckGoSearchRun()

    tools = [
        Tool(
            name="搜索",
            func=search.run,
            description="搜索互联网获取最新信息，输入为搜索关键词"
        ),
    ]

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    agent = initialize_agent(
        tools, llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    return agent


def run_research_assistant():
    """交互式运行研究助手"""
    agent = create_research_assistant()
    print("智能研究助手已启动（输入 exit 退出）")
    print("-" * 40)

    while True:
        user_input = input("\n你: ")
        if user_input.strip().lower() in ("exit", "quit", "q"):
            print("再见！")
            break
        try:
            response = agent.run(user_input)
            print(f"\n助手: {response}")
        except Exception as e:
            print(f"\n出错了: {e}")


# ============================================================
# 项目二: 多Agent协作系统
# ============================================================
class MultiAgentSystem:
    """研究员 → 写手 → 审核员 的协作流程"""

    def __init__(self):
        search = DuckDuckGoSearchRun()

        # 研究员Agent: 负责搜索收集信息
        self.researcher = initialize_agent(
            [Tool(name="搜索", func=search.run, description="搜索信息")],
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        # 写手Agent: 负责撰写报告
        self.writer = initialize_agent(
            [Tool(name="写作", func=lambda x: x, description="整理写作内容")],
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        # 审核员Agent: 负责审核质量
        self.reviewer = initialize_agent(
            [Tool(name="审核", func=lambda x: x, description="审核内容质量")],
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def run(self, topic: str) -> str:
        print(f"\n{'='*50}")
        print(f"主题: {topic}")
        print(f"{'='*50}")

        # 步骤1: 研究
        print("\n[1/3] 研究员正在搜索...")
        research = self.researcher.run(f"搜索关于'{topic}'的最新信息和关键要点")

        # 步骤2: 写作
        print("\n[2/3] 写手正在撰写...")
        draft = self.writer.run(
            f"基于以下研究资料，写一篇关于'{topic}'的简要报告:\n{research}"
        )

        # 步骤3: 审核
        print("\n[3/3] 审核员正在审核...")
        final = self.reviewer.run(
            f"审核以下报告，指出问题并给出改进建议:\n{draft}"
        )

        return final


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("选择运行模式:")
    print("1. 智能研究助手（交互式）")
    print("2. 多Agent协作系统（自动）")
    choice = input("输入 1 或 2: ").strip()

    if choice == "1":
        run_research_assistant()
    elif choice == "2":
        system = MultiAgentSystem()
        result = system.run("LLM Agent的最新发展趋势")
        print(f"\n最终报告:\n{result}")
    else:
        print("无效选择")
