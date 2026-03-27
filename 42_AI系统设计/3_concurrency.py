"""
3. 并发与队列 - 代码示例
演示信号量限制并发、异步批处理、简单任务队列。
"""

import asyncio
import time
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Concurrency Demo")
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 限制LLM并发数
LLM_SEMAPHORE = asyncio.Semaphore(5)

# 简单任务存储
TASKS = {}


class ChatRequest(BaseModel):
    message: str


# ============================================================
# 1. 信号量限制并发
# ============================================================
async def call_llm_limited(message: str) -> str:
    async with LLM_SEMAPHORE:
        # 同一时刻最多5个LLM调用
        response = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content


@app.post("/chat")
async def chat(req: ChatRequest):
    answer = await call_llm_limited(req.message)
    return {"answer": answer}


# ============================================================
# 2. 异步任务队列（后台处理）
# ============================================================
def process_task(task_id: str, message: str):
    """后台处理耗时任务"""
    TASKS[task_id] = {"status": "processing"}
    try:
        response = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=[{"role": "user", "content": message}],
        )
        TASKS[task_id] = {
            "status": "completed",
            "result": response.choices[0].message.content
        }
    except Exception as e:
        TASKS[task_id] = {"status": "failed", "error": str(e)}


@app.post("/task/submit")
async def submit_task(req: ChatRequest, bg: BackgroundTasks):
    """提交异步任务，立即返回任务ID"""
    import uuid
    task_id = str(uuid.uuid4())[:8]
    TASKS[task_id] = {"status": "queued"}
    bg.add_task(process_task, task_id, req.message)
    return {"task_id": task_id, "status": "queued"}


@app.get("/task/{task_id}")
async def get_task(task_id: str):
    """查询任务状态"""
    if task_id not in TASKS:
        return {"error": "任务不存在"}
    return {"task_id": task_id, **TASKS[task_id]}


# ============================================================
# 3. 批量处理
# ============================================================
class BatchRequest(BaseModel):
    messages: list[str]


@app.post("/batch")
async def batch_chat(req: BatchRequest):
    """并发处理多个请求"""
    tasks = [call_llm_limited(msg) for msg in req.messages]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {
        "results": [
            {"answer": r} if isinstance(r, str) else {"error": str(r)}
            for r in results
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
