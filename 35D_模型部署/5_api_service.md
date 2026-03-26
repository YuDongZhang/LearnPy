# 5. FastAPI模型服务

## 为什么用FastAPI

将模型包装为REST API服务：
- 前后端分离，任何客户端都能调用
- 支持并发请求
- 自动生成API文档
- 易于部署和扩展

## 架构

```
客户端(Web/App/CLI) → FastAPI服务 → Ollama/vLLM → 模型
```

## 核心功能

1. `/chat` — 对话接口
2. `/chat/stream` — 流式输出
3. 请求校验（Pydantic）
4. 错误处理
5. CORS跨域支持

## 运行方式

```bash
# 先启动Ollama
ollama serve

# 启动API服务
uvicorn 5_api_service:app --host 0.0.0.0 --port 8080

# 访问API文档
# http://localhost:8080/docs
```

## 生产部署建议

1. 使用Gunicorn + Uvicorn workers
2. 加Nginx反向代理
3. 配置HTTPS
4. 加认证（API Key）
5. 限流保护
6. 日志和监控
