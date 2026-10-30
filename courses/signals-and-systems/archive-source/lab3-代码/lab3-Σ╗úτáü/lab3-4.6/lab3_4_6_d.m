clc
clear all
load ctftmod.mat;
y=dash.*cos(2*pi*f1*t(1:length(dash)));
yo=lsim(bf,af,y,t(1:length(dash)));
figure;
subplot(2,1,1);
plot(y);
xlabel('t');
ylabel('y(t)');
title('The figure of the signal y(t)');
grid on;
subplot(2,1,2);
plot(yo);
xlabel('t');
ylabel('yo(y)');
title('The figure of the signal yo(t)');
grid on;