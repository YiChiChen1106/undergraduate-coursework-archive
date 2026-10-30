# Assignment4_with_ref_answer

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

6. Drones currently play an important role in Russia-Ukraine war in either air strike or battlefield situation awareness. The images below show typical targets for drone or helicopter. [10]

     a) Design an image processing algorithm that can automatically detect and locate the center of target in Figure 1. Describe your method and steps explicitly. You may use a flow chart. [3]

     b) Design an algorithm that can detect and locate the center of target in both Figure 1 and Figure 2. [3]

     c) Discuss the advantages and disadvantages of the above algorithms. Is there any extra work that needs to be done before the algorithm is applied in the airborne electronic system?  [4]

Figure 1

Figure 2

Ref ans:

Basic:

a) Use red color information and employ color component segmentation (thresholding in the red channel). Locate the center by averaging the x and y coordinates of detected red pixels.               

b) Use edge detection methods (1st or 2nd order derivatives), edge linking, Hough transform (in single or multiple channels). 

Use red color information, detect the red flags, locate the big one by size comparison. 

Use a combination of the above methods                                                                                     

c) Consider about the time complexity of the proposed algorithm.

Plus:

Considered about noise and apply smoothing filters in a).           [+1]

Apply geometric transformations to generate a bird-of-view image of fig.2 for preprocessing.         [+2]

Using template matching, or any distance transform such as chamfer distance. [+1]

Using character detection method in natural scene. [+2]

Consider about similar object or scene that looks like a cross.  [+1]