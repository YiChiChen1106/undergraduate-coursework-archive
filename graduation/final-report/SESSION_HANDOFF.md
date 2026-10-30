# Final Report Writing Handoff

## Purpose

This file is a handoff summary for continuing the final report writing in a new session without losing context.

Project topic:

- Improving retinal vessel segmentation based on `nnU-Net`

Primary workspace:

- Code: `F:\shiwangmo`
- Report folder: `F:\Final_report`


## Current Report Files

Main files in `F:\Final_report`:

- English report: [reports_with_21.tex](/mnt/f/Final_report/reports_with_21.tex)
- Chinese checking draft: [reports_with_21_cn.tex](/mnt/f/Final_report/reports_with_21_cn.tex)

Supporting files already present:

- [reports.tex](/mnt/f/Final_report/reports.tex)
- [reports.pdf](/mnt/f/Final_report/reports.pdf)
- [solarcell.pdf](/mnt/f/Final_report/solarcell.pdf)
- Images folder expected by `2.3`: `F:\Final_report\pic\`

Expected image paths used in `2.3`:

- `pic/panet.png`
- `pic/LPT.png`
- `pic/AFFM.png`


## Key Writing Principle

Final output is in English.

Chinese text is only a checking layer for the user to verify meaning and structure before syncing the English version.

The report should follow the school final report structure, not a full IEEE two-column journal layout.

However:

- English style can borrow from IEEE writing
- References use IEEE-style numbered citations


## Template / Structure Decisions

The school materials suggest:

- Use school final report structure
- IEEE article template is a reference, not the primary structure for the final report

Recommended Chapter 2 structure:

- `2.1 Experimental Protocol and Basic Settings`
- `2.2 Baseline and Early Explorations`
- `2.3 PA-Net Module Migration`
- `2.4 Ablation of LPT and AFFM`
- `2.5 MS-Modulated`
- `2.6 MS-Modulated + CA`
- `2.7 MS-DSConv + CA`
- `2.8 clDice and Post-processing`

Interpretation:

- Chapter 2: methods + local observations that motivate the next step
- Chapter 3: full result analysis and discussion


## What Is Already Written

### In both Chinese and English tex files

Already written:

- `2.1`
- `2.1.1`
- `2.1.2`
- `2.2`
- `2.3`

### Current section titles

Chinese:

- `2.1 实验协议与基本设置`
- `2.1.1 数据集与数据组织`
- `2.1.2 实现细节与评价指标`
- `2.2 基线与前期探索`
- `2.3 PA-Net 模块迁移`

English:

- `2.1 Experimental protocol and basic settings`
- `2.1.1 Datasets and data organization`
- `2.1.2 Implementation details and evaluation metrics`
- `2.2 Baseline and early explorations`
- `2.3 PA-Net module migration`


## Current Content Decisions

### Stage split

Experiments are divided into two stages:

- Early exploratory stage: `Exp1` to `Exp3`
- Later main stage: `Exp4` onward

### Core design statement

This statement has already been integrated into `2.1.2` and `2.2`:

- Most later experiments modify the `U-Net` backbone and feature interaction inside `nnU-Net`
- Only a small number of experiments modify `loss` settings or trainer-level training strategy

This is important and should remain consistent in later sections.


## Experimental Chain That Has Been Confirmed

### Early exploratory stage

These experiments were used mainly for comparison with the senior student and to motivate later structural changes.

#### Exp1

- Method: standard `nnU-Net` baseline
- Trainer: `my_train_150`
- Setting: `150 epochs`
- Metrics:
  - `IoU(vessel)`
  - `mIoU`
  - `Recall`
  - `Precision`
  - `Accuracy`
  - `mPA`
  - `F1-score`
- Key result:
  - `F1 = 0.7924`

#### Exp2

- Method: `CLAHE + nnU-Net`
- Trainer: `my_train_150`
- Setting: `150 epochs`
- Metrics: same as `Exp1`
- Key result:
  - `F1 = 0.7827`

#### Exp3

- Method: `CLAHE + nnU-Net + Focal Loss`
- Trainer: `MyTrainer_DiceFocal`
- Setting: `150 epochs`
- Metrics: same as `Exp1`
- Key result:
  - `F1 = 0.7802`

### Important note on early data split

The first three valid experiments did not use a new data split.

They followed the existing training and validation lists to stay consistent with the senior student's setup and allow direct comparison.

This wording has already been updated in both Chinese and English files.


## Early Results Source

The last four pages of [PA-net.pptx](/mnt/c/Users/28100/Desktop/bishe/PA-net.pptx) were successfully read and confirmed as the source of early-stage result summaries.

Recovered values:

### Exp1

- Dice converged at epoch `69`
- Dice: `0.8616999983787537`
- `IoU(vessel)=0.6574`
- `mIoU=0.8107`
- `Recall=0.7688`
- `Precision=0.8219`
- `Accuracy=0.9664`
- `mPA=0.8768`
- `F1-score=0.7924`

### Exp2

- Dice converged at epoch `60`
- Dice: `0.8618999719619751`
- `IoU(vessel)=0.6441`
- `mIoU=0.8041`
- `Recall=0.7282`
- `Precision=0.8497`
- `Accuracy=0.9662`
- `mPA=0.8583`
- `F1-score=0.7827`

### Exp3

- Converged at epoch `53`
- Lowest focal loss: `0.0245999991893768`
- `IoU(vessel)=0.6410`
- `mIoU=0.8023`
- `Recall=0.7255`
- `Precision=0.8489`
- `Accuracy=0.9659`
- `mPA=0.8568`
- `F1-score=0.7802`


## Later Main Stage

### Exp4 and later experiments

This has been confirmed:

- `Exp4` establishes the later-stage baseline on `DRIVE`
- `Exp5` and all later experiments use the same later-stage platform

Shared later-stage protocol:

- Dataset: `DRIVE`
- Preprocessing: later unified single-channel pipeline
- Split: same five-fold split
- Evaluation setting: same later-stage metric system

### Important caution

The user stated:

- During the original `Exp5`, PA-Net was not actually used correctly
- Training still behaved like normal `U-Net`
- The user does not want to present that mistaken run as the formal final result
- The user later reran a correct PA-Net-related experiment

Implication for writing:

- Do not present an incorrect run as a valid PA-Net result
- It is acceptable not to describe the mistaken run in detail
- Final report should keep only corrected and valid results in the formal main tables


## Data / Input Pipeline

### Early stage

- Multi-source training data
- Three-channel separated input
- RGB channels split into independent inputs

### Later stage

- Only `DRIVE`
- Single-channel input
- Preprocessing pipeline:
  - grayscale conversion
  - normalization
  - CLAHE
  - gamma correction

This later preprocessing is linked to `PA-Net`.


## Metrics

### Early stage metric set

Used for `Exp1` to `Exp3`:

- `IoU(vessel)`
- `mIoU`
- `Recall`
- `Precision`
- `Accuracy`
- `mPA`
- `F1-score`

### Later stage metric set

Used for `Exp4` onward:

- `SE`
- `SP`
- `ACC`
- `AUC`
- `PR`
- `F1-score`

### AUC interpretation

This has been explicitly confirmed:

- Probability maps were not saved in the current setup
- Therefore, reported `AUC` is an approximation computed from binary predictions
- This wording is already reflected in `2.1.2`


## Current Section 2.2 Decision

`2.2` has been rewritten as:

- `Baseline and early explorations`

Purpose:

- summarize `Exp1` to `Exp3`
- avoid overloading Chapter 2 with full result analysis
- include a compact summary table

Chinese table already inserted:

- caption: `前期探索实验结果汇总`

English table already inserted:

- caption: `Summary of early exploratory experiments`


## Current Section 2.3 Decision

`2.3` has been written as:

- `PA-Net 模块迁移`
- `PA-Net module migration`

Main logic:

- introduce `LPT` and `AFFM`
- explain their placement and intended function
- state that this is a full migration attempt before ablation

### Figure layout decision

Current figure arrangement in both tex files:

- three figures placed side by side
- same height for all three images

Used paths:

- `pic/panet.png`
- `pic/LPT.png`
- `pic/AFFM.png`

Used setting:

- `height=0.22\textheight, keepaspectratio`


## Citations Already Added

Added to both English and Chinese tex files in IEEE-style `\bibitem` format:

- `ronneberger2015unet`
- `isensee2021nnunet`
- `staal2004drive`
- `hoover2000locating`
- `fraz2012ensemble`
- `budai2013robust`
- `luo2025panet`

### Where citations are already used

- `DRIVE` mention in `2.1`
- `nnU-Net` framework mention in `2.1.2`
- dataset list in `2.1.1`
- PA-Net preprocessing statement in `2.1.1`
- U-Net-style baseline architecture statement in `2.2`


## Important Writing Decisions

### What belongs in Chapter 2

Allowed in Chapter 2:

- method design
- experiment setup
- local observations that motivate the next step

Do not fully expand in Chapter 2:

- deep comparative analysis
- full interpretation of every metric tradeoff
- final integrated discussion

Those belong in Chapter 3.

### Language style decisions

- Final output is English
- Chinese is for checking and alignment
- Avoid loose wording like:
  - `尽量`
  - `主要目的`
  - overly inflated academic wording
- Prefer direct and controlled expressions


## Open Work / Next Recommended Steps

Most natural next step:

- write `2.4 Ablation of LPT and AFFM`

After that:

- `2.5 MS-Modulated`
- `2.6 MS-Modulated + CA`
- `2.7 MS-DSConv + CA`
- `2.8 clDice and Post-processing`


## Known Issues / Things to Watch

1. The current tex files are still based on the school report structure, not a true IEEEtran paper layout.

2. The school zip suggested:
   - exemplar reports are for report structure reference
   - IEEE article template is only a style/template reference

3. Do not blindly convert the whole report into a full IEEE two-column journal paper unless explicitly required.

4. Image files under `F:\Final_report\pic\` must exist, otherwise `2.3` figure compilation will fail.

5. Some old template content after the newly written sections is still the original example text. Later sections should progressively replace that content.


## Recommended Prompting / Session Continuation Strategy

When opening a new session, give the new assistant:

- this file
- the current target file path
- the next section to write

Recommended next instruction:

`Please continue from SESSION_HANDOFF.md, read the current tex files in F:\\Final_report, and write section 2.4 in Chinese first, then sync the English version.`

