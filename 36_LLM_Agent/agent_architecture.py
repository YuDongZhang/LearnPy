"""
Agent架构设计
==========

介绍LLM Agent的架构设计和核心组件。
"""

print("=" * 60)
print("1. Agent整体架构")
print("=" * 60)

print("Agent架构:")
print()
print("  用户输入 -> LLM -> 推理引擎 -> 工具选择 -> 执行 -> 反馈")
print("                    |                              |")
print("                    v                              v")
print("                 记忆系统 <-------------------------+")

print()
print("=" * 60)
print("2. 核心组件")
print("=" * 60)

print("2.1 LLM大脑")
print("  - 推理引擎")
print("  - 决策中心")
print("  - 自然语言理解生成")
print()
print("2.2 工具系统")
print("  - 工具注册")
print("  - 工具选择")
print("  - 工具执行")
print()
print("2.3 记忆系统")
print("  - 短期记忆: 对话上下文")
print("  - 长期记忆: 外部知识")
print()
print("2.4 规划器")
print("  - 任务分解")
print("  - 执行计划")
print("  - 动态调整")

print()
print("=" * 60)
print("3. Agent循环")
print("=" * 60)

print("Agent执行循环:")
print()
print("  1. 接收用户输入")
print("  2. 分析任务意图")
print("  3. 决定行动策略")
print("  4. 执行行动(调用工具或直接回答)")
print("  5. 获取执行结果")
print("  6. 评估结果")
print("  7. 决定是否继续")
print("  8. 返回结果或继续循环")

print()
print("=" * 60)
print("4. Prompt模板设计")
print("=" * 60)

print('''
# Agent系统Prompt示例
AGENT_PROMPT = """你是一个专业的AI助手。

可用工具:
- 搜索: 用于搜索实时信息
- 计算器: 用于数学计算
- 天气: 查询天气信息

工作流程:
1. 理解用户问题
2. 选择合适的工具
3. 执行工具获取信息
4. 基于信息回答问题

注意:
- 如果不确定使用哪个工具，可以分析后选择
- 确保答案准确，必要时多次查询
- 用中文回答用户问题
"""

# 工具描述格式
TOOL_DESCRIPTIONS = [
    {
        "name": "search",
        "description": "搜索实时信息，输入为搜索关键词",
        "parameters": {"type": "string"}
    },
    {
        "name": "calculator", 
        "description": "进行数学计算，输入为数学表达式",
        "parameters": {"type": "string"}
    }
]
''')

print()
print("=" * 60)
print("5. 记忆系统设计")
print("=" * 60)

print("5.1 对话记忆")
print('''
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryMemory

# 简单对话记忆
memory = ConversationBufferMemory()

# 摘要记忆（适用于长对话）
memory = ConversationSummaryMemory(llm=llm)
''')

print()
print("5.2 向量记忆")
print('''
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 长期记忆存储
vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())

# 检索相关记忆
def retrieve_memory(query, k=3):
    return vectorstore.similarity_search(query, k=k)
''')

print()
print("5.3 组合记忆")
print('''
from langchain.memory import CombinedMemory

# 组合多种记忆
memory = CombinedMemory([
    ConversationBufferMemory(),
    VectorStoreRetrieverMemory(vectorstore=vectorstore)
])
''')

print()
print("=" * 60)
print("6. 工具调用设计")
print("=" * 60)

print("6.1 基础工具接口")
print('''
from langchain.tools import Tool

# 定义工具
def search_wiki(query):
    import wikipedia
    return wikipedia.summary(query)

wiki_tool = Tool(
    name="Wikipedia搜索",
    func=search_wiki,
    description="用于搜索Wikipedia，输入为搜索关键词"
)
''')

print()
print("6.2 自定义工具")
print('''
from langchain.tools import BaseTool
from pydantic import BaseModel

class SearchInput(BaseModel):
    query: str

class WikipediaSearchTool(BaseTool):
    name = "wikipedia_search"
    description = "搜索Wikipedia获取信息"
    args_schema = SearchInput

    def _run(self, query):
        import wikipedia
        return wikipedia.summary(query)

wiki_tool = WikipediaSearchTool()
''')

print()
print("=" * 60)
print("7. Agent类型")
print("=" * 60)

print("7.1 行动Agent (Action Agent)")
print("  - 直接决定行动")
print("  - 单步执行")
print("  - 适合简单任务")
print()
print("7.2 计划执行Agent (Plan-and-Execute Agent)")
print("  - 先制定计划")
print("  - 再逐步执行")
print("  - 适合复杂任务")
print()
print("7.3 反思Agent (Reflect Agent)")
print("  - 执行后反思")
print("  - 自我改进")
print("  - 质量更高")

print()
print("=" * 60)
print("8. 错误处理")
print("=" * 60)

print("8.1 工具执行失败")
print('''
try:
    result = tool.invoke(input)
except Exception as e:
    logger.error(f"工具执行失败: {e}")
    result = f"工具执行失败: {str(e)}"
''')

print()
print("8.2 重试机制")
print('''
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_with_retry(agent, input_text):
    return agent.invoke(input_text)
''')

print()
print("=" * 60)
print("9. 多Agent系统")
print("=" * 60)

print("9.1 Agent协作模式")
print('''
class MultiAgentSystem:
    def __init__(self):
        self.agents = {
            "researcher": ResearcherAgent(),
            "writer": WriterAgent(),
            "reviewer": ReviewerAgent()
        }

    def execute(self, task):
        # 1. 研究Agent收集信息
        research_result = self.agents["researcher"].execute(task)

        # 2. 写作Agent生成内容
        draft = self.agents["writer"].execute(research_result)

        # 3. 审核Agent审查
        final = self.agents["reviewer"].execute(draft)

        return final
''')

print()
print("9.2 Agent通信")
print('''
# Agent间通信协议
message = {
    "from": "writer",
    "to": "reviewer",
    "content": draft_content,
    "type": "request_review"
}
''')

print()
print("=" * 60)
print("10. 架构选择")
print("=" * 60)

print("| 架构 | 适用场景 | 复杂度 |")
print("|------|---------|--------|")
print("| 单Agent | 简单任务 | 低 |")
print("| Agent+Tools | 中等任务 | 中 |")
print("| Multi-Agent | 复杂任务 | 高 |")
print("| Agent工作流 | 自动化流程 | 中 |")

print()
print("=" * 60)
print("11. 性能优化")
print("=" * 60)

print("11.1 减少LLM调用")
print("  - 批量处理")
print("  - 缓存结果")
print("  - 条件判断跳过")
print()
print("11.2 工具优化")
print("  - 工具描述清晰")
print("  - 减少不必要调用")
print("  - 工具结果缓存")
print()
print("11.3 记忆优化")
print("  - 选择性记忆")
print("  - 摘要压缩")
print("  - 定期清理")

print()
print("=" * 60)
print("12. 架构总结")
print("=" * 60)

print("Agent架构要点:")
print()
print("* 核心组件:")
print("  - LLM大脑、工具系统、记忆系统、规划器")
print()
print("* 设计原则:")
print("  - 模块化、可扩展、可组合")
print()
print("* 实现考虑:")
print("  - 错误处理、性能优化、安全性")
print()
print("* 架构选择:")
print("  - 根据任务复杂度选择合适架构")
