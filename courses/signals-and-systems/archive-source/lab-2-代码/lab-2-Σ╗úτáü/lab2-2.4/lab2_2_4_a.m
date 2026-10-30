clc
clear
nx1=[0:4];
x1=[1 1 1 1 1];
h1=[1 -1 3 0 1];
h2=[0 2 5 4 -1];
subplot(3,1,1);
stem(nx1,x1);
xlabel('n');
ylabel('x1[n]');
title('The figure of the signal x1[n]');
grid on;
subplot(3,1,2);
stem(nx1,h1);
xlabel('n');
ylabel('h1[n]');
title('The figure of the signal h1[n]');
grid on;
subplot(3,1,3);
stem(nx1,h2);
xlabel('n');
ylabel('h2[n]');
title('The figure of the signal h2[n]');
grid on;