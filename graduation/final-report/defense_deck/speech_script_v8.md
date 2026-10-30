# Defense Speech Script for V13 PPT

Target duration: about 15 minutes  
Project title: Research on Fine Retinal Vessel Segmentation Based on nnU-Net

## Slide 1. Title

Good morning, respected teachers and committee members. My name is Yichi Chen, and today I will present my final-year project, titled "Research on Fine Retinal Vessel Segmentation Based on nnU-Net."

The central topic of this project is retinal vessel segmentation, especially the segmentation of fine and weak vessel branches. In this work, I did not try to replace nnU-Net as a general framework. Instead, I used nnU-Net v2 as a strong baseline and investigated whether task-oriented structural modifications could further improve thin-vessel recovery, vessel continuity, and false-positive control.

On the right side of this slide, I show the basic input and output form of the task: from an original retinal fundus image to a vessel segmentation result. The goal is to produce a vessel map that is more complete and more useful for later clinical interpretation or quantitative analysis.

## Slide 2. Clinical Significance and Use Scenario

Before introducing the method, I would like to explain why this task is meaningful.

Retinal fundus imaging is non-invasive and can reveal microvascular structures inside the eye. These vessel structures are related to ophthalmic diseases and can also provide indirect information about systemic vascular conditions. However, the clinically useful information is not always visible from the raw image alone, especially for fine peripheral vessels, vessel continuity, and subtle morphological changes.

The workflow shown on this slide describes a more realistic use scenario. A fundus image is first acquired from the patient. Then a vessel segmentation model extracts the vascular tree and produces a structured vessel map. Based on this map, later computer-aided diagnosis modules can extract quantitative vascular features, such as vessel calibre, tortuosity, branching pattern, and artery-vein related indicators. These features may support risk assessment or disease suggestions.

So the practical value of this project is not that the model directly gives a final diagnosis. Instead, it improves an important intermediate step. A more complete and reliable vessel map can make downstream feature extraction and clinical review more stable. The final interpretation, patient communication, and treatment or follow-up decisions should still be led by doctors.

## Slide 3. Task Challenges in Fine Vessel Segmentation

Fine retinal vessel segmentation is challenging for several reasons.

First, thin peripheral vessels often have low contrast. In the original image, these vessels can be weak and partly hidden by background texture. Although contrast enhancement can make the vessels more visible, preprocessing alone cannot solve the full segmentation problem.

Second, retinal vessels are not simple straight lines. They include curved branches, bifurcations, local discontinuities, and very small terminal structures. Therefore, the model needs to capture not only local pixel appearance, but also structural continuity.

Third, there is a trade-off between sensitivity and precision. If the model becomes more sensitive, it may recover more fine vessels, but it may also introduce scattered false positives. If the model becomes too conservative, the output may look clean, but weak branches may be missed.

Finally, nnU-Net is already a strong and mature baseline. This means that superficial module stacking is unlikely to bring reliable improvement. The core research question is: what structural changes can still produce useful gains on top of nnU-Net?

## Slide 4. Baseline and Overall Technical Route

This slide summarizes the experimental route of the project.

The first stage was to establish the baseline. I used 2D nnU-Net v2 as the controlled reference, with a patch size of 512 by 512. I also explored preliminary changes such as CLAHE preprocessing and Focal Loss. These changes affected training behavior, but they did not produce stable final improvement.

The second stage focused on structural migration and screening. I transferred ideas from PA-Net, especially LPT and AFFM, into the nnU-Net setting. After that, I used the LPT route as the mainline and tested deformable sampling, multi-scale aggregation, Coordinate Attention, and Dynamic Snake Convolution.

The third stage focused on output refinement and result analysis. Since high-sensitivity models may generate isolated false positives, I used light connected-component post-processing. The models were compared using sensitivity, precision, specificity, accuracy, and F1-score.

For the later-stage structural experiments, I used a unified five-fold validation protocol. This is important because it makes the comparison between modules more meaningful.

## Slide 5. PA-Net Migration and Module Screening

The first structural experiment was PA-Net migration and module screening.

The table shows that direct transplantation of the full PA-Net design was not effective in this setting. Compared with the nnU-Net baseline, the full PA-Net version increased precision, but sensitivity dropped clearly, and the F1-score decreased from 0.7891 to 0.7782. This suggests that the full migration made the model more conservative and less suitable for recovering weak vessel branches.

Then I tested single-module variants. LPT Only achieved an F1-score of 0.7935, and AFFM Only achieved 0.7942. These results were not large improvements, but they were more stable than the full PA-Net migration.

The key conclusion from this slide is that simple module stacking was not enough. The later design should not keep the full PA-Net structure. Instead, the LPT-centered route was retained because it was more relevant to bottleneck structural modeling and could be further adapted for fine-vessel segmentation.

## Slide 6. LPT, Deformable Sampling, and Multi-scale Modeling

After the screening stage, the project moved into the LPT mainline.

The original LPT module uses fixed high-level interaction. However, retinal vessels are curved and slender, so fixed sampling may not align well with vessel geometry. To address this, I tested deformable sampling, where offsets allow the sampling positions to adapt to local vessel structure.

In the experiments, 4-point deformable LPT improved the F1-score to 0.7958. This showed that adaptive sampling was helpful for the task. I also tested modulation, which increased the tendency to detect vessels, but it could reduce precision. This again reflected the sensitivity-precision trade-off.

