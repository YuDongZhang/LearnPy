"""
Agent工具系统
==========

详细介绍Agent中各种工具的设计和使用。
"""

print("=" * 60)
print("1. 工具系统概述")
print("=" * 60)

print("工具系统:")
print("  - Agent与外部世界交互的桥梁")
print("  - 扩展LLM的能力边界")
print("  - 支持各类API和功能")

print()
print("=" * 60)
print("2. 工具类型")
print("=" * 60)

print("| 类型 | 功能 | 示例 |")
print("|------|------|------|")
print("| 搜索 | 获取实时信息 | Google, DDG |")
print("| API | 调用外部服务 | 天气, 股票 |")
print("| 计算 | 数学运算 | 计算器, Python |")
print("| 文件 | 文件操作 | 读写文件 |")
print("| 数据库 | 数据操作 | SQL查询 |")
print("| 代码 | 执行代码 | Python REPL |")

print()
print("=" * 60)
print("3. 基础工具定义")
print("=" * 60)

print("3.1 简单函数工具")
print('''
from langchain.tools import Tool

def get_weather(location):
    return f"{location}天气晴朗，25度"

weather_tool = Tool(
    name="天气查询",
    func=get_weather,
    description="查询指定城市的天气"
)
''')

print()
print("3.2 多参数工具")
print('''
from langchain.tools import Tool
import json

def send_email(to, subject, body):
    return f"邮件已发送给{to}"

def send_email_wrapper(args):
    args_dict = json.loads(args)
    return send_email(**args_dict)

email_tool = Tool(
    name="发送邮件",
    func=send_email_wrapper,
    description="发送邮件，需要to(收件人), subject(主题), body(内容)"
)
''')

print()
print("=" * 60)
print("4. 自定义工具类")
print("=" * 60)

print("4.1 BaseTool")
print('''
from langchain.tools import BaseTool
from pydantic import BaseModel

class WeatherInput(BaseModel):
    location: str
    unit: str = "celsius"

class WeatherTool(BaseTool):
    name = "weather"
    description = "获取指定位置的天气信息"
    args_schema = WeatherInput

    def _run(self, location: str, unit: str = "celsius"):
        # 调用天气API
        return f"{location}天气: 晴, 25度"

weather = WeatherTool()
''')

print()
print("4.2 异步工具")
print('''
from langchain.tools import BaseTool

class AsyncSearchTool(BaseTool):
    name = "async_search"
    description = "异步搜索"

    async def _arun(self, query: str):
        # 异步搜索逻辑
        await asyncio.sleep(1)
        return f"搜索结果: {query}"

search_tool = AsyncSearchTool()
''')

print()
print("=" * 60)
print("5. 搜索工具")
print("=" * 60)

print("5.1 DuckDuckGo搜索")
print('''
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
result = search.run("Python教程")
''')

print()
print("5.2 SerpAPI搜索")
print('''
from langchain_community.tools import SerpAPIWrapper

search = SerpAPIWrapper()
result = search.run("最新AI新闻")
''')

print()
print("5.3 Wikipedia搜索")
print('''
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api = WikipediaAPIWrapper()
wiki = WikipediaQueryRun(api_wrapper=api)
result = wiki.run("Transformer")
''')

print()
print("=" * 60)
print("6. 计算工具")
print("=" * 60)

print("6.1 Python REPL")
print('''
from langchain_experimental.tools import PythonREPLTool

python = PythonREPLTool()

# 执行代码
result = python.run("print([x**2 for x in range(10)])")
''')

print()
print("6.2 计算器")
print('''
from langchain.tools import Tool

def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"错误: {e}"

calc_tool = Tool(
    name="计算器",
    func=calculator,
    description="进行数学计算"
)
''')

print()
print("=" * 60)
print("7. API工具")
print("=" * 60)

print("7.1 HTTP请求工具")
print('''
import requests
from langchain.tools import Tool

def http_request(url, method="GET"):
    response = requests.request(method, url)
    return response.text[:500]

http_tool = Tool(
    name="HTTP请求",
    func=lambda x: http_request(x),
    description="发送HTTP请求"
)
''')

