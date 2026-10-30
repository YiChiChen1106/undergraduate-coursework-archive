from nnunetv2.training.nnUNetTrainer.nnUNetTrainerPANet import nnUNetTrainerPANet
from nnunetv2.training.loss.dice import get_tp_fp_fn_tn
import torch
import torch.nn as nn
from torch.cuda.amp import autocast
import numpy as np


class nnUNetTrainerPANet_AFFM_NoDS(nnUNetTrainerPANet):
    @staticmethod
    def build_network_architecture(*args, **kwargs):
        """
        万能参数版本：完美解决不同版本 nnU-Net 签名不一致导致的 TypeError。
        直接转发所有参数给父类，不再纠结具体的参数位置。
        """
        # 1. 强制在参数中关闭深监督（如果有的话）
        kwargs['enable_deep_supervision'] = False

        # 2. 调用父类构建原始架构
        network = nnUNetTrainerPANet.build_network_architecture(*args, **kwargs)

        # 3. 核心消融手术：将 LPT 替换为 Identity
        if hasattr(network, 'lpt'):
            print("=" * 50)
            print("INFERENCE DEBUG: Overriding architecture, replacing LPT with Identity")
            network.lpt = nn.Identity()

        if hasattr(network, 'deep_supervision'):
            network.deep_supervision = False

        print("=" * 50)
        return network

    def initialize(self):
        # 这里的 initialize 是训练开始时调用的
        self.enable_deep_supervision = False
        super().initialize()
        if hasattr(self.network, 'lpt'):
            self.network.lpt = nn.Identity()
        if hasattr(self.network, 'deep_supervision'):
            self.network.deep_supervision = False
        self.network.to(self.device)
        self.optimizer, self.lr_scheduler = self.configure_optimizers()

    # ... train_step 和 validation_step 保持你之前的代码不变 ...
    def train_step(self, batch: dict) -> dict:
        data = batch['data'].to(self.device, non_blocking=True)
        target = batch['target']
        if isinstance(target, list):
            target = [i.to(self.device, non_blocking=True) for i in target]
        else:
            target = target.to(self.device, non_blocking=True)
        self.optimizer.zero_grad(set_to_none=True)
        with autocast(enabled=True):
            output = self.network(data)
            if isinstance(output, (list, tuple)): output = output[0]
            if isinstance(target, (list, tuple)): target = target[0]
            l = self.loss(output, target)
        l.backward()
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), 12)
        self.optimizer.step()
        return {'loss': l.detach().cpu().numpy()}

    def validation_step(self, batch: dict) -> dict:
        data = batch['data'].to(self.device, non_blocking=True)
        target = batch['target']
        if isinstance(target, list): target = target[0]
        target = target.to(self.device, non_blocking=True)
        with autocast(enabled=True):
            output = self.network(data)
            if isinstance(output, (list, tuple)): output = output[0]
            l = self.loss(output, target)
        output = output.float()
        output_softmax = torch.softmax(output, 1)
        if target.ndim < output.ndim:
            target_onehot = torch.zeros_like(output)
            target_onehot.scatter_(1, target.unsqueeze(1).long(), 1)
        else:
            target_onehot = target
        axes = tuple(range(2, output.ndim))
        tp, fp, fn, _ = get_tp_fp_fn_tn(output_softmax, target_onehot, axes=axes, mask=None, square=False)
        return {
            'loss': l.detach().cpu().numpy(),
            'tp_hard': tp.detach().cpu().numpy(),
            'fp_hard': fp.detach().cpu().numpy(),
            'fn_hard': fn.detach().cpu().numpy(),
        }

    def on_train_start(self):
        super().on_train_start()
        if hasattr(self.network, 'deep_supervision'):
            self.network.deep_supervision = False