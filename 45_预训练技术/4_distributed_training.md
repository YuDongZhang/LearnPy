# 4. 分布式训练

## 为什么需要分布式

- 7B模型fp16需要14GB显存（仅参数）
- 加上梯度+优化器状态需要60GB+
- 单卡放不下 → 多卡并行

## 并行策略

### 数据并行（Data Parallel）
每张卡有完整模型副本，数据分片：
```
GPU0: 模型副本 + 数据batch0
GPU1: 模型副本 + 数据batch1
→ 梯度同步 → 更新
```
最简单，但每卡都要放完整模型。

### 模型并行（Tensor Parallel）
将模型的矩阵运算切分到多卡：
```
GPU0: W的前半部分
GPU1: W的后半部分
→ 通信合并结果
```

### 流水线并行（Pipeline Parallel）
将模型的不同层放到不同卡：
```
GPU0: Layer 0-7
GPU1: Layer 8-15
GPU2: Layer 16-23
GPU3: Layer 24-31
```

### 3D并行
大规模训练同时使用三种并行：
```
数据并行 × 模型并行 × 流水线并行
```

## DeepSpeed ZeRO

微软的显存优化技术：
| 阶段 | 分片内容 | 显存节省 |
|------|---------|---------|
| ZeRO-1 | 优化器状态 | 4x |
| ZeRO-2 | + 梯度 | 8x |
| ZeRO-3 | + 参数 | N倍（N=GPU数） |

## FSDP

PyTorch原生的分布式训练方案，类似ZeRO-3。

## 工具

| 工具 | 特点 |
|------|------|
| DeepSpeed | 微软，功能最全 |
| FSDP | PyTorch原生 |
| Megatron-LM | NVIDIA，大规模训练 |
| Accelerate | HuggingFace，简单易用 |
| ColossalAI | 国产，易用 |
