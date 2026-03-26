"""
4. vLLM高性能推理 - 代码示例
演示如何调用vLLM服务（需要先启动vLLM服务端）。

启动vLLM服务：
  python -m vllm.entrypoints.openai.api_server \
      --model Qwen/Qwen2.5-7B-Instruct --port 8000

或者用Ollama替代测试（API兼容）。
"""

from openai import OpenAI
import time


VLLM_BASE = "http://localhost:8000/v1"


# ============================================================
# 1. 基础调用
# ============================================================
def demo_basic():
    """调用vLLM的OpenAI兼容API"""
    client = OpenAI(base_url=VLLM_BASE, api_key="vllm")

    start = time.time()
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": "简洁回答"},
            {"role": "user", "content": "Python的GIL是什么？"}
        ],
        temperature=0,
        max_tokens=200,
    )
    elapsed = time.time() - start

    print(f"回答: {response.choices[0].message.content}")
    print(f"耗时: {elapsed:.2f}s")
    print(f"Token使用: {response.usage}")


# ============================================================
# 2. 批量请求（测试吞吐量）
# ============================================================
def demo_throughput():
    """并发请求测试吞吐量"""
    from concurrent.futures import ThreadPoolExecutor

    client = OpenAI(base_url=VLLM_BASE, api_key="vllm")
    questions = [
        "什么是装饰器？", "解释GIL", "什么是生成器？",
        "asyncio怎么用？", "什么是元类？",
    ]

    def ask(q):
        r = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": q}],
            max_tokens=100,
        )
        return r.choices[0].message.content

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(ask, questions))
    elapsed = time.time() - start

    print(f"并发 {len(questions)} 个请求，总耗时: {elapsed:.2f}s")
    print(f"平均: {elapsed/len(questions):.2f}s/请求")
    for q, a in zip(questions, results):
        print(f"  {q} → {a[:40]}...")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 基础调用")
    print("=" * 60)
    try:
        demo_basic()
    except Exception as e:
        print(f"连接失败: {e}")
        print("请先启动vLLM服务或Ollama")

    print("\n" + "=" * 60)
    print("2. 吞吐量测试")
    print("=" * 60)
    try:
        demo_throughput()
    except Exception as e:
        print(f"连接失败: {e}")
