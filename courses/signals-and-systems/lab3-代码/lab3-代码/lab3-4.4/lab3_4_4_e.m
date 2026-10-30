clc
clear all
a1=[1 3];
b1=3;
w=linspace(0,10);
H1=freqs(b1,a1,w);
H1mag=abs(H1);
wc=3;
[b2,a2]=butter(2,wc,'s');
H=freqs(b2,a2,w);
figure(1);
subplot(2,1,1)
plot(w,H1mag);
xlabel('frequncy (rad/s)');
ylabel('magnitude of H1');
title('the magnitude of H1');
subplot(2,1,2)
plot(w,abs(H));
xlabel('frequncy (rad/s)');
ylabel('magnitudes of H');
title('the magnitudes of the frequency response of the Butterworth filter');
grid on;
