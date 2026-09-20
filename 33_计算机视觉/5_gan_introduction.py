"""
GAN 生成对抗网络
==============

介绍生成对抗网络 (GAN) 的原理和实现。
"""

print("=" * 60)
print("1. GAN 简介")
print("=" * 60)

print("""
生成对抗网络 (Generative Adversarial Networks, GAN):

由 Ian Goodfellow 于 2014 年提出

核心思想:
  • 两个神经网络相互对抗
  • 生成器 (Generator): 造假
  • 判别器 (Discriminator): 鉴别

类比:
  • 生成器: 造假币的犯罪分子
  • 判别器: 警察
  • 目标: 造出以假乱真的钞票

应用:
  • AI 绘画 (Midjourney, Stable Diffusion)
  • 人脸生成
  • 图像修复
  • 数据增强
  • 风格迁移
""")

print()
print("=" * 60)
print("2. GAN 原理")
print("=" * 60)

print("""
2.1 网络结构

  噪声 z ──┬──→ 生成器 G ──→ 生成图像 G(z)
           │
           └──→ 真实图像 x
                    │
                    ↓
           判别器 D ──→ 真/假 (0-1)

2.2 损失函数 (Minimax Game)

  min_G max_D V(D, G) = E[log D(x)] + E[log(1 - D(G(z)))]

  • 判别器: 最大化区分真伪
  • 生成器: 最小化被识别为假的概率

2.3 训练过程

  1. 固定生成器，训练判别器
  2. 固定判别器，训练生成器
  3. 交替进行

2.4 训练技巧

  • 使用标签平滑
  • 批归一化
  • 学习率调度
  • 谱归一化
""")

print()
print("=" * 60)
print("3. DCGAN 原理")
print("=" * 60)

print("""
Deep Convolutional GAN (DCGAN):

改进:
  • 使用转置卷积上采样
  • 使用 Batch Normalization
  • 移除全连接层
  • 使用 ReLU/Tanh

生成器结构:
  • 输入: 随机噪声 (100维)
  • 转置卷积: 4×4 → 8×8 → 16×16 → 32×32 → 64×64
  • 输出: 64×64×3 图像

判别器结构:
  • 输入: 64×64×3 图像
  • 卷积: 64→32→16→8→4
  • 输出: 1 维 (真/假)
""")

print()
print("=" * 60)
print("4. DCGAN 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn

# 4.1 生成器
class Generator(nn.Module):
    def __init__(self, latent_dim=100, ngf=64):
        super(Generator, self).__init__()

        self.main = nn.Sequential(
            # 输入: latent_dim × 1 × 1
            nn.ConvTranspose2d(latent_dim, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),

            # 4 × 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),

            # 8 × 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),

            # 16 × 16
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),

            # 32 × 32
            nn.ConvTranspose2d(ngf, 3, 4, 2, 1, bias=False),
            nn.Tanh()
            # 输出: 3 × 64 × 64
        )

    def forward(self, input):
        return self.main(input)


# 4.2 判别器
class Discriminator(nn.Module):
    def __init__(self, ndf=64):
        super(Discriminator, self).__init__()

        self.main = nn.Sequential(
            # 输入: 3 × 64 × 64
            nn.Conv2d(3, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            # 32 × 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),

            # 16 × 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),

            # 8 × 8
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),

            # 4 × 4
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)


# 4.3 初始化
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find("Conv") != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find("BatchNorm") != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

# 使用
netG = Generator(latent_dim=100, ngf=64)
netD = Discriminator(ndf=64)

netG.apply(weights_init)
netD.apply(weights_init)
''')

print()
print("=" * 60)
print("5. GAN 训练")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.utils as vutils

# 超参数
latent_dim = 100
batch_size = 64
lr = 0.0002
beta1 = 0.5
epochs = 5

# 设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 模型
netG = Generator(latent_dim).to(device)
netD = Discriminator().to(device)

# 损失
criterion = nn.BCELoss()

# 优化器
optimizerD = optim.Adam(netD.parameters(), lr=lr, betas=(beta1, 0.999))
optimizerG = optim.Adam(netG.parameters(), lr=lr, betas=(beta1, 0.999))

# 真实标签和假标签
real_label = 1
fake_label = 0

# 训练循环
for epoch in range(epochs):
    for i, (images, _) in enumerate(dataloader):
        batch_size = images.size(0)
        images = images.to(device)

        # ---------- 训练判别器 ----------
        netD.zero_grad()

        # 真实图像
        label = torch.full((batch_size,), real_label, device=device)
        output = netD(images).view(-1)
        errD_real = criterion(output, label)

        # 生成图像
        noise = torch.randn(batch_size, latent_dim, 1, 1, device=device)
        fake = netG(noise)
        label.fill_(fake_label)
        output = netD(fake.detach()).view(-1)
        errD_fake = criterion(output, label)

        # 总损失
        errD = errD_real + errD_fake
        errD.backward()
        optimizerD.step()

        # ---------- 训练生成器 ----------
        netG.zero_grad()

        label.fill_(real_label)
        output = netD(fake).view(-1)
        errG = criterion(output, label)
        errG.backward()
        optimizerG.step()

        # 打印
        if i % 50 == 0:
            print(f"[{epoch}/{epochs}][{i}/{len(dataloader)}] "
                  f"Loss_D: {errD.item():.4f} Loss_G: {errG.item():.4f}")

    # 保存生成的图像
    with torch.no_grad():
        fake = netG(fixed_noise).detach().cpu()
    img_grid = vutils.make_grid(fake, padding=2, normalize=True)
''')

