clc
clear
nx1=[0:24];
nh=[0:14];
nx2=[2:24];
x=[zeros(1,2) (1/2).^(nx2-2)];
h=[ones(1,15)];
y=conv(h,x);
ny=[0:length(y)-1];
stem(ny,y);
title('y[n]=x[n]*h[n],When 2<=n<=16,the outputs of conv are real.');
xlabel('n');
ylabel('y[n]');
grid on;