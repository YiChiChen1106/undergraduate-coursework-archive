# nnU-Net revised for retinal vessel segmentation

This repository contains the project code used for the final year project:

**Research on Fine Retinal Vessel Segmentation Based on nnU-Net**

The code is based on nnU-Net v2 and adds retinal-vessel-oriented model variants for the experiments in the report. The main custom implementation files are:

- `nnunetv2/architecture/pa_net.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainer_Baseline100.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_LPT.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_AFFM.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_AFFM_NoDS.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_DeformableLPT_NoAFFM.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_DeformableLPT_8point.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_DeformableLPT_Modulated_4pt.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_MSDeformableLPT_NoAFFM.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_MSDeformableLPT_CA_NoAFFM.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainerPANet_MSDSConvLPT_CA_NoAFFM.py`
- `nnunetv2/training/nnUNetTrainer/nnUNetTrainer_MSDSConv_clDice.py`

Datasets, trained checkpoints, prediction outputs, and experiment result folders are intentionally not included in this repository.
