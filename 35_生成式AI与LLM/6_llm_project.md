# 6. LLM 实战项目

## 项目概述

本章综合运用 LangChain、向量数据库、OpenAI API，实现一个**智能问答系统**：

- 功能：基于文档的问答、多轮对话、引用来源
- 技术栈：LangChain + Chroma 向量数据库 + OpenAI API

## 文档问答系统

加载文档 → 分割 → 向量化 → 检索问答，封装成类：

```python
class DocumentQA:
    def __init__(self, document_path, model="gpt-4o"):
        # 加载文档
        documents = TextLoader(document_path, encoding="utf-8").load()

        # 分割文本
        texts = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50).split_documents(documents)

        # 创建向量存储
        self.vectorstore = Chroma.from_documents(texts, OpenAIEmbeddings())
        self.llm = ChatOpenAI(model=model, temperature=0)

    def ask(self, question):
        qa = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        return qa({"query": question})["result"]

qa_system = DocumentQA("knowledge.txt")
print(qa_system.ask("什么是Python?"))
```

## 多轮对话系统

用 `ConversationBufferMemory` 保存对话历史：

```python
class ChatBot:
    def __init__(self, system_prompt=None):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.memory = ConversationBufferMemory()
        self.prompt = system_prompt or "你是一个友好的AI助手。"
        self.chain = ConversationChain(
            llm=self.llm, memory=self.memory,
            prompt=self.prompt, verbose=True
        )

    def chat(self, message):
        return self.chain.predict(input=message)

    def clear_history(self):
        self.memory.clear()

chatbot = ChatBot(system_prompt="你是一个Python专家")
```

命令行循环：读取用户输入 → 调用 `chat()` → 打印回复，输入 exit/quit/退出 时结束。

## Agent 智能助手

LLM + 工具，自动决策调用：

```python
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun

tools = [
    Tool(name="搜索", func=DuckDuckGoSearchRun().run,
         description="用于搜索实时信息")
]

agent = initialize_agent(
    tools,
    ChatOpenAI(model="gpt-4o", temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.run("今天北京天气怎么样?")
```

## 文本生成工具

封装常见生成任务（博客写作、代码审查）：

```python
class TextGenerator:
    def generate(self, prompt, **kwargs):
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000)
        )
        return response.choices[0].message.content

    def blog_post(self, topic):
        prompt = f"请为博客写一篇关于{topic}的深度文章，包括介绍、原理、实践和总结。"
        return self.generate(prompt, max_tokens=2000)

    def code_review(self, code, language="python"):
        prompt = f"请review以下{language}代码，指出问题和改进建议:\n\n{code}"
        return self.generate(prompt, max_tokens=1500)
```

## 批量处理工具

用 `AsyncOpenAI` + `asyncio.gather` 并发处理多个请求：

```python
class BatchProcessor:
    async def process_single(self, prompt, system_prompt=None):
        ...
        return response.choices[0].message.content

    async def process_batch(self, prompts, system_prompt=None):
        tasks = [self.process_single(p, system_prompt) for p in prompts]
        return await asyncio.gather(*tasks)

results = asyncio.run(processor.process_batch(prompts))
```

## API 服务

用 Flask 封装 /chat 和 /embed 接口：

```python
@app.route("/chat", methods=["POST"])
def chat():
    messages = request.json.get("messages", [])
    response = client.chat.completions.create(
        model="gpt-4o", messages=messages,
        temperature=request.json.get("temperature", 0.7)
    )
    return jsonify({
        "reply": response.choices[0].message.content,
        "usage": {"prompt_tokens": response.usage.prompt_tokens,
                  "completion_tokens": response.usage.completion_tokens}
    })
```

## Streamlit Web 应用

快速搭建聊天界面：`st.chat_input` 输入 → `st.chat_message` 展示历史 → 调用 API 流式/同步生成回复，会话状态用 `st.session_state` 维护。

## 项目打包

```
project/
├── app/           # __init__.py, main.py, config.py, utils.py
├── models/
├── data/
├── tests/
├── requirements.txt   # openai, langchain, langchain-openai, streamlit, ...
├── .env               # OPENAI_API_KEY=sk-xxx
└── README.md
```

## 最佳实践

| 方面 | 做法 |
|------|------|
| 错误处理 | API 错误重试、超时处理、降级策略 |
| 成本控制 | 缓存常用结果、选择合适模型、精简 prompt |
| 性能优化 | 异步处理、并发控制、缓存优化 |
| 安全 | 密钥管理、输入验证、日志脱敏 |

## 下一步

- Agent 工作流、多模态应用
- 微调模型（见后续章节）
- 生产部署

## 代码

讲解对应的示例代码见 `6_llm_project.py`。
