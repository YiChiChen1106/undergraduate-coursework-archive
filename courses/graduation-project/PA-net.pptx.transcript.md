# PA-net

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

## Slide 1

PA-Net: A hybrid architecture for retinal vessel segmentation

2025/11/07

## Slide 2

总体介绍

五个主要组成部分：

convolution block (Conv block)

lightweight parallel transformer (LPT)

adaptive vascular feature fusion module (AFFM)

Up-sampling

Down-sampling

研究背景：卷积神经网络（CNN)如unet难以捕捉对语义分割至关重要的长程依赖关系.为了解决这个问题，需要引入transformer，但是transformer需要大量算力资源和大数据集，为了解决这些问题，文章提出了一个

混合模型，它能：

捕捉长距离依赖（Transformer 的优点）

擅长局部细节（CNN 的优点）

轻量级并适用于小数据集（解决 Transformer 的缺点）

## Slide 3

convolution block (Conv block)

主要结构：

Conv3×3

BN (Batch Normalization)

GELU (高斯误差线性单元)：激活函数

Dropout (随机失活)

组件功能：

BN + Dropout：这两个层共同作用，帮助模型避免过拟合，并提高其泛化能力

GELU：作者提到，GELU 是一种优于传统 ReLU 的激活函数（允许一些负值通过），提供更多梯度，可以加速模型的收敛

## Slide 4

lightweight parallel transformer (LPT)

简述：

这是一个专门为视网膜血管分割任务设计的混合模块。它巧妙地融合了 CNN (卷积神经网络) 和 Transformer 的优点，以解决该任务的两大挑战：

局部细节：血管非常“细长”，容易“断裂”。

全局依赖：血管“跨度大”，形态复杂。

三个组成部分：

LFAU (Local Feature Accepting Unit)

EPA (Efficient Parallel Attention)

CFFN (Convolutional Feedforward Neural Network)

工作流程：

LFAU：先进来一次“局部特征预处理”

EPA：然后并行地、重量级地“提取局部细节 (Dw Conv)”和“捕捉全局依赖 (GAA)”，并将两者融合。

CFFN：最后用一个“轻量级的卷积 FFN”来对融合后的特征进行深度变换和信息提炼。

## Slide 5

LFAU（局部特征接受单元）

公式：LFAU(x) = DwConv(x) + x

作用：为了解决transformer只能处理一维序列数据而产生的两个缺点

1.会丢掉很多空间信息

2.不利于提取局部特征

因此这里使用3 × 3的深度卷积和残差级联，这样可以隐式嵌入位置编码信息，增强空间不变性，提取局部细节信息。