print()
print("7.2 自定义API工具")
print('''
import requests
from langchain.tools import BaseTool
from pydantic import BaseModel

class WeatherInput(BaseModel):
    city: str

class WeatherAPI(BaseTool):
    name = "weather_api"
    description = "获取城市天气"

    def _run(self, city: str):
        # 调用天气API
        api_key = "your_key"
        url = f"https://api.weather.com/v3?city={city}&key={api_key}"
        # return requests.get(url).json()
        return f"{city}天气: 晴朗, 25度"

weather_api = WeatherAPI()
''')

print()
print("=" * 60)
print("8. 文件工具")
print("=" * 60)

print("8.1 文件读取")
print('''
from langchain_community.tools import FileManagementTool

read_tool = FileManagementTool(
    root_dir=".",
    selected_tools=["read"],
    file_pattern="*.txt"
)

content = read_tool.invoke("data/notes.txt")
''')

print()
print("8.2 文件写入")
print('''
from langchain_community.tools import FileManagementTool

write_tool = FileManagementTool(
    root_dir=".",
    selected_tools=["write"]
)

write_tool.invoke({"file_path": "output.txt", "content": "Hello World"})
''')

print()
print("=" * 60)
print("9. 工具组合")
print("=" * 60)

print("9.1 组合多个工具")
print('''
from langchain.agents import AgentType, initialize_agent, Tool

tools = [
    Tool(name="搜索", func=lambda x: "搜索结果", description="搜索"),
    Tool(name="计算", func=lambda x: str(eval(x)), description="计算"),
    Tool(name="天气", func=lambda x: "天气: 晴", description="查天气"),
]

agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
''')

print()
print("9.2 工具选择策略")
print('''
# 基于任务自动选择工具
def select_tool(task):
    if "搜索" in task:
        return "搜索"
    elif "计算" in task:
        return "计算"
    else:
        return "通用"
''')

print()
print("=" * 60)
print("10. 工具描述优化")
print("=" * 60)

print("好的工具描述:")
print('''
Tool(
    name="天气查询",
    func=get_weather,
    description="获取指定城市的当前天气信息。
                输入: 城市名称(字符串)
                输出: 天气状况、温度、湿度等"
)
''')

print()
print("避免:")
print("  - description太简略")
print("  - 输入输出格式不明确")
print("  - 功能描述模糊")

print()
print("=" * 60)
print("11. 工具错误处理")
print("=" * 60)

print("11.1 工具内部错误处理")
print('''
def safe_tool(input_data):
    try:
        # 正常逻辑
        return process(input_data)
    except ValueError as e:
        return f"输入错误: {str(e)}"
    except TimeoutError:
        return "请求超时，请稍后重试"
    except Exception as e:
        return f"未知错误: {str(e)}"
''')

print()
print("11.2 Agent级别错误处理")
print('''
agent = initialize_agent(
    tools,
    llm,
    handle_parsing_errors="抱歉，我遇到了问题，请重试",
    max_iterations=3
)
''')

print()
print("=" * 60)
print("12. 工具安全")
print("=" * 60)

print("12.1 敏感信息保护")
print('''
import os
from langchain.tools import Tool

# 使用环境变量
api_key = os.getenv("API_KEY")

def safe_api_call(query):
    # 不在日志中记录敏感信息
    return api_wrapper.call(query, hide_key=True)

tool = Tool(func=safe_api_call, ...)
''')

print()
print("12.2 权限控制")
print('''
class RestrictedTool(BaseTool):
    def _run(self, input_data):
        if not self.check_permission(input_data):
            raise PermissionError("无权限执行此操作")
        return self.process(input_data)
''')

print()
print("=" * 60)
print("13. 工具总结")
print("=" * 60)

print("工具系统要点:")
print()
print("* 工具类型:")
print("  - 搜索、计算、API、文件、代码")
print()
print("* 工具定义:")
print("  - 简单函数、BaseTool、异步")
print()
print("* 最佳实践:")
print("  - 清晰的描述")
print("  - 完善的错误处理")
print("  - 适当的权限控制")
print()
print("* 工具组合:")
print("  - 多工具协作")
print("  - 工具选择策略")
