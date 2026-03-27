# 第四十一章：AI全栈开发

## 本章目标

- 掌握AI应用的前后端架构设计
- 学会用FastAPI构建AI后端服务
- 学会用Streamlit/Gradio快速搭建AI前端
- 掌握WebSocket实现流式输出
- 掌握数据库集成（用户管理、对话历史）
- 完成一个完整的AI产品

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 内容 |
|------|----------|----------|------|
| 1 | 1_architecture.md | 1_architecture.py | AI应用架构设计 |
| 2 | 2_backend.md | 2_backend.py | FastAPI后端开发 |
| 3 | 3_streaming.md | 3_streaming.py | 流式输出与WebSocket |
| 4 | 4_frontend.md | 4_frontend.py | Streamlit/Gradio前端 |
| 5 | 5_database.md | 5_database.py | 数据库与用户系统 |
| 6 | 6_auth_ratelimit.md | 6_auth_ratelimit.py | 认证与限流 |
| 7 | 7_fullstack_project.md | 7_fullstack_project.py | 全栈实战项目 |

## 前置知识

- Python基础
- LLM基础（第35章）
- RAG（第35C章）
- 模型部署（第35D章）

## 安装依赖

```bash
pip install fastapi uvicorn streamlit gradio
pip install sqlalchemy aiosqlite python-jose passlib
pip install openai websockets httpx
```

## 章节导航

[上一章：Skills](../39_Skills/README.md) | [下一章：AI系统设计](../42_AI系统设计/README.md)
