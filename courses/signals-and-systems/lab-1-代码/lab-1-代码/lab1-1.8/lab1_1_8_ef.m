clc
clear
x1 = str2sym('cos(pi*t/5)');
x2 = str2sym('sin(pi*t/5)');
x3 = str2sym('exp(i*2*pi*t/3) + exp(i*pi*t)');

syms a t real;  % 确保 a 和 t 定义为符号变量，并且 t 是实数
E1 = int(x1^2, [-a, a]);  % 计算 x1^2 在 [-a,a] 区间内的能量
E2 = int(x2^2, [-a, a]);  % 计算 x2^2 在 [-a,a] 区间内的能量

x3c = conj(x3);  % 使用 conj 函数获取 x3 的共轭复数
E3 = int(x3*x3c, [-a, a]);  % 计算 x3*x3c 在 [-a,a] 区间内的能量

P1 = E1 / (2 * a);  % 平均功率 P1 = E1 / (2a)
P2 = E2 / (2 * a);  % 平均功率 P2 = E2 / (2a)
P3 = E3 / (2 * a);  % 平均功率 P3 = E3 / (2a)

% 绘制功率图
figure(1);
subplot(3,1,1);
ezplot(P1, [0.1, 60]);  % 绘制 P1 随 a 变化的图
xlabel('a');
ylabel('Pa for x1');
title('Plot of Pa for x1');

subplot(3,1,2);
ezplot(P2, [0.1, 60]);  % 绘制 P2 随 a 变化的图
xlabel('a');
ylabel('Pa for x2');
title('Plot of Pa for x2');

subplot(3,1,3);
ezplot(P3, [0.1, 60]);  % 绘制 P3 随 a 变化的图
xlabel('a');
ylabel('Pa for x3');
title('Plot of Pa for x3');

% 计算 P1 和 P2 的和，并化简
sumP = P1 + P2;
r = simplify(sumP);  % 化简 sumP
disp('Simplified sum of P1 and P2:');
disp(r);
