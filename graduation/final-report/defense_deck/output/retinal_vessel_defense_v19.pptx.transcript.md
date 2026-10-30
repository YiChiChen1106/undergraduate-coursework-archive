# retinal_vessel_defense_v19

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

## Slide 1

Final-Year Project Defense

Research on Fine Retinal Vessel Segmentation Based on nnU-Net

Chen Yichi | GUID: [student-id-redacted]

A controlled nnU-Net-based study focused on retinal vessel segmentation, especially fine and weak vessel branches.

I use nnU-Net v2 as a strong baseline and investigate whether task-oriented structural modifications can improve thin-vessel recovery, vessel continuity, and false-positive control.

Task:Original image  →  Vessel segmentation

Original fundus image

→

Vessel segmentation

The goal is to obtain a more complete vessel map for further analysis.

.

## Slide 2

Clinical value of vessel segmentation

Clinical Significance and Use Scenario

Why this project is meaningful?

Keywords: retinal fundus imaging, non-invasive, microvascular structure, eye diseases, systemic vascular conditions

realistic clinical workflow

Fundus

Image

Vessel

Segmentation

Vascular Feature

Extraction

CAD Risk /

Disease Suggestion

Doctor

Review

Patient

Management

keyword:fundus image,patient,vascular tree,structurual vessel map,computer-aided diagnosis systems,vascular features

However,decision,reference,doctor

## Slide 3

Problem definition

Task Challenges in Fine Vessel Segmentation

Talk track: Fine vessels have low contrast and complex shapes, so recovery and false-positive control must be balanced.

Original fundus image

Fine peripheral vessels are weak and partly hidden by background texture.

Contrast-enhanced view

Preprocessing can make vessels clearer, but segmentation still needs structural modeling.

•

Thin peripheral vessels are low-contrast and easily confused with background texture.

•

Curved branches, bifurcations, and local discontinuities require structural continuity modeling.

•

Higher sensitivity often introduces scattered false positives, so SE and PR must be balanced.

•

A mature baseline such as nnU-Net leaves limited room for superficial improvements.

Core research question: what structural changes still produce useful gains on top of nnU-Net?

Keyword:

Challenges, fine peripheral vessels,low-contrast, weak,original fundus image,hidden,background texture

straight, Curved branches, bifurcations, local discontinuities, local appearance, structural continuity,

trade-off, sensitivity,precision,recover,false positive, how to improve fine-vessel recovery while controlling false positives

## Slide 4

Baseline foundation

From U-Net to nnU-Net Baseline

Talk track: U-Net provides the structure; nnU-Net is self-configuring and already reaches baseline F1 = 0.7891.

U-Net

•

Encoder extracts semantic features; decoder recovers spatial resolution.

•

Skip connections help preserve local detail for segmentation.

nnU-Net

Builds on the U-Net-style design, It is a self-configuring segmentation framework.

Dataset fingerprint

Reads data properties and task setting.

->

Auto configuration

Its preprocessing, patch size, training plan, and inference settings can automatically adapt to different datasets.

->

Strong baseline

Provides a controlled reference for later changes.

Project position:keep nnU-Net as a strong baseline and test whether task-oriented structural changes could further improve fine vessel segmentation

.

This makes the later comparison stricter: useful gains must appear on top of an already strong framework.

Keyword: 

baseline foundation,classic encoder-decoder network,medical image segmentation,

strong segmentation performance,following experiments,0.7891

replace, baseline, task-oriented structural changes , improve fine vessel segmentation

## Slide 5

Experimental design

Baseline and Overall Technical Route

Talk track: The route is baseline setup, structural screening, LPT-based improvement, and final evaluation.

Stage 1

Baseline setup

nnU-Net v2 establishes the controlled reference.

Preliminary exploration

CLAHE and Focal Loss affect convergence but do not improve final performance.

Stage 2

PA-Net migration

LPT and AFFM are transferred and screened under nnU-Net.

LPT mainline

deformable sampling, multi-scale aggregation, Coordinate Attention, and Dynamic Snake Convolution.

Stage 3

Output refinement

Connected-component filtering targets small isolated false positives.

Result analysis

Models are compared by SE, PR, SP, ACC, and F1-score.

512 x 512

