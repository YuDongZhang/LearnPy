"""
3. 工具系统 - 代码示例
演示三种定义工具的方式，以及常用预置工具的使用。
"""

import json
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ============================================================
# 方式一：简单函数 + Tool包装
# ============================================================
def search_mock(query: str) -> str:
    """模拟搜索工具"""
    return f"搜索'{query}'的结果: 这是一条模拟的搜索结果。"


search_tool = Tool(
    name="搜索",
    func=search_mock,
    description="搜索互联网信息，输入为搜索关键词"
)


# ============================================================
# 方式二：继承BaseTool（支持多参数+参数校验）
# ============================================================
class EmailInput(BaseModel):
    to: str
    subject: str
    body: str


class SendEmailTool(BaseTool):
    name: str = "发送邮件"
    description: str = "发送邮件。输入JSON: {to, subject, body}"
    args_schema: type = EmailInput

    def _run(self, to: str, subject: str, body: str) -> str:
        # 实际项目中调用邮件API
        return f"邮件已发送给{to}，主题: {subject}"


email_tool = SendEmailTool()


# ============================================================
# 方式三：带错误处理的工具
# ============================================================
def safe_calculator(expression: str) -> str:
    """带完善错误处理的计算器"""
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "输入错误: 只支持数学表达式（数字和+-*/）"
        result = eval(expression)
        return f"计算结果: {result}"
    except ZeroDivisionError:
        return "错误: 除数不能为零"
    except SyntaxError:
        return "错误: 表达式格式不正确"
    except Exception as e:
        return f"未知错误: {e}"


calc_tool = Tool(
    name="计算器",
    func=safe_calculator,
    description="数学计算，输入数学表达式，如 '(1+2)*3'"
)


# ============================================================
# 组合多个工具创建Agent
# ============================================================
tools = [search_tool, email_tool, calc_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    # 测试不同工具的调用
    queries = [
        "帮我搜索一下Python异步编程的资料",
        "计算 (100 + 200) * 0.8",
    ]
    for q in queries:
        print(f"\n{'='*50}")
        print(f"用户: {q}")
        result = agent.run(q)
        print(f"Agent: {result}")
