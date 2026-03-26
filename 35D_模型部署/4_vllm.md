# 4. vLLM高性能推理

## 什么是vLLM

vLLM是目前最快的LLM推理引擎，核心技术是PagedAttention，大幅提升吞吐量。

## 核心优势

- **高吞吐量**：比HuggingFace Transformers快2-24倍
- **PagedAttention**：高效管理KV Cache显存
- **连续批处理**：动态合并请求，提高GPU利用率
- **OpenAI兼容API**：无缝替换OpenAI接口

## 安装（需要Linux + GPU）

```bash
pip install vllm
```

## 启动服务

```bash
# 启动OpenAI兼容的API服务
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000 \
    --max-model-len 4096
```

## 支持量化模型

```bash
# GPTQ量化模型
python -m vllm.entrypoints.openai.api_server \
    --model TheBloke/Qwen2.5-7B-GPTQ \
    --quantization gptq

# AWQ量化模型
python -m vllm.entrypoints.openai.api_server \
    --model TheBloke/Qwen2.5-7B-AWQ \
    --quantization awq
```

## API调用

vLLM兼容OpenAI API，直接用openai库：
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="vllm")
```

## vLLM vs Ollama

| 特性 | vLLM | Ollama |
|------|------|--------|
| 性能 | 最快 | 中等 |
| 并发 | 优秀 | 一般 |
| 易用性 | 中等 | 最简单 |
| 平台 | Linux | 全平台 |
| 适用 | 生产环境 | 开发/个人 |
