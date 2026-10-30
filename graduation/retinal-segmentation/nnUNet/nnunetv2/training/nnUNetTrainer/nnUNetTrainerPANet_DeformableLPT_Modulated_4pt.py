from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_DeformableLPT_NoAFFM
import torch


class nnUNetTrainerPANet_DeformableLPT_Modulated_4pt(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            # 1. 执行父类初始化（确定通道数、Loss 缩放等）
            super().initialize()

            print("=" * 60)
            print("ADVANCED EXPERIMENT: Modulated Deformable LPT (4-Point)")
            print("Configuration: No AFFM | 4-pt Sampling | Sigmoid Mask Active")
            print("Goal: Evaluate 'Selection' mechanism on slender vessel connectivity")
            print("=" * 60)

            # 2. 获取架构参数
            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            # 强制开启深监督，确保训练收敛性 [cite: 539, 562]
            arch_kwargs['deep_supervision'] = True

            # 3. 实例化加了 Modulation Mask 的模型
            # 确保你 pa_net.py 中的 PANet_DeformableLPT_NoAFFM 已按上一步代码更新
            self.network = PANet_DeformableLPT_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            # 4. 重新配置优化器（必须步骤，否则无法训练新参数）
            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def build_network(self):
        """ 用于推理和验证的架构构建 """
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        # 推理时关闭深监督辅助输出
        arch_kwargs['deep_supervision'] = False

        return PANet_DeformableLPT_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )