# Graduation Thesis Handoff (2026-04-16)

## 1. Core Working Principle

- Final thesis output is **English**.
- Chinese draft is the **working draft / checking layer**.
- Current writing strategy:
  - Write in **Chinese first**
  - Confirm structure and content
  - Then sync to English

- Do **not** continue writing in the old structure unless necessary.
- The **new main Chinese file** is:
  - `F:\Final_report\reports_restructured_cn.tex`
- The **new main English file** is:
  - `F:\Final_report\reports_restructured_en.tex`
- Shared bibliography file:
  - `F:\Final_report\references.bib`


## 2. Teacher-Approved Overall Thesis Structure

This structure was approved and should be treated as the main target structure:

1. Introduction
2. Theoretical Foundations and Related Methods
3. Improved Model Design and Implementation
4. Experimental Results and Analysis
5. Conclusions and Future Work

In Chinese, the current chapter titles are:

- `第1章 绪论`
- `第2章 理论基础与相关方法`
- `第3章 改进模型设计与实现`
- `第4章 实验结果与分析`
- `第5章 总结与展望`


## 3. Important Style / Formatting Requirements from User

- The structure should look like a **good graduation thesis**, not like an experimental log.
- Avoid over-fragmented `2.x / 3.x` tiny sections unless clearly necessary.
- Prefer **large chapter blocks with stronger chapter identity**.
- Writing style should be:
  - formal
  - conservative
  - closer to teacher-provided exemplar theses
- Avoid obvious AI writing traces:
  - too much symmetry
  - template-like transitions
  - exaggerated significance claims
  - over-polished generic sentences
- Use the `humanizer` idea when polishing prose, but still keep thesis tone.
- Do not write in a hype-heavy paper style.
- Do not overuse slogans like:
  - “significant”
  - “pivotal”
  - “important role” everywhere


## 4. Reference / Citation Requirements

- User explicitly wants **IEEE-style citation behavior**.
- Switched to **BibTeX + IEEEtran style** in the new restructured files.

In both restructured files, the ending is now:

```tex
\bibliographystyle{IEEEtran}
\bibliography{references}
```

- Therefore citation numbering should follow **order of first appearance in text**, not manual `\bibitem` order.
- Shared `.bib` file:
  - `F:\Final_report\references.bib`

### Compile order for new files

For Chinese:

```bash
xelatex reports_restructured_cn.tex
bibtex reports_restructured_cn
xelatex reports_restructured_cn.tex
xelatex reports_restructured_cn.tex
```

For English:

```bash
xelatex reports_restructured_en.tex
bibtex reports_restructured_en
xelatex reports_restructured_en.tex
xelatex reports_restructured_en.tex
```

### Important bibliography note

- Keep only references actually relevant to the thesis.
- Already removed unrelated template references from the new restructured Chinese file.
- The `.bib` file currently contains only thesis-relevant references:
  - U-Net
  - nnU-Net
  - DRIVE
  - Hoover
  - Fraz
  - Budai
  - PA-Net
  - Deeply-Supervised Nets
  - Deformable DETR
  - Deformable ConvNets v2
  - Coordinate Attention
  - Dynamic Snake Convolution
  - UNet++
  - Attention U-Net


## 5. Very Important Research-Narrative Constraints

These points were repeatedly clarified and must be preserved:

### AFFM timeline

- Do **not** say AFFM was abandoned too early.
- AFFM was **not** rejected immediately after the first ablation.
- The narrative must preserve that:
  1. AFFM was tested
  2. deep supervision compatibility was checked
  3. AFFM was tested again under deformable LPT
  4. only **after that** was AFFM no longer retained in the main line

### CoordAtt / CA timeline

- Do **not** write that `CoordAtt` was already present in earlier `MS-Modulated`.
- `CA` belongs to the later `MS-Modulated + CA` stage.

### DSConv usage

- `MS-DSConv` / dynamic snake convolution is **not** a full-network convolution replacement.
- It is used in the **bottleneck LPT multi-scale sampling branch**.
- It replaces the previous discrete cross-level deformable sampling in that branch.

### Post-processing motivation

- One key narrative point:
  - `MS-DSConv + CA` gave strong `SE / AUC / F1`
  - but `PR = 0.7997`, below `0.8`
  - this low PR is the direct reason for later connected-component post-processing

### clDice narrative

- `clDice` should be kept as a **real but not retained** exploration.
- Do not delete it from the thesis.
- Do not elevate it to a final main solution.


## 6. Current File Roles

### Old files

These contain a lot of already-written content but are no longer the main structure:

- `F:\Final_report\reports_with_21_cn.tex`
- `F:\Final_report\reports_with_21.tex`

They are now mainly:
- source material
- a content reservoir
- useful for migration

### New files

These are the files that should be continued:

- Chinese main draft:
  - `F:\Final_report\reports_restructured_cn.tex`
- English main draft:
  - `F:\Final_report\reports_restructured_en.tex`


## 7. Current Status of the Restructured Chinese Thesis

File:

- `F:\Final_report\reports_restructured_cn.tex`

### Already written in the restructured Chinese file

- `1.1 研究背景与意义`
  - already written
  - already cited
  - already humanized / made less AI-like

- `1.2 国内外研究现状`
  - already written
  - already expanded
  - now includes:
    - traditional methods
    - deep learning and U-Net
    - CNN / U-Net limitations
    - why attention mechanisms became necessary
    - representative U-Net variants
    - why `nnU-Net` is already a strong baseline and why improving on it is meaningful
  - already cited

### Not yet written in the restructured Chinese file

- `1.3 视网膜血管分割面临的主要问题`
- `1.4 本文的研究内容与技术路线`
- `1.5 论文结构安排`

- Entire Chapter 2 (new structure) is still placeholder only
- Entire Chapter 3 (new structure) is still placeholder only
- Entire Chapter 4 (new structure) is still placeholder only
- Chapter 5 is still placeholder only


## 8. Current Status of the Restructured English Thesis

File:

- `F:\Final_report\reports_restructured_en.tex`

### Already written

- `1.1 Research Background and Significance`
  - already written
  - already cited
  - already humanized

### Not yet written

- `1.2 Related Work`
- `1.3 Major Challenges in Retinal Vessel Segmentation`
- `1.4 Main Research Content and Technical Route`
- `1.5 Organization of the Thesis`

- All later chapters are still placeholders


## 9. Existing Written Content in the Old Draft That Can Be Migrated Later

The old Chinese draft already contains a **fully developed experiment chain** that should later be migrated into the new structure:

### Existing old Chapter 2 contents in old draft

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

### Existing old Chapter 3 draft in old draft

The old Chinese file also already contains a drafted analysis chapter:

- `3 结果分析与讨论`
- `3.1 整体结果对比`
- `3.2 关键指标权衡分析`
- `3.3 结构演化路径分析`
- `3.4 后处理与 clDice 的补充分析`

This material is useful, but should be migrated carefully into the new structure rather than extended in-place.


## 10. Mapping from Old Structure to New Structure

This mapping was already decided and should be followed:

### New Chapter 2: Theoretical Foundations and Related Methods

Use theory-only or method-background portions extracted from old content:

- old `2.1` -> part of new `2.2`
- old `2.3` -> part of new `2.3`
- old `2.6`, `2.7`, `2.8` -> part of new `2.4`
- old `2.9`, `2.10`, `2.11` -> part of new `2.5`

### New Chapter 3: Improved Model Design and Implementation

Main migration target for the already-written experimental evolution:

- new `3.1` <- old `2.1`
- new `3.2` <- old `2.2`
- new `3.3` <- old `2.3 + 2.4 + 2.5`
- new `3.4` <- old `2.6 + 2.7`
- new `3.5` <- old `2.8 + 2.9`
- new `3.6` <- old `2.10 + 2.11`
- new `3.7` <- old `2.12`

### New Chapter 4: Experimental Results and Analysis

Should be written as concentrated comparative analysis, mainly based on:

- old drafted Chinese Chapter 3
- already prepared figures


## 11. Key Experimental Results and Interpretations to Preserve

### Main structural line

- `nnU-Net v2 baseline`
  - `SE = 0.7627`
  - `SP = 0.9852`
  - `ACC = 0.9659`
  - `AUC = 0.8739`
  - `PR = 0.8238`
  - `F1 = 0.7891`

