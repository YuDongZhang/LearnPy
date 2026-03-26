"""
1. Agent概述 - 代码示例
用一个最简单的Agent演示ReAct模式的基本流程。
"""

from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# ========== 1. 创建LLM ==========
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# ========== 2. 定义工具 ==========
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="搜索",
        func=search.run,
        description="搜索互联网获取实时信息，输入为搜索关键词"
    )
]

# ========== 3. 创建Agent ==========
# ZERO_SHOT_REACT_DESCRIPTION: 最基础的ReAct Agent
# verbose=True: 打印每一步的 Thought / Action / Observation
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ========== 4. 运行Agent ==========
if __name__ == "__main__":
    question = "Python 3.12有哪些新特性？"
    print(f"问题: {question}\n")
    result = agent.run(question)
    print(f"\n最终回答: {result}")
