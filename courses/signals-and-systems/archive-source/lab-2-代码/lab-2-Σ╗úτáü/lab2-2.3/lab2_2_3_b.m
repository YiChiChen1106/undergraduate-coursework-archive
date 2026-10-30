clc
clear
t=[0:1:10];
b=1;
a=[1 0.5];
s=step(b,a,t);
h=impulse(b,a,t);
h2=sym('(2*(1-exp(-t/2)))*heaviside(t)'); % derivative of eq2.14
figure(1);
plot(t,s);
xlabel ('t');
ylabel('s(t)');
title('The step response of dy(t)/dt=-0.5y(t)+x(t)');
figure(2);
subplot(2,1,1);
plot(t,h);
xlabel ('t');
ylabel('h(t)');
title('The impulse response of dy(t)/dt=-0.5y(t)+x(t)');
subplot(2,1,2);
ezplot(diff(h2),[0:10]);
xlabel ('t');
ylabel('h2(t)');
title('Plot of the derivative of eq2.14');