print()
print("=" * 60)
print("6. 条件 GAN (cGAN)")
print("=" * 60)

print("""
条件生成对抗网络 (cGAN):

改进:
  • 生成器和判别器都加入条件信息
  • 可以控制生成内容

应用:
  • 图像到图像转换
  • 文本生成图像
  • 类别特定生成

条件:
  • 类别标签
  • 文本描述
  • 分割图
""")

print()
print('''
# cGAN 实现
class cGenerator(nn.Module):
    def __init__(self, latent_dim=100, num_classes=10, ngf=64):
        super(cGenerator, self).__init__()

        self.label_emb = nn.Embedding(num_classes, num_classes)

        self.main = nn.Sequential(
            nn.ConvTranspose2d(latent_dim + num_classes, ngf * 8, 4, 1, 0),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),

            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),

            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),

            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),

            nn.ConvTranspose2d(ngf, 3, 4, 2, 1),
            nn.Tanh()
        )

    def forward(self, noise, labels):
        label_embedding = self.label_emb(labels).unsqueeze(2).unsqueeze(3)
        gen_input = torch.cat((noise, label_embedding), dim=1)
        return self.main(gen_input)


class cDiscriminator(nn.Module):
    def __init__(self, num_classes=10, ndf=64):
        super(cDiscriminator, self).__init__()

        self.label_emb = nn.Embedding(num_classes, 3 * 64 * 64)

        self.main = nn.Sequential(
            nn.Conv2d(6, ndf, 4, 2, 1),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(ndf, ndf * 2, 4, 2, 1),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(ndf * 4, 1, 4, 1, 0),
            nn.Sigmoid()
        )

    def forward(self, img, labels):
        label_embedding = self.label_emb(labels)
        label_embedding = label_embedding.view(img.size(0), 3, 64, 64)
        d_in = torch.cat((img, label_embedding), dim=1)
        return self.main(d_in)
''')

print()
print("=" * 60)
print("7. Pix2Pix (图像转换)")
print("=" * 60)

print("""
Pix2Pix: Image-to-Image Translation with CGAN

应用:
  • 素描 → 照片
  • 白天 → 夜晚
  • 分割图 → 真实图像
  • 线条画 → 彩色图

架构:
  • 生成器: U-Net
  • 判别器: PatchGAN

损失函数:
  L_GAN + λ * L_L1

  L_L1: 像素级 L1 损失
""")

print()
print("=" * 60)
print("8. CycleGAN (无配对转换)")
print("=" * 60)

print("""
CycleGAN: Unpaired Image-to-Image Translation

特点:
  • 无需配对数据
  • 两个生成器, 两个判别器

循环一致性损失:
  • X → G(X) → F(G(X)) ≈ X
  • Y → F(Y) → G(F(Y)) ≈ Y

应用:
  • 马 → 斑马
  • 油画 → 照片
  • 夏季 → 冬季
""")

print()
print("=" * 60)
print("9. StyleGAN")
print("=" * 60)

print("""
StyleGAN (NVIDIA):

特点:
  • 风格向量控制生成
  • 渐进式增长训练
  • 高级特征分离

应用:
  • 人脸生成
  • AI 头像
  • 艺术创作

版本:
  • StyleGAN (2018)
  • StyleGAN2 (2019) - 改进质量
  • StyleGAN3 (2021) - 解决_aliasing

潜在空间操作:
  • 改变发型
  • 调整年龄
  • 切换表情
  • 改变性别
""")

print()
print("=" * 60)
print("10. Stable Diffusion")
print("=" * 60)

print("""
Stable Diffusion:

基于扩散模型的图像生成:

原理:
  1. 前向扩散: 逐步加噪声
  2. 反向扩散: 逐步去噪声

组成:
  • VAE: 图像编码/解码
  • UNet: 去噪网络
  • CLIP Text Encoder: 文本编码
  • Scheduler: 采样调度

应用:
  • Text-to-Image (文生图)
  • Image-to-Image (图生图)
  • Inpainting (修复)
  • ControlNet (控制生成)

主流模型:
  • Stable Diffusion v1.5
  • Stable Diffusion XL (SDXL)
  • Playground, Midjourney
""")

print()
print("=" * 60)
print("11. GAN 训练技巧")
print("=" * 60)

print("""
11.1 模式崩溃

  问题: 生成器只生成几种样本
  解决:
    • 使用小批量 discrimination
    • 标签平滑
    • 多次更新 D

11.2 训练不稳定

  解决:
    • 学习率调度
    • 谱归一化 (Spectral Normalization)
    • WGAN-GP
    • 自适应学习率

11.3 判别器过强

  解决:
    • 标签噪声
    • 判别器 dropout
    • 交替训练

11.4 评估指标

  • Inception Score (IS)
  • Fréchet Inception Distance (FID)
  • 人工评估
""")

print()
print("=" * 60)
print("12. GAN 总结")
print("=" * 60)

print("""
GAN 要点:

✓ 核心思想:
  • 生成器 vs 判别器
  • 对抗训练

✓ 经典架构:
  • DCGAN: CNN 基础
  • cGAN: 条件控制
  • Pix2Pix: 图像转换
  • CycleGAN: 无配对转换

✓ 高级模型:
  • StyleGAN: 风格控制
  • BigGAN: 高质量生成
  • Diffusion: 当前主流

✓ 训练技巧:
  • 标签平滑
  • 谱归一化
  • 渐进式增长

✓ 应用:
  • AI 绘画
  • 数据增强
  • 风格迁移
  • 图像修复
""")
