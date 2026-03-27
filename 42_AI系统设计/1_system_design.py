"""
1. AI系统架构 - 代码示例
演示健康检查、优雅降级、重试机制。
"""

import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Production AI Service")

# 主LLM和备用LLM
primary_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# fallback_client = OpenAI(base_url="http://localhost:11435/v1", api_key="ollama")

CACHE = {}  # 简单缓存，生产用Redis


class ChatRequest(BaseModel):
    message: str


# ========== 健康检查 ==========
@app.get("/health")
async def health():
    """检查LLM服务是否可用"""
    try:
        primary_client.models.list()
        return {"status": "healthy", "llm": "ok"}
    except Exception:
        return {"status": "degraded", "llm": "unavailable"}


# ========== 带重试和降级的调用 ==========
async def call_llm_with_fallback(message: str, max_retries: int = 2) -> str:
    # 1. 检查缓存
    if message in CACHE:
        return CACHE[message] + " (来自缓存)"

    # 2. 重试调用主LLM
    for attempt in range(max_retries):
        try:
            response = primary_client.chat.completions.create(
                model="qwen2.5:7b",
                messages=[{"role": "user", "content": message}],
                timeout=30,
            )
            answer = response.choices[0].message.content
            CACHE[message] = answer  # 存入缓存
            return answer
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)  # 等待后重试
                continue

    # 3. 降级
    return "抱歉，服务暂时不可用，请稍后重试。"


@app.post("/chat")
async def chat(req: ChatRequest):
    answer = await call_llm_with_fallback(req.message)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
