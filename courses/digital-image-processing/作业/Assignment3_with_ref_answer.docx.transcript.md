# Assignment3_with_ref_answer

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Q4.1 Explain qualitatively what effect the following transformations will have on the Discrete Fourier Transform of an image:

(a) random shuffling of the intensity values of the image pixels,

Answer: will significantly increase the high frequency content due to considerable fluctuation between neighboring intensity values, and lower frequency components (except for DC value) will reduce in magnitude.

However, in the case of some special images, such as a binary image with pixel values changing alternatively from 0 to 1 in either direction, things will be totally different. Random shuffling will decrease instead of increase the high frequency content.

(b) convolution of the image with a Gaussian kernel of very tiny (nearly zero) standard deviation,

Answer: will have nearly no effect on the DFT as the image is being convolved with just a delta function.