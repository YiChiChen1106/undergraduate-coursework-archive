# V13 PPT Bilingual Speech Script with Memory Keywords

说明：这份文件用于理解和背诵。每一段包含英文原文、中文理解和记忆关键词。正式答辩时仍以英文表达为准。

Target duration: about 15 minutes  
Project title: Research on Fine Retinal Vessel Segmentation Based on nnU-Net

## Slide 1. Title

### Paragraph 1

**EN:** Good morning, respected teachers and committee members. My name is Yichi Chen, and today I will present my final-year project, titled "Research on Fine Retinal Vessel Segmentation Based on nnU-Net."

**中文：** 各位老师、各位答辩委员会成员，大家上午好。我叫陈一驰，今天我将介绍我的毕业设计项目，题目是“Research on Fine Retinal Vessel Segmentation Based on nnU-Net”。

**关键词：** 开场；自我介绍；项目题目；final-year project；nnU-Net

### Paragraph 2

**EN:** The central topic of this project is retinal vessel segmentation, especially the segmentation of fine and weak vessel branches. In this work, I did not try to replace nnU-Net as a general framework. Instead, I used nnU-Net v2 as a strong baseline and investigated whether task-oriented structural modifications could further improve thin-vessel recovery, vessel continuity, and false-positive control.

**中文：** 本项目的核心主题是视网膜血管分割，尤其关注细小、弱响应血管分支的分割。在这项工作中，我并不是要替代 nnU-Net 这个通用框架，而是以 nnU-Net v2 作为较强基线，研究面向任务的结构改进是否能进一步提升细血管恢复、血管连续性和假阳性控制。

**关键词：** retinal vessel segmentation；fine vessels；nnU-Net baseline；structural modifications；continuity；false positives

### Paragraph 3

**EN:** On the right side of this slide, I show the basic input and output form of the task: from an original retinal fundus image to a vessel segmentation result. The goal is to produce a vessel map that is more complete and more useful for later clinical interpretation or quantitative analysis.

**中文：** 在这一页右侧，我展示了任务最基本的输入和输出形式：从原始眼底图像到血管分割结果。目标是生成一张更完整、更适合后续临床解释或定量分析的血管图。

**关键词：** input-output；fundus image；vessel map；clinical interpretation；quantitative analysis

## Slide 2. Clinical Significance and Use Scenario

### Paragraph 1

**EN:** Before introducing the method, I would like to explain why this task is meaningful.

**中文：** 在介绍方法之前，我想先说明为什么这个任务有意义。

**关键词：** motivation；meaning；before method

### Paragraph 2

**EN:** Retinal fundus imaging is non-invasive and can reveal microvascular structures inside the eye. These vessel structures are related to ophthalmic diseases and can also provide indirect information about systemic vascular conditions. However, the clinically useful information is not always visible from the raw image alone, especially for fine peripheral vessels, vessel continuity, and subtle morphological changes.

**中文：** 眼底成像是非侵入式检查，可以观察眼内微血管结构。这些血管结构与眼科疾病相关，也能间接反映一些全身性血管状况。但是，有临床价值的信息并不总是能从原始图像中直接看清，尤其是外周细血管、血管连续性和细微形态变化。

**关键词：** non-invasive；microvascular structure；ophthalmic disease；systemic vascular condition；fine peripheral vessels；morphology

### Paragraph 3

**EN:** The workflow shown on this slide describes a more realistic use scenario. A fundus image is first acquired from the patient. Then a vessel segmentation model extracts the vascular tree and produces a structured vessel map. Based on this map, later computer-aided diagnosis modules can extract quantitative vascular features, such as vessel calibre, tortuosity, branching pattern, and artery-vein related indicators. These features may support risk assessment or disease suggestions.

**中文：** 这一页的流程展示了更接近实际应用的场景。首先采集患者的眼底图像；然后血管分割模型提取血管树，生成结构化血管图。基于这张血管图，后续计算机辅助诊断模块可以提取定量血管特征，例如血管口径、弯曲度、分支模式，以及动静脉相关指标。这些特征可以支持风险评估或疾病提示。

