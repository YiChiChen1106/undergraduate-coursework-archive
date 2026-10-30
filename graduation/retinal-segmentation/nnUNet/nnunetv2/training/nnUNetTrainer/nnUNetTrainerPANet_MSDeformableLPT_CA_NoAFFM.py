from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_MSDeformableLPT_CA_NoAFFM
import torch
from torch.cuda.amp import autocast  # 确保导入正确


class nnUNetTrainerPANet_MSDeformableLPT_CA_NoAFFM(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            super().initialize()

            # --- 核心改动：物理禁用 AMP ---
            # 设置为 None 后，nnU-Net 内部逻辑会意识到不使用混合精度
            self.grad_scaler = None

            print("=" * 60)
            print("EXPERIMENT: MS-LPT + CA (FP32 MODE)")
            print("Status: AMP Disabled to prevent CUDA Illegal Instruction")
            print("=" * 60)

            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True

            self.network = PANet_MSDeformableLPT_CA_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def train_step(self, batch: dict) -> dict:
        """
        全精度兼容的训练步，包含梯度裁剪
        """
        x = batch['data']
        y = batch['target']

        x = x.to(self.device, non_blocking=True)
        y = [i.to(self.device, non_blocking=True) for i in y]

        self.optimizer.zero_grad()

        # 如果 grad_scaler 为 None，直接走 FP32 逻辑
        if self.grad_scaler is None:
            # 1. 直接前向传播（不使用 autocast）
            output = self.network(x)
            l = self.loss(output, y)

            # 2. 直接反向传播
            l.backward()

            # 3. 梯度裁剪（防御梯度爆炸）
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)

            # 4. 更新
            self.optimizer.step()
        else:
            # 备用：万一以后想开 AMP，保留这部分逻辑
            with autocast(enabled=True):
                output = self.network(x)
                l = self.loss(output, y)
            self.grad_scaler.scale(l).backward()
            self.grad_scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)
            self.grad_scaler.step(self.optimizer)
            self.grad_scaler.update()

        return {'loss': l.detach().cpu().numpy()}

    def build_network(self):
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        arch_kwargs['deep_supervision'] = False
        return PANet_MSDeformableLPT_CA_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )