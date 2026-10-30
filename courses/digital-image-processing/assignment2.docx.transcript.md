# assignment2

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

3.14 The images shown below are quite different, but their histograms are the same. Suppose that each image is blurred with a 3 x 3 average mask. 

Would the histograms of the blurred images still be equal? Explain.[3] 

Answer: No, the histograms would no longer be equal. Although the original histograms are the same, the two images have different spatial distributions of gray levels. A histogram only describes the overall frequency of gray levels, not the spatial arrangement of pixels. When applying a 3 × 3 average (lowpass) filter, each pixel value is replaced by the average of its neighbors. The result depends on the local structure of the image, which differs between the two images. Therefore, after blurring, the histograms will not be identical.

If your answer is yes, sketch the histogram, if it is no, sketch the two histograms. [2] 

3.17 Discuss the limiting effect of repeatedly applying a 3 × 3 lowpass spatial filter to a digital image.You may ignore border effects.Is this effect different from applying a 5 × 5 filter?[5] 

Answer:

Limiting effect of repeated 3 × 3 filtering: Each application of the filter smooths the image by attenuating high-frequency components. Repeated application causes progressive blurring, and in the limit, the image converges to a constant image where all pixel values are equal to the global average gray level.

Difference compared to a 5 × 5 filter: A 5 × 5 filter averages over a larger neighborhood, producing stronger smoothing in a single step. It removes details more quickly and converges to the constant image faster. However, the ultimate limiting result is the same for both filters: a flat image of constant intensity.