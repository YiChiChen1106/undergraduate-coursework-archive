clc
clear
x2=[ones(1,6) zeros(1,5)];
nx2=[0:10];
h=[0:5];
a=1;
y2=filter(h,a,x2);
figure(1);
subplot(2,1,1);
stem(nx2,x2);
xlabel('n');
ylabel('x2[n]');
title('the figure of x2[n]');
grid on;
subplot(2,1,2);
stem([0:10],y2);
xlabel('n');
ylabel('y2[n]');
title('the figure of y2[n]');
grid on;