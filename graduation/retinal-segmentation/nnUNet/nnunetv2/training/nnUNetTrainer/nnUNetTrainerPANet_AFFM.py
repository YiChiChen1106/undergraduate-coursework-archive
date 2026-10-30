from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
import torch.nn as nn


class nnUNetTrainerPANet_AFFM(nnUNetTrainerPANet):
    def initialize(self):
        """
        继承并增强初始化逻辑
        """
        # 1. 先调用父类的 initialize 完成网络、优化器、Loss 的标准初始化
        super().initialize()

        # 2. 【消融核心】将 LPT 替换为 Identity (跳过 Transformer 计算)
        # 这样网络在运行到 Bottleneck 时，会直接经过卷积后进入 Decoder，不再经过 LPT
        if hasattr(self.network, 'lpt'):
            print("=" * 50)
            print("ABLATION STUDY: Replacing LPT with nn.Identity() (AFFM Only Mode)")
            print("=" * 50)
            self.network.lpt = nn.Identity()

            # 重新把网络搬运到设备，确保改动生效
            self.network.to(self.device)

            # 由于参数变了（去掉了 LPT 的参数），我们需要重新初始化优化器
            # 否则 Adam 可能会因为找不到 LPT 的梯度而报错
            self.optimizer, self.lr_scheduler = self.configure_optimizers()
        else:
            print("❌ ERROR: Could not find LPT module in self.network!")

    def build_network(self):
        """
        保持与父类一致的构建逻辑，具体的“切除”手术在 initialize 里做更安全
        """
        return super().build_network()