clc
clear all
load splat
y=y(1:8192);
N=8192;
fs=8192;
Y=fftshift(fft(y));
w=[-pi:2*pi/N:pi-pi/N]*fs;
Y2=abs(Y);
y2=ifft(fftshift(Y2));
y2=real(y2);
sound(y2,fs)
