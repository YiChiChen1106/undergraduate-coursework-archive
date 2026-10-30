clc
clear all
n=0:64;
x=(sin((pi/4).*(n-32)))./((pi/4).*(n-32));
x(33)=1;
x1=cos((pi/2).*n).*x;
X1=fftshift(fft(x1,256));
mag1=abs(X1);
w = linspace(0,2*pi,256);
figure;
plot(w,mag1);
set(gca,'Xtick',[0,pi/4,pi/2,3*pi/4,pi,5*pi/4,3*pi/2,7*pi/4,2*pi]);
set(gca,'XTickLabel',{'-pi','-3pi/4','-pi/2','-pi/4',' 0','pi/4','pi/2','3*pi/4','pi'});
xlabel('w');
ylabel('Magnitude');
title('The figure of the magnitude of DTFT of the signal x_1[n]=x[n]cos(w_cn)');