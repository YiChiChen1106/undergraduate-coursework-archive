from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_DeformableLPT_Full
import torch


class nnUNetTrainerPANet_Deformable_Full(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            super().initialize()

            print("=" * 60)
            print("RUNNING FULL MODEL: Deformable LPT + AFFM (Adaptive Fusion)")
            print("=" * 60)

            # 获取 nnU-Net 自动计算的架构参数
            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True

            # 实例化完全体模型
            self.network = PANet_DeformableLPT_Full(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            # 必须重新配置优化器以关联新模型的参数
            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def build_network(self):
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        return PANet_DeformableLPT_Full(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )