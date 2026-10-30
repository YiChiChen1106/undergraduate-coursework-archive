# Assignment3

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Q4.1 Explain qualitatively what effect the following transformations will have on the Discrete Fourier Transform of an image: 

random shuffling of the intensity values of the image pixels, 

convolution of the image with a Gaussian kernel of very tiny (nearly zero) standard deviation, 

answer：

random shuffling of the intensity values of the image pixels: Randomly shuffling the pixel intensities will destroy the spatial structure and correlation inherent in the original image. A typical image has most of its energy concentrated in the low-frequency components of its Discrete Fourier Transform (DFT), which appear at the center of the spectrum. After shuffling, the image becomes spatially similar to white noise. This scrambling will cause the energy in the frequency domain to be spread out across the entire spectrum, resulting in a significant increase in the magnitude of high-frequency components and a loss of the original low-frequency dominance.

convolution of the image with a Gaussian kernel of very tiny (nearly zero) standard deviation: A Gaussian kernel with a standard deviation approaching zero approximates an impulse function (or Dirac delta function). In the spatial domain, convolving an image with an impulse function is an identity operation, meaning the image itself will remain virtually unchanged. According to the Convolution Theorem, convolution in the spatial domain is equivalent to element-wise multiplication in the frequency domain. The Fourier transform of an impulse function is a constant value (a flat spectrum, approximately 1 at all frequencies). Therefore, multiplying the image's original DFT by this constant, flat spectrum will result in the DFT remaining almost unchanged