clc
clear
nh=[-1 0 1];
h=[2 0 -2];
nx=[0 1 2];
x=[1 0 1];
k1=nh(1)+nx(1);
k2=length(h)+length(x)-2;
ny=[k1:k1+k2];
y=conv(h,x);
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
subplot(3,1,3);
stem(ny,y);
xlabel('n');
ylabel('y[n]');
title('The figure of the signaly[n]=x[n]*h[n]');
grid on;
