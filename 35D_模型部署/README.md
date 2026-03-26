# 第35D章：模型部署与推理优化

## 本章目标

- 掌握大模型本地部署方法（Ollama、vLLM）
- 理解模型量化技术（GPTQ、AWQ、GGUF）
- 学会用FastAPI包装模型服务
- 了解推理优化技巧

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 内容 |
|------|----------|----------|------|
| 1 | 1_deploy_overview.md | 1_deploy_overview.py | 部署概述与方案对比 |
| 2 | 2_ollama.md | 2_ollama.py | Ollama本地部署 |
| 3 | 3_quantization.md | 3_quantization.py | 模型量化 |
| 4 | 4_vllm.md | 4_vllm.py | vLLM高性能推理 |
| 5 | 5_api_service.md | 5_api_service.py | FastAPI模型服务 |

## 前置知识

- Python基础
- 生成式AI与LLM（第35章）

## 安装依赖

```bash
pip install fastapi uvicorn openai requests
# Ollama: https://ollama.com 下载安装
# vLLM: pip install vllm（需要Linux + GPU）
```

## 章节导航

[上一章：RAG](../35C_RAG/README.md) | [下一章：LLM Agent](../36_LLM_Agent/README.md)
