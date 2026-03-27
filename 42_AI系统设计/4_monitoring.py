"""
4. 监控与日志 - 代码示例
演示结构化日志和Prometheus指标。
"""

import time
import json
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Monitoring Demo")


# ============================================================
# 1. 结构化日志
# ============================================================
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log.update(record.extra_data)
        return json.dumps(log, ensure_ascii=False)

logger = logging.getLogger("ai_app")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# ============================================================
# 2. Prometheus指标
# ============================================================
REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])
TOKEN_USAGE = Counter("app_tokens_total", "Total tokens used", ["model"])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(latency)

    # 结构化日志
    record = logging.LogRecord("ai_app", logging.INFO, "", 0, "request", (), None)
    record.extra_data = {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "latency_ms": round(latency * 1000, 2),
    }
    logger.handle(record)

    return response


@app.get("/metrics")
async def metrics():
    """Prometheus指标端点"""
    return PlainTextResponse(generate_latest(), media_type="text/plain")


@app.post("/chat")
async def chat():
    """模拟对话接口"""
    TOKEN_USAGE.labels("qwen2.5:7b").inc(150)
    return {"answer": "这是一个监控演示"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
