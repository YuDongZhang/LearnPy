# 6. Docker容器化部署

## 为什么用Docker

- 环境一致性（开发=生产）
- 一键部署
- 易于扩展
- 隔离性好

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Docker Compose

一键启动整个AI应用栈：

```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    ports: ["8080:8080"]
    environment:
      - LLM_BASE=http://ollama:11434/v1
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on: [ollama, db]

  ollama:
    image: ollama/ollama
    ports: ["11434:11434"]
    volumes: ["ollama_data:/root/.ollama"]

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes: ["pg_data:/var/lib/postgresql/data"]

  frontend:
    build: ./frontend
    ports: ["8501:8501"]
    depends_on: [backend]

volumes:
  ollama_data:
  pg_data:
```

## 部署流程

```bash
# 构建并启动
docker compose up -d

# 查看日志
docker compose logs -f backend

# 扩展后端实例
docker compose up -d --scale backend=3
```

## 生产部署建议

1. 使用多阶段构建减小镜像
2. 不要在镜像中存储密钥
3. 配置健康检查
4. 设置资源限制（CPU、内存）
5. 使用Docker网络隔离
6. 日志输出到stdout（方便收集）
