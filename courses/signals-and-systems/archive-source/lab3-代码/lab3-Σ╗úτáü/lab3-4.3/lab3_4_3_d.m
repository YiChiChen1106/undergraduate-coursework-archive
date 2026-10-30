clc
clear all
load splat
y=y(1:8192);
N=8192;
fs=8192;
Y=fftshift(fft(y));
w=[-pi:2*pi/N:pi-pi/N]*fs;
Y3=exp(j.*phase(Y));
y3=ifft(fftshift(Y3));
y3=real(y3);
sound(y3,fs)