补充信息DwConv(x):Depth-wise convolution(深度卷积）

与标准卷积的区别：比如对于一个64*64*3的特征图，他要输出一个128通道的，如果标准卷积需要一个3*3的内核，那这个内核的真实尺寸是3*3*3，他一共需要3*3*3*128个参数

而深度卷积会对于三个通道先各用一个3*3*1的内核进行滑动，第二步用128个1*1*3的内核进行三层的相加，这样只需要3*（3*3*1）+128*（1*1*3）=411 个参数

作用：在提取局部特征的同时，保持模块的轻量化

## Slide 6

EPA (高效的并行注意力机制)

公式：EPA(x) = GELU(Conv(GAA(Conv(x))) + DwConv(x)) + x

原理：输入并行输入Dw Conv（再次提取局部特征）和 GAA

（门控轴向注意机制，用于提取长程依赖关系），之后将 Dw Conv 的输出和 GAA 的输出相加（+），实现了局部与全局信息的融合，融合后的结果通过 GELU 激活函数，这一部分再与原始输入最后进行残差连接。

重点介绍：GAA

GAA(x) = Attnw(AttnH(x))

流程：

Conv 1x1(降维）

Gated Multi-Head Attn Width(宽度轴注意力)

Gated Multi-Head Attn Height (高度轴注意力)

Conv 1x1 (升维)

作用：将Transformer 2D 注意力计算分解为两个 1D 计算，大大降低了成本

## Slide 7

CFFN卷积前馈神经网络

公式：CFFN(x) = Conv(DwConv(Conv(x))) + x

组成：路径1 (处理)：依次通过 Conv 1x1 -> Dw Conv -> Conv 1x1

           路径2 (残差)：原始输入 (来自EPA) 直接连接到最后的加法器

输出：两条路径的结果相加（+）

这是标准 Transformer 中“前馈神经网络 (FFN)”的卷积替代版

一般的FFN通常由两个全连接层组成，负责捕捉通道相关性，但问题是，全连接层 (Fully Connected Layer) 会“压平”特征图，它不关心像素的 (x, y) 坐标，因此会破坏（corrupt）宝贵的空间信息，而CFFN是由一组卷积操作替换了全连接层。

Conv 1x1（升维）将通道数扩展 4 倍，因为在更高维度的“特征空间”中进行处理，这被证明更有效

3x3 Depth-wise Conv在上一步的 4倍通道数特征图上进行卷积，它在保留空间结构的同时，高效地混合了局部的空间特征。这是全连接层完全做不到的

Conv 1x1 (降维)将特征图投影回原来的维度，准备好进入下一个 LPT 模块或网络的下一层

## Slide 8

AFFM自适应血管特征融合模块

作用：替换掉unet简单的跳跃连接 ，来最大程度解决解决 U-Net 下采样导致的空间信息丢失（尤其是微血管）

工作流程：

输入：来自多个尺度的特征 F1, F2, F3（以及 F0）

尺度统一：通过 Conv 1x1、Down 和 Up 操作，将 F1, F2, F3 统一到相同尺度，得到 C1, C2, C3

生成注意力图：将 C1, C2, C3 拼接 (Concat) -> Conv 1x1 (压缩到3通道) -> Softmax

结果：得到三个空间注意力权重 A1, A2, A3，这三个变量分别代表了在每个像素上，来自 C1, C2, C3 的信息应该占有的“权重”或“重要性”

加权融合：FB1 = C1 * A1, FB2 = C2 * A2, FB3 = C3 * A3

输出：(FB1 + FB2 + FB3) 再与 F0 拼接 (Concat)

优势：与简单地将不同层拼接相比，AFFM通过softmax学习

网络浅层的高分辨率细节信息和深层的低分辨率上下文信息，从而得出一个动态的、自适应的权重，极大地提升模型（尤其是分割和检测模型）的性能。

## Slide 9

结果 & 创新点

创新点 1：将 LPT 作为 nnU-Net 的新“底部”

创新点 2：将 AFFM 作为 nnU-Net 的新“跳跃连接

## Slide 10

自己的成果

一共做了四次训练（三次有效）

三次有效的训练都以DRIVE数据集为测试集，训练集和验证集都按刘师兄给的名单做了划分，这样好对比成果

第一次实验，就是以dice系数为标准，nnunet训练了150个epoch，模型在第69个epoch达到收敛，dice系数为0.8616999983787537 ，整体测试结果如表：

IoU (血管)

mIoU

Recall

Precision

Accuracy

mPA

F1-score

0.6574

0.8107

0.7688

0.8219

0.9664

0.8768

0.7924

## Slide 11

第二次实验

第二次实验也以dice系数为标准，nnunet训练了150个epoch，但是将所有数据集都用clahe图像增强技术,模型在第60个epoch达到收敛，相比没数据加强之前，初始dice系数变高了（0.7128到0.7512），dice系数增幅加快，但是在达到收敛后dice系数和第一次几乎相同，为0.8618999719619751，最终会经过检测，结果为：

IoU (血管)

mIoU

Recall

Precision

Accuracy

mPA

F1-score

0.6441

0.8041

0.7282

0.8497

0.9662

0.8583

0.7827

## Slide 12

第三次实验

第三次实验我还是以CLAHE数据增强，但是这次以focal loss为标准，Dice系数更关注于分割区域的重叠程度，而focal loss模型更关注难以处理的像素（例如细小血管、血管边缘）以及处理类别不平衡（背景像素远多于血管像素）。而我们的眼底血管分割更希望模型在这些困难区域表现更好，减少错误分类。这次也训练了150个epoch,训练在第53个epoch收敛，focal loss达到最低值0.0245999991893768

IoU (血管)

mIoU

Recall

Precision

Accuracy

mPA

F1-score

0.6410

0.8023

0.7255

0.8489

0.9659

0.8568

0.7802

## Slide 13

与刘师兄数据的对比

分割方法

IoU 血管

mIoU

Recall

Precision

Accuracy

mPA

F1-score

Hrnet

0.4686

0.6995

0.6890

0.5943

0.9344

0.8230

0.6382

Deeplabv3+

0.5764

0.7601

0.8388

0.6483

0.9477

0.8983

0.7313

UNet

0.6441

0.8026

0.7735

0.7937

0.9637

0.8775

0.7835

CLAHE+UNet

0.6409

0.8015

0.7452

0.8206

0.9646

0.8651

0.7811

CLAHE+改进 UNet

0.6560

0.8089

0.8002

0.7845

0.9644

0.8899

0.7923

nnunet

0.6574

0.8107

0.7688

0.8219

0.9664

0.8768

0.7924

CLAHE+nnunet

0.6441

0.8041

0.7282

0.8497

0.9662

0.8583

0.7827

CLAHE+nnunet

+focal loss

0.6410

0.8023

0.7255

0.8489

0.9659

0.8568

0.7802