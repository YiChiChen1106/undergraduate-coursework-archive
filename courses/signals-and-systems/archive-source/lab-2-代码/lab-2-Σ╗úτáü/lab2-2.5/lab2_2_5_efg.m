clc
clear all
%.....(e).....%
a1=[1 -3/5];
b1=[1];
n=[0:19];
x1=[ones(1,20)];
s1=filter(b1,a1,x1);
figure(1);
subplot(2,1,1);
stem(n,s1);
xlabel('n');
ylabel('s1[n]');
title('The figure of the signal s1[n]');
grid on;


y2(1)=1;
for k=2:20
y2(k)=((3/5).^(k-1))*y2(k-1)+x1(k);
end
s2=[];
for m=0:19
s2(end+1)=y2(m+1);
end
subplot(2,1,2);
stem(n,s2);
xlabel('n');
ylabel('s2[n]');
title('The figure of the signal s2[n]');
grid on;
%........(f).........%

x0=[1 zeros(1,19)];
h1=filter(b1,a1,x0);
y0(1)=1;
for k=2:20
y0(k)=((3/5)^(k-1))*y0(k-1)+x0(k);
end
h2=[];
for m=0:19
h2(end+1)=y0(m+1);
end
z1=conv(h1,x1);
Z1=[];
for i1=1:20
Z1(end+1)=z1(i1);
end
figure(2);
subplot(2,1,1);
stem(n,Z1,'b');
xlabel('n');
ylabel('z1[n]');
title('The figure of the signal z1[n]');

z2=conv(h2,x1);
Z2=[];
for i2=1:20
Z2(end+1)=z2(i2);
end
subplot(2,1,2);
stem(n,Z2);
xlabel('n');
ylabel('z2[n]');
title('The figure of the signal z2[n]');
%........(g).........%
figure(3);
stem(n,s1,'b');
hold on;
stem(n,Z1,'k');
xlabel('n');
ylabel('s1[n]&z1[n]');
title('The figure of the signals s1[n](blue) and z1[n](black)');
grid on;
figure(4);
subplot(2,1,1);
stem(n,s2);
xlabel('n');
ylabel('s2[n]');
title('The figure of the signal s2[n]');
grid on;
subplot(2,1,2);
stem(n,Z2);
xlabel('n');
ylabel('z2[n]');
title('The figure of the signal z2[n]');
grid on;
