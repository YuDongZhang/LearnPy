# 2. FastAPI后端开发

## 为什么选FastAPI

- 异步支持（async/await），适合IO密集的LLM调用
- 自动生成API文档（Swagger UI）
- Pydantic类型校验，请求/响应自动验证
- 性能优秀，接近Node.js

## 核心概念

### 路由（Router）
按功能模块拆分API：
- `/api/chat` — 对话相关
- `/api/auth` — 认证相关
- `/api/docs` — 文档管理（RAG）

### 依赖注入
FastAPI的依赖注入系统，用于：
- 数据库连接管理
- 用户认证
- 配置注入

### 中间件
请求/响应的全局处理：
- CORS跨域
- 日志记录
- 错误处理
- 请求计时

## 异步LLM调用

LLM推理是IO密集操作，必须用异步：
```python
@app.post("/chat")
async def chat(req: ChatRequest):
    # 异步调用LLM
    response = await aclient.chat.completions.create(...)
    return {"answer": response.choices[0].message.content}
```

## 错误处理

统一的错误处理机制：
- 业务错误 → 自定义HTTPException
- LLM超时 → 504 Gateway Timeout
- 模型不可用 → 503 Service Unavailable
- 参数错误 → 422 Validation Error

## 配置管理

用Pydantic Settings管理配置：
- 环境变量
- .env文件
- 不同环境（dev/staging/prod）
