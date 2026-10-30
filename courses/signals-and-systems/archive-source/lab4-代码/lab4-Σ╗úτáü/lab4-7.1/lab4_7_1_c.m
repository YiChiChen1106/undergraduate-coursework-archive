clc
clear all
n=[0:8191];
T=1/8192;
t=n./8192;
x=sin(2000*pi*t);
[X,w]=ctfts(x,T);
figure;
plot(w,abs(X));
xlabel('w');
ylabel('The amplitude');
title('The figure of the magnitude of the continuous-time Fourier transform of the resonstructed signal');
grid on;
% index=find(abs(X)>1);
% alpha=angle(X(index))*180/pi