**关键词：** workflow；fundus acquisition；vessel tree；structured map；vascular features；CAD risk

### Paragraph 4

**EN:** So the practical value of this project is not that the model directly gives a final diagnosis. Instead, it improves an important intermediate step. A more complete and reliable vessel map can make downstream feature extraction and clinical review more stable. The final interpretation, patient communication, and treatment or follow-up decisions should still be led by doctors.

**中文：** 因此，本项目的实际价值不是让模型直接给出最终诊断，而是改进一个重要的中间环节。更完整、更可靠的血管图可以让下游特征提取和临床复核更加稳定。最终解释、患者沟通以及治疗或随访决策仍然应该由医生主导。

**关键词：** not final diagnosis；intermediate step；reliable vessel map；feature extraction；doctor-led；follow-up

## Slide 3. Task Challenges in Fine Vessel Segmentation

### Paragraph 1

**EN:** Fine retinal vessel segmentation is challenging for several reasons.

**中文：** 细小视网膜血管分割有几个方面的挑战。

**关键词：** challenges；fine vessels；overview

### Paragraph 2

**EN:** First, thin peripheral vessels often have low contrast. In the original image, these vessels can be weak and partly hidden by background texture. Although contrast enhancement can make the vessels more visible, preprocessing alone cannot solve the full segmentation problem.

**中文：** 第一，外周细血管通常对比度较低。在原始图像中，这些血管可能很弱，并且部分被背景纹理遮挡。虽然对比度增强可以让血管更清楚，但仅靠预处理不能解决完整的分割问题。

**关键词：** low contrast；peripheral vessels；background texture；CLAHE；preprocessing limitation

### Paragraph 3

**EN:** Second, retinal vessels are not simple straight lines. They include curved branches, bifurcations, local discontinuities, and very small terminal structures. Therefore, the model needs to capture not only local pixel appearance, but also structural continuity.

**中文：** 第二，视网膜血管不是简单直线结构。它们包含弯曲分支、分叉点、局部断裂和很小的末端结构。因此，模型不仅要捕捉局部像素外观，还要保持结构连续性。

**关键词：** curved branches；bifurcations；discontinuities；terminal vessels；structural continuity

### Paragraph 4

**EN:** Third, there is a trade-off between sensitivity and precision. If the model becomes more sensitive, it may recover more fine vessels, but it may also introduce scattered false positives. If the model becomes too conservative, the output may look clean, but weak branches may be missed.

**中文：** 第三，sensitivity 和 precision 之间存在权衡。模型更敏感时可能恢复更多细血管，但也可能引入分散假阳性；模型过于保守时输出更干净，但弱分支可能被漏掉。

**关键词：** sensitivity；precision；trade-off；false positives；conservative prediction；missed branches

### Paragraph 5

**EN:** Finally, nnU-Net is already a strong and mature baseline. This means that superficial module stacking is unlikely to bring reliable improvement. The core research question is: what structural changes can still produce useful gains on top of nnU-Net?

**中文：** 最后，nnU-Net 本身已经是很强、很成熟的基线。因此，简单堆叠模块不太可能带来可靠提升。核心研究问题是：在 nnU-Net 之上，什么样的结构改动仍然能够带来有用增益？

**关键词：** strong baseline；module stacking；reliable improvement；research question；structural changes

## Slide 4. Baseline and Overall Technical Route

### Paragraph 1

**EN:** This slide summarizes the experimental route of the project.

**中文：** 这一页总结了项目的实验路线。

**关键词：** experimental route；overview；pipeline

### Paragraph 2

**EN:** The first stage was to establish the baseline. I used 2D nnU-Net v2 as the controlled reference, with a patch size of 512 by 512. I also explored preliminary changes such as CLAHE preprocessing and Focal Loss. These changes affected training behavior, but they did not produce stable final improvement.

**中文：** 第一阶段是建立基线。我使用 2D nnU-Net v2 作为受控参考，patch size 为 512×512。我也探索了 CLAHE 预处理和 Focal Loss 等初步修改。这些变化会影响训练行为，但没有带来稳定的最终提升。

