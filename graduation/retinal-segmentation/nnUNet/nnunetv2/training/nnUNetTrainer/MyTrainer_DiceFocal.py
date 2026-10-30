# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from contextlib import contextmanager
from time import time
import sys
from batchgenerators.utilities.file_and_folder_operations import join
from typing import Union, List # <-- [修正] 添加了这行导入

# 1. 导入 nnU-Net 的基础训练器和相关工具
from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer
# 2. 导入 nnU-Net 的 Dice Loss 和 get_tp_fp_fn_tn 函数
from nnunetv2.training.loss.dice import MemoryEfficientSoftDiceLoss, get_tp_fp_fn_tn
# DO NOT import DeepSupervisionWrapper from nnunetv2 directly anymore
from nnunetv2.utilities.collate_outputs import collate_outputs

# --- [!] 从 torch._dynamo 导入 OptimizedModule (如果存在，用于类型检查) ---
try:
    from torch._dynamo import OptimizedModule
except ImportError:
    # 定义一个虚拟类，如果 torch.compile 不可用或版本不同
    class OptimizedModule: pass
# --- End Import ---


# -------------------------------------------------------------------------
# Modified DeepSupervisionWrapper (Unchanged)
# -------------------------------------------------------------------------
class ModifiedDeepSupervisionWrapper(nn.Module):
    def __init__(self, loss, weights):
        super(ModifiedDeepSupervisionWrapper, self).__init__()
        self.weights = weights
        self.loss = loss

    def forward(self, *args):
        total_loss_weighted_sum = 0
        for i, inputs in enumerate(zip(*args)):
            if self.weights[i] != 0.0:
                loss_output = self.loss(*inputs)
                current_level_total_loss = loss_output['loss']
                total_loss_weighted_sum += self.weights[i] * current_level_total_loss
        return total_loss_weighted_sum

# -------------------------------------------------------------------------
# FocalLossForSegmentation (Unchanged)
# -------------------------------------------------------------------------
class FocalLossForSegmentation(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, reduction='mean', ignore_index=None):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, logits, target):
        num_classes = logits.shape[1]
        probs = F.softmax(logits, dim=1)
        target_squeezed = target.squeeze(1).long()

        if self.ignore_index is not None:
            valid_mask = (target_squeezed != self.ignore_index)
        else:
            valid_mask = torch.ones_like(target_squeezed, dtype=torch.bool)

        target_squeezed_masked = torch.where(valid_mask, target_squeezed, 0)
        target_one_hot = F.one_hot(target_squeezed_masked, num_classes=num_classes)
        target_one_hot = target_one_hot.permute(0, target_one_hot.ndim - 1, *range(1, target_one_hot.ndim - 1)).float()

        pt = torch.sum(probs * target_one_hot, dim=1, keepdim=True)
        pt = torch.clamp(pt, 1e-9, 1.0 - 1e-9)
        focal_term = (1 - pt) ** self.gamma
        ce_term = -torch.log(pt)

        if self.alpha is not None:
            alpha_weight = torch.ones_like(target, device=logits.device) * (1 - self.alpha)
            alpha_weight = torch.where(target == 1, self.alpha, alpha_weight)
            loss = alpha_weight * focal_term * ce_term
        else:
            loss = focal_term * ce_term

        if self.ignore_index is not None:
            loss = loss * valid_mask.unsqueeze(1)
            num_valid_pixels = valid_mask.sum()
        else:
            num_valid_pixels = torch.numel(valid_mask)

        if self.reduction == 'mean':
            if num_valid_pixels > 0:
                loss = loss.sum() / num_valid_pixels
            else:
                loss = torch.tensor(0.0, device=logits.device, dtype=logits.dtype)
        elif self.reduction == 'sum':
            loss = loss.sum()
        return loss

