clc
clear
a1=[1 -3/5];
b1=[1];
n=[0:19];
x1=[1 zeros(1,19)];
h1=filter(b1,a1,x1);
figure(1);
stem(n,h1);
xlabel('n');
ylabel('h1[n]');
title('The figure of the signal h1[n]');
grid on;
y2(1)=1;
for k=2:20
y2(k)=((3/5)^(k-1))*y2(k-1)+x1(k);
end
h2=[];
for m=0:19
h2(end+1)=y2(m+1);
end
figure;
stem(n,h2);
xlabel('n');
ylabel('h2[n]');
title('The figure of the signal h2[n]');
grid on;