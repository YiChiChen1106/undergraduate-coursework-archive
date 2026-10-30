# Assignment4

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

[student-id-redacted]

陈一驰

For the target in Figure 1, the most robust method is Color-based Segmentation. First, preprocess the image with a Gaussian Blur to reduce noise, then convert it from RGB to HSV color space to isolate the specific red hue range. Generate a binary mask via thresholding, use morphological operations (opening/closing) to clean the mask, and finally extract the contour to calculate the target's center using image moments.

To detect targets in both figures, a Shape and Contrast-based Algorithm is required. Convert the images to grayscale and apply Otsu’s thresholding or Canny edge detection to separate high-contrast man-made objects from the natural background. Extract contours and apply geometric filtering: use circularity analysis to identify the rings in Figure 2 and polygon approximation to identify the rectangular board in Figure 1, then compute the centroid of the identified shape.

These traditional algorithms have the advantage of low computational cost and high speed, but suffer from the disadvantage of poor robustness against changing lighting conditions and partial occlusions. Before application in an airborne system, extra work is needed: Coordinate Transformation to map pixel coordinates to GPS locations using drone attitude data, Image Stabilization to counter flight vibrations, and Multi-frame Tracking (e.g., Kalman Filter) to ensure stable target locking.