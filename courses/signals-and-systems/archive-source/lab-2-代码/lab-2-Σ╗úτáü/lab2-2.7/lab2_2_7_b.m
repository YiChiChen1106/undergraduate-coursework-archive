clc
clear
N=4;
M=5;
nx=[0:4];
nh=[0:3];
h=[1 0 0 1];
x=[1 0 0 0 1];
subplot(3,1,1);
stem(nh,h);
xlabel('n');
ylabel('h[n]');
title('The figure of the signal h[n]');
grid on;
subplot(3,1,2);
stem(nx,x);
xlabel('n');
ylabel('x[n]');
title('The figure of the signal x[n]');
grid on;
y=conv(h,x);
ny=[0:length(y)-1];
subplot(3,1,3);
stem(ny,y);
xlabel('n');
ylabel('y[n]');
title('The figure of the signal y[n]=h[n]*x[n]');
grid on;