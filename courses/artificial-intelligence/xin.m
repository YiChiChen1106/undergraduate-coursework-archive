t = linspace(0, 2*pi, 1000);
x = 16*sin(t).^3;
y = 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t);

figure;
fill(x, y, 'r'); % 填充红色
axis equal;

xlabel('x');
ylabel('y');
grid on;
