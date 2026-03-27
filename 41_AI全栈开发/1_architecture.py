"""
1. AI应用架构 - 代码示例
演示最小可运行的AI后端骨架。
"""

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="AI App Skeleton")
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


class ChatRequest(BaseModel):
    message: str
    model: str = "qwen2.5:7b"


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """最简单的AI对话接口"""
    response = client.chat.completions.create(
        model=req.model,
        messages=[{"role": "user", "content": req.message}],
    )
    return ChatResponse(answer=response.choices[0].message.content)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    print("启动: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
