import torch
import torch.nn as nn
import torch.nn.functional as F
from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer
from nnunetv2.training.loss.dice import get_tp_fp_fn_tn
from nnunetv2.architecture.pa_net import PANet_MSDSConvLPT_CA_NoAFFM

# ================= 1. 直接在 Trainer 内部定义 clDice 算法 =================

# --- clDice 骨架提取核心算法：切记不可删除 ---

def soft_erode(img):
    if len(img.shape) == 4:
        p1 = -F.max_pool2d(-img, (3, 1), (1, 1), (1, 0))
        p2 = -F.max_pool2d(-p1, (1, 3), (1, 1), (0, 1))
        return p2
    elif len(img.shape) == 5:
        p1 = -F.max_pool3d(-img, (3, 1, 1), (1, 1, 1), (1, 0, 0))
        p2 = -F.max_pool3d(-p1, (1, 3, 1), (1, 1, 1), (0, 1, 0))
        p3 = -F.max_pool3d(-p2, (1, 1, 3), (1, 1, 1), (0, 0, 1))
        return p3
    return img

def soft_dilate(img):
    if len(img.shape) == 4:
        return F.max_pool2d(img, (3, 3), (1, 1), (1, 1))
    elif len(img.shape) == 5:
        return F.max_pool3d(img, (3, 3, 3), (1, 1, 1), (1, 1, 1))
    return img

def soft_open(img):
    return soft_dilate(soft_erode(img))

def soft_skel(img, iter_):
    img_mans = img
    for _ in range(iter_):
        img_erode = soft_erode(img)
        img_open = soft_open(img_erode)
        delta = F.relu(img_erode - img_open)
        img_mans = torch.max(img_mans, delta)
        img = img_erode
    return img_mans

# --- 之前报错的类，请确保缩进正确 ---

class SoftclDiceLoss(nn.Module):
    def __init__(self, iter_=3, smooth=1.):
        super(SoftclDiceLoss, self).__init__()
        self.iter = iter_
        self.smooth = smooth

    def forward(self, y_pred, y_true):
        # 强制转换类型解决 Short 报错
        y_true = y_true.float()
        y_pred = y_pred.float()

        if len(y_true.shape) != len(y_pred.shape):
            y_true = F.one_hot(y_true.squeeze(1).long(), y_pred.shape[1]).permute(0, 3, 1, 2).float()
            
        skel_true = soft_skel(y_true, self.iter)
        skel_pred = soft_skel(y_pred, self.iter)
        
        tprec = (torch.sum(skel_pred[:, 1:] * y_true[:, 1:]) + self.smooth) / (torch.sum(skel_pred[:, 1:]) + self.smooth)    
        tsens = (torch.sum(skel_true[:, 1:] * y_pred[:, 1:]) + self.smooth) / (torch.sum(skel_true[:, 1:]) + self.smooth)    
        
        return 1.0 - 2.0 * (tprec * tsens) / (tprec + tsens)
# ================= 2. 定义 Trainer 类 =================

