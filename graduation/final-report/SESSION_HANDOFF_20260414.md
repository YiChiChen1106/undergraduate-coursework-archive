# Final Report Session Handoff (2026-04-14)

## Purpose

This file is the latest handoff summary for continuing the final report writing in a new session without losing context.

Project topic:

- Improving retinal vessel segmentation based on `nnU-Net`

Primary workspaces:

- Code: `F:\shiwangmo`
- Report folder: `F:\Final_report`


## Main Report Files

Current working files:

- English report: `F:\Final_report\reports_with_21.tex`
- Chinese checking draft: `F:\Final_report\reports_with_21_cn.tex`

Supporting files:

- `F:\Final_report\reports.tex`
- `F:\Final_report\reports.pdf`
- `F:\Final_report\pic\`


## Writing Principles

- Final output is in English.
- Chinese text is a checking layer for meaning and structure alignment.
- Overall structure follows the school final report format, not a full IEEE two-column paper.
- Citation style is IEEE-like numbered citation.
- Chapter 2 is for methods, setup, and concise local observations that motivate the next step.
- Chapter 3 is for concentrated comparative analysis and discussion.


## Current Report Status

### Chinese draft status

The following Chapter 2 sections are already written in Chinese:

- `2.1 实验协议与基本设置`
- `2.2 基线与前期探索`
- `2.3 PA-Net 模块迁移`
- `2.4 LPT 与 AFFM 的消融`
- `2.5 AFFM 与深监督的兼容性验证`
- `2.6 LPT 中的可变形注意力`
- `2.7 Modulated 与多尺度可变形 LPT`
- `2.8 MS-Modulated 与 Coordinate Attention`
- `2.9 MS-DSConv 与 CA`
- `2.10 小连通域后处理`
- `2.11 clDice 损失探索`
- `2.12 本章小结`

Chinese Chapter 3 framework has also been inserted:

- `3 结果分析与讨论`
- `3.1 整体结果对比`
- `3.2 关键指标权衡分析`
- `3.3 结构演化路径分析`
- `3.4 后处理与 clDice 的补充分析`

### English draft status

The following Chapter 2 sections are already written in English:

- `2.1 Experimental protocol and basic settings`
- `2.2 Baseline and early explorations`
- `2.3 PA-Net module migration`
- `2.4 Ablation of LPT and AFFM`
- `2.5 Compatibility check between AFFM and deep supervision`
- `2.6 Deformable attention in LPT`
- `2.7 Modulated and multi-scale deformable LPT`
- `2.8 MS-Modulated and Coordinate Attention`
- `2.9 MS-DSConv and CA`
- `2.10 Small connected-component post-processing`
- `2.11 Exploration of clDice loss`
- `2.12 Chapter Summary`

Important:

- English Chapter 3 has **not** been rewritten yet.
- The English file still contains the original template `Discussion` section after Chapter 2.
- The next major writing task is to replace English Chapter 3 with the Chinese Chapter 3 framework and then fill it section by section.


## Key Structural Decisions Already Confirmed

### Early stage

- `Exp1` to `Exp3` are early exploratory experiments.
- They kept the original split to stay comparable with the senior student's setup.
- Metrics used in this stage:
  - `IoU(vessel)`
  - `mIoU`
  - `Recall`
  - `Precision`
  - `Accuracy`
  - `mPA`
  - `F1-score`

### Later main stage

- From `Exp4` onward, experiments use the unified later-stage pipeline on `DRIVE`.
- Metrics used in this stage:
  - `SE`
  - `SP`
  - `ACC`
  - `AUC`
  - `PR`
  - `F1-score`

### Important writing decisions

- Do **not** present the incorrect original PA-Net run as a formal valid PA-Net result.
- Do **not** say AFFM was abandoned before the deformable + AFFM comparison stage.
- The decision to stop using AFFM was written only **after** the `Deformable LPT + AFFM` comparison.
- `CoordAtt` belongs to the later `MS-Modulated + CA` stage, not the earlier `MS-Modulated` stage.
- `Dynamic Snake Convolution` is used in the **bottleneck LPT multi-scale sampling branch**, not as a full-network convolution replacement.


## Confirmed Experiment Chain and Representative Results

### Early exploratory stage

- `Exp1`: nnU-Net baseline, `F1 = 0.7924`
- `Exp2`: CLAHE + nnU-Net, `F1 = 0.7827`
- `Exp3`: CLAHE + nnU-Net + Focal Loss, `F1 = 0.7802`

### Later main-stage structure line

- nnU-Net v2 baseline:
  - `SE = 0.7627`
  - `SP = 0.9852`
  - `ACC = 0.9659`
  - `AUC = 0.8739`
  - `PR = 0.8238`
  - `F1 = 0.7891`

- PA-Net full migration:
  - `F1 = 0.7782`

- LPT only:
  - `F1 = 0.7935`

- AFFM only:
  - `F1 = 0.7942`

- AFFM without deep supervision:
  - `F1 = 0.7883`

- Deformable LPT (No AFFM, 4 pt):
  - `SE = 0.7634`
  - `AUC = 0.8749`
  - `F1 = 0.7958`

- Deformable LPT + AFFM:
  - `F1 = 0.7933`

- Deformable LPT (No AFFM, 8 pt):
  - `F1 = 0.7946`

- Modulated Deformable (4 pt):
  - `SE = 0.7660`
  - `AUC = 0.8759`
  - `F1 = 0.7950`

- MS-Modulated (4 pt):
  - `SP = 0.9870`
  - `ACC = 0.9673`
  - `PR = 0.8419`
  - `F1 = 0.7954`

- MS-Modulated + CA:
  - `SE = 0.7697`
  - `AUC = 0.8777`
  - `F1 = 0.7973`

- MS-DSConv + CA:
  - `SE = 0.8083`
  - `SP = 0.9815`
  - `ACC = 0.9666`
  - `AUC = 0.8949`
  - `PR = 0.7997`
  - `F1 = 0.8020`

### Post-processing on MS-DSConv + CA

- `X = 0`
  - `SE = 0.8083`
  - `PR = 0.7997`
  - `F1 = 0.8020`

- `X = 20`
  - `SE = 0.8059`
  - `PR = 0.8035`
  - `F1 = 0.8027`
  - This is currently written as the **best balance point**.

- `X = 30`
  - `SE = 0.8046`
  - `PR = 0.8048`
  - `F1 = 0.8026`

- `X = 90`
  - `SE = 0.7995`
  - `PR = 0.8089`
  - `F1 = 0.8021`

Interpretation already written:

- MS-DSConv + CA improved topology-sensitive detection strongly, but `PR = 0.7997` was low.
- This low PR is the direct motivation for the later connected-component post-processing step.

### clDice exploration

Trainer / code:

- `F:\shiwangmo\nnUNet\nnunetv2\training\nnUNetTrainer\nnUNetTrainer_MSDSConv_clDice.py`
- `clDice` is added as an auxiliary loss with weight `0.3`.
- It is applied to the highest-resolution output branch.

Results with clDice:

- `X = 0`
  - `SE = 0.8110 ± 0.0477`
  - `AUC = 0.8958 ± 0.0220`
  - `PR = 0.7944 ± 0.0500`
  - `F1 = 0.8003 ± 0.0243`

- `X = 20`
  - `SE = 0.8079 ± 0.0484`
  - `AUC = 0.8945 ± 0.0223`
  - `PR = 0.7976 ± 0.0500`
  - `F1 = 0.8004 ± 0.0244`

- `X = 30`
  - `SE = 0.8061 ± 0.0486`
  - `AUC = 0.8937 ± 0.0224`
  - `PR = 0.7990 ± 0.0499`
  - `F1 = 0.8002 ± 0.0245`

- `X = 90`
  - `SE = 0.8002 ± 0.0498`
  - `AUC = 0.8910 ± 0.0230`
  - `PR = 0.8025 ± 0.0496`
  - `F1 = 0.7989 ± 0.0243`

Interpretation already written:

- `clDice` slightly improves `SE` and `AUC`.
- But it does **not** beat the best non-clDice result.
- At `X = 20`, `F1 = 0.8004`, which is lower than `0.8027` without clDice.
- Therefore clDice is written as a reasonable but **not retained** final option.


## Figures Already Inserted into Chapter 2

- `F:\Final_report\pic\panet.png`
- `F:\Final_report\pic\LPT.png`
- `F:\Final_report\pic\AFFM.png`
- `F:\Final_report\pic\deep_supervision.png`
- `F:\Final_report\pic\Deformable_Attention.png`
- `F:\Final_report\pic\Modulated_Deformable_Sampling.png`
- `F:\Final_report\pic\MS_modulated_DF.png`
- `F:\Final_report\pic\MS_CA.png`
- `F:\Final_report\pic\MSDS.png`
- `F:\Final_report\pic\Postprocess_Threshold_Metrics_dual_axis.png`

Chapter 3 candidate analysis figures already identified:

- `F:\Final_report\pic\Comparison_of_AUC_DF.png`
- `F:\Final_report\pic\Comparison_of_F1_DF.png`
- `F:\Final_report\pic\Comparison_of_SE_DF.png`
- `F:\Final_report\pic\Performance_Balance_Comparison.png`


## References Already Added

The following task-specific references have already been inserted into both tex files:

- `ronneberger2015unet`
- `isensee2021nnunet`
- `staal2004drive`
- `hoover2000locating`
- `fraz2012ensemble`
- `budai2013robust`
- `luo2025panet`
- `lee2015dsn`
- `zhu2021deformabledetr`
- `zhu2019dcnv2`
- `hou2021coordatt`
- `qi2023dsc`


## Compile Notes

- The report is currently configured to compile with:
  - `XeLaTeX`: `Times New Roman` / `Arial` / `Consolas` / `Cambria Math`
  - `pdfLaTeX`: fallback to `mathptmx`
- The earlier `TeX Gyre` / `XITS Math` attempt failed because those fonts were not available on this machine.
- If a citation shows as `?`, rerun the compile at least once or twice after changes.
- The English file was fixed after `hou2021coordatt` was missing from the bibliography.


## Current Best Writing Strategy for New Sessions

If you open a new session, give the assistant:

- this file
- the current target tex file path
- the exact next task

Recommended next instruction:

`Please continue from SESSION_HANDOFF_20260414.md, read the current tex files in F:\\Final_report, and start writing Chapter 3 in Chinese first.`


## Recommended Next Steps

The most natural next task is:

1. Write Chinese Chapter 3 based on the inserted framework:
   - `3.1 整体结果对比`
   - `3.2 关键指标权衡分析`
   - `3.3 结构演化路径分析`
   - `3.4 后处理与 clDice 的补充分析`

2. Use the existing Chapter 3 analysis figures there, not in Chapter 2.

3. After Chinese Chapter 3 is stable, sync it into the English report.


## Very Important Memory / Interpretation Notes

- Do not say AFFM was abandoned before the deformable + AFFM comparison.
- Do not say `CoordAtt` was already present in the earlier `MS-Modulated` stage.
- DSConv is used in the bottleneck LPT multi-scale sampling branch, not as a full-network convolution replacement.
- The post-processing step is motivated by the low PR of `MS-DSConv + CA`.
- `clDice` should be kept as a real but non-retained exploration, not erased from the report and not elevated to a main final method.
- Chapter 2 is already long enough; do not keep expanding it unless absolutely necessary.
- The next serious writing task is Chapter 3.
