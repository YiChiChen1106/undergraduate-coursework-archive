clc
clear all
a=[1 -3];
b=[1 2 5];
zs=roots(b)
ps=roots(a)
figure;
plot(real(zs),imag(zs),'o');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram');
hold on;
plot(real(ps),imag(ps),'x');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram');
axis([-4 4 -4 4]);
grid on;