# 6. 训练技巧与调优

## 学习率

微调中最重要的超参数。

| 微调方法 | 推荐学习率 |
|---------|-----------|
| 全量微调 | 1e-5 ~ 5e-5 |
| LoRA | 1e-4 ~ 3e-4 |
| QLoRA | 1e-4 ~ 2e-4 |

> 学习率太大 → 训练不稳定、灾难性遗忘
> 学习率太小 → 收敛慢、效果差

## 学习率调度

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| cosine | 余弦退火，平滑下降 | 最常用 |
| linear | 线性下降 | 简单有效 |
| constant_with_warmup | 预热后恒定 | 短训练 |

建议：warmup_ratio=0.03~0.1，让学习率先缓慢上升再下降。

## 批次大小与梯度累积

显存不够用大batch_size时，用梯度累积等效：

```
有效批次大小 = per_device_batch_size × gradient_accumulation_steps × GPU数量
```

例如：batch_size=1, accumulation=16, 1卡 → 有效批次=16

推荐有效批次大小：16-64

## 训练轮数

| 数据量 | 推荐epochs |
|--------|-----------|
| <1000条 | 3-5 |
| 1000-10000条 | 2-3 |
| >10000条 | 1-2 |

> 数据少时多训几轮，数据多时1-2轮就够。过多轮数会过拟合。

## 混合精度训练

- **fp16**：大多数GPU支持，显存减半
- **bf16**：A100/H100/4090等支持，数值更稳定，推荐
- 配置：`fp16=True` 或 `bf16=True`

## 梯度检查点（Gradient Checkpointing）

用计算换显存：前向传播时不保存中间激活值，反向传播时重新计算。

- 显存减少约30-50%
- 训练速度慢约20-30%
- 配置：`gradient_checkpointing=True`

## 过拟合防治

| 方法 | 说明 |
|------|------|
| 减少epochs | 最直接的方法 |
| 增大数据量 | 根本解决方案 |
| weight_decay | 权重衰减正则化（0.01-0.1） |
| dropout | LoRA的lora_dropout（0.05-0.1） |
| 早停 | 验证集loss不再下降时停止 |

## 灾难性遗忘

微调后模型可能丢失原有的通用能力。缓解方法：
1. 学习率不要太大
2. 训练轮数不要太多
3. 混入部分通用数据
4. 使用LoRA（天然缓解，因为原始权重冻结）

## 训练监控

推荐使用 wandb 或 tensorboard 监控：
- train_loss 曲线（应该平滑下降）
- eval_loss 曲线（不应该上升）
- 学习率变化
- GPU显存和利用率

```bash
# wandb
pip install wandb
wandb login

# tensorboard
tensorboard --logdir ./output/runs
```

## DeepSpeed

多卡训练和显存优化框架：
- ZeRO Stage 1：优化器状态分片
- ZeRO Stage 2：+ 梯度分片
- ZeRO Stage 3：+ 参数分片（可训练超大模型）

配合Hugging Face Accelerate使用：
```bash
accelerate launch --config_file ds_config.yaml train.py
```
