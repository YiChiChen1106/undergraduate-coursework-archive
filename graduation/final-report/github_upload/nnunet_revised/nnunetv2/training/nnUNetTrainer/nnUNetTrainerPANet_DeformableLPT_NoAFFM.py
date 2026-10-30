from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_DeformableLPT_NoAFFM
import torch


class nnUNetTrainerPANet_DeformableLPT_NoAFFM(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            super().initialize()

            # 显式获取并设置深监督开关
            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True  # 强制开启，适配 nnU-Net 默认行为

            self.network = PANet_DeformableLPT_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def build_network(self):
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        return PANet_DeformableLPT_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )