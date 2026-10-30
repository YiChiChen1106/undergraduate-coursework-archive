# UNET

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

## Slide 1

U-Net: Convolutional Networks for Biomedical Image Segmentation

## Slide 2

网络结构 

左半部分:收缩路径 (编码器)

结构：有好几层，一层中有两次 （3x3 卷积（No padding)+ReLU激活）+一次2x2最大池化

效果：

两次 3x3 卷积（No padding)可以提取空间特征，     并扩大感受野。

 ReLU引入了更多的非线性，增强了网络的“表达能力”，使其能够学习到更复杂、更精细的特征。否则两次卷积的叠加只相当于一次5x5的卷积。

一次2x2最大池化（下采样）减半特征图的高度和宽度，减少分辨率，能让网络获得更大的感受野，看得更“广” 。

	在层与层之间还有一步操作，得将通道数×2，

以此来补偿因池化操作导致的空间信息减少，并提取更丰富的特征。

Fig1.U-net architecture (example for 32x32 pixels in the lowest resolution). 

## Slide 3

网络结构

Fig1.U-net architecture (example for 32x32 pixels in the lowest resolution). 

右半部分：扩张路径（解码器)

结构：与收缩路径对称 。每个层级包含一次2x2的上卷积 ，它将特征通道数量减半 ；一次与收缩路径中对应层级特征图的拼接以及两次3x3卷积 + ReLU激活 。

效果：

一次2x2上卷积 (上采样)：逐步恢复特征图的高度和宽度 ，将收缩路径中学到的抽象特征信息传递到更高分辨率的层级中 ，是对下采样操作的逆过程。

拼接操作 (Skip Connection)：它将收缩路径中保留的、高分辨率的、包含精准空间位置信息的特征图 ，与上采样后的、包含高级语义信息的特征图结合起来。此举极大地弥补了因下采样丢失的细节信息，从而实现精准的像素级定位 

两次3x3卷积 + ReLU：对拼接后的特征图进行学习和融合，让网络学会如何结合上下文信息（来自上采样）和局部细节信息（来自拼接），从而生成更精确的分割图 

## Slide 4

网络结构

跳跃连接 (Skip Connection)

它是连接收缩路径（左半部分）和扩张路径（右半部分）的中间连接，是Unet的核心

原理：

在扩张路径的每一个层级，网络会执行以下操作：

1.首先，通过上卷积（up-convolution）将来自深层网络的特征图尺寸放大 

2.然后，找到收缩路径中与之对称、尺寸相应的那个特征图 

3.由于收缩路径中的卷积操作没有填充（padding），特征图会比扩张路径的略大一些，因此需要对其进行裁剪 (crop)，使两者的尺寸完全匹配 

4.最后，将裁剪后的高分辨率特征图与上采样后的特征图进行拼接 (concatenation)，将它们沿着通道维度堆叠在一起 （3，4步与上张图的第三部对应）

效果：通过跳跃连接，能将左边的高维细节和右边的抽象地位信息结合，正是这种深层与浅层特征的融合，使得U-Net即使在训练数据很少的情况下，也能够生成非常清晰和精确的分割结果 