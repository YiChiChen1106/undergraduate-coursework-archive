clc
clear
x1 = str2sym('cos(pi*t/5)');  % 使用 str2sym 进行字符串转符号表达式
x2 = str2sym('sin(pi*t/5)');
m = str2sym('exp(i*2*pi*t/3)');
n = str2sym('exp(i*pi*t)');
x3 = m + n;

figure(1);
subplot(2,1,1);
ezplot(x1, [0,20]);  % 绘制 x1(t)
xlabel('t');
ylabel('x1(t)');
grid on;

subplot(2,1,2);
ezplot(x2, [0,20]);  % 绘制 x2(t)
xlabel('t');
ylabel('x2(t)');
grid on;

figure(2);
subplot(2,1,1);
ezplot(real(x3), [0,12]);  % 绘制 x3 的实部
xlabel('t');
ylabel('The real components of x3(t)');
grid on;

subplot(2,1,2);
ezplot(imag(x3), [0,12]);  % 绘制 x3 的虚部
xlabel('t');
ylabel('The imaginary components of x3(t)');
grid on;
