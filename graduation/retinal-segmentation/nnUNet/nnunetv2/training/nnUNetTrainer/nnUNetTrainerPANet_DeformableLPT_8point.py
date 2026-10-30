from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_DeformableLPT_NoAFFM
import torch


class nnUNetTrainerPANet_DeformableLPT_8point(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            # 1. 执行父类的标准初始化，确保 num_input_channels 等变量已就绪
            super().initialize()

            print("=" * 60)
            print("EXPERIMENT: Deformable LPT (8-Point) + No AFFM")
            print("Description: Replacing GAA with 8-point Deformable Attention [cite: 110]")
            print("=" * 60)

            # 2. 获取架构参数并显式开启深监督开关
            # 注意：nnU-Net 默认在训练中使用深监督来优化收敛
            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True

            # 3. 实例化 8 点采样版本的模型
            # 确保你的 pa_net.py 中 PANet_DeformableLPT_NoAFFM 的 LPT 模块已改为 8 点
            self.network = PANet_DeformableLPT_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            # 4. 重新挂载优化器，确保参数梯度正常更新
            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def build_network(self):
        """
        此函数在推理（Inference）或某些导出操作中会被 nnU-Net 调用。
        必须返回与训练时一致的架构。
        """
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        # 在推理时通常不需要深监督输出
        arch_kwargs['deep_supervision'] = False

        return PANet_DeformableLPT_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )