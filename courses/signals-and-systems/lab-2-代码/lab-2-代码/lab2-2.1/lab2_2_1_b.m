clc
clear
x=[ones(1,6)];
y=conv(x,x);
ny=[0:length(y)-1];%L=6+6-1-1
stem(ny,y);
xlabel('n');
ylabel('y[n]');
title('the figure of the signal y[n]=x[n] * x[n]');
grid on;
