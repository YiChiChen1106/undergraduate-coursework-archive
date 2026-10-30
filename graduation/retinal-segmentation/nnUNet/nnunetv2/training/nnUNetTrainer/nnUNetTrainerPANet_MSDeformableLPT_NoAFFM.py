from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_MSDeformableLPT_NoAFFM
import torch


class nnUNetTrainerPANet_MSDeformableLPT_NoAFFM(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            super().initialize()

            print("=" * 60)
            print("ULTIMATE EXPERIMENT: Multi-Scale Modulated Deformable LPT")
            print("Configuration: No AFFM | Cross-layer Sampling | 4-pt/Level")
            print("=" * 60)

            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True

            self.network = PANet_MSDeformableLPT_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def build_network(self):
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        return PANet_MSDeformableLPT_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )