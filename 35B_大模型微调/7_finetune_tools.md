# 7. 微调工具实战

## 工具对比

| 工具 | 特点 | 适合谁 |
|------|------|--------|
| Transformers + PEFT | 最灵活，完全可控 | 想深入理解原理的开发者 |
| LLaMA-Factory | 一站式，WebUI+命令行 | 快速上手，不想写太多代码 |
| Unsloth | 速度快2-5x，显存省60% | 追求效率，显存紧张 |
| Axolotl | 配置文件驱动 | 喜欢YAML配置的人 |
| Swift（魔搭） | 中文生态好 | 国内用户 |

## LLaMA-Factory

### 简介
LLaMA-Factory是一个一站式大模型微调平台，支持100+模型，提供WebUI和命令行两种方式。

### 安装
```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
pip install -e ".[torch,metrics]"
```

### WebUI方式
```bash
llamafactory-cli webui
```
打开浏览器，在界面上选择模型、数据集、微调方法，点击开始训练。

### 命令行方式
```bash
llamafactory-cli train examples/train_lora/llama3_lora_sft.yaml
```

### 配置文件示例
```yaml
model_name_or_path: meta-llama/Meta-Llama-3-8B-Instruct
stage: sft
finetuning_type: lora
lora_rank: 8
lora_target: all
dataset: alpaca_zh
template: llama3
output_dir: output/llama3-lora
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
num_train_epochs: 3
learning_rate: 1.0e-4
bf16: true
```

## Unsloth

### 简介
Unsloth通过优化内核实现2-5倍加速和60%显存节省，API与Hugging Face兼容。

### 安装
```bash
pip install unsloth
```

### 使用方式
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3-8b-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)
```
后续训练流程与Hugging Face一致。

## 工具选择建议

```
初学者，想快速体验 → LLaMA-Factory（WebUI）
想深入理解原理 → Transformers + PEFT（手写代码）
追求训练速度 → Unsloth
生产环境部署 → Transformers + PEFT 或 vLLM
```
