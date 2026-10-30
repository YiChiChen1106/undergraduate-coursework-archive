# [student-id-redacted]_YiChi_Chen_risk_assessment

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

GLASGOW COLLEGE, UESTC

Final year individual

PROJECT RISK ASSESSMENT 

Student Name:

Chen YiChi

Student UoG & UESTC IDs:

[student-id-redacted]+[student-id-redacted]

Project Title:

Research on Deep Learning based Fine Segmentation Technology of Retinal Blood Vessels in the Fundus

Supervisor (1st) Name:

Yu Jiali

The supervisor should think ahead and set out a work plan for the student. All potential hazards should be identified and necessary control measures made clear to the student. This risk assessment must be signed by the supervisor and the student, before work begins. 

WORK ACTIVITY

Please provide a description of the project plan:

This project aims to apply and improve the nnU-Net v2 framework for high-accuracy, automated segmentation of retinal vessels from fundus images.

The main project activities are as follows:

1.Investigation and Background Study

Investigate the application background and clinical significance of automated retinal vessel segmentation for the early diagnosis of diseases (e.g., diabetic retinopathy, hypertension).

Survey the academic and industry frontier, including current State-of-the-Art (SOTA) methods, challenges, and development trends in medical image segmentation.

Conduct a literature review of foundational deep learning architectures (e.g., U-Net, DeepLab, Segformer) and the principles of the nnU-Net v2 framework.

Research and compare loss functions (e.g., Focal Loss, Tversky Loss) suitable for addressing the high class imbalance inherent in vessel segmentation.

2.Data Preparation & Environment Setup:

Collection and organization of public fundus datasets (e.g., DRIVE, STARE, CHASE_DB1).

Conversion and preprocessing of images and ground truth masks to meet the specific format requirements of nnU-Net v2, creating a unified dataset.

Setup of the deep learning environment (Python, PyTorch, CUDA, nnU-Net v2 framework) on the development workstation.

3.Baseline Modelling:

Training and validation of the standard nnU-Net v2 framework (using its default Dice + Cross-Entropy loss configuration) on the prepared datasets.

Running evaluations to establish baseline performance metrics (e.g., IoU, F1-score, Recall, Precision) to serve as a control for subsequent improvements.

4.Model Improvement & Experimentation:

Analysis of the baseline model's limitations (e.g., segmentation of fine, thin vessels).

Implementation and integration of a combined Focal Loss and Dice Loss function within the nnU-Net v2 framework to better address the class imbalance.

Systematic training, validation, and testing of this improved model configuration.

5.Results Analysis & Thesis Writing:

Quantitative and qualitative comparison of the baseline and improved models, focusing on performance metrics and visual quality (especially for fine vessels).

Composition of the Final Year Project Thesis, detailing the research background, methodology, experiments, results, and conclusions.

6.Project Finalisation & Defence:

Preparation of the final project presentation slides and participation in the graduation defence.

HAZARDS

Please identify ALL significant hazards associated with the project e.g. electrical, chemical, biological, mechanical etc. (use separate sheet if necessary):

1. Electrical Hazards:

Risk of Electric Shock: Use of high-performance workstations, GPU servers, and monitors powered by mains electricity. Damaged or faulty wiring, plugs, or improper handling (e.g., liquid spills) pose a risk of electric shock.

2. Heat / Fire Hazards:

Hot Components: Training deep learning models (especially nnU-Net) requires intensive, prolonged GPU usage. GPUs under high load generate significant heat. Direct contact with components (e.g., GPU, heat sinks) can cause burns.

Fire Risk: Overheating of components could lead to a fire hazard if the workstation/server ventilation is obstructed (e.g., by papers, clutter) or if the cooling system (fans) fails.

TRAINING

Will the student receive relevant safety training?                                     √    Yes         No           

Details of Training:

1. Electrical Safety: The student will receive induction on basic electrical safety protocols for handling high-performance, mains-powered equipment (workstations, servers). This includes:

Visual inspection of plugs and cables before use.

Procedures for reporting any damaged or faulty equipment immediately to the supervisor or lab technician.

Awareness of the critical danger of having liquids (drinks, etc.) near electrical hardware.

2. Fire & Heat Safety: Training will be provided on the specific hazards associated with high-load computing:

Awareness of the burn risk from hot components (e.g., GPU heat sinks) during or after intensive training runs.

Instruction on the critical importance of maintaining clear airflow and ventilation for the workstation/server at all times, ensuring vents are not obstructed by papers or other items.

Induction on standard fire safety procedures, including the location of the nearest CO2 (electrical safe) fire extinguisher and the building's emergency evacuation routes.

Who will provide Training: Liu Zhishuai

Is the training adequate to control all hazards that have been identified?  Yes         No 

COSHH

Will the COSHH regulations apply?                                                           Yes       No

If Yes, please detail all COSHH assessments the student is required to read:

SUPERVISION

 Will the student be supervised at all times?                    

If Yes, please name people who will provide supervision:

Liu Zhishuai

      Yes       No 

CONCLUSION

Are you satisfied that risks are adequately controlled?                              Yes         No 

If No, what further measures will be taken to reduce risk to an acceptable level?

(e.g. written scheme of work, physical controls, engineered solutions etc.)

Ethical Gateway Questions (Please answer the following questions.)

Does the study involve vulnerable participants or those unable to give informed consent? 

(e.g. children, people with learning disabilities, your own students)

Yes ☐ No ☒

Does the study require permission of a gatekeeper for access to participants? 

(e.g. schools, self-help groups, residential homes, hospitals)

Yes ☐ No ☒

Is it necessary for participants to be involved without consent? 

(e.g. covert observation in non-public places)

Yes ☐ No ☒

Does the study involve sensitive topics?

(e.g. obtaining information about sexual activity, substance abuse)

Yes ☐ No ☒

Is blood, tissue samples or any other substances be taken from participants?

(e.g. blood, urine, stools, skin)

Yes ☐ No ☒

Does the study involve intrusive interventions?

(e.g. The administration of drugs, hypnosis, physical exercise)

Yes ☐ No ☒

Are financial or other inducements be offered to participants?

(With the exception reasonable expenses or small tokens of appreciation)

Yes ☐ No ☒

Does the study investigate any aspect of illegal activity?

 (e.g. drugs, crime, underage alcohol consumption or sexual activity)

Yes ☐ No ☒

Will work reveal personally attributable confidential information (written, audio or video), or cause undue distress, degrade personal dignity, or infringe human rights?

(eg. Show characteristics of someone’s personality, cause distressful emotions, participant will need to be stressed beyond what is considered normal for them, contacting people under threatening circumstances)

Yes ☐ No ☒

Does the work involve, environmental issues?  

(e.g. Relates to real life environmental judgements, such as climate change, species and habitat loss, and pollution.)

Yes ☐ No ☒

Will the work present ethical problems for tutors, or the university, or participating companies or organisations?

(eg Will the work infringe intellectual property rights.)

Yes ☐ No ☒

Are (non-human) animals involved with the work?

(e.g. Might the work inflict physical or psychological cruelty, pain, disfigurement or unnecessary restraint)

Yes ☐ No ☒

If the answer to any of the ethical gateway questions above is “Yes”, or if there are any other significant ethical issues, then further ethical consideration is required.

In any proposal involving human participants clear explanation of how informed consent will be obtained, how confidentiality will be observed, how the nature of research and the means of dissemination of the outcomes will be communicated to the participants must be provided.

Summarise below the ethical issues involved in the proposal and how these will be addressed.

Summary of Ethical Issues

None

Signed (student) 

Date:2025/10/30

Signed (1st Supervisor):

Date: 2025/10/30