Then I introduced multi-scale modeling. The idea was to reuse shallow details together with deeper semantic information, so that the model could balance local fine-vessel details and broader structural context. Overall, this stage showed that vessel-aware sampling and multi-scale information were more promising than direct full-module migration.

## Slide 7. Coordinate Attention and Dynamic Snake Convolution

This slide introduces the two most important retained structural ideas: Coordinate Attention and Dynamic Snake Convolution.

Coordinate Attention adds direction-aware positional recalibration. In retinal vessel segmentation, position and direction are important because vessels have elongated structures. Coordinate Attention helps the network emphasize informative spatial responses after multi-scale aggregation.

Dynamic Snake Convolution provides a different inductive bias. Instead of treating convolution as a rigid local operation, it uses a trajectory-style sampling pattern that is more suitable for slender and curved objects. This is especially relevant for fine retinal vessels, where continuity along a vessel path matters.

The observed effect was that sensitivity increased strongly, which means the model recovered more vessel pixels. However, precision dropped in some settings, which means more false positives were also introduced. Therefore, this stage improved fine-vessel recovery, but it also made false-positive control more important.

## Slide 8. Post-processing and clDice Exploration

After MS-DSConv and Coordinate Attention, the remaining problem was mainly output refinement.

The retained refinement method was connected-component filtering. The idea is simple: very small isolated components are more likely to be false positives than real vessel structures. In the final retained setting, the threshold X equals 20. This light post-processing step reduced small isolated noise and improved the final F1-score to 0.8027.

I also explored clDice because it is designed to emphasize topology and skeleton-like structure, which seems suitable for vessel segmentation. However, in the representative setting with X equals 20, clDice increased sensitivity in some cases but reduced precision and F1-score. Therefore, it was explored but not retained in the final scheme.

This slide shows an important point: improving sensitivity alone is not sufficient. For this task, the final output must balance thin-vessel recovery and false-positive suppression.

## Slide 9. Quantitative Results

This slide summarizes the quantitative results under the unified later-stage comparison.

The nnU-Net baseline F1-score was 0.7891. The full PA-Net migration dropped to 0.7782, which confirmed that direct transplantation was not suitable. Deformable LPT improved the result to 0.7958. Multi-scale and attention-based variants then pushed the performance further.

The final retained scheme, which combines MS-DSConv, Coordinate Attention, and light connected-component post-processing with X equals 20, achieved an F1-score of 0.8027. This is an absolute F1 gain of 0.0136 over the later-stage nnU-Net baseline.

The final sensitivity and precision were 0.8059 and 0.8035, respectively. This indicates that the final solution did not only increase detection tendency; it also brought the output back to a more balanced state.

I would describe the improvement as modest but meaningful. It is modest because nnU-Net is already strong and the absolute gain is not very large. It is meaningful because the gain follows a consistent technical route and is obtained under the same comparison protocol.

## Slide 10. Qualitative Results

The qualitative results help explain the numerical behavior.

In the representative cases, the baseline predictions are relatively clean, but they often miss weak and thin vessel branches. This is consistent with a conservative prediction pattern.

The later models, especially the MS-DSConv plus Coordinate Attention design, recover more continuous branches and more fine vessel structures. In some local regions, the vessel map becomes more complete and better connected.

However, these qualitative results also show why post-processing is needed. When the model becomes more sensitive, it may generate isolated noisy components. The connected-component filtering step helps reduce this scattered noise without changing the main vessel structure too aggressively.

So the qualitative interpretation is consistent with the quantitative results: the final method improves fine-vessel recovery, but the improvement must be controlled by output refinement.

## Slide 11. Limitations and Future Work

This project still has several limitations.

First, the validation scope is limited to the public benchmark conditions used in this study. This means the current result should not be directly interpreted as proof of clinical robustness.

Second, false-positive control still partly relies on rule-based post-processing. Although this is effective and lightweight, it would be better to move more of this control into the model or the training objective.

Third, the mechanisms behind DSConv, Coordinate Attention, and multi-scale interaction still need deeper interpretability analysis. The experiments show useful behavior, but more analysis is needed to explain when and why each module works.

Finally, some fine branches and low-response regions remain difficult. This is expected because the weakest vessels are close to the boundary between anatomical structure and image noise.

For future work, I would test broader data from different devices, pathologies, and annotation styles. I would also analyze nnU-Net preprocessing more specifically for retinal images, explore learned false-positive control, and evaluate the method with more clinically oriented evidence.

## Slide 12. Conclusion and Q&A

To conclude, this project identified a modest but stable improvement path within nnU-Net for fine retinal vessel segmentation.

The final retained scheme is MS-DSConv plus Coordinate Attention, followed by light connected-component post-processing. The final F1-score is 0.8027, compared with the baseline value of 0.7891.

The main contribution is not a single large performance jump. Instead, the contribution is a controlled experimental route: starting from nnU-Net, screening migrated modules, refining the LPT-centered structure, improving vessel-aware modeling, and finally balancing sensitivity with false-positive control.

Overall, the study shows that fine retinal vessel segmentation benefits from structural modeling that respects vessel continuity and from careful output refinement. At the same time, the method remains a research-stage improvement and should be further validated before any clinical use.

That is the end of my presentation. Thank you for your attention, and I welcome your questions.
