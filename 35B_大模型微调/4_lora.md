# 4. LoRA与QLoRA微调（重点）

## LoRA原理

LoRA（Low-Rank Adaptation）的核心思想：

模型权重的变化可以用低秩矩阵近似。不直接修改原始权重W，而是在旁边加一个低秩分解 ΔW = A × B：

```
原始: Y = W × X
LoRA: Y = W × X + (A × B) × X

其中:
  W: 原始权重矩阵（冻结不动）
  A: 降维矩阵 (d × r)，r << d
  B: 升维矩阵 (r × d)
  r: 秩（rank），通常4-64
```

只训练A和B，参数量极小（原模型的0.1%左右），但效果接近全量微调。

## LoRA关键参数

| 参数 | 说明 | 常用值 |
|------|------|--------|
| r (rank) | 秩，越大表达能力越强 | 8-64 |
| lora_alpha | 缩放系数 | 通常等于r或2r |
| lora_dropout | Dropout比率 | 0.05-0.1 |
| target_modules | 应用LoRA的层 | q_proj, v_proj等 |

### rank怎么选
- r=8：轻量级，适合简单任务
- r=16-32：常用，平衡效果和效率
- r=64：接近全量微调效果

### target_modules怎么选
- 最少：只加在q_proj和v_proj（注意力层的Q和V）
- 推荐：q_proj, k_proj, v_proj, o_proj（所有注意力投影）
- 最多：加上gate_proj, up_proj, down_proj（FFN层也加）

## QLoRA

QLoRA = LoRA + 4bit量化，进一步降低显存：

1. 将基座模型量化为4bit（NF4格式）
2. 在量化模型上应用LoRA
3. 训练时只更新LoRA参数（fp16/bf16）

显存对比（7B模型）：
| 方法 | 显存 |
|------|------|
| 全量微调 | ~60GB |
| LoRA(fp16) | ~16GB |
| QLoRA(4bit) | ~6GB |

## 训练流程

```
1. 加载模型（QLoRA需要4bit量化加载）
2. 配置LoraConfig
3. 用get_peft_model包装模型
4. 配置TrainingArguments
5. 用SFTTrainer训练
6. 保存LoRA权重（很小，通常几十MB）
7. 推理时合并或单独加载
```

## 权重合并

训练完成后可以将LoRA权重合并回基座模型：
```python
merged_model = model.merge_and_unload()
```
合并后就是一个普通模型，推理无额外开销。

也可以不合并，推理时动态加载LoRA适配器，方便切换不同任务版本。

## LoRA最佳实践

1. 先用小rank(8)快速验证，再逐步增大
2. 学习率比全量微调大一些（1e-4 ~ 3e-4）
3. target_modules至少包含q_proj和v_proj
4. QLoRA训练时用bf16（如果GPU支持）
5. 训练完先评估再决定是否合并