**关键词：** baseline；2D nnU-Net v2；512×512；CLAHE；Focal Loss；no stable gain

### Paragraph 3

**EN:** The second stage focused on structural migration and screening. I transferred ideas from PA-Net, especially LPT and AFFM, into the nnU-Net setting. After that, I used the LPT route as the mainline and tested deformable sampling, multi-scale aggregation, Coordinate Attention, and Dynamic Snake Convolution.

**中文：** 第二阶段关注结构迁移和筛选。我把 PA-Net 中的思想，特别是 LPT 和 AFFM，迁移到 nnU-Net 设置中。之后，我以 LPT 路线为主线，测试了 deformable sampling、多尺度聚合、Coordinate Attention 和 Dynamic Snake Convolution。

**关键词：** PA-Net migration；LPT；AFFM；deformable sampling；multi-scale；CA；DSConv

### Paragraph 4

**EN:** The third stage focused on output refinement and result analysis. Since high-sensitivity models may generate isolated false positives, I used light connected-component post-processing. The models were compared using sensitivity, precision, specificity, accuracy, and F1-score.

**中文：** 第三阶段关注输出精修和结果分析。由于高敏感性模型可能产生孤立假阳性区域，我使用了轻量连通域后处理。模型比较使用 sensitivity、precision、specificity、accuracy 和 F1-score。

**关键词：** output refinement；connected components；isolated false positives；metrics；F1-score

### Paragraph 5

**EN:** For the later-stage structural experiments, I used a unified five-fold validation protocol. This is important because it makes the comparison between modules more meaningful.

**中文：** 对后期结构实验，我使用统一的五折验证协议。这很重要，因为它让不同模块之间的比较更有意义。

**关键词：** five-fold validation；unified protocol；fair comparison；module comparison

## Slide 5. PA-Net Migration and Module Screening

### Paragraph 1

**EN:** The first structural experiment was PA-Net migration and module screening.

**中文：** 第一个结构实验是 PA-Net 迁移和模块筛选。

**关键词：** first structural experiment；PA-Net；screening

### Paragraph 2

**EN:** The table shows that direct transplantation of the full PA-Net design was not effective in this setting. Compared with the nnU-Net baseline, the full PA-Net version increased precision, but sensitivity dropped clearly, and the F1-score decreased from 0.7891 to 0.7782. This suggests that the full migration made the model more conservative and less suitable for recovering weak vessel branches.

**中文：** 表格显示，直接迁移完整 PA-Net 在当前设置下并不有效。与 nnU-Net 基线相比，完整 PA-Net 版本提高了 precision，但 sensitivity 明显下降，F1-score 从 0.7891 降到 0.7782。这说明完整迁移让模型更保守，不太适合恢复弱血管分支。

**关键词：** full PA-Net；precision up；sensitivity down；F1 0.7782；conservative；weak branches

### Paragraph 3

**EN:** Then I tested single-module variants. LPT Only achieved an F1-score of 0.7935, and AFFM Only achieved 0.7942. These results were not large improvements, but they were more stable than the full PA-Net migration.

**中文：** 接着我测试了单模块变体。LPT Only 的 F1-score 为 0.7935，AFFM Only 为 0.7942。这些提升不大，但比完整 PA-Net 迁移更稳定。

**关键词：** single-module variants；LPT Only；AFFM Only；small gain；more stable

### Paragraph 4

**EN:** The key conclusion from this slide is that simple module stacking was not enough. The later design should not keep the full PA-Net structure. Instead, the LPT-centered route was retained because it was more relevant to bottleneck structural modeling and could be further adapted for fine-vessel segmentation.

**中文：** 这一页的关键结论是：简单堆叠模块不够。后续设计不应保留完整 PA-Net 结构，而应保留以 LPT 为中心的路线，因为它更接近 bottleneck 结构建模，也更适合继续针对细血管分割改造。

**关键词：** no simple stacking；discard full PA-Net；retain LPT；bottleneck modeling；fine-vessel adaptation

## Slide 6. LPT, Deformable Sampling, and Multi-scale Modeling

### Paragraph 1

**EN:** After the screening stage, the project moved into the LPT mainline.