# -------------------------------------------------------------------------
# Dice_and_Focal_loss (Returns dict, Unchanged)
# -------------------------------------------------------------------------
class Dice_and_Focal_loss(nn.Module):
    def __init__(self, dice_kwargs, focal_kwargs, weight_dice=1.0, weight_focal=1.0, use_ignore_label=False):
        super().__init__()
        self.weight_dice = weight_dice
        self.weight_focal = weight_focal
        self.use_ignore_label = use_ignore_label
        self.ignore_label_in_focal = focal_kwargs.get('ignore_index', None)
        self.dc = MemoryEfficientSoftDiceLoss(apply_nonlin=F.softmax, **dice_kwargs)
        self.focal = FocalLossForSegmentation(**focal_kwargs)

    def forward(self, net_output, target):
        dc_loss = torch.tensor(0.0, device=net_output.device, dtype=net_output.dtype)
        focal_loss = torch.tensor(0.0, device=net_output.device, dtype=net_output.dtype)

        if self.weight_dice > 0:
            if self.use_ignore_label:
                mask = (target != self.ignore_label_in_focal).float()
                target_dice = torch.where(target == self.ignore_label_in_focal, 0, target)
                dc_loss = self.dc(net_output, target_dice, loss_mask=mask)
            else:
                dc_loss = self.dc(net_output, target)

        if self.weight_focal > 0:
            focal_loss = self.focal(net_output, target)

        total_loss = self.weight_dice * dc_loss + self.weight_focal * focal_loss

        return {
            'loss': total_loss,
            'dice_loss': dc_loss,
            'focal_loss': focal_loss
        }

