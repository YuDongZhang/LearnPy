# 11. 投机解码与多Token预测

## 解码阶段的瓶颈

自回归生成：每步产1个token、每步跑完整模型；decode阶段batch小、
算子小，GPU大量算力闲置（Mamba-3称之为"冷GPU"问题，见第10章）。

```
朴素解码: N个token = N次完整前向, 且每次只用了GPU的一小部分算力
```

## 投机解码（Speculative Decoding）

核心观察：验证k个token和生成1个token，对大模型都是一次前向（并行算k个位置的logits）。

```
1) draft (小模型) 连写k个候选token
2) target (大模型) 对 [上文+候选] 做一次前向 → 同时得到k个位置的预测
3) 接受最长正确前缀; 全对时附赠target自己的下一个token
   押对: 1次target前向产 k+1 个token
   押错: 接受前缀 + 修正1个, 继续
```

关键性质：**无损**。贪心模式下输出与target自身解码完全一致；
采样模式用拒绝采样保证分布一致（p/q比较，见论文）。

决定成败的是draft与target的对齐度：

| draft | 接受率 | 效果 |
|-------|--------|------|
| 同源小模型/蒸馏 | 70-90% | 加速2-3x |
| 随机小模型 | ≈0 | 反而更慢（白付起草开销）|

## MTP 多Token预测（DeepSeek-V3 / Nemotron 3）

训练时给模型加一个MTP模块，同时预测 t+2：

```
MTP输入 = 主模型hidden(t) ⊕ emb(t+1) → 投影 → 额外block → 预测t+2
训练时t+1用ground truth (teacher forcing)
```

双重收益：
- **训练**：forced lookahead，学到更有规划性的表示
- **推理**：MTP头就是"原生草稿"（自投机），免掉独立draft模型
  每次前向 = 主头出1个token + 顺带验证上轮MTP押注 → 最高2x

## 相关变体

| 变体 | 思路 |
|------|------|
| EAGLE | 在hidden层而非token层起草，接受率更高 |
| Medusa | 多个头同时预测多个未来位置 |
| 投机 + MTP | Nemotron 3：MTP层 + 原生投机解码 |

## 代码

`11_speculative_decoding.py`：训练target/draft/MTP（循环序列任务）、
投机解码（接受率与加速比统计）、随机draft反例、MTP自投机生成。
