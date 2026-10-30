% part 1
clear all;
close all;
clc;
%% Physical Parameters
g = 9.81; % m/s^2, gravitational constant
m = 5; % kg, mass
l = 0.4; % m, length
c = 0.7; % Nm/rad, damping coefficient
I = m * (l/2)^2; % moment of inertia
%% Frequency and Time-Domain Characteristics
wn = sqrt(m * g * l / (2 * I)); % undamped natural frequency in rad/s
xi = c / (2 * I * wn); % damping ratio
wd = wn * sqrt(1 - xi^2); % damped natural frequency in rad/s
tr = 1 / wd * atan(sqrt(1 - xi^2) / xi); % rise time
tp = pi / wd; % peak time
ts = 3 / (xi * wn); % settling time
Mp = 100 * exp(-xi * wn * tp); % overshoot
% Display info
sprintf('wn = %.4f rad/s', wn)
sprintf('wd = %.4f rad/s', wd)
sprintf('xi = %.4f', xi)
sprintf('tr = %.4f s', tr)
sprintf('tp = %.4f s', tp)
sprintf('ts = %.4f s', ts)
sprintf('Mp = %.2f %%', Mp)
%% Original Plant Transfer Function
sys = tf(1/I, [1 2*xi*wn wn^2]); % G(s)
%% PID Gains (adjustable)
Kp = 5;
Ki = 0;
Kd = 0;
% Define PID terms
sysKp = tf(Kp, 1);
sysKi = tf(Ki, [1 0]);
sysKd = tf([Kd 0], 1);
% Open-loop TF with PID controller: OLTF = (Kp + Ki/s + Kd*s) * G(s)
OLTF = (sysKp + sysKi + sysKd) * sys;
% Closed-loop TF: CLTF = OLTF / (1 + OLTF)
CLTF = OLTF / (1 + OLTF);
%% Step Response
%% Step Response (with and without controller)
t = 0:1e-6:5;
figure(1);
h = stepplot(sys, CLTF, t); % 同时画出 sys 和 CLTF 的响应
title('Step Response Comparison: Uncontrolled Plant vs. PID-Controlled System');
legend('Original Plant (sys)', 'PID Controlled System (CLTF)');
grid on;
%% Pole-Zero Map
figure(2)
pzplot(CLTF)
legend('CLTF')
title('Pole–Zero Map of Closed-Loop PID System')
%% Plot poles of OLTF and CLTF separately (subplot)
p_oltf = pole(OLTF);
p_cltf = pole(CLTF);
figure(3);
%% Pole-Zero Maps: OLTF vs CLTF (Subplots)
subplot(2,1,1)
pzplot(OLTF)
title('Pole-Zero Map of Open-loop Transfer Function (OLTF)')
legend('OLTF')
grid off
subplot(2,1,2)
pzplot(CLTF)
title('Pole-Zero Map of Closed-loop Transfer Function (CLTF)')
legend('CLTF')
grid off
%% Damping and Performance Info
damp(CLTF)
stepinfo(CLTF)
%% Export for Simulink
J = I; % plant inertia 