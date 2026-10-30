clc
clear all
n=[0:40];
h=[];
syms w
for i=0:1:40
h(i+1)=(1/(2*pi))*int(j*exp(-j*20*w+j*w*i),w,-pi,0)+(1/(2*pi))*int(-j*exp(-j*20*w+j*w*i),w,0,pi);
end
figure;
stem(n,h);
xlabel('n');
ylabel('h_2_0[n]');
title('The figure of the impulse response h_2_0[n]');
grid on;
%.......(e)........%
figure;
subplot(2,1,1);
plot(abs(fft(h,256)));
xlabel('w');
ylabel('The amplitude');
title('The figure of the magnitude of the DTFT of the windowed and shifted impulse response');
grid on;
subplot(2,1,2);
plot(unwrap(fftshift(angle(fft(h,256)))));
xlabel('w');
ylabel('The phase');
title('The figure of the phase of the DTFT of the windowed and shifted impulse response');
grid on;