**中文：** 经过筛选阶段后，项目进入 LPT 主线。

**关键词：** screening result；LPT mainline；next stage

### Paragraph 2

**EN:** The original LPT module uses fixed high-level interaction. However, retinal vessels are curved and slender, so fixed sampling may not align well with vessel geometry. To address this, I tested deformable sampling, where offsets allow the sampling positions to adapt to local vessel structure.

**中文：** 原始 LPT 使用固定的高层交互方式。但视网膜血管弯曲且细长，固定采样可能无法很好贴合血管几何形状。为了解决这一点，我测试了 deformable sampling，通过 offsets 让采样位置适应局部血管结构。

**关键词：** fixed interaction；curved vessels；slender structure；deformable sampling；offsets；geometry alignment

### Paragraph 3

**EN:** In the experiments, 4-point deformable LPT improved the F1-score to 0.7958. This showed that adaptive sampling was helpful for the task. I also tested modulation, which increased the tendency to detect vessels, but it could reduce precision. This again reflected the sensitivity-precision trade-off.

**中文：** 实验中，4-point deformable LPT 将 F1-score 提升到 0.7958，说明自适应采样对任务有帮助。我也测试了 modulation，它增强了模型检测血管的倾向，但可能降低 precision。这再次体现了 sensitivity 与 precision 的权衡。

**关键词：** 4-point deformable LPT；F1 0.7958；adaptive sampling；modulation；detection tendency；trade-off

### Paragraph 4

**EN:** Then I introduced multi-scale modeling. The idea was to reuse shallow details together with deeper semantic information, so that the model could balance local fine-vessel details and broader structural context. Overall, this stage showed that vessel-aware sampling and multi-scale information were more promising than direct full-module migration.

**中文：** 随后我引入多尺度建模。思路是结合浅层细节和深层语义信息，让模型在局部细血管细节和更大范围结构上下文之间取得平衡。总体来看，这一阶段说明，面向血管的采样和多尺度信息比直接迁移完整模块更有前景。

**关键词：** multi-scale modeling；shallow details；deep semantics；local detail；structural context；vessel-aware sampling

## Slide 7. Coordinate Attention and Dynamic Snake Convolution

### Paragraph 1

**EN:** This slide introduces the two most important retained structural ideas: Coordinate Attention and Dynamic Snake Convolution.

**中文：** 这一页介绍最终保留下来的两个重要结构思想：Coordinate Attention 和 Dynamic Snake Convolution。

**关键词：** retained modules；Coordinate Attention；DSConv；core ideas

### Paragraph 2

**EN:** Coordinate Attention adds direction-aware positional recalibration. In retinal vessel segmentation, position and direction are important because vessels have elongated structures. Coordinate Attention helps the network emphasize informative spatial responses after multi-scale aggregation.

**中文：** Coordinate Attention 加入方向感知的位置重标定。在视网膜血管分割中，位置和方向很重要，因为血管是细长结构。Coordinate Attention 帮助网络在多尺度聚合之后强调更有信息量的空间响应。

**关键词：** direction-aware；positional recalibration；elongated vessels；spatial response；after multi-scale aggregation

### Paragraph 3

**EN:** Dynamic Snake Convolution provides a different inductive bias. Instead of treating convolution as a rigid local operation, it uses a trajectory-style sampling pattern that is more suitable for slender and curved objects. This is especially relevant for fine retinal vessels, where continuity along a vessel path matters.

**中文：** Dynamic Snake Convolution 提供了另一种归纳偏置。它不是把卷积看作刚性局部操作，而是使用类似轨迹的采样模式，更适合细长和弯曲目标。这对细小视网膜血管尤其相关，因为沿血管路径的连续性非常重要。

**关键词：** inductive bias；trajectory sampling；slender objects；curved objects；vessel path；continuity

### Paragraph 4

**EN:** The observed effect was that sensitivity increased strongly, which means the model recovered more vessel pixels. However, precision dropped in some settings, which means more false positives were also introduced. Therefore, this stage improved fine-vessel recovery, but it also made false-positive control more important.

