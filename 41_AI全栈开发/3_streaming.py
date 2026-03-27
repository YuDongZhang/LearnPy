"""
3. 流式输出 - 代码示例
演示SSE和WebSocket两种流式方案。

运行: uvicorn 3_streaming:app --port 8080
"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Streaming Demo")
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"


class ChatRequest(BaseModel):
    message: str


# ============================================================
# 1. SSE流式输出（推荐）
# ============================================================
@app.post("/chat/stream")
async def chat_sse(req: ChatRequest):
    """Server-Sent Events流式输出"""
    def generate():
        stream = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": req.message}],
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# ============================================================
# 2. WebSocket流式输出
# ============================================================
@app.websocket("/ws/chat")
async def chat_websocket(ws: WebSocket):
    """WebSocket双向通信"""
    await ws.accept()
    try:
        while True:
            message = await ws.receive_text()
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": message}],
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    await ws.send_text(content)
            await ws.send_text("[DONE]")
    except Exception:
        pass


# ============================================================
# 3. 普通接口（对比用）
# ============================================================
@app.post("/chat")
async def chat_normal(req: ChatRequest):
    """非流式，等全部生成完再返回"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": req.message}],
    )
    return {"answer": response.choices[0].message.content}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
