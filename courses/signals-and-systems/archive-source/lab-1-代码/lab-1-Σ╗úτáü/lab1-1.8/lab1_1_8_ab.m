clc
clear
x1=sym('cos(pi*t/5)');
x2=sym('sin(pi*t/5)');
m=sym('exp(i*2*pi*t/3)');
n=sym('exp(i*pi*t)');
x3=m+n;
figure(1);
subplot(2,1,1);
ezplot(x1,[0,20]),xlabel('t'),ylabel('x1(t)'),grid on;
subplot(2,1,2);
ezplot(x2,[0,20]),xlabel('t'),ylabel('x2(t)'),grid on;
figure(2)
subplot(2,1,1);
ezplot(compose('real(x3)',x3),[0,12]);xlabel('t');ylabel('The real componentsof x3(t)');
grid on;
subplot(2,1,2);
ezplot(compose('imag(x3)',x3),[0,12]);xlabel('t');ylabel('The imaginary components of x3(t)');
grid on;