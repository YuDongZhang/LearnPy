"""
LLM Agent概述
==========

介绍LLM Agent的基本概念、发展历程和核心思想。
"""

print("=" * 60)
print("1. Agent简介")
print("=" * 60)

print("LLM Agent:")
print()
print("定义:")
print("  - 基于LLM的智能代理系统")
print("  - 能够自主规划和执行任务")
print("  - 调用外部工具完成复杂操作")
print("  - 具备记忆和推理能力")
print()
print("与传统LLM的区别:")
print("  - 传统LLM: 被动响应")
print("  - Agent: 主动规划+行动")

print()
print("=" * 60)
print("2. Agent发展历程")
print("=" * 60)

print("| 年份 | 里程碑 |")
print("|------|--------|")
print("| 2022 | ReAct论文提出 |")
print("| 2023 | LangChain发布 |")
print("| 2023 | AutoGPT发布 |")
print("| 2023 | BabyAGI发布 |")
print("| 2023 | GPT-4 API + Function Calling |")
print("| 2024 | Agent工作流流行 |")

print()
print("=" * 60)
print("3. Agent核心能力")
print("=" * 60)

print("3.1 推理能力")
print("  - 理解复杂问题")
print("  - 分解任务步骤")
print("  - 逻辑推理")
print()
print("3.2 规划能力")
print("  - 制定执行计划")
print("  - 动态调整")
print("  - 目标分解")
print()
print("3.3 工具使用")
print("  - 调用API")
print("  - 搜索引擎")
print("  - 代码执行")
print()
print("3.4 记忆系统")
print("  - 短期记忆: 对话历史")
print("  - 长期记忆: 外部存储")

print()
print("=" * 60)
print("4. ReAct模式")
print("=" * 60)

print("ReAct (Reason + Act):")
print()
print("核心思想:")
print("  - Thought: 推理当前情况")
print("  - Action: 执行具体行动")
print("  - Observation: 观察结果")
print()
print("示例流程:")
print("  用户: 今天的天气适合跑步吗?")
print("  Thought: 我需要先查询天气信息")
print("  Action: 调用天气API [北京]")
print("  Observation: 天气晴，25度，PM2.5=30")
print("  Thought: 天气很好，适合跑步")
print("  Answer: 今天天气晴朗，温度25度，适合跑步")

print()
print("=" * 60)
print("5. Agent vs Prompt工程")
print("=" * 60)

print("| 方面 | Prompt工程 | Agent |")
print("|------|-----------|-------|")
print("| 交互方式 | 单轮/多轮对话 | 自主执行 |")
print("| 工具使用 | 无 | 有 |")
print("| 复杂任务 | 有限 | 强大 |")
print("| 适用场景 | 问答、创作 | 自动化 |")

print()
print("=" * 60)
print("6. Agent类型")
print("=" * 60)

print("6.1 单一Agent")
print("  - 处理单一类型任务")
print("  - 简单高效")
print()
print("6.2 多Agent系统")
print("  - 多个Agent协作")
print("  - 角色分工")
print("  - 复杂任务处理")
print()
print("6.3 Agent工作流")
print("  - 预定义流程")
print("  - 条件分支")
print("  - 自动化执行")

print()
print("=" * 60)
print("7. 主流框架")
print("=" * 60)

print("7.1 LangChain")
print("  - 最流行的LLM开发框架")
print("  - 丰富的Agent组件")
print("  - 完整的工具生态")
print()
print("7.2 LlamaIndex")
print("  - 专注于数据处理")
print("  - 知识库构建")
print("  - RAG优化")
print()
print("7.3 AutoGPT")
print("  - 自主Agent代表")
print("  - 目标导向")
print("  - 自我反思")
print()
print("7.4 BabyAGI")
print("  - 任务管理系统")
print("  - 动态任务生成")
print("  - 简单架构")

print()
print("=" * 60)
print("8. Agent应用场景")
print("=" * 60)

print("| 场景 | 应用 |")
print("|------|------|")
print("| 智能客服 | 自动问答+业务办理 |")
print("| 个人助理 | 日程管理+信息检索 |")
print("| 编程助手 | 代码生成+调试 |")
print("| 数据分析 | 数据处理+可视化 |")
print("| 自动化 | 工作流执行 |")
print("| 科研 | 文献综述+实验设计 |")

print()
print("=" * 60)
print("9. 安装依赖")
print("=" * 60)

print("pip install langchain")
print("pip install langchain-openai")
print("pip install langchain-community")
print("pip install duckduckgo-search")
print("pip install serpapi")
print("pip install wikipedia")

print()
print("=" * 60)
print("10. 简单示例")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# 定义工具
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="搜索",
        func=search.run,
        description="搜索实时信息"
    )
]

# 创建Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 使用
result = agent.run("Python和JavaScript哪个更适合后端开发?")
print(result)
''')

print()
print("=" * 60)
print("11. Agent挑战")
print("=" * 60)

print("11.1 可靠性")
print("  - Agent可能执行错误操作")
print("  - 需要错误处理和验证")
print()
print("11.2 成本控制")
print("  - 多轮调用成本高")
print("  - 需要优化调用次数")
print()
print("11.3 安全性")
print("  - 工具权限管理")
print("  - 防止恶意调用")
print()
print("11.4 评估")
print("  - 难以评估Agent效果")
print("  - 需要设计评估指标")

print()
print("=" * 60)
print("12. Agent总结")
print("=" * 60)

print("LLM Agent要点:")
print()
print("* 核心能力:")
print("  - 推理、规划、工具使用、记忆")
print()
print("* 技术基础:")
print("  - ReAct模式")
print("  - LangChain框架")
print("  - 工具系统")
print()
print("* 应用场景:")
print("  - 智能客服、个人助理")
print("  - 编程助手、自动化")
print()
print("* 发展趋势:")
print("  - 多Agent协作")
print("  - Agent工作流")
print("  - 自主学习")
