% 导入
data1 = vdd0;
data2 = vdd1;
data3 = vdd2;
data4 = vdd3;
data5 = vdd4;
% 绘制5条曲线
figure;
hold on;
plot(data1(:,1), data1(:,2), '-x','LineWidth', 1, 'DisplayName', 'VDD=0V');
plot(data2(:,1), data2(:,2), '-o','LineWidth', 1, 'DisplayName', 'VDD=1V');
plot(data3(:,1), data3(:,2), '-rd','LineWidth', 1, 'DisplayName', 'VDD=2V');
plot(data4(:,1), data4(:,2), 'b','LineWidth', 1, 'DisplayName', 'VDD=3V');
plot(data5(:,1), data5(:,2), 'LineWidth', 1, 'DisplayName', 'VDD=20V');
% 设置图像的标签和标题
xlabel('VGS');
ylabel('ID');
title('ID VS VGS');
legend('show');
grid on;
hold off;