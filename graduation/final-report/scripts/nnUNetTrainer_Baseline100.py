import torch

from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer


class nnUNetTrainer_Baseline100(nnUNetTrainer):
    """
    Baseline trainer for the later main experiments.

    This trainer keeps the default nnU-Net training pipeline unchanged and only
    overrides the number of epochs to 100 so that it matches the later
    experimental protocol described in the thesis.

    Note:
    - Five-fold cross-validation is not implemented inside the trainer.
    - It is controlled by running this trainer separately for fold 0~4.
    """

    def __init__(
        self,
        plans: dict,
        configuration: str,
        fold: int,
        dataset_json: dict,
        device: torch.device = torch.device("cuda"),
    ):
        super().__init__(plans, configuration, fold, dataset_json, device)
        self.num_epochs = 100