Patch size

2D nnU-Net v2

5-fold

Validation

Unified later-stage protocol

100 epochs

Training

Most structural experiments

Keywords: overall technical route, 

establish the baseline. 2D nnU-Net v2,baseline,patch size, preliminary changes,  stable final improvement

structural migration ,module screening, transferred ideas, PA-Net, nnU-Net v2,LPT,main route

output refinement ,result evaluation, light connected-component post-processing, reduce isolated false positives

## Slide 6

First structural screening

PA-Net Migration and Module Screening

Talk track: Full PA-Net became conservative; AFFM gain was unstable, so I retained the LPT-centered route.

Ablation snapshot

Unified 5-fold validation

Model

SE

PR

F1-score

F1 change

nnU-Net v2 Baseline

0.7627

0.8238

0.7891

Reference

PA-Net Full

0.7211

0.8570

0.7782

-0.0109

LPT Only

0.7597

0.8361

0.7935

+0.0044

AFFM Only

0.7573

0.8400

0.7942

+0.0051

0.7942

Best transferred F1

AFFM only

+0.0044

LPT branch gain

over baseline F1

-0.0109

Full migration

below baseline F1

What the screening shows

Direct transplantation was not effective.

•

Full PA-Net increased PR, but sacrificed SE and reduced F1-score.

•

Single-module variants were more stable under the same protocol.

•

LPT remained the clearest route for later bottleneck structural modeling.

Design implication: keep the LPT-centered route, then test finer vessel-aware modules.

Screening criterion

F1 gain without clear SE loss

Next route

LPT-centered modeling

Module-level decision after screening

PA-Net Full

Not retained

Whole-branch migration lost sensitivity and F1-score.

LPT Only

Retained

Most relevant structural path for bottleneck redesign.

AFFM Only

Reference only

Slight F1 gain, but less aligned with later fine-vessel focus.

Although AFFM Only had a slightly higher F1-score in this table, its gain was not stable in the following control experiment.LPT Only kept higher sensitivity and was more suitable for later bottleneck structural modeling.Therefore, I selected LPT as the main route for the following experiments.

## Slide 7

Structural mainline

LPT-centered mainline, Deformable Sampling, and Multi-scale Modeling

Talk track: Fixed sampling may not follow curved vessels; deformable LPT uses offsets and improves F1 to 0.7958.

The mainline gradually shifts from fixed high-level interaction to vessel-aware sampling.

Fixed LPT

Original high-level structural module.

->

Deformable

Offsets adapt sampling to curved vessels.

->

Multi-scale

Cross-level features support both detail and context.

Two-row evidence

Model

SE

PR

F1-score

LPT Only

0.7597

0.8361

0.7935

Deformable LPT, 4-point

0.7634

0.8371

0.7958

Adaptive sampling raises both SE and F1-score, supporting the LPT mainline before later multi-scale refinement.

Keyword:LPT-centered mainline

original LPT, fixed high-level interaction,neglect, thin, curved, locally irregular, fixed sapling,align well with local vessel structures

address this problem, deformable sampling, LPT module, learnable offsets, sampling positions adapt to local vessel structures

table,adaptive sampling helps recover more thin vessels and also improves the overall model balance.

multi-scale modeling, combines shallow details with deep semantic information. 

vessel-aware sampling ,promising ,fine-vessel segmentation.

## Slide 8

From position awareness to trajectory modeling

Coordinate Attention and Dynamic Snake Convolution

Talk track: CA adds direction-aware attention; DSConv follows curved vessels, raising SE and F1 but lowering PR.

Coordinate Attention

Adds direction-aware positional recalibration after multi-scale aggregation.

Dynamic Snake Convolution

form a snake-like sampling path, suitable for thin and curved vessel structures.

.

Stepwise evidence

Model

SE

PR

F1-score

MS-Modulated

0.7582

0.8419

0.7954

MS-Modulated + CA

0.7697

0.8324

0.7973

MS-DSConv + CA

0.8083

0.7997

0.8020

CA improves SE and F1-score; DSConv increases them further, while lower PR reveals the recovery vs false-positive trade-off.

Keywords:two modules

Coordinate Attention,focus, direction and position, figure, horizontal and vertical information, direction-aware attention maps,important, retinal vessels,thin and curved

