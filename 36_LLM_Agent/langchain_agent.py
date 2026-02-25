"""
LangChain Agent使用
==========

详细介绍LangChain中Agent的使用方法。
"""

print("=" * 60)
print("1. LangChain Agent概述")
print("=" * 60)

print("LangChain Agent:")
print("  - LangChain框架的核心组件")
print("  - 封装了ReAct逻辑")
print("  - 支持多种Agent类型")
print("  - 丰富的工具集成")

print()
print("=" * 60)
print("2. 初始化Agent")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI

# 创建LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 定义工具
def search_function(query):
    return f"搜索结果: {query}的相关信息"

tools = [
    Tool(
        name="搜索",
        func=search_function,
        description="用于搜索信息"
    )
]

# 初始化Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 使用
result = agent.run("Python的装饰器是什么?")
''')

print()
print("=" * 60)
print("3. AgentType类型")
print("=" * 60)

print("3.1 ZERO_SHOT_REACT_DESCRIPTION")
print("  - 最常用类型")
print("  - 零样本推理")
print("  - 基于工具描述选择")
print()
print("3.2 CHAT_ZERO_SHOT_REACT_DESCRIPTION")
print("  - 聊天模型版本")
print("  - 优化了对话格式")
print()
print("3.3 CONVERSATIONAL_REACT_DESCRIPTION")
print("  - 对话式Agent")
print("  - 保持对话上下文")
print()
print("3.4 PLAN_AND_EXECUTE_AGENT")
print("  - 先计划后执行")
print("  - 适合复杂任务")
print()
print("3.5 TOOL_AGENT")
print("  - 纯工具调用Agent")
print("  - 无对话能力")

print()
print("=" * 60)
print("4. 工具定义")
print("=" * 60)

print("4.1 简单函数工具")
print('''
from langchain.tools import Tool

def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "计算错误"

calc_tool = Tool(
    name="计算器",
    func=calculator,
    description="用于数学计算，输入数学表达式"
)
''')

print()
print("4.2 自定义工具类")
print('''
from langchain.tools import BaseTool
from pydantic import BaseModel

class SearchInput(BaseModel):
    query: str

class MySearchTool(BaseTool):
    name = "我的搜索"
    description = "搜索互联网获取信息"
    args_schema = SearchInput

    def _run(self, query):
        # 实现搜索逻辑
        return f"搜索: {query}"

search_tool = MySearchTool()
''')

print()
print("=" * 60)
print("5. 预置工具")
print("=" * 60)

print("5.1 搜索工具")
print('''
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import GoogleSearchRun

# DuckDuckGo搜索
search = DuckDuckGoSearchRun()

# Google搜索(需要API)
google_search = GoogleSearchRun()
''')

print()
print("5.2 文件工具")
print('''
from langchain_community.tools import FileManagementTool

# 读取文件
read_tool = FileManagementTool(
    root_dir=".",
    selected_tools=["read"]
)

# 写入文件
write_tool = FileManagementTool(
    root_dir=".",
    selected_tools=["write"]
)
''')

print()
print("5.3 Python工具")
print('''
from langchain_experimental.tools import PythonREPLTool

# Python代码执行
python_tool = PythonREPLTool()
result = python_tool.run("print(1+2)")
''')

print()
print("=" * 60)
print("6. AgentChain")
print("=" * 60)

print("6.1 基础AgentChain")
print('''
from langchain.chains import AgentExecutor

# 创建Agent执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    max_iterations=10,
    verbose=True
)

# 执行
result = agent_executor.invoke({"input": "Python如何处理JSON?"})
''')

print()
print("6.2 自定义Agent")
print('''
from langchain.agents import Agent
from langchain.agents.agent_types import AgentType

class MyAgent(Agent):
    @classmethod
    def create_prompt(cls, tools):
        return """你是一个AI助手..."""

    @classmethod
    def _validate_tools(cls, tools):
        return tools

    def _fix_old_methods(self, tools):
        pass

agent = MyAgent(tools=tools, llm=llm)
''')

print()
print("=" * 60)
print("7. 记忆系统集成")
print("=" * 60)

print("7.1 对话记忆")
print('''
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 多轮对话
agent.run("你好")
agent.run("Python是什么?")
agent.run("它和Java的区别是什么?")
''')

print()
print("=" * 60)
print("8. 输出解析")
print("=" * 60)

print("8.1 AgentOutputParser")
print('''
from langchain.agents.output_parser import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish

class MyOutputParser(AgentOutputParser):
    def parse(self, text):
        if "Final Answer" in text:
            return AgentFinish(
                return_values={"output": text.split("Final Answer:")[-1].strip()},
                log=text
            )
        # 解析Action
        return AgentAction(...)

agent = initialize_agent(
    tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    output_parser=MyOutputParser()
)
''')

print()
print("=" * 60)
print("9. 错误处理")
print("=" * 60)

print("9.1 最大迭代限制")
print('''
agent = initialize_agent(
    tools, llm,
    max_iterations=5,  # 最多5次调用
    max_execution_time=60,  # 最多60秒
    early_stopping=True
)
''')

print()
print("9.2 自定义错误处理")
print('''
from langchain.callbacks import BaseCallbackHandler

class MyCallbackHandler(BaseCallbackHandler):
    def on_agent_error(self, error, **kwargs):
        print(f"Agent错误: {error}")

agent = initialize_agent(
    tools, llm,
    callbacks=[MyCallbackHandler()],
    handle_parsing_errors=True  # 自动处理解析错误
)
''')

print()
print("=" * 60)
print("10. 实用示例")
print("=" * 60)

print("10.1 研究助手Agent")
print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="搜索",
        func=search.run,
        description="搜索最新信息"
    )
]

research_agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 研究任务
topic = "Transformer架构"
result = research_agent.run(f"请搜索{topic}的最新发展和应用")
''')

print()
print("10.2 编程助手Agent")
print('''
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import Tool

python_repl = PythonREPLTool()

tools = [
    Tool(
        name="Python执行",
        func=python_repl.run,
        description="执行Python代码"
    )
]

code_agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = code_agent.run("写一个快速排序算法并执行")
''')

print()
print("=" * 60)
print("11. LangChain Agents对比")
print("=" * 60)

print("| Agent类型 | 特点 | 适用场景 |")
print("|----------|------|---------|")
print("| ZERO_SHOT | 零样本 | 简单任务 |")
print("| CONVERSATIONAL | 对话 | 客服 |")
print("| PLAN_AND_EXECUTE | 计划+执行 | 复杂任务 |")
print("| CHAT_ZERO_SHOT | 聊天版 | 对话场景 |")

print()
print("=" * 60)
print("12. 总结")
print("=" * 60)

print("LangChain Agent要点:")
print()
print("* 核心组件:")
print("  - Agent、Tools、Memory")
print()
print("* 使用流程:")
print("  - 定义工具 -> 初始化Agent -> 执行任务")
print()
print("* 关键配置:")
print("  - agent_type、max_iterations、memory")
print()
print("* 最佳实践:")
print("  - 清晰的工具描述")
print("  - 合理的错误处理")
print("  - 适当的记忆管理")
