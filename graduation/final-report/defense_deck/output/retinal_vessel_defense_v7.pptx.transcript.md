# retinal_vessel_defense_v7

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

Why this task matters

Clinical Significance and Use Scenario

The model is designed as a clinician-in-the-loop aid, not an automatic diagnosis system.

1. Retinal image acquisition

A non-invasive fundus image captures visible microvascular structure.

2. AI-assisted segmentation

The model extracts fine vessel branches and candidate vascular structure.

3. Clinician-led interpretation

The vessel map supports diagnosis, follow-up comparison, and treatment planning.

## Slide 3

Problem definition

Task Challenges in Fine Vessel Segmentation

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

Experimental design

Baseline and Overall Technical Route

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

## Slide 5

First structural screening

PA-Net Migration and Module Screening

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

## Slide 6

Structural mainline

LPT, Deformable Sampling, and Multi-scale Modeling

The mainline gradually shifts from fixed high-level interaction to vessel-aware sampling.

Fixed LPT

Original high-level structural module.

->

Deformable

Offsets adapt sampling to curved vessels.

->

Multi-scale

Cross-level features support both detail and context.

•

4-point deformable LPT improves F1-score to 0.7958.

•

Modulation increases detection tendency but can reduce precision.

•

Multi-scale sampling improves overall balance by reusing shallow detail.

## Slide 7

From position awareness to trajectory modeling

Coordinate Attention and Dynamic Snake Convolution

Coordinate Attention

Adds direction-aware positional recalibration after multi-scale aggregation.

Dynamic Snake Convolution

Uses continuous trajectory-style sampling to better follow slender and curved vessels.

Observed effect: SE rises strongly, but PR drops, revealing a clear recovery vs false-positive trade-off.

## Slide 8

Refinement after high-sensitivity prediction

Post-processing and clDice Exploration

Two refinement ideas address what remains after MS-DSConv + CA.

Retained: connected-component filtering at X = 20 removes small isolated false positives and gives F1 = 0.8027.

Explored but not retained: clDice increases sensitivity in some settings, but lowers PR and F1-score under the representative X = 20 setting.

## Slide 9

Unified later-stage comparison

Quantitative Results

0.8027

Final F1-score

MS-DSConv + CA, X = 20

+0.0136

Absolute F1 gain

vs. later-stage nnU-Net baseline

0.8059 / 0.8035

Sensitivity / Precision

balanced after light filtering

The improvement is modest, but it is obtained under the same later-stage protocol and follows a consistent SE-PR trade-off.

## Slide 10

Representative prediction behavior

Qualitative Results

Baseline predictions are cleaner but often miss weak fine vessels.

MS-DSConv + CA recovers more continuous branches, with post-processing reducing isolated noise.

## Slide 11

What remains open

Limitations and Future Work

Current limitations

•

Validation scope is still limited to the public benchmark conditions used here.

•

False-positive control partly depends on rule-based post-processing.

•

The mechanism behind DSConv, CA, and multi-scale interaction needs deeper interpretability analysis.

•

Some fine branches and low-response regions remain difficult.

Future work

•

Analyze nnU-Net internal preprocessing more specifically for retinal images.

•

Move false-positive control further into the network or training objective.

•

Test broader data from different devices, pathologies, and annotation styles.

•

Explore a more coordinated encoder-decoder structural design.

## Slide 12

Conclusion

A modest but stable improvement path was identified within nnU-Net.

Final retained scheme: MS-DSConv + Coordinate Attention + light connected-component post-processing.

0.8027

Final F1-score

vs. 0.7891 baseline

Q&A

Thank you.