"""
Agent实战项目
==========

通过实际项目练习Agent的开发。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("项目1: 智能研究助手")
print()
print("功能:")
print("  - 自动搜索信息")
print("  - 内容摘要")
print("  - 生成报告")
print()
print("技术栈:")
print("  - LangChain")
print("  - DuckDuckGo搜索")
print("  - OpenAI API")

print()
print("=" * 60)
print("2. 智能研究助手")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# 初始化LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 搜索工具
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="搜索",
        func=search.run,
        description="搜索互联网获取最新信息"
    ),
    Tool(
        name="摘要",
        func=lambda x: f"已对内容进行摘要: {x[:100]}...",
        description="对长文本进行摘要"
    )
]

# 记忆系统
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建Agent
research_agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 使用
result = research_agent.run("搜索Python异步编程的最新发展")
''')

print()
print("=" * 60)
print("3. 编程助手Agent")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Python执行工具
python_repl = PythonREPLTool()

# 代码审查工具
def code_review(code):
    review_prompt = f"请审查以下Python代码的问题:\\n{code}"
    return review_prompt

tools = [
    Tool(
        name="执行代码",
        func=python_repl.run,
        description="执行Python代码并返回结果"
    ),
    Tool(
        name="代码审查",
        func=code_review,
        description="审查代码问题"
    )
]

code_agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 使用
result = code_agent.run("写一个快速排序算法并执行测试")
''')

print()
print("=" * 60)
print("4. 数据分析Agent")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
import pandas as pd

llm = ChatOpenAI(model="gpt-4o", temperature=0)
python = PythonREPLTool()

def load_data(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return f"已加载CSV文件，共{len(df)}行"
    return "不支持的文件格式"

def describe_data(file_path):
    df = pd.read_csv(file_path)
    return str(df.describe())

tools = [
    Tool(
        name="加载数据",
        func=load_data,
        description="加载CSV数据文件"
    ),
    Tool(
        name="数据分析",
        func=describe_data,
        description="分析数据统计信息"
    ),
    Tool(
        name="执行代码",
        func=python.run,
        description="执行Python代码进行分析"
    )
]

data_agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = data_agent.run("分析sales.csv文件的销售趋势")
''')

print()
print("=" * 60)
print("5. 多Agent系统")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 研究Agent
research_tools = [
    Tool(name="搜索", func=lambda x: f"搜索结果: {x}", description="搜索")
]
research_agent = initialize_agent(
    research_tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 写作Agent
write_tools = [
    Tool(name="写作", func=lambda x: f"已写作: {x}", description="写作")
]
writer_agent = initialize_agent(
    write_tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 审核Agent
review_tools = [
    Tool(name="审核", func=lambda x: f"审核意见: {x}", description="审核")
]
reviewer_agent = initialize_agent(
    review_tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 协作流程
class MultiAgentWorkflow:
    def execute(self, topic):
        # 1. 研究
        research = research_agent.run(f"研究{topic}")

        # 2. 写作
        draft = writer_agent.run(f"基于以下研究写一篇报告: {research}")

        # 3. 审核
        final = reviewer_agent.run(f"审核以下报告: {draft}")

        return final

workflow = MultiAgentWorkflow()
result = workflow.execute("AI的未来发展")
''')

print()
print("=" * 60)
print("6. 个人助理Agent")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# 日程管理
def add_event(event):
    return f"已添加日程: {event}"

def get_events(date):
    return f"{date}的日程: 会议 10:00"

# 提醒工具
def set_reminder(reminder):
    return f"已设置提醒: {reminder}"

tools = [
    Tool(name="添加日程", func=add_event, description="添加日程"),
    Tool(name="查看日程", func=get_events, description="查看日程"),
    Tool(name="设置提醒", func=set_reminder, description="设置提醒"),
]

memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

assistant = initialize_agent(
    tools, llm,
    agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 对话式交互
while True:
    user_input = input("你: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = assistant.run(user_input)
    print(f"助手: {response}")
''')

print()
print("=" * 60)
print("7. 自动化工作流")
print("=" * 60)

print('''
from langchain.agents import AgentExecutor, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import schedule
import time

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 报告生成Agent
report_tools = [
    Tool(name="搜索", func=lambda x: f"数据: {x}", description="搜索"),
    Tool(name="分析", func=lambda x: f"分析: {x}", description="分析"),
    Tool(name="生成报告", func=lambda x: f"报告: {x}", description="生成")
]

report_agent = initialize_agent(
    report_tools, llm,
    agent_type=AgentType.PLAN_AND_EXECUTE_AGENT
)

def daily_report():
    print("开始生成每日报告...")
    result = report_agent.run("生成昨天的销售数据报告")
    print(f"报告完成: {result}")

# 定时执行
schedule.every().day.at("09:00").do(daily_report)

while True:
    schedule.run_pending()
    time.sleep(60)
''')

print()
print("=" * 60)
print("8. Agent调试技巧")
print("=" * 60)

print("8.1 开启verbose模式")
print('''
agent = initialize_agent(
    tools, llm,
    verbose=True  # 显示详细日志
)
''')

print()
print("8.2 限制迭代次数")
print('''
agent = initialize_agent(
    tools, llm,
    max_iterations=5,  # 最多5次
    early_stopping=True
)
''')

print()
print("8.3 捕获中间步骤")
print('''
from langchain.agents import AgentExecutor

executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True
)

result = executor.invoke({"input": "你的问题"})
print(result["intermediate_steps"])  # 中间步骤
''')

print()
print("=" * 60)
print("9. 最佳实践")
print("=" * 60)

print("9.1 工具设计")
print("  - 工具描述清晰准确")
print("  - 处理各种边界情况")
print("  - 返回格式一致")
print()
print("9.2 错误处理")
print("  - Agent级别: handle_parsing_errors")
print("  - 工具级别: try-except包装")
print("  - 降级策略")
print()
print("9.3 成本控制")
print("  - 设置max_tokens")
print("  - 缓存常用结果")
print("  - 减少不必要的调用")

print()
print("=" * 60)
print("10. 项目结构")
print("=" * 60)

print("project/")
print("├── agents/")
print("│   ├── __init__.py")
print("│   ├── base.py")
print("│   ├── research.py")
print("│   └── assistant.py")
print("├── tools/")
print("│   ├── __init__.py")
print("│   ├── search.py")
print("│   └── calculator.py")
print("├── memory/")
print("│   └── memory.py")
print("├── main.py")
print("└── requirements.txt")

print()
print("=" * 60)
print("11. 总结")
print("=" * 60)

print("Agent项目要点:")
print()
print("* 实战项目:")
print("  - 智能研究助手")
print("  - 编程助手")
print("  - 数据分析")
print("  - 个人助理")
print()
print("* 开发技巧:")
print("  - verbose调试")
print("  - 迭代限制")
print("  - 中间步骤捕获")
print()
print("* 最佳实践:")
print("  - 工具清晰描述")
print("  - 完善错误处理")
print("  - 成本控制")
print()
print("* 扩展方向:")
print("  - 多Agent协作")
print("  - Agent工作流")
print("  - 自主学习")
