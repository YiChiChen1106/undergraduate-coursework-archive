
clc
clear all
n=0:64;
x=(sin((pi/4).*(n-32)))./((pi/4).*(n-32));
x(33)=1;
figure;
stem(n,x);
xlabel('n');
ylabel('x[n]');
title('the figure of x[n]');
X=fftshift(fft(x,256));
w = linspace(0,2*pi,256);
mag=abs(X);
figure;
plot(w,mag);
set(gca,'Xtick',[0,pi/4,pi/2,3*pi/4,pi,5*pi/4,3*pi/2,7*pi/4,2*pi]);
set(gca,'XTickLabel',{'-pi','-3pi/4','-pi/2','-pi/4',' 0','pi/4','pi/2','3*pi/4','pi'});
xlabel('w');
ylabel('Magnitude');
title('The figure of the magnitude of DTFT of the signal x[n]');
