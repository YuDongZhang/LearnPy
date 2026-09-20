# 4. LLM API 使用指南

## API 调用流程

```
1. 获取API Key → 2. 安装SDK → 3. 构建请求 → 4. 发送调用 → 5. 处理响应
```

基本结构：

```python
client = OpenAI(api_key="xxx")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...]
)
result = response.choices[0].message.content
```

## 基本文本调用

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
print(f"Usage: {response.usage}")  # token 用量
```

## 流式输出

设置 `stream=True`，逐块接收，体验更好：

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "写一个Python教程"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## 函数调用 (Function Calling)

定义函数 schema，模型决定何时调用：

```python
functions = [{
    "name": "get_weather",
    "description": "获取天气信息",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "城市名称"}
        },
        "required": ["location"]
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "北京天气怎么样?"}],
    tools=[{"type": "function", "function": functions[0]}]
)

tool_call = response.choices[0].message.tool_calls[0]
print(tool_call.function.name)       # get_weather
print(tool_call.function.arguments)  # {"location": "北京"}
```

## Embeddings

文本转向量，用于相似度检索：

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Python是一种高级编程语言"
)
embedding = response.data[0].embedding
print(f"Embedding维度: {len(embedding)}")

# 支持批量
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["Python编程", "Java开发", "Web前端"]
)
```

## 各家 API 对比

| 提供商 | SDK | 模型 |
|--------|-----|------|
| OpenAI | `pip install openai` | GPT-4o、GPT-4 Turbo、Embeddings、DALL-E |
| Anthropic | `pip install anthropic` | Claude 系列，长上下文 |
| Google | `pip install google-generativeai` | Gemini，多模态 |
| 百度 | `pip install qianfan` | 文心一言 |
| 阿里 | `pip install dashscope` | 通义千问 |
| 智谱 | `pip install zhipuai` | GLM |

Claude 调用示例：

```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": "解释什么是机器学习"}]
)
print(message.content[0].text)
```

## 错误处理与重试

```python
from openai import RateLimitError, APIError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    print("达到速率限制，请稍后重试")
except APIError as e:
    print(f"API错误: {e}")
```

用 `tenacity` 实现指数退避重试：

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_api_with_retry(prompt):
    ...
```

## LangChain 集成

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key="your-key")

messages = [
    SystemMessage(content="你是一个Python专家"),
    HumanMessage(content="什么是装饰器?")
]
response = llm.invoke(messages)

for chunk in llm.stream(messages):  # 流式
    print(chunk.content, end="", flush=True)
```

## 本地模型

- **Ollama**：安装后 `ollama run llama3`，Python 端 `Ollama(model="llama3")`
- **llama.cpp**：`pip install llama-cpp-python`
- **vLLM**：高性能推理框架

## 成本优化

| 策略 | 做法 |
|------|------|
| 模型选择 | 简单任务用 GPT-3.5/4o-mini，复杂任务用 GPT-4o |
| 减少 Token | 精简 prompt、摘要中间结果、设置合适 max_tokens |
| 缓存 | System prompt 缓存、常用查询缓存 |
| 微调 | 特定任务微调小模型，减少示例数量 |

## 并发处理

```python
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
    prompts = ["什么是Python?", "什么是Java?", "什么是Go?"]
    results = await asyncio.gather(*[call_api(p) for p in prompts])

asyncio.run(main())
```

## 代码

讲解对应的示例代码见 `4_llm_api_usage.py`。
