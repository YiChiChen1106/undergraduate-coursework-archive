# Compact Defense Script for V18 Deck

Target duration: about 15 minutes.

## Slide 1. Title

Good afternoon, respected teachers and committee members.
Today I will present my final-year project, Research on Fine Retinal Vessel Segmentation Based on nnU-Net.

This project focuses on retinal vessel segmentation, especially fine and weak vessel branches.
I use nnU-Net v2 as a strong baseline, and investigate whether task-oriented structural modifications can improve thin-vessel recovery, vessel continuity, and false-positive control.

On the right side, this slide shows the task: from an original fundus image to a vessel segmentation result.
The goal is to obtain a more complete vessel map for further analysis.

## Slide 2. Clinical Significance and Use Scenario

Before introducing the method, I would like to explain why this project is meaningful.

Retinal fundus imaging is non-invasive, and it can show microvascular structures inside the eye.
These structures are related to eye diseases, and may also reflect some systemic vascular conditions.

In a realistic clinical workflow, the fundus image is first acquired from the patient.
Then, the segmentation model extracts the vascular tree and generates a structured vessel map.
Based on this map, computer-aided diagnosis systems can extract vascular features.

However, the model cannot make the final clinical decision.
It is only a reference for doctors, and the final decision should still be made by doctors.

## Slide 3. Task Challenges in Fine Vessel Segmentation

This slide summarizes the main challenges in fine vessel segmentation.

First, fine peripheral vessels usually have low contrast.
They can be weak in the original fundus image, and sometimes hidden by background texture.

Second, retinal vessels are not simple straight lines.
They include curved branches, bifurcations, local discontinuities, and very small terminal vessels.
So the model needs to capture not only local appearance, but also structural continuity.

Third, there is a trade-off between sensitivity and precision.
If the model is more sensitive, it can recover more thin vessels, but it may also introduce more false positives.
Therefore, the key question is how to improve fine-vessel recovery while controlling false positives.

## Slide 4. From U-Net to nnU-Net Baseline

This slide explains the project's baseline foundation.

U-Net is a classic encoder-decoder network for medical image segmentation.
The encoder extracts semantic information, and the decoder recovers spatial resolution.
Skip connections help preserve local details for segmentation.

nnU-Net builds on the U-Net-style design.
It is a self-configuring segmentation framework.
Its preprocessing, patch size, training plan, and inference settings can automatically adapt to different datasets.

Because of this, nnU-Net has strong segmentation performance.
In the following experiments, the baseline F1-score already reaches 0.7891.

So in this project, I did not try to replace nnU-Net.
Instead, I kept nnU-Net as a strong baseline and tested whether task-oriented structural changes could further improve fine vessel segmentation.

## Slide 5. Baseline and Overall Technical Route

This slide summarizes the overall technical route of this project.

The first stage is to establish the baseline.
I used 2D nnU-Net v2 as the baseline, with a patch size of 512 by 512.
I also tested some preliminary changes, including CLAHE preprocessing and Focal Loss.
However, they did not bring stable final improvement.

The second stage focuses on structural migration and module screening.
I transferred ideas from PA-Net to nnU-Net v2, especially LPT and AFFM.
Later, I chose LPT as the main route, and further tested deformable sampling, multi-scale aggregation, Coordinate Attention, and Dynamic Snake Convolution.

The third stage is about output refinement and result evaluation.
I used light connected-component post-processing to reduce isolated false positives.
The models were compared using sensitivity, precision, specificity, accuracy, and F1-score.

## Slide 6. PA-Net Migration and Module Screening

This slide shows the PA-Net migration and module screening experiment.

First, I tested the full PA-Net migration.
The results show that direct transplantation of PA-Net into the nnU-Net framework was not effective.
Although precision increased, sensitivity dropped clearly, and the F1-score decreased by about 0.011.
This indicates that the model became too conservative, so many weak vessel branches were missed.

Then, I tested two single-module variants: LPT Only and AFFM Only.
Both of them had more stable performance than the full PA-Net migration.

Although AFFM Only had a slightly higher F1-score in this table, its gain was not stable in the following control experiment.
LPT Only kept higher sensitivity and was more suitable for later bottleneck structural modeling.
Therefore, I selected LPT as the main route for the following experiments.

## Slide 7. LPT, Deformable Sampling, and Multi-scale Modeling

After the screening stage, the project moved into the LPT-centered mainline.

The original LPT uses fixed high-level interaction.
However, retinal vessels are thin, curved, and locally irregular, so fixed sampling may not align well with local vessel structures.

To address this problem, I introduced deformable sampling into the LPT module.
The idea is to use learnable offsets to help the sampling positions adapt to local vessel structures.