**中文：** 观察到的效果是 sensitivity 明显提高，说明模型恢复了更多血管像素。但是在一些设置下 precision 会下降，说明假阳性也增加了。因此，这一阶段提升了细血管恢复能力，但也让假阳性控制变得更重要。

**关键词：** sensitivity increase；more vessel pixels；precision drop；false positives；fine-vessel recovery；control needed

## Slide 8. Post-processing and clDice Exploration

### Paragraph 1

**EN:** After MS-DSConv and Coordinate Attention, the remaining problem was mainly output refinement.

**中文：** 在 MS-DSConv 和 Coordinate Attention 之后，剩下的主要问题是输出精修。

**关键词：** after MS-DSConv；after CA；output refinement

### Paragraph 2

**EN:** The retained refinement method was connected-component filtering. The idea is simple: very small isolated components are more likely to be false positives than real vessel structures. In the final retained setting, the threshold X equals 20. This light post-processing step reduced small isolated noise and improved the final F1-score to 0.8027.

**中文：** 最终保留的精修方法是连通域过滤。思路很简单：非常小的孤立连通区域更可能是假阳性，而不是真实血管结构。在最终设置中，阈值 X=20。这个轻量后处理减少了小孤立噪声，并把最终 F1-score 提升到 0.8027。

**关键词：** connected-component filtering；small isolated components；false positives；X=20；light post-processing；F1 0.8027

### Paragraph 3

**EN:** I also explored clDice because it is designed to emphasize topology and skeleton-like structure, which seems suitable for vessel segmentation. However, in the representative setting with X equals 20, clDice increased sensitivity in some cases but reduced precision and F1-score. Therefore, it was explored but not retained in the final scheme.

**中文：** 我也探索了 clDice，因为它强调拓扑和类似骨架的结构，看起来适合血管分割。但是在代表性设置 X=20 下，clDice 在某些情况下提高 sensitivity，却降低 precision 和 F1-score。因此，它被探索过，但没有保留在最终方案中。

**关键词：** clDice；topology；skeleton；sensitivity up；precision down；not retained

### Paragraph 4

**EN:** This slide shows an important point: improving sensitivity alone is not sufficient. For this task, the final output must balance thin-vessel recovery and false-positive suppression.

**中文：** 这一页说明了一个重要观点：单纯提高 sensitivity 不够。对于这个任务，最终输出必须在细血管恢复和假阳性抑制之间取得平衡。

**关键词：** sensitivity not enough；balance；thin-vessel recovery；false-positive suppression；final output

## Slide 9. Quantitative Results

### Paragraph 1

**EN:** This slide summarizes the quantitative results under the unified later-stage comparison.

**中文：** 这一页总结统一后期比较设置下的定量结果。

**关键词：** quantitative results；unified comparison；later-stage protocol

### Paragraph 2

**EN:** The nnU-Net baseline F1-score was 0.7891. The full PA-Net migration dropped to 0.7782, which confirmed that direct transplantation was not suitable. Deformable LPT improved the result to 0.7958. Multi-scale and attention-based variants then pushed the performance further.

**中文：** nnU-Net 基线 F1-score 为 0.7891。完整 PA-Net 迁移降到 0.7782，说明直接迁移不适合。Deformable LPT 将结果提升到 0.7958。随后，多尺度和注意力相关变体进一步推动性能提升。

**关键词：** baseline 0.7891；PA-Net 0.7782；direct migration not suitable；Deformable LPT 0.7958；multi-scale；attention

### Paragraph 3

**EN:** The final retained scheme, which combines MS-DSConv, Coordinate Attention, and light connected-component post-processing with X equals 20, achieved an F1-score of 0.8027. This is an absolute F1 gain of 0.0136 over the later-stage nnU-Net baseline.

**中文：** 最终保留方案结合 MS-DSConv、Coordinate Attention，以及 X=20 的轻量连通域后处理，F1-score 达到 0.8027。相比后期 nnU-Net 基线，这是 0.0136 的绝对 F1 提升。

**关键词：** final scheme；MS-DSConv；CA；X=20；F1 0.8027；gain 0.0136

### Paragraph 4

