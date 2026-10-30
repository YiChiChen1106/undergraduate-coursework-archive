clc
clear all
load splat
y=y(1:8192);
N=8192;
fs=8192;
Y=fftshift(fft(y));
w=[-pi:2*pi/N:pi-pi/N]*fs;
plot(w,abs(Y));
xlabel('w');
ylabel('|Y|');
title('The plot of the magnitude of the continuous-time Fourier transform');
Y1=conj(Y);
y1=ifft(fftshift(Y1));
y1=real(y1);
sound(y1,fs)