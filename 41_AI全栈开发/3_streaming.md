# 3. 流式输出与WebSocket

## 为什么需要流式输出

LLM生成回答需要几秒到几十秒。如果等全部生成完再返回，用户体验很差。流式输出让用户看到"逐字打出"的效果。

## 两种流式方案

### SSE（Server-Sent Events）
- 服务端单向推送
- 基于HTTP，简单可靠
- 前端用EventSource接收
- 推荐方案

### WebSocket
- 双向通信
- 适合需要客户端实时发送的场景
- 实现稍复杂

## SSE实现

后端用FastAPI的StreamingResponse：
```python
@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def generate():
        stream = await client.chat.completions.create(..., stream=True)
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## WebSocket实现

```python
@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    while True:
        message = await ws.receive_text()
        # 流式返回
        async for token in generate_stream(message):
            await ws.send_text(token)
```

## 前端对接

Streamlit用`st.write_stream()`，原生支持流式显示。
React/Vue用EventSource或WebSocket API。
