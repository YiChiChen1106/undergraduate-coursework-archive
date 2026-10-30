# logbook

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Log Book

我的任务是The

primary objective of this project is to leverage the nnU-Net v2 framework to

establish a high-performance baseline for retinal vessel segmentation and

subsequently develop and evaluate a novel, improved model incorporating a

modified loss function

然后在10月1号至10月7日，我在网上阅读了pytorch的技术文档，并学习了如何加载数据集，添加package，如何构造一个稳定的环境，并学习了卷积层和池化层的概念，并上手处理了CIFAR数据集，

10月9日-10月17日我系统学习了U-net的论文，并在bilibili看了别人如何搭建U-net环境，并处理几个比较有名的数据集，并编写了一个PPT用于10月17日组会汇报，

10月17-10月24，我在网上继续浏览U-net的各种变种,包括U-mamba，U-Net++，ResUNet，nnU-Net，这段时间我发现nnunet不是一个固定的新架构，而是一个自适应框架。它能根据给定数据集的特性（如图像大小、分辨率、模态等），自动配置最优的 U-Net 架构（包括 2D U-Net, 3D U-Net, U-Net 级联等）以及预处理和后处理流程。在各种生物医学图像分割竞赛中取得了顶尖的成绩，证明了其强大的泛化性和鲁棒性。因此我决定将研究对象从宽泛的Unet聚焦于nnunet。

10月24日，我成功从GitHub上下载了nnunet的源码，并新搭建了一个nnunetv2环境，我遇到了1.nvidia版本过低导致训练无法正常进行，2.nnunetv2和nnunetv1的文件命名情况不一样，而我误用了nnunetv1的命名方式导致模型训练是找不到已经经过转化的数据集。3.nnunet需要三维nii数据，而我一开始只生成了一维nii数据，我需要将一维数据进行适当拓展  

10.25-10.26

我听从了supervisor的意见，根据他给我已指定好的训练集验证集 测试集名单将数据集分成了三部分，并将最大epoch数设成了150.

问题：我发现一开始我在测试集测试的时候发现 mIoU  ，Recall等数值非常低，经过排查，在经过supervisor提醒，我发现是在nnunetv2的图像增强时会使图片进行翻转：

成果：---------------------- 评估结果 (平均值) ----------------------

成功处理了 40 / 40 个图像对。

指标          | 计算值

--------------|---------

IoU (血管)    | 0.6574

mIoU          | 0.8107

Recall        | 0.7688

Precision     | 0.8219

Accuracy      | 0.9664

mPA           | 0.8768

F1-score      | 0.7924

----------------------------------------------------------------

10.27

在我将10月26日的结果与supervisor交流后，我将数据集的原始数据换成了CLAHE增强后的数据集。我又进行了一边训练这次没有遇到问题。

结果：模型的收敛速度比未增强前更快，但结果跟未增强前几乎没什么区别

IoU (血管)    | 0.6574

mIoU          | 0.8107

Recall        | 0.7688

Precision     | 0.8219

Accuracy      | 0.9664

mPA           | 0.8768

F1-score      | 0.7924

10.28

我将10.27结果汇报给supervisor，将模型训练过程中的标准从dice系数变为了focal loss，我又进行了一遍训练，结果还是没有多大变化

IoU (血管)    | 0.6410

mIoU          | 0.8023

Recall        | 0.7255

Precision     | 0.8489

Accuracy      | 0.9659

mPA           | 0.8568

F1-score      | 0.7802