The table shows that, compared with LPT Only, 4-point Deformable LPT increases sensitivity from 0.7597 to 0.7634, and F1-score from 0.7935 to 0.7958.
This result shows that adaptive sampling helps recover more thin vessels and also improves the overall model balance.

After that, I further explored multi-scale modeling.
It combines shallow details with deep semantic information.
Overall, this stage shows that vessel-aware sampling is more promising than fixed sampling for fine-vessel segmentation.

## Slide 8. Coordinate Attention and Dynamic Snake Convolution

This slide introduces two modules: Coordinate Attention and Dynamic Snake Convolution.

First, Coordinate Attention helps the model focus more on direction and position.
As shown in the figure, it uses horizontal and vertical information to generate direction-aware attention maps.
This is especially important because retinal vessels are thin and curved.

Second, Dynamic Snake Convolution helps the model follow thin and curved vessels.
In the figure, the sampling points form a snake-like sampling path.
This makes it more suitable for thin and curved vessel structures.

The table shows the step-by-step result.
After adding Coordinate Attention, sensitivity improves from 0.7582 to 0.7697, and F1-score increases from 0.7954 to 0.7973.
After adding Dynamic Snake Convolution, SE further increases to 0.8083, and F1-score increases to 0.8020.

However, PR drops from 0.8419 to 0.8324, and then to 0.7997.
This means the model also introduces more false positives.
This leads to the next stage: I use post-processing to reduce these false positives.

## Slide 9. Post-processing and clDice Exploration

This slide explains the refinement stage after MS-DSConv plus CA.

In the previous stage, the model recovered more thin vessels, but it also introduced more false positives.
Most of these false positives are small isolated regions.

Therefore, I used light connected-component filtering.
The idea is simple: if a predicted region is small and isolated, it is more likely to be noise, so it can be removed by an area threshold.

The chart on the left shows that when the area threshold is 20, the model reaches its best F1-score of 0.8027.
Precision improves with only a small decrease in sensitivity.

After that, I also tested clDice, because it focuses on vessel continuity.
However, clDice increases sensitivity in some settings, but lowers PR and F1-score under the representative X = 20 setting.
Therefore, clDice was not retained, and the final refinement method is light connected-component post-processing.

## Slide 10. Quantitative Results

This slide shows the quantitative results under the unified later-stage comparison.

The bar chart compares the results of representative models.
As you can see, the baseline model has an F1-score of 0.7891.
The final model, MS-DSConv plus CA with post-processing, reaches an F1-score of 0.8027.

So the absolute improvement is 0.0136.
The gain is not very large, but it is stable and explainable.

The table on the right shows the trade-off between SE and PR.
For sensitivity, the final model increases from 0.7627 to 0.8059.
This indicates that the final model has a stronger ability to recover fine vessels.

On the other hand, precision has a controlled decrease from 0.8238 to 0.8035.
Overall, the quantitative results show a better balance between fine-vessel recovery and false-positive control.

## Slide 11. Qualitative Results

This slide shows the qualitative results for two representative cases.

The main observation is that the baseline prediction is relatively clean, but it misses some small vessel branches.
Compared with the baseline, MS-DSConv plus CA recovers more fine vessels and gives better local continuity.
This is consistent with the higher sensitivity mentioned in the previous slide.

After post-processing, the visual change is not very large.
This is because the post-processing step is lightweight.
Its role is mainly to make a small correction to isolated components, rather than changing the whole vessel structure.

Overall, this slide shows the same trade-off as the earlier metrics: the final model improves fine-vessel recovery, but still has some limitations in false-positive control.

## Slide 12. Limitations and Future Work

This slide summarizes the limitations and future work of the whole project.

First, experimental validation is still limited to public benchmark data.
So in the future, the method should be tested on more datasets from different disease conditions and imaging devices.

Second, false-positive control is still a limitation.
In this project, false-positive reduction still depends partly on rule-based post-processing.
Future work should integrate false-positive control into the model or training objective.

Third, the structural modules still need deeper interpretability analysis.
For example, we need to better understand how Coordinate Attention and Dynamic Snake Convolution help different vessel regions.

Overall, this project is still a research-stage improvement.
Future work should focus on robustness, explainability, and clinical-style validation.

## Slide 13. Conclusion and Q&A

To conclude, this project focuses on fine retinal vessel segmentation based on nnU-Net.

The final retained solution is multi-scale Dynamic Snake Convolution, Coordinate Attention, and light connected-component post-processing.

It achieves an F1-score of 0.8027, which is higher than the baseline of 0.7891.
The improvement is modest but stable.

Overall, it proves that task-oriented structural design can still improve nnU-Net for fine-vessel segmentation.

Thank you for your attention.
I am happy to answer your questions.
