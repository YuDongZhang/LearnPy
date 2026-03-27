# 5. 数据库与用户系统

## AI应用需要存什么

| 数据 | 存储方式 | 说明 |
|------|---------|------|
| 用户信息 | 关系数据库 | 账号、密码、配置 |
| 对话历史 | 关系数据库 | 消息记录、会话管理 |
| 文档向量 | 向量数据库 | RAG的Embedding |
| 文件 | 文件系统/对象存储 | 上传的文档 |
| 缓存 | Redis | 热点查询缓存 |

## 技术选型

| 场景 | 推荐 |
|------|------|
| 开发/小项目 | SQLite + Chroma |
| 生产环境 | PostgreSQL + Milvus/Pgvector |
| 缓存 | Redis |

## SQLAlchemy ORM

Python最流行的ORM，支持同步和异步：
- 定义模型（User、Conversation、Message）
- 自动建表
- 异步查询（配合FastAPI）

## 数据模型设计

```
User (用户)
├── id, username, password_hash, created_at
│
Conversation (会话)
├── id, user_id, title, created_at
│
Message (消息)
├── id, conversation_id, role, content, created_at
```

## 对话历史管理

- 创建新会话
- 保存每轮消息（user + assistant）
- 加载历史消息（多轮对话上下文）
- 会话列表展示
