clc
clear all
a1=[1 3];
b1=3;
figure(1);
freqs(b1,a1);
title('the magnitude and phase of H1');
w=linspace(0,10);
H1=freqs(b1,a1,w);
H1mag=abs(H1);
a2=[1 1/3];
b2=1/3;
figure(2);
freqs(b2,a2);
H2=freqs(b2,a2,w);
title('the magnitude and phase of H2');
H2mag=abs(H2);
figure(3);
subplot(2,1,1)
plot(w,H1mag);
xlabel('frequncy (rad/s)');
ylabel('magnitude of H1');
title('the magnitude of H1');
subplot(2,1,2);
plot(w,H2mag);
xlabel('frequncy (rad/s)');
ylabel('magnitude of H2');
title('the magnitude of H2');
%........(c)..........%
t=linspace(0,5);
I1=impulse(b1,a1,t);
I2=impulse(b2,a2,t);
figure(4);
plot(t,I1);
xlabel('t');
ylabel('I1');
title('The figure of the impulse response of System 1');
grid on;
figure(5);
plot(t,I2);
xlabel('t');
ylabel('I2');
title('The figure of the impulse response of System 2');