"""
2. FastAPI后端 - 代码示例
演示路由拆分、依赖注入、中间件、错误处理。
"""

import time
import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


# ========== 请求计时中间件 ==========
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {elapsed:.2f}s")
    return response


# ========== 配置管理 ==========
class Settings:
    MODEL: str = "qwen2.5:7b"
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7

settings = Settings()

def get_settings():
    return settings


# ========== 请求/响应模型 ==========
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=500, ge=1, le=4096)

class ChatResponse(BaseModel):
    answer: str
    tokens_used: int
    model: str


# ========== 路由 ==========
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, cfg: Settings = Depends(get_settings)):
    try:
        response = client.chat.completions.create(
            model=cfg.MODEL,
            messages=[{"role": "user", "content": req.message}],
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        return ChatResponse(
            answer=response.choices[0].message.content,
            tokens_used=response.usage.total_tokens if response.usage else 0,
            model=cfg.MODEL,
        )
    except Exception as e:
        logger.error(f"LLM调用失败: {e}")
        raise HTTPException(503, "模型服务不可用，请稍后重试")


@app.get("/api/health")
async def health():
    return {"status": "ok", "model": settings.MODEL}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
