from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_LPTOnly
import torch


class nnUNetTrainerPANet_LPT(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            # 1. 执行父类的标准初始化（确定通道、Loss 等）
            super().initialize()

            print("=" * 50)
            print("ABLATION STUDY A: Forcing PANet_LPTOnly (LPT active, AFFM removed)")
            print("=" * 50)

            # 2. 强制替换网络为消融版本
            # 获取父类初始化时计算好的架构参数
            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['n_stages'] = 5  # 保持 5 层一致性 [cite: 196]
            if len(arch_kwargs['features_per_stage']) > 5:
                arch_kwargs['features_per_stage'] = arch_kwargs['features_per_stage'][:5]

            # 3. 实例化消融模型
            self.network = PANet_LPTOnly(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            # 4. 重新挂载优化器，确保参数对应
            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def build_network(self):
        # 这里的返回值供推理和某些内部初始化使用
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        return PANet_LPTOnly(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )