# Chen_Yichi_Logbook_0428_filled

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Logbook

From:2025/10/01  To:2026/04/28

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

October

1. PyTorch Fundamentals (10/1-10/7):

- Read PyTorch technical documentation.

- Learned data loading, environment configuration, and CNN concepts (convolutional/pooling layers).

- Practiced processing the CIFAR dataset.

2. U-Net Deep Dive (10/9-10/17):

- Systematically studied the U-Net paper.

- Learned U-Net environment setup and dataset processing through tutorials.

- Prepared and delivered a presentation for the group meeting on 10/17.

3. Framework Focus (10/17-10/24):

- Researched U-Net variants (U-mamba, U-Net++, ResUNet).

- Identified nnU-Net as an adaptive framework and decided to make it the research focus.

- Downloaded nnU-Net v2 source code and set up a new environment.

- Resolved configuration issues (Nvidia driver version, v1/v2 naming differences, 3D Nii data format).

4. Baseline Model Training & Debugging (10/25-10/26):

- Followed supervisor's guidance to split the dataset (train/validation/test).

- Set max epochs to 150 and started training.

- Discovered that test set metrics (mIoU, Recall) were extremely low.

- After a reminder from the supervisor, investigated and confirmed the issue was caused by image flipping during nnU-Net v2 data augmentation.

- Obtained baseline evaluation results (mIoU: 0.8107).

5. Experimental Iterations (10/27-10/28):

- (10/27) Discussed results with supervisor; retrained using the CLAHE-enhanced dataset. Results showed no significant improvement.

- (10/28) Reported results; per supervisor's guidance, changed the loss function to Focal Loss and retrained. Results still showed no significant change.

1

face- to-face

3

Second supervisor:

Liu ZhiShuai

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

November

1. PA-Net Preprocessing Replication (11/01-11/07):

Studied and implemented the four-step preprocessing pipeline from the PA-Net paper: Graying, Standardization, CLAHE, and Gamma Transform .

 Integrated these custom scripts into the nnU-Net data pipeline to enhance vessel-to-background separation .

2. Robust Strategy: 5-Fold Cross-Validation (11/08-11/15):

Transitioned from a fixed dataset split to a 5-fold cross-validation strategy on the DRIVE dataset to minimize partitioning bias .

Developed a batch evaluation script to automate the calculation of SE, SP, ACC, and AUC metrics.

3. Core Module Development: LPT and AFFM (11/16-11/24):

Analyzed the mathematical definitions of the Lightweight Parallel Transformer (LPT) and Adaptive Vascular Feature Fusion Module (AFFM) .

 Wrote PyTorch code for the LFAU and EPA units within the LPT bottleneck .

4. Structural Integration & Resource Optimization (11/25-11/30):

Embedded the LPT into the nnU-Net bottleneck and replaced standard skip connections with the AFFM .

 Optimized batch sizes to prevent "Out of Memory" (OOM) errors on the 8GB RTX 4060 hardware.

1 

Face-to-face

2

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

December

1. Experiment 5 Execution & Data Analysis (12/01-12/07):

 Ran full training sessions for the modified nnU-Net+LPT+AFFM architecture .

 Conducted a comparative analysis of quantitative results, observing an unexpected drop in Sensitivity (SE).

2. Conflict Mechanism Investigation (12/08-12/15):

 Investigated the structural conflict between the AFFM’s multi-level fusion and nnU-Net’s Deep Supervision mechanism .

Hypothesized that mixed signals from the AFFM lead to "negative optimization" in the decoder layers.

3. Troubleshooting Spatial Calibration (12/16-12/22):

Debugged the "180-degree rotation bug" by recalibrating the NIfTI affine transformation matrix .

Verified geometric consistency by visualizing the 2D-to-3D pseudo-conversion outputs .

4. Interim Report Preparation (12/23-12/31):

 Aggregated all data for the final comparison tables (Table 5 & 6) and visualized results (Figures 1-5) .

 Outlined future work for 2026, focusing on isolated ablation studies for LPT and AFFM.

2

1 Face-to-face, 1 online

4

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

January

1. Baseline Re-check and PA-Net Ablation (01/01-01/12):- Re-ran the nnU-Net baseline and PA-Net variants under the same DRIVE 5-fold protocol.- Compared Full PA-Net, LPT Only, AFFM Only, and LPT+AFFM settings.2. Interaction Between AFFM and Deep Supervision (01/13-01/20):- Reviewed failed cases and metric trends from the ablation experiments.- Found that AFFM did not provide stable gains within the nnU-Net decoder structure.3. Direction Refinement (01/21-01/31):- Chose the LPT route as the main direction for later structural improvement.- Updated experiment notes and prepared a clearer ablation plan for the final report.

2

1 Face-to-face, 1 online/WeChat

3

Technical discussion with PhD student Liu Zhishuai on PA-Net integration and ablation interpretation.

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

February

1. Deformable LPT Design (02/01-02/09):- Replaced the GAA operation in LPT with deformable sampling to better adapt to thin and curved vessels.- Implemented 4-point and 8-point deformable sampling variants.2. Module Combination Tests (02/10-02/18):- Tested Deformable LPT without AFFM and Deformable LPT combined with AFFM.- Added modulation and multi-scale aggregation for local vessel-structure modelling.3. Model Selection (02/19-02/28):- Compared F1, sensitivity and precision trends across the new variants.- Retained the 4-point Deformable LPT without AFFM as a more stable branch for the next stage.

2

1 Face-to-face, 1 online/WeChat

3

Informal discussion with lab peers on deformable sampling design and training stability.

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

March

1. Attention and Structural Convolution (03/01-03/10):- Added Coordinate Attention to strengthen position-aware channel weighting.- Integrated Dynamic Snake Convolution into the multi-scale sampling branch.2. Extended Ablation (03/11-03/20):- Compared MS-Modulated+CA and MS-DSConv+CA under the same evaluation protocol.- Observed improved sensitivity and F1, but reduced precision, suggesting more false-positive pixels.3. Post-processing Exploration (03/21-03/31):- Started threshold-based false-positive removal experiments.- Explored clDice loss as a possible topology-aware training objective.

2

1 Face-to-face, 1 online/WeChat

4

Group discussion on qualitative results, metric trade-offs and false-positive control.

Month

List the main activities (only few words per activity)

Interaction with the supervisor

Any other form of supervisory interaction (second supervisor, industry, fellows etc.)

Number of meetings

Mode of meeting (face- to-face, online e.g., Skype, WeChat etc.)

Number of emails exchanged

April

1. Final Experiment Selection (04/01-04/10):- Completed the post-processing threshold comparison and retained X=20 as the final setting.- Tested clDice; it increased sensitivity but reduced precision and F1, so it was not retained.2. Quantitative and Qualitative Reporting (04/11-04/18):- Generated representative DRIVE overlays and mask comparisons for the final report.- Summarised the final model as MS-DSConv + CA with light post-processing.3. Final Report Preparation (04/19-04/28):- Expanded the abstract, reference list and result figures after supervisor feedback.- Finalised the cover pages, plagiarism statement, and submission PDFs.- Reported the final F1 improvement from 0.7891 to 0.8027 (+0.0136) as a stable but modest gain.

3

2 Face-to-face, 1 online/WeChat

6

Supervisor feedback on the final report; peer checks on figures, references and PDF formatting.