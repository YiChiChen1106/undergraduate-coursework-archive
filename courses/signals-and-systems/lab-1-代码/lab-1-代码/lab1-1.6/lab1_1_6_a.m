clc
syms T t   % 明确定义符号变量 T 和 t
x = sin(2*pi*t/T);  % 定义符号表达式
x5 = subs(x, T, 5);  % 用 5 替换符号 T
ezplot(x5, [0, 10]);  % 绘制 x5 的图像
xlabel('t');
ylabel('x5');
grid on;
