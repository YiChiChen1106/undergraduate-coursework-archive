# Assignment1_with_ref_answer

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

1. In a simple RGB image, the R, G, and B component images have the horizontal intensity profiles shown in the following diagram. What color would a person see in the middle column of this image? [2 marks]

Ans:   

Answer with the above image shown      [2 marks]

Grey green/light green/bright green…     [2 marks]

Green                               [1 mark]

Other answer                         [0 mark]

==============reference code to generate the above image===================

A = zeros(512,512,3);

r = 1:-1/511:0;

l = ones(512,1);

A(:,:,1) = l*r;

g1 = 0:1/255:1;g2 = 1:-1/255:0;

g = [g1,g2];

A(:,:,2) = l*g;

b = 0:1/511:1;

A(:,:,3) = l*b;

imshow(A)