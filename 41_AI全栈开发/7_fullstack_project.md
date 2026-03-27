# 7. 全栈实战项目

## 项目：AI聊天助手（完整产品）

### 功能
- 用户注册/登录（JWT认证）
- 多会话管理（创建、切换、删除）
- 流式对话（SSE）
- 对话历史持久化
- API Key限流
- Streamlit前端

### 架构
```
Streamlit前端 → FastAPI后端 → Ollama/OpenAI
                    ↕
              SQLite数据库
```

### 运行方式
```bash
# 启动后端
uvicorn 7_fullstack_project:app --port 8080

# 启动前端（另一个终端）
streamlit run 7_frontend.py
```

### 项目文件
- `7_fullstack_project.py` — 后端（FastAPI + SQLite + LLM）
- `7_frontend.py` — 前端（Streamlit聊天界面）

### 扩展方向
- 加入RAG（文档上传+问答）
- 加入Agent能力（工具调用）
- 换PostgreSQL + Redis
- Docker部署
- 加入管理后台
