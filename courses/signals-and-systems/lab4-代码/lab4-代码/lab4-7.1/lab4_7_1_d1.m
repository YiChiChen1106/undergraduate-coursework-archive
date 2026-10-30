clc
clear all
n=[0:8191];
T=1/8192;
t=n./8192;
x=sin(3000*pi*t);
figure;
subplot(2,1,1);
stem(n(1:50),x(1:50));
xlabel('n');
ylabel('x[n]');
title('The figure of the first fifty samples of x[n] versus n');
grid on;
subplot(2,1,2);
plot(t(1:50),x(1:50));
xlabel('t');
ylabel('x(t)');
title('The figure of the first fifty samples of x(t) versus the sampling times');
grid on;
[X,w]=ctfts(x,T);
figure;
plot(w,abs(X));
xlabel('w');
ylabel('The amplitude');
title('The figure of the magnitude of the continuous-time Fourier transform of the resonstructed signal');
grid on;