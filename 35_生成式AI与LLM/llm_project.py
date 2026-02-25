"""
LLM实战项目
==========

通过实际项目练习LLM的应用开发。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("项目1: 智能问答系统")
print()
print("功能:")
print("  - 基于文档的问答")
print("  - 多轮对话")
print("  - 引用来源")
print()
print("技术栈:")
print("  - LangChain")
print("  - Chroma向量数据库")
print("  - OpenAI API")

print()
print("=" * 60)
print("2. 文档问答系统")
print("=" * 60)

print('''
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

class DocumentQA:
    def __init__(self, document_path, model="gpt-4o"):
        # 加载文档
        loader = TextLoader(document_path, encoding="utf-8")
        documents = loader.load()

        # 分割文本
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        texts = text_splitter.split_documents(documents)

        # 创建向量存储
        embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma.from_documents(texts, embeddings)

        # 创建LLM
        self.llm = ChatOpenAI(model=model, temperature=0)

    def ask(self, question):
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        result = qa({"query": question})
        return result["result"]

# 使用
qa_system = DocumentQA("knowledge.txt")
answer = qa_system.ask("什么是Python?")
print(answer)
''')

print()
print("=" * 60)
print("3. 多轮对话系统")
print("=" * 60)

print('''
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class ChatBot:
    def __init__(self, system_prompt=None):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.memory = ConversationBufferMemory()

        if system_prompt:
            self.prompt = system_prompt
        else:
            self.prompt = "你是一个友好的AI助手。"

        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )

    def chat(self, message):
        response = self.chain.predict(input=message)
        return response

    def clear_history(self):
        self.memory.clear()

# 使用
chatbot = ChatBot(system_prompt="你是一个Python专家")

while True:
    user_input = input("你: ")
    if user_input.lower in ["exit", "quit", "退出"]:
        break
    response = chatbot.chat(user_input)
    print(f"AI: {response}")
''')

print()
print("=" * 60)
print("4. Agent智能助手")
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
        description="用于搜索实时信息"
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
result = agent.run("今天北京天气怎么样?")
print(result)
''')

print()
print("=" * 60)
print("5. 文本生成工具")
print("=" * 60)

print('''
from openai import OpenAI
import os

class TextGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt, template=None, **kwargs):
        if template:
            prompt = template.format(prompt=prompt)

        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000)
        )

        return response.choices[0].message.content

    def blog_post(self, topic):
        prompt = f"请为博客写一篇关于{topic}的深度文章，"
        prompt += "包括介绍、原理、实践和总结。"
        return self.generate(prompt, max_tokens=2000)

    def code_review(self, code, language="python"):
        prompt = f"请review以下{language}代码，指出问题和改进建议:\n\n{code}"
        return self.generate(prompt, max_tokens=1500)

# 使用
generator = TextGenerator()
article = generator.blog_post("Python异步编程")
print(article[:500])
''')

print()
print("=" * 60)
print("6. 批量处理工具")
print("=" * 60)

print('''
import asyncio
from openai import AsyncOpenAI
import os

class BatchProcessor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def process_single(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        return response.choices[0].message.content

    async def process_batch(self, prompts, system_prompt=None):
        tasks = [self.process_single(p, system_prompt) for p in prompts]
        return await asyncio.gather(*tasks)

# 使用
processor = BatchProcessor()

prompts = [
    "Python的特点是什么?",
    "Java的特点是什么?",
    "Go的特点是什么?"
]

results = asyncio.run(processor.process_batch(prompts))

for prompt, result in zip(prompts, results):
    print(f"Q: {prompt}")
    print(f"A: {result[:200]}...")
    print()
''')

print()
print("=" * 60)
print("7. API服务")
print("=" * 60)

print('''
from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=data.get("temperature", 0.7)
    )

    return jsonify({
        "reply": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens
        }
    })

@app.route("/embed", methods=["POST"])
def embed():
    data = request.json
    text = data.get("text", "")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return jsonify({
        "embedding": response.data[0].embedding
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
''')

print()
print("=" * 60)
print("8. Streamlit应用")
print("=" * 60)

print('''
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI助手", page_icon="🤖")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 AI智能助手")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 输入框
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 生成回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages]
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
''')

print()
print("=" * 60)
print("9. 项目打包")
print("=" * 60)

print("9.1 目录结构")
print()
print("project/")
print("├── app/")
print("│   ├── __init__.py")
print("│   ├── main.py")
print("│   ├── config.py")
print("│   └── utils.py")
print("├── models/")
print("├── data/")
print("├── tests/")
print("├── requirements.txt")
print("├── .env")
print("└── README.md")
print()
print("9.2 requirements.txt")
print()
print("openai>=1.0.0")
print("langchain>=0.1.0")
print("langchain-openai")
print("streamlit")
print("python-dotenv")
print("flask")
print()
print("9.3 .env 文件")
print()
print("OPENAI_API_KEY=sk-xxx")

print()
print("=" * 60)
print("10. 最佳实践")
print("=" * 60)

print("10.1 错误处理")
print()
print("  - API错误重试")
print("  - 超时处理")
print("  - 降级策略")
print()
print("10.2 成本控制")
print()
print("  - 缓存常用结果")
print("  - 选择合适模型")
print("  - 精简prompt")
print()
print("10.3 性能优化")
print()
print("  - 异步处理")
print("  - 并发控制")
print("  - 缓存优化")
print()
print("10.4 安全")
print()
print("  - 密钥管理")
print("  - 输入验证")
print("  - 日志脱敏")

print()
print("=" * 60)
print("11. 总结")
print("=" * 60)

print("LLM项目要点:")
print()
print("* 实战项目:")
print("  - 文档问答系统")
print("  - 多轮对话")
print("  - Agent智能助手")
print("  - 文本生成工具")
print("  - API服务")
print("  - Web应用")
print()
print("* 工具栈:")
print("  - LangChain")
print("  - LangGraph")
print("  - Streamlit")
print("  - Flask/FastAPI")
print()
print("* 最佳实践:")
print("  - 错误处理")
print("  - 成本控制")
print("  - 性能优化")
print("  - 安全")
print()
print("* 下一步:")
print("  - Agent工作流")
print("  - 多模态应用")
print("  - 微调模型")
print("  - 生产部署")
