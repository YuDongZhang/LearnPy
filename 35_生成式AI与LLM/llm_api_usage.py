"""
LLM API使用指南
============

介绍如何调用各种LLM API，包括OpenAI、Anthropic、Google等。
"""

print("=" * 60)
print("1. API调用基础")
print("=" * 60)

print("""
API调用流程:

1. 获取API Key
2. 安装SDK
3. 构建请求
4. 发送调用
5. 处理响应

基本结构:
  client = OpenAI(api_key="xxx")
  response = client.chat.completions.create(
      model="gpt-4",
      messages=[...]
  )
  result = response.choices[0].message.content
""")

print()
print("=" * 60)
print("2. OpenAI API")
print("=" * 60)

print("""
OpenAI API:

安装:
  pip install openai

环境变量:
  export OPENAI_API_KEY="your-key"

或代码中设置:
  client = OpenAI(api_key="sk-xxx")
""")

print()
print("=" * 60)
print("3. 基本文本调用")
print("=" * 60)

print('''
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 简单对话
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "什么是Python?"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)

# 查看完整响应
print(f"Usage: {response.usage}")
''')

print()
print("=" * 60)
print("4. 流式输出")
print("=" * 60)

print('''
from openai import OpenAI

client = OpenAI()

# 流式响应
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "写一个Python教程"}
    ],
    stream=True
)

# 逐块接收
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
''')

print()
print("=" * 60)
print("5. 函数调用")
print("=" * 60)

print('''
from openai import OpenAI

client = OpenAI()

# 定义函数
functions = [
    {
        "name": "get_weather",
        "description": "获取天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["location"]
        }
    }
]

# 调用
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "北京天气怎么样?"}
    ],
    tools=[{"type": "function", "function": functions[0]}]
)

# 获取函数调用
tool_call = response.choices[0].message.tool_calls[0]
print(f"Function: {tool_call.function.name}")
print(f"Arguments: {tool_call.function.arguments}")
''')

print()
print("=" * 60)
print("6. Embeddings")
print("=" * 60)

print('''
from openai import OpenAI

client = OpenAI()

# 获取文本Embedding
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Python是一种高级编程语言"
)

embedding = response.data[0].embedding
print(f"Embedding维度: {len(embedding)}")

# 批量处理
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=[
        "Python编程",
        "Java开发",
        "Web前端"
    ]
)

for item in response.data:
    print(f"文本: {item.index}, 维度: {len(item.embedding)}")
''')

print()
print("=" * 60)
print("7. Claude API")
print("=" * 60)

print("""
Anthropic Claude API:

安装:
  pip install anthropic

使用:
""")

print('''
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 调用Claude
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "解释什么是机器学习"}
    ]
)

print(message.content[0].text)
print(f"使用tokens: {message.usage.input_tokens + message.usage.output_tokens}")
''')

print()
print("=" * 60)
print("8. Gemini API")
print("=" * 60)

print("""
Google Gemini API:

安装:
  pip install google-generativeai
""")

print('''
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 列出可用模型
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

# 调用模型
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("什么是深度学习?")
print(response.text)

# 流式输出
response = model.generate_content(
    "写一篇关于AI的文章",
    stream=True
)

for chunk in response:
    print(chunk.text, end="")
''')

print()
print("=" * 60)
print("9. 国内API")
print("=" * 60)

print("""
9.1 百度文心一言

  pip install qianfan

9.2 阿里通义千问

  pip install dashscope

9.3 智谱GLM

  pip install zhipuai
""")

print()
print("=" * 60)
print("10. 错误处理")
print("=" * 60)

print('''
from openai import OpenAI
from openai import RateLimitError, APIError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("达到速率限制，请稍后重试")
except APIError as e:
    print(f"API错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
''')

print()
print("=" * 60)
print("11. 重试机制")
print("=" * 60)

print('''
import time
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_api_with_retry(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 使用
result = call_api_with_retry("什么是Python?")
print(result)
''')

print()
print("=" * 60)
print("12. LangChain集成")
print("=" * 60)

print('''
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 初始化
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key="your-key"
)

# 调用
messages = [
    SystemMessage(content="你是一个Python专家"),
    HumanMessage(content="什么是装饰器?")
]

response = llm.invoke(messages)
print(response.content)

# 流式
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
''')

print()
print("=" * 60)
print("13. 本地模型")
print("=" * 60)

print("""
13.1 Ollama

  安装: ollama.ai
  
  使用:
  ollama run llama3
  
  Python:
  from langchain_community.llms import Ollama
  llm = Ollama(model="llama3")

13.2 llama.cpp

  pip install llama-cpp-python

13.3 vLLM

  高性能推理框架
""")

print()
print("=" * 60)
print("14. 价格优化")
print("=" * 60)

print("""
14.1 模型选择

  • GPT-4o: 最强，最贵
  • GPT-4 Turbo: 性价比高
  • GPT-3.5 Turbo: 便宜，快速

14.2 减少Token

  • 精简prompt
  • 摘要中间结果
  • 适当max_tokens

14.3 缓存

  • System prompt缓存
  • 常用查询缓存

14.4 微调

  • 特定任务微调
  • 减少示例数量
""")

print()
print("=" * 60)
print("15. 并发处理")
print("=" * 60)

print('''
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def call_api(prompt):
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def main():
    prompts = [
        "什么是Python?",
        "什么是Java?",
        "什么是Go?"
    ]

    # 并发调用
    tasks = [call_api(p) for p in prompts]
    results = await asyncio.gather(*tasks)

    for prompt, result in zip(prompts, results):
        print(f"Q: {prompt}")
        print(f"A: {result[:100]}...")
        print()

asyncio.run(main())
''')

print()
print("=" * 60)
print("16. 完整示例")
print("=" * 60)

print('''
import os
from openai import OpenAI

class LLMClient:
    def __init__(self, api_key=None, model="gpt-4o"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.default_temperature = 0.7
        self.default_max_tokens = 1000

    def chat(self, prompt, system_prompt=None, **kwargs):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", self.default_temperature),
            max_tokens=kwargs.get("max_tokens", self.default_max_tokens)
        )

        return response.choices[0].message.content

    def chat_with_history(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

# 使用
client = LLMClient()
result = client.chat("Python的装饰器是什么?", system_prompt="你是一个Python专家")
print(result)
''')

print()
print("=" * 60)
print("17. API总结")
print("""
LLM API使用要点:

✓ 主流API:
  • OpenAI GPT
  • Anthropic Claude
  • Google Gemini
  • 国内: 百度/阿里/智谱

✓ 核心功能:
  • 文本生成
  • 流式输出
  • 函数调用
  • Embeddings

✓ 最佳实践:
  • 错误处理
  • 重试机制
  • 并发优化
  • 成本控制

✓ 工具:
  • LangChain
  • LangSmith
  • 本地部署
""")
