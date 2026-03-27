# 5. CI/CD与自动化部署

## ML项目的CI/CD

```
代码提交 → 自动测试 → 自动训练/评估 → 自动部署
```

## GitHub Actions示例

```yaml
name: ML Pipeline
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install -r requirements.txt
      - run: pytest tests/

  evaluate:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: python evaluate.py
      - run: python check_metrics.py  # 指标达标才继续

  deploy:
    needs: evaluate
    runs-on: ubuntu-latest
    steps:
      - run: docker build -t my-ai-app .
      - run: docker push my-ai-app
      - run: kubectl rollout restart deployment/ai-app
```

## 部署策略

| 策略 | 说明 | 风险 |
|------|------|------|
| 直接替换 | 停旧启新 | 有停机时间 |
| 蓝绿部署 | 两套环境切换 | 需要双倍资源 |
| 金丝雀部署 | 先切少量流量 | 最安全 |
| 滚动更新 | 逐步替换实例 | Kubernetes默认 |

## 回滚

部署后发现问题，快速回滚：
```bash
# Docker
docker compose up -d --force-recreate

# Kubernetes
kubectl rollout undo deployment/ai-app
```

## LLM项目的CI/CD特点

- Prompt变更也需要走CI/CD
- 评估用LLM-as-Judge自动化
- RAG数据更新触发重建索引
- 模型切换通过配置而非重新部署
