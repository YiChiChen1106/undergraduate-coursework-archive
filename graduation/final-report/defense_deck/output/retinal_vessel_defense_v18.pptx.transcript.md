# retinal_vessel_defense_v18

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

## Slide 1

Final-Year Project Defense

Research on Fine Retinal Vessel Segmentation Based on nnU-Net

Chen Yichi | GUID: [student-id-redacted] | UESTC4006P

A controlled nnU-Net-based study focused on thin-vessel recovery, structural continuity, and false-positive control.

Original image  →  Vessel segmentation

Original image

→

Vessel segmentation

The project studies how nnU-Net can better recover fine retinal vessel structure.

## Slide 2

Clinical value of vessel segmentation

Clinical Significance and Use Scenario

Keywords: non-invasive -> vessel map -> vascular features -> doctor review

Clinical support, not automatic diagnosis.

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

Segmentation provides the measurable vessel map used by later CAD modules.

Final diagnosis and patient decisions remain under doctor supervision.

## Slide 3

Problem definition

Task Challenges in Fine Vessel Segmentation

Keywords: low contrast -> complex structure -> SE/PR trade-off

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

## Slide 4

Baseline foundation

From U-Net to nnU-Net Baseline

Keywords: U-Net structure -> self-configuring nnU-Net -> strong baseline 0.7891

U-Net

•

Encoder extracts semantic features; decoder recovers spatial resolution.

•

Skip connections help preserve local detail for segmentation.

nnU-Net

A self-configuring segmentation framework built around U-Net-style designs.

Dataset fingerprint

Reads data properties and task setting.

->

Auto configuration

Adapts preprocessing, patch size, and training plan.

->

Strong baseline

Provides a controlled reference for later changes.

Project position: keep nnU-Net v2 as the baseline, then test task-oriented structural changes for fine vessels.

This makes the later comparison stricter: useful gains must appear on top of an already strong framework.

## Slide 5

Experimental design

Baseline and Overall Technical Route

Keywords: baseline -> module screening -> post-processing and evaluation

Stage 1

Baseline setup

nnU-Net v2 establishes the controlled reference.

Preliminary exploration

CLAHE and Focal Loss affect convergence but do not improve final performance.

Stage 2

PA-Net migration

LPT and AFFM are transferred and screened under nnU-Net.

LPT mainline

Deformable sampling, multi-scale aggregation, CA, and DSConv are tested.

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

## Slide 6

First structural screening

PA-Net Migration and Module Screening

Keywords: full PA-Net conservative -> AFFM unstable -> retain LPT

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

Direct transplantation was not enough.

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

## Slide 7

Structural mainline

LPT, Deformable Sampling, and Multi-scale Modeling

Keywords: fixed LPT -> learnable offsets -> adaptive sampling improves F1

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

## Slide 8

From position awareness to trajectory modeling

Coordinate Attention and Dynamic Snake Convolution

Keywords: CA direction maps -> DSConv snake path -> SE up, PR down

Coordinate Attention

Adds direction-aware positional recalibration after multi-scale aggregation.

Dynamic Snake Convolution

Uses continuous trajectory-style sampling to better follow slender and curved vessels.

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

## Slide 9

Refinement after high-sensitivity prediction

Post-processing and clDice Exploration

Keywords: small isolated false positives -> X=20 -> clDice not retained

Two refinement ideas address what remains after MS-DSConv + CA.

Retained: connected-component filtering at X = 20 removes small isolated false positives and gives F1 = 0.8027.

Explored but not retained: clDice increases sensitivity in some settings, but lowers PR and F1-score under the representative X = 20 setting.

## Slide 10

Unified later-stage comparison

Quantitative Results

Keywords: F1 0.7891 -> 0.8027; SE up, PR controlled

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

The improvement is modest, but it is obtained under the same later-stage protocol and follows a consistent SE-PR trade-off.

## Slide 11

Representative prediction behavior

Qualitative Results

Keywords: baseline cleaner -> more fine branches -> lightweight correction

Baseline predictions are cleaner but often miss weak fine vessels.

MS-DSConv + CA recovers more continuous branches; post-processing only makes a light correction.

## Slide 12

What remains open

Limitations and Future Work

Keywords: more data -> model-level FP control -> interpretability and clinical validation

Current limitations

•

Validation is still limited to public benchmark conditions.

•

False-positive control partly relies on rule-based post-processing.

•

DSConv, CA, and multi-scale interactions need deeper interpretability analysis.

•

Fine branches and low-response regions remain difficult.

Defense position: the method is a research-stage improvement, not a finished clinical product.

Future work

•

Analyze nnU-Net preprocessing specifically for retinal images.

•

Move false-positive control into the network or training objective.

•

Test broader data across devices, pathologies, and annotation styles.

•

Explore a more coordinated encoder-decoder structural design.

Research direction: move from benchmark gains toward robustness, explainability, and use-case evidence.

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

Keywords: final method -> F1 0.8027 -> modest but stable -> Q&A

0.8027

Final F1-score

vs. 0.7891 baseline

Q&A

Thank you.