clc
clear
x1 = str2sym('cos(pi*t/5)');
x2 = str2sym('sin(pi*t/5)');
x3 = str2sym('exp(i*2*pi*t/3) + exp(i*pi*t)');

syms a t real;  % 确保变量 a 和 t 定义为符号变量，并且是实数
E1 = int(x1^2, [-a, a]);  % 计算 x1^2 在 [-a,a] 范围内的能量
E2 = int(x2^2, [-a, a]);  % 计算 x2^2 在 [-a,a] 范围内的能量

x3c = conj(x3);  % 使用 conj 函数来获取 x3 的复共轭
E3 = int(x3*x3c, [-a, a]);  % 计算 x3*x3c 在 [-a,a] 范围内的能量

% 绘制能量图
figure(1);
subplot(3,1,1);
ezplot(E1, [0, 30]);  % 绘制 E1 相对于 a 的图像
xlabel('a');
ylabel('Ea for x1');
title('Plot of Ea for x1');

subplot(3,1,2);
ezplot(E2, [0, 30]);  % 绘制 E2 相对于 a 的图像
xlabel('a');
ylabel('Ea for x2');
title('Plot of Ea for x2');

subplot(3,1,3);
ezplot(E3, [0, 30]);  % 绘制 E3 相对于 a 的图像
xlabel('a');
ylabel('Ea for x3');
title('Plot of Ea for x3');

% 计算固定区间的能量
Et1 = int(x1^2, [-5, 5]);  % 计算 x1^2 在 [-5,5] 范围内的能量
Et2 = int(x2^2, [-5, 5]);  % 计算 x2^2 在 [-5,5] 范围内的能量
ET3 = int(x3*x3c, [-3, 3]);  % 计算 x3*x3c 在 [-3,3] 范围内的能量

Et3 = eval(ET3);  % 计算并评估 ET3 的值
disp(Et1);
disp(Et2);
disp(Et3);
