# Logbook Cover Sheet

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Logbook

From:2025/10/01  To:2025/1/10

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