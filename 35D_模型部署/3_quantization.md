# 3. 模型量化

## 什么是量化

将模型权重从高精度（FP16/FP32）压缩到低精度（INT8/INT4），减少显存占用和加速推理。

## 量化效果

以7B模型为例：
| 精度 | 显存 | 速度 | 质量损失 |
|------|------|------|---------|
| FP16 | ~14GB | 基准 | 无 |
| INT8 | ~7GB | 快 | 极小 |
| INT4(GPTQ) | ~4GB | 更快 | 小 |
| INT4(AWQ) | ~4GB | 更快 | 很小 |
| GGUF Q4 | ~4GB | CPU可用 | 小 |

## 主流量化格式

### GPTQ
- GPU推理专用
- 需要校准数据集
- 社区模型多（TheBloke等）

### AWQ
- GPU推理，质量略优于GPTQ
- 更快的量化速度
- 推荐用于生产环境

### GGUF
- llama.cpp使用的格式
- 支持CPU和GPU混合推理
- Ollama默认使用此格式
- 多种量化级别（Q2到Q8）

## 使用量化模型

### 方式1：直接下载量化版
HuggingFace上有大量预量化模型：
```
TheBloke/Qwen2.5-7B-GPTQ
TheBloke/Qwen2.5-7B-AWQ
```

### 方式2：自己量化
用AutoGPTQ或AutoAWQ工具量化。

### 方式3：Ollama自动处理
Ollama下载的模型已经是GGUF量化版。

## 量化选择建议

```
有GPU + 生产环境 → AWQ
有GPU + 快速使用 → GPTQ
无GPU / Ollama → GGUF
追求质量 → FP16（不量化）
```
