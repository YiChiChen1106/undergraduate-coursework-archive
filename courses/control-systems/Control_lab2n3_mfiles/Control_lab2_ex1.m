% Control_lab2_ex1.m
% Lab2 Task I: 二阶摆系统建模、时域响应与极点分析

clear; close all; clc;

%% 1. 基础参数
m0 = 5;        % 质量 (kg)
l0 = 0.4;      % 摆长 (m)
c0 = 0.5;      % 阻尼系数 (N·m·s/rad)
g  = 9.81;     % 重力加速度 (m/s^2)

%% 2. 计算惯量、ω_n、ζ
I0  = m0*(l0/2)^2;                          % 转动惯量
wn0 = sqrt( (m0*g*l0/2) / I0 );             % 无阻尼固有频率
xi0 = c0 / (2*I0*wn0);                      % 阻尼比
wd0 = wn0*sqrt(1 - xi0^2);                  % 阻尼振荡频率

%% 3. 构造标准二阶传递函数
sys0 = tf( wn0^2, [1, 2*xi0*wn0, wn0^2] );

%% 4. 单位阶跃响应 & 性能指标
figure;
step(sys0);
title('Unit-step Response (m=5, l=0.4, c=0.5)');
grid on;

info0 = stepinfo(sys0);
fprintf('\n【Base case】\n');
fprintf('  Rise time   : %.3f s\n', info0.RiseTime);
fprintf('  Peak time   : %.3f s\n', info0.PeakTime);
fprintf('  Settling time: %.3f s\n', info0.SettlingTime);
fprintf('  Overshoot   : %.2f %%\n', info0.Overshoot);

%% 5. 极点–零点图
figure;
pzmap(sys0);
title('Pole-Zero Map (base case)');
grid on;

%% 6. 参数敏感性分析
tests = { ...
  'm', [5, 10];      % 质量 m
  'l', [0.4, 0.8];   % 摆长 l
  'c', [0.5, 1.0]    % 阻尼 c
};

fprintf('\n【Sensitivity Analysis】\n');
for i = 1:size(tests,1)
  name = tests{i,1};
  vals = tests{i,2};
  for v = vals
    switch name
      case 'm'
        m = v; l = l0; c = c0;
      case 'l'
        m = m0; l = v; c = c0;
      case 'c'
        m = m0; l = l0; c = v;
    end
    I  = m*(l/2)^2;
    wn = sqrt((m*g*l/2)/I);
    xi = c/(2*I*wn);
    sys = tf(wn^2, [1, 2*xi*wn, wn^2]);
    info = stepinfo(sys);
    fprintf('  %s = %.2f → Tr=%.3f s, Tp=%.3f s, Ts=%.3f s, Mp=%.2f%%\n', ...
      name, v, info.RiseTime, info.PeakTime, info.SettlingTime, info.Overshoot);
  end
end


