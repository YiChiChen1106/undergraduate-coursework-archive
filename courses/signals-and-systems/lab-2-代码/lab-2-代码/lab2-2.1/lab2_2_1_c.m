clc
clear
x=[ones(1,6)];
nx=[0:5];
h=[0:5];
nh=[0:5];
y=conv(h,x);
nx=[0:length(x)-1];
nh=[0:length(h)-1];
ny=[0:length(y)-1];
figure(1);
subplot(2,1,1);
stem(nx,x);
xlabel('n');
ylabel('x[n]');
title('the figure of the signal x[n] ');
grid on;
subplot(2,1,2);
stem(nh,h);
xlabel('n');
ylabel('h[n]');
title('the figure of the signal h[n] ');
grid on;
figure(2);
stem(ny,y);
xlabel('n');
ylabel('y[n]');
title('the figure of the signal y[n]=x[n] * h[n]');
grid on;
