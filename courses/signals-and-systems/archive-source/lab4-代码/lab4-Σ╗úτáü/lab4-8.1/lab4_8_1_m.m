clc
clear all
n=0:40;
h=[];
syms k
for i=0:1:40
h(i+1)=(1/(2*pi))*int(j*exp(-j*20*k+j*k*i),k,-pi,0)+(1/(2*pi))*int(-j*exp(-j*20*k+j*k*i),k,0,pi);
end
w = linspace(0,2*pi,256);
n1=0:64;
x=(sin((pi/4).*(n1-32)))./((pi/4).*(n1-32));
x(33)=1;
xh=conv(h,x);
xh=xh(21:85);
x2=sin((pi/2).*n1).*xh;
X2=fftshift(fft(x2,256));
mag3=abs(X2);
figure;
plot(w,mag3);
set(gca,'Xtick',[0,pi/4,pi/2,3*pi/4,pi,5*pi/4,3*pi/2,7*pi/4,2*pi]);
set(gca,'XTickLabel',{'-pi','-3pi/4','-pi/2','-pi/4',' 0','pi/4','pi/2','3*pi/4','pi'});
xlabel('w');
ylabel('Magnitude');
title('Plot of magnitude of X2');