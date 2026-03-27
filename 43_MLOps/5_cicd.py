"""
5. CI/CD - 代码示例
生成GitHub Actions配置和部署脚本。
"""


# ============================================================
# 1. 生成GitHub Actions配置
# ============================================================
def generate_github_actions():
    """生成ML项目的CI/CD配置"""
    workflow = '''name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v

  evaluate:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run evaluation
        run: python scripts/evaluate.py
      - name: Check metrics
        run: python scripts/check_metrics.py

  deploy:
    needs: evaluate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t my-ai-app:${{ github.sha }} .
      - name: Deploy
        run: echo "Deploy to production"
'''
    with open(".github_actions_ml.yml", "w") as f:
        f.write(workflow)
    print("已生成 .github_actions_ml.yml")
    print(workflow)


# ============================================================
# 2. 指标检查脚本
# ============================================================
def generate_check_metrics():
    """生成指标检查脚本"""
    script = '''"""检查模型指标是否达标"""
import json
import sys

THRESHOLDS = {
    "accuracy": 0.80,
    "latency_p99": 10.0,  # 秒
}

def check():
    with open("evaluation_results.json") as f:
        metrics = json.load(f)

    passed = True
    for metric, threshold in THRESHOLDS.items():
        value = metrics.get(metric, 0)
        if metric == "latency_p99":
            ok = value <= threshold
        else:
            ok = value >= threshold

        status = "PASS" if ok else "FAIL"
        print(f"  {status}: {metric} = {value} (threshold: {threshold})")
        if not ok:
            passed = False

    if not passed:
        print("\\n指标未达标，阻止部署")
        sys.exit(1)
    print("\\n所有指标达标，允许部署")

if __name__ == "__main__":
    check()
'''
    with open("check_metrics.py", "w") as f:
        f.write(script)
    print("已生成 check_metrics.py")


# ============================================================
# 3. 部署脚本
# ============================================================
def generate_deploy_script():
    """生成部署脚本"""
    script = '''#!/bin/bash
# AI应用部署脚本

set -e

IMAGE="my-ai-app"
TAG="${1:-latest}"

echo "部署 $IMAGE:$TAG"

# 1. 构建
docker build -t $IMAGE:$TAG .

# 2. 健康检查（旧服务）
echo "检查旧服务..."
curl -sf http://localhost:8080/health || echo "旧服务不可用"

# 3. 停止旧服务
docker compose down

# 4. 启动新服务
docker compose up -d

# 5. 等待新服务就绪
echo "等待新服务启动..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
        echo "新服务已就绪"
        exit 0
    fi
    sleep 2
done

echo "新服务启动超时，回滚"
docker compose down
# 回滚逻辑...
exit 1
'''
    with open("deploy.sh", "w") as f:
        f.write(script)
    print("已生成 deploy.sh")


if __name__ == "__main__":
    print("=" * 60)
    print("生成CI/CD配置文件")
    print("=" * 60)
    generate_github_actions()
    print()
    generate_check_metrics()
    print()
    generate_deploy_script()