- `PA-Net (Full)`
  - `F1 = 0.7782`
  - not final

- `LPT Only`
  - `F1 = 0.7935`

- `AFFM Only`
  - `F1 = 0.7942`

- `AFFM w/o DS`
  - `F1 = 0.7883`

- `Deformable LPT (No AFFM, 4 pt)`
  - `SE = 0.7634`
  - `AUC = 0.8749`
  - `F1 = 0.7958`

- `Deformable LPT + AFFM`
  - `F1 = 0.7933`
  - important because this is where AFFM was finally not kept

- `Deformable LPT (No AFFM, 8 pt)`
  - `F1 = 0.7946`

- `Modulated Deformable (4 pt)`
  - `SE = 0.7660`
  - `AUC = 0.8759`
  - `F1 = 0.7950`

- `MS-Modulated (4 pt)`
  - `SP = 0.9870`
  - `ACC = 0.9673`
  - `PR = 0.8419`
  - `F1 = 0.7954`

- `MS-Modulated + CA`
  - `SE = 0.7697`
  - `AUC = 0.8777`
  - `F1 = 0.7973`

- `MS-DSConv + CA`
  - `SE = 0.8083`
  - `SP = 0.9815`
  - `ACC = 0.9666`
  - `AUC = 0.8949`
  - `PR = 0.7997`
  - `F1 = 0.8020`

### Post-processing results on MS-DSConv + CA

- `X=0`
  - `SE = 0.8083`
  - `PR = 0.7997`
  - `F1 = 0.8020`

- `X=20`
  - `SE = 0.8059`
  - `PR = 0.8035`
  - `F1 = 0.8027`
  - currently treated as the best trade-off

- `X=30`
  - `SE = 0.8046`
  - `PR = 0.8048`
  - `F1 = 0.8026`

- `X=90`
  - `SE = 0.7995`
  - `PR = 0.8089`
  - `F1 = 0.8021`

### clDice results

- `X=0`
  - `SE = 0.8110 ± 0.0477`
  - `AUC = 0.8958 ± 0.0220`
  - `PR = 0.7944 ± 0.0500`
  - `F1 = 0.8003 ± 0.0243`

- `X=20`
  - `SE = 0.8079 ± 0.0484`
  - `AUC = 0.8945 ± 0.0223`
  - `PR = 0.7976 ± 0.0500`
  - `F1 = 0.8004 ± 0.0244`

- `X=30`
  - `SE = 0.8061 ± 0.0486`
  - `AUC = 0.8937 ± 0.0224`
  - `PR = 0.7990 ± 0.0499`
  - `F1 = 0.8002 ± 0.0245`

- `X=90`
  - `SE = 0.8002 ± 0.0498`
  - `AUC = 0.8910 ± 0.0230`
  - `PR = 0.8025 ± 0.0496`
  - `F1 = 0.7989 ± 0.0243`

Interpretation already fixed:

- `clDice` improved `SE / AUC` slightly
- but did not beat the best non-clDice result
- therefore retained as exploration only


## 12. Existing Figures Already Prepared

### Chapter-2 / method-evolution-related figures already created

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

### Chapter-4 analysis figures already prepared

- `F:\Final_report\pic\Comparison_of_AUC_DF.png`
- `F:\Final_report\pic\Comparison_of_F1_DF.png`
- `F:\Final_report\pic\Comparison_of_SE_DF.png`
- `F:\Final_report\pic\Performance_Balance_Comparison.png`


## 13. What Should Be Written Next in the New Session

Recommended immediate next step:

1. Continue writing the restructured Chinese main file:
   - next target: `1.3 视网膜血管分割面临的主要问题`

Then:

2. finish Chapter 1 in Chinese:
   - `1.3`
   - `1.4`
   - `1.5`

3. continue Chapter 2 in Chinese

Only after Chinese structure is stable:

4. sync corresponding English sections into:
   - `F:\Final_report\reports_restructured_en.tex`


## 14. Short Prompt for the Next Session

Recommended message to paste into the next chat:

`Please continue from SESSION_HANDOFF_20260416_RESTRUCTURED.md, and keep working in F:\\Final_report\\reports_restructured_cn.tex. The next task is to write Section 1.3 in Chinese under the new thesis structure.`