# -------------------------------------------------------------------------
# 定义你的自定义训练器 MyTrainer_DiceFocal
# -------------------------------------------------------------------------
class MyTrainer_DiceFocal(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device('cuda')):
        super().__init__(plans, configuration, fold, dataset_json, device)
        self.print_to_log_file("Using custom trainer MyTrainer_DiceFocal with Dice + Focal Loss.")
        self.logger.my_fantastic_logging['train_dice_losses'] = []
        self.logger.my_fantastic_logging['train_focal_losses'] = []
        self.logger.my_fantastic_logging['val_dice_losses'] = []
        self.logger.my_fantastic_logging['val_focal_losses'] = []
        self.logger.my_fantastic_logging['ema_val_dice_losses'] = []
        self.logger.my_fantastic_logging['ema_val_focal_losses'] = []
        self.logger.my_fantastic_logging['ema_combined_score'] = []
        self.print_to_log_file("Initialized logger for dice_loss, focal_loss components and their EMAs.")
        self.w_dice_for_best = 0.0
        self.w_focal_for_best = 1.0
        self.print_to_log_file(f"Model selection weights: w_dice={self.w_dice_for_best}, w_focal={self.w_focal_for_best}")
        self._best_ema = None
        self._best_combined_score = -np.inf
        self.current_ema_dice = None
        self.current_ema_focal_loss = None
        self.current_ema_combined_score = None
        self.ema_weight = 0.9
        # self.num_epochs = 150

    @contextmanager
    def dummy_context(self):
        yield None

    def _build_loss(self):
        # ... (loss building logic remains the same) ...
        dice_kwargs = {'batch_dice': self.configuration_manager.batch_dice,
                       'smooth': 1e-5, 'do_bg': False, 'ddp': self.is_ddp}
        focal_gamma = 2.0
        focal_alpha = 0.25
        ignore_label = self.label_manager.ignore_label
        focal_kwargs = {'alpha': focal_alpha, 'gamma': focal_gamma,
                        'ignore_index': ignore_label, 'reduction': 'mean'}
        weight_dice = 1.0
        weight_focal = 1.0

        combined_loss = Dice_and_Focal_loss(dice_kwargs=dice_kwargs, focal_kwargs=focal_kwargs,
                                            weight_dice=weight_dice, weight_focal=weight_focal,
                                            use_ignore_label=(ignore_label is not None))

        if self.enable_deep_supervision:
            deep_supervision_scales = self._get_deep_supervision_scales()
            weights = np.array([1 / (2 ** i) for i in range(len(deep_supervision_scales))])
            if self.is_ddp and not self._do_i_compile():
                 weights[-1] = 1e-6
            else:
                 weights[-1] = 0
            weights = weights / weights.sum()
            loss = ModifiedDeepSupervisionWrapper(combined_loss, weights)
            self.print_to_log_file(f"Using Deep Supervision with loss weights: {weights}")
        else:
            loss = combined_loss
            self.print_to_log_file("Deep Supervision is disabled.")

        self.print_to_log_file(f"Instantiated Dice+Focal Loss: weight_dice={weight_dice}, weight_focal={weight_focal}, focal_gamma={focal_gamma}, focal_alpha={focal_alpha}, ignore_label={ignore_label}")
        return loss


    def train_step(self, batch: dict) -> dict:
        # ... (train_step logic remains the same) ...
        data = batch['data']
        target = batch['target']

        data = data.to(self.device, non_blocking=True)
        if isinstance(target, list):
            target_list = [i.to(self.device, non_blocking=True) for i in target]
        else:
            target_list = target.to(self.device, non_blocking=True) # Should be tensor, but keep logic

        self.optimizer.zero_grad(set_to_none=True)
        context = torch.autocast(self.device.type, enabled=True) if self.device.type == 'cuda' else self.dummy_context()
        with context:
            output = self.network(data)
            l = self.loss(output, target_list) # self.loss handles list target if DS is on

        if self.grad_scaler is not None:
            self.grad_scaler.scale(l).backward()
            self.grad_scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), 12)
            self.grad_scaler.step(self.optimizer)
            self.grad_scaler.update()
        else:
            l.backward()
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), 12)
            self.optimizer.step()

        underlying_loss_fn = self.loss.loss if isinstance(self.loss, ModifiedDeepSupervisionWrapper) else self.loss
        output_for_logging = output[0] if isinstance(output, (list, tuple)) else output
        target_for_logging = target_list[0] if isinstance(target_list, list) else target_list

        with torch.no_grad():
             loss_components_dict = underlying_loss_fn(output_for_logging, target_for_logging)
             dice_loss_component = loss_components_dict['dice_loss']
             focal_loss_component = loss_components_dict['focal_loss']

        return {
            'loss': l.detach().cpu().numpy(),
            'dice_loss': dice_loss_component.detach().cpu().numpy(),
            'focal_loss': focal_loss_component.detach().cpu().numpy()
        }

    def validation_step(self, batch: dict) -> dict:
        # ... (validation_step logic remains the same, using target_tensor) ...
        data = batch['data']
        target = batch['target'] # Target might be a list from dataloader

        data = data.to(self.device, non_blocking=True)
        if isinstance(target, list):
            target_tensor = target[0].to(self.device, non_blocking=True)
        else:
            target_tensor = target.to(self.device, non_blocking=True)

        context = torch.autocast(self.device.type, enabled=True) if self.device.type == 'cuda' else self.dummy_context()
        original_mode = self.network.training
        self.network.eval()
        with context:
            with torch.no_grad():
                output = self.network(data)
                underlying_loss_fn = self.loss.loss if isinstance(self.loss, ModifiedDeepSupervisionWrapper) else self.loss
                output_for_loss = output[0] if isinstance(output, (list, tuple)) else output
                target_for_loss = target_tensor

                loss_components_dict = underlying_loss_fn(output_for_loss, target_for_loss)
                l = loss_components_dict['loss']
                dice_loss_component = loss_components_dict['dice_loss']
                focal_loss_component = loss_components_dict['focal_loss']
            del data
        self.network.train(original_mode)

        output_for_dice = output[0] if isinstance(output, (list, tuple)) else output
        target_for_dice = target_tensor
        axes = [0] + list(range(2, output_for_dice.ndim))

        if self.label_manager.has_regions:
             predicted_segmentation_onehot = (torch.sigmoid(output_for_dice) > 0.5).long()
        else:
             output_seg = output_for_dice.argmax(1)[:, None]
             predicted_segmentation_onehot = torch.zeros(output_for_dice.shape, device=output_for_dice.device, dtype=torch.float32)
             predicted_segmentation_onehot.scatter_(1, output_seg, 1)
             del output_seg

        mask = None
        target_for_dice_calc = target_for_dice
        if self.label_manager.has_ignore_label:
             if not self.label_manager.has_regions:
                  mask = (target_tensor != self.label_manager.ignore_label).float()
                  target_for_dice_calc = torch.where(target_tensor == self.label_manager.ignore_label, 0, target_tensor)
             else:
                  if target_tensor.dtype == torch.bool:
                       mask = ~target_tensor[:, -1:]
                  else:
                       mask = 1 - target_tensor[:, -1:]
                  target_for_dice_calc = target_tensor[:, :-1]

        tp, fp, fn, _ = get_tp_fp_fn_tn(predicted_segmentation_onehot, target_for_dice_calc, axes=axes, mask=mask)
        tp_hard = tp.detach().cpu().numpy()
        fp_hard = fp.detach().cpu().numpy()
        fn_hard = fn.detach().cpu().numpy()
        if not self.label_manager.has_regions:
             if len(tp_hard) > 1:
                  tp_hard = tp_hard[1:]
                  fp_hard = fp_hard[1:]
                  fn_hard = fn_hard[1:]

        return {
            'loss': l.detach().cpu().numpy(),
            'dice_loss': dice_loss_component.detach().cpu().numpy(),
            'focal_loss': focal_loss_component.detach().cpu().numpy(),
            'tp_hard': tp_hard,
            'fp_hard': fp_hard,
            'fn_hard': fn_hard
        }

    # on_train_epoch_end logging (unchanged)
    def on_train_epoch_end(self, train_outputs: list):
        # ... (logic remains the same) ...
        outputs = collate_outputs(train_outputs)
        loss_here = np.mean(outputs['loss'])
        dice_loss_here = np.mean(outputs['dice_loss'])
        focal_loss_here = np.mean(outputs['focal_loss'])

        if self.is_ddp:
            losses_tr = [None for _ in range(torch.distributed.get_world_size())]
            torch.distributed.all_gather_object(losses_tr, loss_here)
            loss_here = np.mean(losses_tr)
            dice_losses_tr = [None for _ in range(torch.distributed.get_world_size())]
            torch.distributed.all_gather_object(dice_losses_tr, dice_loss_here)
            dice_loss_here = np.mean(dice_losses_tr)
            focal_losses_tr = [None for _ in range(torch.distributed.get_world_size())]
            torch.distributed.all_gather_object(focal_losses_tr, focal_loss_here)
            focal_loss_here = np.mean(focal_losses_tr)

        self.logger.log('train_losses', loss_here, self.current_epoch)
        self.logger.log('train_dice_losses', dice_loss_here, self.current_epoch)
        self.logger.log('train_focal_losses', focal_loss_here, self.current_epoch)


    # on_validation_epoch_end logging (unchanged)
    def on_validation_epoch_end(self, val_outputs: list):
        # ... (logic remains the same) ...
        outputs_collated = collate_outputs(val_outputs)
        tp = np.sum(outputs_collated['tp_hard'], 0)
        fp = np.sum(outputs_collated['fp_hard'], 0)
        fn = np.sum(outputs_collated['fn_hard'], 0)

        loss_here = np.mean(outputs_collated['loss'])
        dice_loss_here = np.mean(outputs_collated['dice_loss'])
        focal_loss_here = np.mean(outputs_collated['focal_loss'])

        if self.is_ddp:
            # ... (DDP aggregation logic remains the same) ...
            world_size = torch.distributed.get_world_size()
            tps = [None for _ in range(world_size)]
            torch.distributed.all_gather_object(tps, tp)
            tp = np.vstack([i[None] for i in tps]).sum(0)
            fps = [None for _ in range(world_size)]
            torch.distributed.all_gather_object(fps, fp)
            fp = np.vstack([i[None] for i in fps]).sum(0)
            fns = [None for _ in range(world_size)]
            torch.distributed.all_gather_object(fns, fn)
            fn = np.vstack([i[None] for i in fns]).sum(0)

            losses_val = [None for _ in range(world_size)]
            torch.distributed.all_gather_object(losses_val, loss_here)
            loss_here = np.mean(losses_val)
            dice_losses_val = [None for _ in range(world_size)]
            torch.distributed.all_gather_object(dice_losses_val, dice_loss_here)
            dice_loss_here = np.mean(dice_losses_val)
            focal_losses_val = [None for _ in range(world_size)]
            torch.distributed.all_gather_object(focal_losses_val, focal_loss_here)
            focal_loss_here = np.mean(focal_losses_val)


        global_dc_per_class = [i for i in [2 * i / (2 * i + j + k + 1e-8) for i, j, k in zip(tp, fp, fn)]]
        mean_fg_dice = np.nanmean(global_dc_per_class) if len(global_dc_per_class) > 0 else 0.0

        self.logger.log('mean_fg_dice', mean_fg_dice, self.current_epoch)
        self.logger.log('dice_per_class_or_region', global_dc_per_class, self.current_epoch)
        self.logger.log('val_losses', loss_here, self.current_epoch)
        self.logger.log('val_dice_losses', dice_loss_here, self.current_epoch)
        self.logger.log('val_focal_losses', focal_loss_here, self.current_epoch)

    # on_epoch_end (unchanged, includes EMA and combined score logic)
    def on_epoch_end(self):
        # ... (logic remains the same as previous combined score version) ...
        self.logger.log('epoch_end_timestamps', time(), self.current_epoch)

        current_dice = self.logger.my_fantastic_logging.get('mean_fg_dice', [np.nan])[-1]
        current_focal_loss = self.logger.my_fantastic_logging.get('val_focal_losses', [np.nan])[-1]

        if self.current_ema_dice is None:
            self.current_ema_dice = current_dice if not np.isnan(current_dice) else -np.inf
        elif not np.isnan(current_dice):
            self.current_ema_dice = self.current_ema_dice * self.ema_weight + (1 - self.ema_weight) * current_dice

        if self.current_ema_focal_loss is None:
            self.current_ema_focal_loss = current_focal_loss if not np.isnan(current_focal_loss) else np.inf
        elif not np.isnan(current_focal_loss):
            self.current_ema_focal_loss = self.current_ema_focal_loss * self.ema_weight + (1 - self.ema_weight) * current_focal_loss

        if self.current_ema_dice is not None and self.current_ema_focal_loss is not None and \
           not np.isinf(self.current_ema_dice) and not np.isinf(self.current_ema_focal_loss):
            self.current_ema_combined_score = self.w_dice_for_best * self.current_ema_dice - self.w_focal_for_best * self.current_ema_focal_loss
        else:
            self.current_ema_combined_score = -np.inf

        self.logger.log('ema_fg_dice', self.current_ema_dice, self.current_epoch)
        self.logger.log('ema_val_focal_losses', self.current_ema_focal_loss, self.current_epoch)
        self.logger.log('ema_combined_score', self.current_ema_combined_score, self.current_epoch)

        train_loss_total = self.logger.my_fantastic_logging.get('train_losses', [np.nan])[-1]
        train_loss_dice = self.logger.my_fantastic_logging.get('train_dice_losses', [np.nan])[-1]
        train_loss_focal = self.logger.my_fantastic_logging.get('train_focal_losses', [np.nan])[-1]
        val_loss_total = self.logger.my_fantastic_logging.get('val_losses', [np.nan])[-1]
        val_loss_dice = self.logger.my_fantastic_logging.get('val_dice_losses', [np.nan])[-1]
        val_loss_focal = self.logger.my_fantastic_logging.get('val_focal_losses', [np.nan])[-1]
        pseudo_dice = self.logger.my_fantastic_logging.get('dice_per_class_or_region', [[np.nan]])[-1]
        epoch_start_time = self.logger.my_fantastic_logging.get('epoch_start_timestamps', [0])[-1]
        epoch_end_time = self.logger.my_fantastic_logging.get('epoch_end_timestamps', [0])[-1]
        epoch_time = epoch_end_time - epoch_start_time if epoch_end_time > epoch_start_time else np.nan

        self.print_to_log_file(f'train_loss_total {np.round(train_loss_total, decimals=4)}')
        self.print_to_log_file(f'train_loss_dice {np.round(train_loss_dice, decimals=4)}')
        self.print_to_log_file(f'train_loss_focal {np.round(train_loss_focal, decimals=4)}')
        self.print_to_log_file(f'val_loss_total {np.round(val_loss_total, decimals=4)}')
        self.print_to_log_file(f'val_loss_dice {np.round(val_loss_dice, decimals=4)}')
        self.print_to_log_file(f'val_loss_focal {np.round(val_loss_focal, decimals=4)}')
        if isinstance(pseudo_dice, list) and len(pseudo_dice) > 0:
             if not np.isnan(pseudo_dice).any():
                 self.print_to_log_file(f'Pseudo dice {np.round(pseudo_dice, decimals=4)}')
             else:
                 self.print_to_log_file(f'Pseudo dice [nan]')
        else:
             self.print_to_log_file(f'Pseudo dice [nan]')
        self.print_to_log_file(f'EMA Dice: {np.round(self.current_ema_dice, decimals=4) if self.current_ema_dice is not None else "N/A"}')
        self.print_to_log_file(f'EMA Focal Loss: {np.round(self.current_ema_focal_loss, decimals=4) if self.current_ema_focal_loss is not None else "N/A"}')
        self.print_to_log_file(f'EMA Combined Score: {np.round(self.current_ema_combined_score, decimals=4) if self.current_ema_combined_score is not None else "N/A"}')
        self.print_to_log_file(f"Epoch time: {np.round(epoch_time, decimals=2)} s")

        current_epoch = self.current_epoch
        if (current_epoch + 1) % self.save_every == 0 and current_epoch != (self.num_epochs - 1):
            self.save_checkpoint(join(self.output_folder, 'checkpoint_latest.pth'))

        if self.current_ema_combined_score is not None and not np.isinf(self.current_ema_combined_score) and \
           (self._best_combined_score is None or self.current_ema_combined_score > self._best_combined_score):
            self._best_combined_score = self.current_ema_combined_score
            self._best_ema = self.current_ema_dice
            self.print_to_log_file(f"Yayy! New best EMA Combined Score: {np.round(self._best_combined_score, decimals=4)} (EMA Dice: {np.round(self._best_ema, decimals=4)})")
            self.save_checkpoint(join(self.output_folder, 'checkpoint_best.pth'))

        if self.local_rank == 0:
            self.logger.plot_progress_png(self.output_folder)

        self.current_epoch += 1

    # save_checkpoint (unchanged, includes combined score)
    def save_checkpoint(self, filename: str) -> None:
        if self.local_rank == 0:
            if not self.disable_checkpointing:
                if self.is_ddp:
                    mod = self.network.module
                else:
                    mod = self.network
                # Check if the module is an instance of OptimizedModule without relying on the specific import path
                if 'OptimizedModule' in str(type(mod)):
                     try:
                          mod = mod._orig_mod
                     except AttributeError:
                          pass # Fallback if attribute name changes

                checkpoint = {
                    'network_weights': mod.state_dict(),
                    'optimizer_state': self.optimizer.state_dict(),
                    'grad_scaler_state': self.grad_scaler.state_dict() if self.grad_scaler is not None else None,
                    'logging': self.logger.get_checkpoint(),
                    '_best_ema': self._best_ema,
                    '_best_combined_score': self._best_combined_score,
                    'current_epoch': self.current_epoch + 1,
                    'init_args': self.my_init_kwargs,
                    'trainer_name': self.__class__.__name__,
                    'inference_allowed_mirroring_axes': self.inference_allowed_mirroring_axes,
                    'current_ema_dice': self.current_ema_dice,
                    'current_ema_focal_loss': self.current_ema_focal_loss,
                    'current_ema_combined_score': self.current_ema_combined_score
                }
                torch.save(checkpoint, filename)
            else:
                self.print_to_log_file('No checkpoint written, checkpointing is disabled')

    # load_checkpoint (unchanged, includes combined score)
    def load_checkpoint(self, filename_or_checkpoint: Union[dict, str]) -> None:
        # ... (logic remains the same as previous combined score version) ...
        if not self.was_initialized:
            self.initialize()

        if isinstance(filename_or_checkpoint, str):
            checkpoint = torch.load(filename_or_checkpoint, map_location=self.device, weights_only=False)
        else:
            checkpoint = filename_or_checkpoint

        new_state_dict = {}
        for k, value in checkpoint['network_weights'].items():
            key = k
            if key not in self.network.state_dict().keys() and key.startswith('module.'):
                key = key[7:]
            new_state_dict[key] = value

        self.my_init_kwargs = checkpoint['init_args']
        self.current_epoch = checkpoint['current_epoch']
        self.logger.load_checkpoint(checkpoint['logging'])
        self._best_ema = checkpoint.get('_best_ema', None)
        self._best_combined_score = checkpoint.get('_best_combined_score', -np.inf)
        self.current_ema_dice = checkpoint.get('current_ema_dice', None)
        self.current_ema_focal_loss = checkpoint.get('current_ema_focal_loss', None)
        self.current_ema_combined_score = checkpoint.get('current_ema_combined_score', None)
        self.inference_allowed_mirroring_axes = checkpoint.get(
            'inference_allowed_mirroring_axes', self.inference_allowed_mirroring_axes)

        if self.is_ddp:
             net_to_load = self.network.module
        else:
             net_to_load = self.network

        # Check type without direct import dependency
        if 'OptimizedModule' in str(type(net_to_load)):
             try:
                  net_to_load._orig_mod.load_state_dict(new_state_dict)
             except AttributeError:
                  net_to_load.load_state_dict(new_state_dict)
        else:
             net_to_load.load_state_dict(new_state_dict)

        self.optimizer.load_state_dict(checkpoint['optimizer_state'])
        if self.grad_scaler is not None:
            if checkpoint['grad_scaler_state'] is not None:
                self.grad_scaler.load_state_dict(checkpoint['grad_scaler_state'])
        self.print_to_log_file(f"Loaded checkpoint from epoch {self.current_epoch}. Best combined score was {self._best_combined_score:.4f}.")


    # Other methods...