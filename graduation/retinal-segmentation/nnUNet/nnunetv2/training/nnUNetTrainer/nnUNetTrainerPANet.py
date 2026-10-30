from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer

try:
    from nnunetv2.architecture.pa_net import PANet
except ImportError:
    raise ImportError("无法导入 pa_net.py，请检查路径。")

from torch.optim import Adam
from torch.optim.lr_scheduler import CosineAnnealingLR
import torch


class nnUNetTrainerPANet(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device('cuda')):
        super().__init__(plans=plans, configuration=configuration, fold=fold,
                         dataset_json=dataset_json, device=device)
        # 训练轮数
        self.num_epochs = 100

    def initialize(self):
        if not self.was_initialized:
            # 1. 确定输入通道数
            if self.num_input_channels is None:
                if 'channel_names' in self.dataset_json:
                    self.num_input_channels = len(self.dataset_json['channel_names'].keys())
                elif 'modality' in self.dataset_json:
                    self.num_input_channels = len(self.dataset_json['modality'].keys())
                else:
                    self.num_input_channels = 1

            # 2. 补齐关键训练属性
            self.batch_size = self.configuration_manager.batch_size
            self.patch_size = self.configuration_manager.patch_size
            # 强制设置预处理线程数为 1，解决显存利用率过高导致的 illegal memory access
            self.num_processes_splitting = 1
            self.num_processes_validation = 1
            # 3. 【核心修复】使用 V2 正确的内部方法名初始化 Loss
            self.loss = self._build_loss()

            # 4. 架构参数修正
            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            target_stages = 5
            arch_kwargs['n_stages'] = target_stages
            if len(arch_kwargs['features_per_stage']) > target_stages:
                arch_kwargs['features_per_stage'] = arch_kwargs['features_per_stage'][:target_stages]

            print(f"！！！最终构建：n_stages={target_stages}, Loss={type(self.loss).__name__} ！！！")
            print("\n" + "=" * 50)
            print("CRITICAL: FORCING ARCHITECTURE REPLACEMENT TO PANet!")
            print("=" * 50 + "\n")
            # 5. 实例化并搬运到 GPU
            self.network = PANet(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            print(f"Current Network Type: {type(self.network)}")

            # 6. 初始化优化器并标记
            self.optimizer, self.lr_scheduler = self.configure_optimizers()
            self.was_initialized = True
    def build_network(self):
        """
        这个方法会被 super().initialize() 调用。
        虽然我们在 initialize 里又覆盖了一次，但在这里返回正确的类可以减少显存碎片。
        """
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        return PANet(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )

    def configure_optimizers(self):
        """
        定义优化器和学习率调度器
        """
        # 建议使用较低的学习率，Adam 初始 1e-4 比较稳妥
        optimizer = Adam(self.network.parameters(), lr=1e-4, weight_decay=self.weight_decay)
        scheduler = CosineAnnealingLR(optimizer, T_max=self.num_epochs)
        return optimizer, scheduler

    def on_train_start(self):
        super().on_train_start()
        # 同步深监督开关
        # if hasattr(self.network, 'deep_supervision'):
        #     self.network.deep_supervision = self.enable_deep_supervision

    def validation_step(self, batch: dict) -> dict:
        data = batch['data']
        target = batch['target']
        if isinstance(data, torch.Tensor):
            data = data.to(self.device, non_blocking=True)
        if isinstance(target, torch.Tensor):
            target = target.to(self.device, non_blocking=True)
        elif isinstance(target, list):
            target = [i.to(self.device, non_blocking=True) for i in target]

        # 1. 正常前向传播
        self.network.deep_supervision = True
        output = self.network(data)

        # 2. 核心修复：直接调用内部真正的 Loss 函数，避开 list 断言
        # 如果 self.loss 是 DeepSupervisionWrapper，它内部有一个 .loss 属性才是真正的计算逻辑
        if hasattr(self.loss, 'loss'):
            # 情况 A: 预测返回了 list (深监督开启)
            if isinstance(output, (list, tuple)):
                l = self.loss(output, target)
                output_seg = output[0]
            # 情况 B: 预测只返回了单 Tensor (比如 eval 模式)
            else:
                actual_target = target[0] if isinstance(target, (list, tuple)) else target
                # 直接用内部 loss 计算单图的损失
                l = self.loss.loss(output, actual_target)
                output_seg = output
        else:
            # 如果没有包装，按常规处理
            l = self.loss(output, target)
            output_seg = output[0] if isinstance(output, (list, tuple)) else output

        # 3. 后续指标计算 (保持不变，用于生成你图片中的 SE, SP, ACC 等)
        output_seg = output_seg.argmax(1, keepdim=True)
        target_seg = target[0] if isinstance(target, list) else target

        num_classes = self.label_manager.num_segmentation_heads + 1
        tp = torch.zeros(num_classes - 1).to(self.device)
        fp = torch.zeros(num_classes - 1).to(self.device)
        fn = torch.zeros(num_classes - 1).to(self.device)

        for i in range(1, num_classes):
            curr_output = (output_seg == i)
            curr_target = (target_seg == i)
            tp[i - 1] = torch.sum(curr_output & curr_target)
            fp[i - 1] = torch.sum(curr_output & (~curr_target))
            fn[i - 1] = torch.sum((~curr_output) & curr_target)

        return {
            'loss': l.detach().cpu().numpy(),
            'tp_hard': tp.detach().cpu().numpy(),
            'fp_hard': fp.detach().cpu().numpy(),
            'fn_hard': fn.detach().cpu().numpy(),
        }
    # 关键：重写推理时的网络调用逻辑
    def predict_sliding_window_return_logits(self, input_image, *args, **kwargs):
        # 验证推理时必须关闭深监督，否则 flip() 会报错
        self.network.deep_supervision = False
        ret = super().predict_sliding_window_return_logits(input_image, *args, **kwargs)
        # 恢复状态以供后续训练使用
        self.network.deep_supervision = self.enable_deep_supervision
        return ret

    @staticmethod
    def build_network_architecture(*args, **kwargs):
        """
        修正 UnboundLocalError，确保 arch_kwargs 始终被定义。
        """
        import torch
        # 1. 初始化变量，防止 UnboundLocalError
        arch_kwargs = None

        # 2. 尝试从传入参数中寻找配置
        all_values = list(args) + list(kwargs.values())
        for obj in all_values:
            if hasattr(obj, 'network_arch_init_kwargs'):
                # 必须做深度拷贝，防止修改原始配置影响其他流程
                import copy
                arch_kwargs = copy.deepcopy(obj.network_arch_init_kwargs)
                break

        # 3. 兜底逻辑：如果探测失败，使用手动预设
        if arch_kwargs is None:
            print("⚠️ 警告：无法自动获取配置，正在使用手动预设参数构建 PA-Net...")
            arch_kwargs = {
                'n_stages': 5,
                'features_per_stage': [32, 64, 128, 256, 512],
                'conv_op': 'torch.nn.modules.conv.Conv2d',
                'kernel_sizes': [[3, 3]] * 5,
                'strides': [[1, 1], [2, 2], [2, 2], [2, 2], [2, 2]],
                'n_conv_per_stage': [2] * 5,
                'n_conv_per_stage_decoder': [2] * 4,
                'conv_bias': True,
                'norm_op': 'torch.nn.modules.instancenorm.InstanceNorm2d',
                'norm_op_kwargs': {'eps': 1e-05, 'affine': True},
                'nonlin': 'torch.nn.LeakyReLU',
                'nonlin_kwargs': {'inplace': True}
            }
        else:
            # 如果探测成功，强制将层数改为训练时的 5 层
            arch_kwargs['n_stages'] = 5
            if 'features_per_stage' in arch_kwargs:
                arch_kwargs['features_per_stage'] = arch_kwargs['features_per_stage'][:5]

        # 4. 根据你上次运行的报错信息，强制对齐输入通道和类别
        # checkpoint 里是 [32, 1, 3, 3] 和 [2, 32, 1, 1]
        num_input_channels = 1
        num_classes = 2

        print(f"！！！最终参数对齐：构建 5 层 PANet，通道={num_input_channels}，类别={num_classes}！！！")

        return PANet(
            input_channels=num_input_channels,
            num_classes=num_classes,
            **arch_kwargs
        )