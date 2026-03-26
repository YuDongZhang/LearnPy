"""
4. LangChain Agent实践 - 代码示例
演示不同类型的LangChain Agent及调试技巧。
"""

from langchain.agents import AgentType, AgentExecutor, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ========== 工具定义 ==========
def search(query: str) -> str:
    return f"搜索结果: 关于'{query}'的最新信息..."


def calculator(expr: str) -> str:
    try:
        return str(eval(expr))
    except:
        return "计算错误"


tools = [
    Tool(name="搜索", func=search, description="搜索信息，输入关键词"),
    Tool(name="计算器", func=calculator, description="数学计算，输入表达式"),
]


# ============================================================
# 示例1: 基础ReAct Agent（零样本）
# ============================================================
def demo_zero_shot():
    agent = initialize_agent(
        tools, llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    result = agent.run("Python的GIL是什么？")
    print(f"回答: {result}")


# ============================================================
# 示例2: 带记忆的对话Agent
# ============================================================
def demo_conversational():
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    agent = initialize_agent(
        tools, llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )
    # 多轮对话，Agent会记住上下文
    agent.run("什么是装饰器？")
    agent.run("它和闭包有什么关系？")  # Agent知道"它"指装饰器


# ============================================================
# 示例3: AgentExecutor高级配置
# ============================================================
def demo_agent_executor():
    agent = initialize_agent(
        tools, llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,          # 最多5轮
        max_execution_time=30,     # 最多30秒
        handle_parsing_errors=True,  # 自动处理解析错误
        return_intermediate_steps=True  # 返回中间步骤
    )
    result = agent.invoke({"input": "搜索Python 3.12新特性，然后计算3.12*100"})

    # 查看中间步骤（调试利器）
    print("\n中间步骤:")
    for step in result["intermediate_steps"]:
        action, observation = step
        print(f"  Action: {action.tool} | Input: {action.tool_input}")
        print(f"  Observation: {observation}")

    print(f"\n最终回答: {result['output']}")


# ============================================================
# 运行演示
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("示例1: 基础ReAct Agent")
    print("=" * 60)
    demo_zero_shot()

    print("\n" + "=" * 60)
    print("示例2: 带记忆的对话Agent")
    print("=" * 60)
    demo_conversational()

    print("\n" + "=" * 60)
    print("示例3: AgentExecutor高级配置")
    print("=" * 60)
    demo_agent_executor()
