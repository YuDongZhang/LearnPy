# 2. Ollama本地部署

## 什么是Ollama

Ollama是最简单的大模型本地部署工具，一条命令就能运行模型。支持Windows/Mac/Linux。

## 安装

从 https://ollama.com 下载安装包，或命令行安装：
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows/Mac: 下载安装包
```

## 基本使用

```bash
# 下载并运行模型
ollama run qwen2.5:7b

# 查看已下载的模型
ollama list

# 拉取模型（不运行）
ollama pull llama3.1:8b

# 删除模型
ollama rm qwen2.5:7b
```

## 常用模型

| 模型 | 命令 | 大小 |
|------|------|------|
| Qwen2.5 7B | `ollama run qwen2.5:7b` | ~4.7GB |
| Llama 3.1 8B | `ollama run llama3.1:8b` | ~4.7GB |
| Mistral 7B | `ollama run mistral` | ~4.1GB |
| Phi-3 3.8B | `ollama run phi3` | ~2.3GB |
| DeepSeek Coder | `ollama run deepseek-coder:6.7b` | ~3.8GB |

## API调用

Ollama启动后自动提供REST API（默认端口11434）：

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "什么是Python的装饰器？",
  "stream": false
}'
```

## 与OpenAI API兼容

Ollama兼容OpenAI API格式，可以直接用openai库调用：
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

## 自定义模型（Modelfile）

可以基于已有模型创建自定义版本：
```
FROM qwen2.5:7b
SYSTEM "你是一个Python编程专家，用简洁的中文回答。"
PARAMETER temperature 0
```

```bash
ollama create my-python-expert -f Modelfile
ollama run my-python-expert
```