**EN:** The final sensitivity and precision were 0.8059 and 0.8035, respectively. This indicates that the final solution did not only increase detection tendency; it also brought the output back to a more balanced state.

**中文：** 最终 sensitivity 和 precision 分别为 0.8059 和 0.8035。这说明最终方案不是单纯提高检测倾向，而是把输出拉回到更平衡的状态。

**关键词：** sensitivity 0.8059；precision 0.8035；not only detection；balanced output

### Paragraph 5

**EN:** I would describe the improvement as modest but meaningful. It is modest because nnU-Net is already strong and the absolute gain is not very large. It is meaningful because the gain follows a consistent technical route and is obtained under the same comparison protocol.

**中文：** 我会把这个提升描述为“幅度不大，但有意义”。说它幅度不大，是因为 nnU-Net 已经很强，绝对增益并不大；说它有意义，是因为这个提升遵循了一条一致的技术路线，并且是在相同比较协议下得到的。

**关键词：** modest but meaningful；strong nnU-Net；absolute gain；consistent route；same protocol

## Slide 10. Qualitative Results

### Paragraph 1

**EN:** The qualitative results help explain the numerical behavior.

**中文：** 定性结果可以帮助解释数值表现。

**关键词：** qualitative results；explain metrics；visual evidence

### Paragraph 2

**EN:** In the representative cases, the baseline predictions are relatively clean, but they often miss weak and thin vessel branches. This is consistent with a conservative prediction pattern.

**中文：** 在代表性样例中，基线预测相对干净，但经常漏掉弱的、细小的血管分支。这与保守预测模式一致。

**关键词：** baseline clean；miss weak branches；thin vessels；conservative pattern

### Paragraph 3

**EN:** The later models, especially the MS-DSConv plus Coordinate Attention design, recover more continuous branches and more fine vessel structures. In some local regions, the vessel map becomes more complete and better connected.

**中文：** 后期模型，尤其是 MS-DSConv 加 Coordinate Attention，恢复了更多连续分支和细血管结构。在一些局部区域中，血管图更完整，连通性也更好。

**关键词：** later models；MS-DSConv + CA；continuous branches；fine vessels；more complete；better connected

### Paragraph 4

**EN:** However, these qualitative results also show why post-processing is needed. When the model becomes more sensitive, it may generate isolated noisy components. The connected-component filtering step helps reduce this scattered noise without changing the main vessel structure too aggressively.

**中文：** 但是，定性结果也说明为什么需要后处理。当模型更敏感时，可能产生孤立噪声。连通域过滤可以减少这种分散噪声，同时不会过度改变主要血管结构。

**关键词：** post-processing needed；more sensitive；isolated noise；connected-component filtering；main vessel preserved

### Paragraph 5

**EN:** So the qualitative interpretation is consistent with the quantitative results: the final method improves fine-vessel recovery, but the improvement must be controlled by output refinement.

**中文：** 因此，定性解释与定量结果是一致的：最终方法提升了细血管恢复能力，但这种提升必须通过输出精修来控制。

**关键词：** qualitative-quantitative consistency；fine-vessel recovery；output refinement；controlled improvement

## Slide 11. Limitations and Future Work

### Paragraph 1

**EN:** This project still has several limitations.

**中文：** 这个项目仍然有几个局限性。

**关键词：** limitations；honest evaluation；future direction

### Paragraph 2

**EN:** First, the validation scope is limited to the public benchmark conditions used in this study. This means the current result should not be directly interpreted as proof of clinical robustness.

**中文：** 第一，验证范围仍然限制在本研究使用的公开基准条件下。这意味着当前结果不能直接解释为临床鲁棒性的证明。

**关键词：** public benchmark；limited validation；not clinical proof；robustness

### Paragraph 3

**EN:** Second, false-positive control still partly relies on rule-based post-processing. Although this is effective and lightweight, it would be better to move more of this control into the model or the training objective.

**中文：** 第二，假阳性控制仍然部分依赖基于规则的后处理。虽然这种方式有效且轻量，但更理想的方向是把更多控制能力转移到模型本身或训练目标中。

