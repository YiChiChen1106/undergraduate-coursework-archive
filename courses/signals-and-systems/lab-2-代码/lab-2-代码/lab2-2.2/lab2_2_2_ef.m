clc
clear
x=[ones(1,6)];
nx=[0:5];
b=[0:5];
a=1;
ny=[0:5];
y=filter(b,a,x);
figure(1);
subplot(2,1,1);
stem(nx,x);
xlabel('n');
ylabel('x[n]');
title('the figure of x[n]');
grid on;
subplot(2,1,2);
stem(ny,y);
xlabel('n');
ylabel('y[n]');
title('the figure of y[n]');
grid on;


