"""
2. Ollama本地部署 - 代码示例
演示通过Python调用Ollama的API。
前提：已安装Ollama并运行 ollama serve
"""

import requests
from openai import OpenAI

OLLAMA_BASE = "http://localhost:11434"


# ============================================================
# 1. 直接调用Ollama REST API
# ============================================================
def demo_rest_api():
    """使用requests调用Ollama原生API"""
    response = requests.post(
        f"{OLLAMA_BASE}/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": "用一句话解释Python的GIL",
            "stream": False,
        }
    )
    if response.ok:
        result = response.json()
        print(f"回答: {result['response']}")
        print(f"耗时: {result.get('total_duration', 0)/1e9:.2f}s")
    else:
        print(f"错误: {response.status_code} - 请确认Ollama已启动")


# ============================================================
# 2. 用OpenAI SDK调用（推荐）
# ============================================================
def demo_openai_compatible():
    """Ollama兼容OpenAI API，直接用openai库"""
    client = OpenAI(base_url=f"{OLLAMA_BASE}/v1", api_key="ollama")

    response = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": "你是Python专家，简洁回答。"},
            {"role": "user", "content": "装饰器和闭包的关系是什么？"}
        ],
        temperature=0,
    )
    print(f"回答: {response.choices[0].message.content}")


# ============================================================
# 3. 流式输出
# ============================================================
def demo_streaming():
    """流式输出，逐字显示"""
    client = OpenAI(base_url=f"{OLLAMA_BASE}/v1", api_key="ollama")

    stream = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": "Python有哪些核心特性？列举5个"}],
        stream=True,
    )
    print("流式输出: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()


# ============================================================
# 4. 列出可用模型
# ============================================================
def demo_list_models():
    """查看Ollama已下载的模型"""
    response = requests.get(f"{OLLAMA_BASE}/api/tags")
    if response.ok:
        models = response.json().get("models", [])
        print(f"已下载 {len(models)} 个模型:")
        for m in models:
            size_gb = m.get("size", 0) / 1024**3
            print(f"  {m['name']:30s} {size_gb:.1f}GB")
    else:
        print("无法连接Ollama，请确认已启动: ollama serve")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("4. 列出模型")
    print("=" * 60)
    demo_list_models()

    print("\n" + "=" * 60)
    print("1. REST API调用")
    print("=" * 60)
    demo_rest_api()

    print("\n" + "=" * 60)
    print("2. OpenAI兼容调用")
    print("=" * 60)
    demo_openai_compatible()

    print("\n" + "=" * 60)
    print("3. 流式输出")
    print("=" * 60)
    demo_streaming()
