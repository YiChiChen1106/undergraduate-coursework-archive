clc
clear all
x3=[ones(1,8) zeros(1,24)];
a3=(1/32)*fft(x3);
n=[0:31];
x3_2=0;
x3_8=0;
x3_12=0;
x3_all=0;
for k=1:2
x3_2=x3_2+a3(k+1)*exp(i*k*pi*n/16)+a3(-k+33)*exp(i *(-k)*pi*n/16);
end
x3_2=x3_2+a3(1);
for k=1:8
x3_8=x3_8+a3(k+1)*exp(i*k*pi*n/16)+a3(-k+33)*exp(i *(-k)*pi*n/16);
end
x3_8=x3_8+a3(1);
for k=1:12
x3_12=x3_12+a3(k+1)*exp(i*k*pi*n/16)+a3(-k+33)*exp(i*(-k)*pi*n/16);
end
x3_12=x3_12+a3(1);
for k=1:15
x3_all=x3_all+a3(k+1)*exp(i*k*pi*n/16)+a3(-k+33)*exp(i*(-k)*pi*n/16);
end
x3_all=x3_all+a3(1)+a3(17)*exp(i*16*pi*n/16);
figure(1);
subplot(2,2,1);
stem(n,x3_2);
xlabel('n');
ylabel('x3_2[n]');
title('The figure of the signal x3_2[n]');
grid on;
subplot(2,2,2);
stem(n,x3_8);
xlabel('n');
ylabel('x3_8[n]');
title('The figure of the signal x3_8[n]');
grid on;
subplot(2,2,3);
stem(n,x3_12);
xlabel('n');
ylabel('x3_12[n]');
title('The figure of the signal x3_12[n]');
grid on;
subplot(2,2,4);
stem(n,x3_all);
xlabel('n');
ylabel('x3_all[n]');
title('The figure of the signal x3_all[n]');
grid on;
figure(2);
stem(n,x3,'filled');
xlabel('n'),ylabel('x3[n] & x3_2[n] & x3_8[n] & x3_12[n] & x3_all[n]'),grid on;
hold on;
stem(n,x3_2,'g');
hold on;
stem(n,x3_8,'b*');
hold on;
stem(n,x3_12,'k');
hold on;
stem(n,x3_all,'r');
title('x3[n](filled),x3_2[n](green),x3_8[n](blue star),x3_12[n](black) and x3_all[n](red)');
legend on