class nnUNetTrainer_MSDSConv_clDice(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device('cuda')):
        super().__init__(plans=plans, configuration=configuration, fold=fold,
                         dataset_json=dataset_json, device=device)
        self.num_epochs = 100

    def _get_network_module(self):
        mod = self.network.module if self.is_ddp else self.network
        if hasattr(mod, "_orig_mod"):
            mod = mod._orig_mod
        return mod

    def initialize(self):
        if not self.was_initialized:
            super().initialize()
            # 核心稳定性配置
            self.grad_scaler = None 
            self.cl_loss_func = SoftclDiceLoss(iter_=3)

            print("=" * 60)
            print("SNAKE + clDice EXPERIMENT: FP32 MODE")
            print("Target: Topology Connectivity + Tubular Constraint")
            print("Status: AMP Disabled | Gradient Clipping (1.0) | clDice Weight (0.3)")
            print("=" * 60)

            arch_kwargs = self.configuration_manager.network_arch_init_kwargs
            arch_kwargs['deep_supervision'] = True 

            self.network = PANet_MSDSConvLPT_CA_NoAFFM(
                input_channels=self.num_input_channels,
                num_classes=self.label_manager.num_segmentation_heads,
                **arch_kwargs
            ).to(self.device)

            self.optimizer, self.lr_scheduler = self.configure_optimizers()

    def set_deep_supervision_enabled(self, enabled: bool):
        mod = self._get_network_module()
        if hasattr(mod, 'deep_supervision'):
            mod.deep_supervision = enabled

    def train_step(self, batch: dict) -> dict:
        x = batch['data'].to(self.device, non_blocking=True)
        y = [i.to(self.device, non_blocking=True) for i in batch['target']]

        self.optimizer.zero_grad()

        # 1. 前向传播
        output = self.network(x)
        
        # 2. 计算基础损失 (DC + CE)
        l_base = self.loss(output, y)
        
        # 3. 计算 clDice 损失 (仅针对最高分辨率输出)
        p0 = torch.sigmoid(output[0])
        t0 = y[0]
        l_cl = self.cl_loss_func(p0, t0)
        
        # 总损失权重：基础(1.0) + clDice(0.3)
        total_loss = l_base + 0.3 * l_cl
        
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)
        self.optimizer.step()

        return {'loss': total_loss.detach().cpu().numpy()}

    def validation_step(self, batch: dict) -> dict:
        data = batch['data'].to(self.device, non_blocking=True)
        target = batch['target']

        if isinstance(target, list):
            target = [i.to(self.device, non_blocking=True) for i in target]
        else:
            target = target.to(self.device, non_blocking=True)

        output = self.network(data)

        if hasattr(self.loss, 'loss') and not isinstance(output, (list, tuple)):
            actual_target = target[0] if isinstance(target, (list, tuple)) else target
            l = self.loss.loss(output, actual_target)
        else:
            l = self.loss(output, target)

        if self.enable_deep_supervision and isinstance(output, (list, tuple)):
            output = output[0]
            target = target[0]
        elif isinstance(target, (list, tuple)):
            target = target[0]

        axes = [0] + list(range(2, output.ndim))

        if self.label_manager.has_regions:
            predicted_segmentation_onehot = (torch.sigmoid(output) > 0.5).long()
        else:
            output_seg = output.argmax(1)[:, None]
            predicted_segmentation_onehot = torch.zeros(output.shape, device=output.device, dtype=torch.float32)
            predicted_segmentation_onehot.scatter_(1, output_seg, 1)
            del output_seg

        if self.label_manager.has_ignore_label:
            if not self.label_manager.has_regions:
                mask = (target != self.label_manager.ignore_label).float()
                target = target.clone()
                target[target == self.label_manager.ignore_label] = 0
            else:
                if target.dtype == torch.bool:
                    mask = ~target[:, -1:]
                else:
                    mask = 1 - target[:, -1:]
                target = target[:, :-1]
        else:
            mask = None

        tp, fp, fn, _ = get_tp_fp_fn_tn(predicted_segmentation_onehot, target, axes=axes, mask=mask)

        tp_hard = tp.detach().cpu().numpy()
        fp_hard = fp.detach().cpu().numpy()
        fn_hard = fn.detach().cpu().numpy()
        if not self.label_manager.has_regions:
            tp_hard = tp_hard[1:]
            fp_hard = fp_hard[1:]
            fn_hard = fn_hard[1:]

        return {'loss': l.detach().cpu().numpy(), 'tp_hard': tp_hard, 'fp_hard': fp_hard, 'fn_hard': fn_hard}

    def build_network(self):
        arch_kwargs = self.configuration_manager.network_arch_init_kwargs
        arch_kwargs['deep_supervision'] = False 
        return PANet_MSDSConvLPT_CA_NoAFFM(
            input_channels=self.num_input_channels,
            num_classes=self.label_manager.num_segmentation_heads,
            **arch_kwargs
        )
