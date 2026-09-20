# 5. GAN生成对抗网络

## 核心思想

GAN (Generative Adversarial Networks) 由 Ian Goodfellow 于 2014 年提出：**两个神经网络相互对抗**。

- **生成器 (Generator)**：造假——把随机噪声变成假图像
- **判别器 (Discriminator)**：鉴别——判断图像是真是假

类比：生成器是造假币的犯罪分子，判别器是警察，对抗的结果是造出以假乱真的钞票。

应用：AI 绘画、人脸生成、图像修复、数据增强、风格迁移。

## 原理

```
噪声 z ──→ 生成器 G ──→ 生成图像 G(z) ──┐
                                        ├──→ 判别器 D ──→ 真/假 (0-1)
真实图像 x ────────────────────────────┘
```

损失函数（Minimax 博弈）：

```
min_G max_D V(D, G) = E[log D(x)] + E[log(1 - D(G(z)))]

判别器: 最大化区分真伪的能力
生成器: 最小化被识别为假的概率
```

训练过程：固定生成器训练判别器 → 固定判别器训练生成器 → 交替进行。

## DCGAN

DCGAN (Deep Convolutional GAN) 的改进：
- 使用转置卷积上采样
- 使用 Batch Normalization
- 移除全连接层
- 生成器用 ReLU/Tanh，判别器用 LeakyReLU

生成器：噪声 (100维) → 转置卷积逐级上采样 4→8→16→32→64 → 输出 64×64×3 图像。

```python
class Generator(nn.Module):
    def __init__(self, latent_dim=100, ngf=64):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # ... 逐级上采样 ...
            nn.ConvTranspose2d(ngf, 3, 4, 2, 1, bias=False),
            nn.Tanh()   # 输出: 3 × 64 × 64
        )

    def forward(self, input):
        return self.main(input)
```

判别器则是镜像的卷积网络，末端 Sigmoid 输出真/假概率。

## 训练循环

```python
criterion = nn.BCELoss()
optimizerD = optim.Adam(netD.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizerG = optim.Adam(netG.parameters(), lr=0.0002, betas=(0.5, 0.999))

# ---------- 训练判别器 ----------
# 真实图像标签 1, 生成图像标签 0, 两部分损失相加
errD = criterion(netD(images), real) + criterion(netD(fake.detach()), fake_label)

# ---------- 训练生成器 ----------
# 让生成图像在判别器那里看起来像真的一样
errG = criterion(netD(fake), real_label)
```

关键点：训练判别器时对生成图像用 `fake.detach()`，避免梯度传回生成器。

## GAN家族

| 模型 | 特点 | 应用 |
|------|------|------|
| DCGAN | CNN 基础的 GAN | 通用图像生成 |
| cGAN | 生成器/判别器加入条件信息（类别、文本） | 可控生成 |
| Pix2Pix | U-Net 生成器 + PatchGAN 判别器，配对数据 | 素描→照片、分割图→真实图 |
| CycleGAN | 无需配对数据，两个生成器+两个判别器，循环一致性损失 | 马→斑马、油画→照片 |
| StyleGAN | 风格向量控制生成，渐进式增长 | 人脸生成、AI 头像 |
| Diffusion | 逐步加噪/去噪 | 当前主流 |

CycleGAN 循环一致性：X → G(X) → F(G(X)) ≈ X。

## Stable Diffusion

基于扩散模型的图像生成：

```
前向扩散: 逐步给图像加噪声
反向扩散: 从噪声逐步恢复图像
```

组成：VAE（编码/解码）、UNet（去噪网络）、CLIP Text Encoder（文本编码）、Scheduler（采样调度）。

应用：文生图、图生图、Inpainting 修复、ControlNet 控制生成。

## 训练技巧

| 问题 | 解决方案 |
|------|---------|
| 模式崩溃（只生成几种样本） | 小批量 discrimination、标签平滑、多次更新 D |
| 训练不稳定 | 学习率调度、谱归一化、WGAN-GP |
| 判别器过强 | 标签噪声、判别器 dropout、交替训练 |

评估指标：Inception Score (IS)、Fréchet Inception Distance (FID)。

## 代码

讲解对应的示例代码见 `5_gan_introduction.py`。
