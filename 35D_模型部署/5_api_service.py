"""
5. FastAPI模型服务 - 代码示例
将Ollama/vLLM包装为带校验的API服务。

运行: uvicorn 5_api_service:app --host 0.0.0.0 --port 8080
文档: http://localhost:8080/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="LLM API Service", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 后端LLM（Ollama或vLLM）
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
DEFAULT_MODEL = "qwen2.5:7b"


# ============================================================
# 请求/响应模型
# ============================================================
class ChatRequest(BaseModel):
    message: str
    model: str = DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 500


class ChatResponse(BaseModel):
    answer: str
    model: str
    tokens_used: int


# ============================================================
# API接口
# ============================================================
@app.get("/")
def root():
    return {"service": "LLM API", "status": "running"}


@app.get("/models")
def list_models():
    """列出可用模型"""
    try:
        models = client.models.list()
        return {"models": [m.id for m in models.data]}
    except Exception as e:
        raise HTTPException(500, f"获取模型列表失败: {e}")


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """对话接口"""
    try:
        response = client.chat.completions.create(
            model=req.model,
            messages=[{"role": "user", "content": req.message}],
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        return ChatResponse(
            answer=response.choices[0].message.content,
            model=req.model,
            tokens_used=response.usage.total_tokens if response.usage else 0,
        )
    except Exception as e:
        raise HTTPException(500, f"推理失败: {e}")


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    """流式对话接口"""
    def generate():
        stream = client.chat.completions.create(
            model=req.model,
            messages=[{"role": "user", "content": req.message}],
            temperature=req.temperature,
            max_tokens=req.max_tokens,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")


# ============================================================
# 启动说明
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("启动API服务: http://localhost:8080")
    print("API文档: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
