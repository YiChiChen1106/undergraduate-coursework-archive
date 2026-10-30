from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.architecture.pa_net import PANet_MSDSConvLPT_CA_NoAFFM
import torch
from torch.cuda.amp import autocast

class nnUNetTrainerPANet_MSDSConvLPT_CA_NoAFFM(nnUNetTrainerPANet):
    def initialize(self):
        if not self.was_initialized:
            super().initialize()
            
            # --- 核心稳定性配置 ---
            # 禁用 AMP (混合精度) 以防止 DSConv 累积偏移导致的数值溢出
            self.grad_scaler = None 

            print("=" * 60)
            print("SNAKE EXPERIMENT: Multi-Scale MSDSConv + CA (FP32 MODE)")
            print("Target: Break F1-Score 0.80 via Tubular Topology Constraint")
            print("Status: AMP Disabled | Gradient Clipping Active (1.0)")
            print("=" * 60)

            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True 

            # 实例化带蛇形采样与坐标注意力的模型
            self.network = PANet_MSDSConvLPT_CA_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def train_step(self, batch: dict) -> dict:
        """
        针对蛇形卷积优化的全精度训练步
        """
        x = batch['data']
        y = batch['target']

        x = x.to(self.device, non_blocking=True)
        y = [i.to(self.device, non_blocking=True) for i in y]

        self.optimizer.zero_grad()

        # 强制走 FP32 逻辑，确保 cumsum 偏移量的精确度
        output = self.network(x)
        l = self.loss(output, y)
        l.backward()
        
        # 梯度裁剪：防止蛇形轨迹在初期训练时剧烈波动
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)
        
        self.optimizer.step()

        return {'loss': l.detach().cpu().numpy()}

    def build_network(self):
        """ 推理阶段架构构建 """
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        arch_kwargs['deep_supervision'] = False 
        return PANet_MSDSConvLPT_CA_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )