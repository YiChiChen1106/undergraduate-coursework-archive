clc
clear all
load ctftmod.mat;
z=[dash dash dot dot];
figure(1);
plot(z);
xlabel('t');
ylabel('Z');
title('The figure of the letter Z in Morse code.');
grid on;
figure(2);
freqs(bf,af);