**关键词：** false-positive control；rule-based post-processing；lightweight；model-level control；training objective

### Paragraph 4

**EN:** Third, the mechanisms behind DSConv, Coordinate Attention, and multi-scale interaction still need deeper interpretability analysis. The experiments show useful behavior, but more analysis is needed to explain when and why each module works.

**中文：** 第三，DSConv、Coordinate Attention 和多尺度交互背后的机制仍需更深入的可解释性分析。实验显示它们有用，但还需要更多分析来解释每个模块何时、为何起作用。

**关键词：** interpretability；DSConv；CA；multi-scale interaction；when and why

### Paragraph 5

**EN:** Finally, some fine branches and low-response regions remain difficult. This is expected because the weakest vessels are close to the boundary between anatomical structure and image noise.

**中文：** 最后，一些细小分支和低响应区域仍然很难处理。这是可以预期的，因为最弱血管接近解剖结构和图像噪声之间的边界。

**关键词：** fine branches；low response；weak vessels；anatomy-noise boundary；remaining difficulty

### Paragraph 6

**EN:** For future work, I would test broader data from different devices, pathologies, and annotation styles. I would also analyze nnU-Net preprocessing more specifically for retinal images, explore learned false-positive control, and evaluate the method with more clinically oriented evidence.

**中文：** 未来工作方面，我会测试来自不同设备、病理情况和标注风格的更广泛数据；也会更具体地分析 nnU-Net 预处理流程在眼底图像中的作用，探索可学习的假阳性控制，并用更接近临床场景的证据评估方法。

**关键词：** broader data；devices；pathologies；annotation styles；nnU-Net preprocessing；learned false-positive control；clinical evidence

## Slide 12. Conclusion and Q&A

### Paragraph 1

**EN:** To conclude, this project identified a modest but stable improvement path within nnU-Net for fine retinal vessel segmentation.

**中文：** 总结来说，本项目在 nnU-Net 框架内找到了一条针对细小视网膜血管分割的、幅度不大但较稳定的改进路径。

**关键词：** conclusion；modest improvement；stable path；within nnU-Net；fine vessels

### Paragraph 2

**EN:** The final retained scheme is MS-DSConv plus Coordinate Attention, followed by light connected-component post-processing. The final F1-score is 0.8027, compared with the baseline value of 0.7891.

**中文：** 最终保留方案是 MS-DSConv 加 Coordinate Attention，并在输出端加入轻量连通域后处理。最终 F1-score 是 0.8027，而基线值是 0.7891。

**关键词：** final scheme；MS-DSConv + CA；connected-component post-processing；F1 0.8027；baseline 0.7891

### Paragraph 3

**EN:** The main contribution is not a single large performance jump. Instead, the contribution is a controlled experimental route: starting from nnU-Net, screening migrated modules, refining the LPT-centered structure, improving vessel-aware modeling, and finally balancing sensitivity with false-positive control.

**中文：** 本项目的主要贡献不是某一个很大的性能跳跃，而是一条受控实验路线：从 nnU-Net 出发，筛选迁移模块，细化以 LPT 为中心的结构，提升面向血管的建模能力，最后平衡 sensitivity 和假阳性控制。

**关键词：** controlled route；not large jump；screen modules；LPT-centered refinement；vessel-aware modeling；balance sensitivity

### Paragraph 4

**EN:** Overall, the study shows that fine retinal vessel segmentation benefits from structural modeling that respects vessel continuity and from careful output refinement. At the same time, the method remains a research-stage improvement and should be further validated before any clinical use.

**中文：** 总体来看，研究表明细小视网膜血管分割受益于尊重血管连续性的结构建模，也受益于谨慎的输出精修。同时，该方法仍属于研究阶段的改进，在任何临床使用前都需要进一步验证。

**关键词：** vessel continuity；structural modeling；output refinement；research-stage；further validation；clinical use

### Paragraph 5

**EN:** That is the end of my presentation. Thank you for your attention, and I welcome your questions.

**中文：** 我的汇报到此结束。感谢各位老师的聆听，欢迎提出问题。

**关键词：** closing；thank you；questions；Q&A
