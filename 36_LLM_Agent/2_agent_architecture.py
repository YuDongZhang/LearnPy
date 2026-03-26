"""
2. Agent架构 - 代码示例
演示Agent的核心组件：LLM、工具、记忆、Prompt模板。
"""

from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_openai import ChatOpenAI

# ========== 1. LLM大脑 ==========
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# ========== 2. 工具系统 ==========
def calculator(expression: str) -> str:
    """安全的计算器工具"""
    try:
        # 只允许数学表达式
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "错误: 只支持数学表达式"
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"


def get_weather(city: str) -> str:
    """模拟天气查询工具"""
    # 实际项目中调用天气API
    weather_data = {
        "北京": "晴，25°C，湿度40%",
        "上海": "多云，22°C，湿度65%",
        "广州": "小雨，28°C，湿度80%",
    }
    return weather_data.get(city, f"{city}: 暂无数据")


tools = [
    Tool(name="计算器", func=calculator, description="数学计算，输入数学表达式"),
    Tool(name="天气查询", func=get_weather, description="查询城市天气，输入城市名"),
]

# ========== 3. 记忆系统 ==========
# 方式A: 完整对话记忆（短对话推荐）
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 方式B: 摘要记忆（长对话推荐）
# summary_memory = ConversationSummaryMemory(llm=llm)

# ========== 4. 组装Agent ==========
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=buffer_memory,
    verbose=True,
    max_iterations=5,           # 防止死循环
    handle_parsing_errors=True  # 自动处理解析错误
)

# ========== 5. 多轮对话演示 ==========
if __name__ == "__main__":
    queries = [
        "北京今天天气怎么样？",
        "那上海呢？",
        "帮我算一下 (25 + 22) / 2",
    ]
    for q in queries:
        print(f"\n用户: {q}")
        result = agent.run(q)
        print(f"Agent: {result}")
