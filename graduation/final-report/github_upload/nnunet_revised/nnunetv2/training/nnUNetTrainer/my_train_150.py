import torch  # <-- [!] 修正：添加这一行来导入 torch 库

# 1. 导入 nnUNetTrainer (而不是 nnUNetTrainerV2)
from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer

# 2. 你的类继承自 nnUNetTrainer
class my_train_150(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device('cuda')):

        # 运行 nnUNetTrainer 的初始化
        super().__init__(plans, configuration, fold, dataset_json, device)

        # 覆盖 epoch 数量
        self.num_epochs = 150

        # (注意：这个基础 nnUNetTrainer 默认没有“早停”逻辑，
        # 它会严格运行 150 个 epoch。)