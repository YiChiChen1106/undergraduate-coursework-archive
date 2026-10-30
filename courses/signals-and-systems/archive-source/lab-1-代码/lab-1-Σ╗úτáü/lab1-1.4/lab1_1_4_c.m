clc
n=[0:3];
x=[1 0 2 1];
y=log(x);
subplot(2,1,1);
stem(n,x);xlabel('n');ylabel('x[n]');title('The figure of the signal x[n]');
grid on;
subplot(2,1,2);
stem(n,y);xlabel('n');ylabel('y[n]');title('Theh figure of the signal y[n]');
grid on;