"""
6. Docker部署 - 代码示例
生成Dockerfile和docker-compose.yml配置。
"""


def generate_dockerfile():
    """生成AI应用的Dockerfile"""
    dockerfile = '''FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

# 启动
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
'''
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)
    print("已生成 Dockerfile")
    print(dockerfile)


def generate_compose():
    """生成docker-compose.yml"""
    compose = '''version: "3.8"

services:
  # AI后端
  backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - LLM_BASE=http://ollama:11434/v1
      - DATABASE_URL=sqlite:///./data/app.db
    volumes:
      - app_data:/app/data
    depends_on:
      ollama:
        condition: service_healthy
    restart: unless-stopped

  # Ollama LLM服务
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  # Streamlit前端
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - API_BASE=http://backend:8080
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  ollama_data:
  app_data:
'''
    with open("docker-compose.yml", "w") as f:
        f.write(compose)
    print("已生成 docker-compose.yml")
    print(compose)


def generate_requirements():
    """生成requirements.txt"""
    reqs = """fastapi==0.115.0
uvicorn==0.30.0
openai==1.50.0
sqlalchemy==2.0.35
python-jose==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.9.0
prometheus-client==0.21.0
httpx==0.27.0
"""
    with open("requirements.txt", "w") as f:
        f.write(reqs)
    print("已生成 requirements.txt")


if __name__ == "__main__":
    print("=" * 60)
    print("生成Docker部署文件")
    print("=" * 60)
    generate_dockerfile()
    print()
    generate_compose()
    print()
    generate_requirements()
    print("\n部署命令:")
    print("  docker compose up -d")
    print("  docker compose logs -f")