Dynamic Snake Convolution, follow thin and curved vessels, sampling points, snake-like sampling path, suitable,  thin and curved vessel structures

step-by-step,add,sensitivity,F1

However,precision, introduces more false positive, leads to the next stage, use post-processing to reduce these false positives

## Slide 9

refinement stage after MS-DSConv plus CA

Post-processing and clDice Exploration

Talk track: Small isolated false positives are filtered at X = 20; clDice was explored but not retained.

Two refinement ideas address what remains after MS-DSConv + CA.

Retained: connected-component filtering at X = 20 removes small isolated false positives and gives F1 = 0.8027.

Explored but not retained: clDice increases sensitivity in some settings, but lowers PR and F1-score under the representative X = 20 setting.

Keywords:previous stage,recover more vessel.introduce more false positive, small isolated regions.

light connected-component filtering, predicted region, small and isolated,likely,noise,remove, area threshold.

Chart,x=20, best F1-score of 0.8027, Precision improves with only a small decrease in sensitivity.

clDice, focuses on vessel continuity. However,

Therefore,clDice, not retained, final refinement method, light connected-component filtering.

## Slide 10

Unified later-stage comparison

Quantitative Results

Talk track: Final F1 improves from 0.7891 to 0.8027; SE increases while PR remains controlled.

0.8027

Final F1-score

MS-DSConv + CA, X = 20

+0.0136

Absolute F1 gain

vs. later-stage nnU-Net baseline

SE / PR trade-off

Model

SE

PR

Baseline

0.7627

0.8238

Final

0.8059

0.8035

Overall, the quantitative results show a better balance between fine-vessel recovery and false-positive control.

Keywords: quantitative results under the unified later-stage comparison.

bar chart, results of representative models

baseline model, F1-score of 0.7891, final model, F1-score of 0.8027

absolute improvement 0.0136,not very big,stable and explainable

table on the right, trade-off between SE and PR, sensitivity, from 0.7627 to 0.8059, a stronger ability to recover fine vessels.

precision, a controlled decrease from 0.8238 to 0.8035

## Slide 11

Representative prediction behavior

Qualitative Results

Talk track: The baseline is cleaner but misses branches; the final model recovers more fine vessels with light correction.

the baseline prediction is relatively clean, but it misses some small vessel branches

.

MS-DSConv plus CA recovers more fine vessels and gives better local continuity.

Keywords: qualitative results for two representative cases

main observation, consistent with the higher sensitivity mentioned in the previous slide

After post-processing, visual change is not very large, post-processing step is lightweight ,role ,small correction to isolated components, changing the whole vessel structure

Overall, the same trade-off as the earlier metrics, the final model improves fine-vessel recovery, but still has some limitations in false-positive control.

## Slide 12

What remains open

Limitations and Future Work

Talk track: Future work needs broader data, model-level false-positive control, interpretability, and clinical validation.

Current limitations

•

experimental validation is still limited to public benchmark data

.

•

False-positive control partly relies on rule-based post-processing.

•

structural modules still need deeper interpretability analysis

Defense position: the method is a research-stage improvement, not a finished clinical product.

Future work

•

tested on more datasets from different disease conditions and imaging devices.

•

integrate false-positive control into the model or training objective.

•

better understand how Coordinate Attention and Dynamic Snake Convolution help different vessel regions.

Overall, this project is still a research-stage improvement.Future work should focus on robustness, explainability, and clinical-style validation.

Next validation route

1

Broader data

Evaluate cross-device and cross-pathology robustness beyond the current benchmark setting.

2

Model-integrated control

Reduce isolated false positives through training objectives or learned refinement.

3

Clinical-style evidence

Assess reliability with expert review, failure cases, and diagnosis-oriented use scenarios.

## Slide 13

Conclusion

A modest but stable improvement path was identified within nnU-Net.

Final retained scheme: MS-DSConv + Coordinate Attention + light connected-component post-processing.

To conclude, this project focuses on fine retinal vessel segmentation based on nnU-Net.

Overall, it proves that task-oriented structural design can still improve nnU-Net for fine-vessel segmentation.

0.8027

Final F1-score

vs. 0.7891 baseline

Q&A

Thank you.