%% UESTC4003 Control - Computer Lab Exercises Solution
% This script covers Lab 1, Lab 2, and Lab 3.
clear all; close all; clc;

%% ========================================================================
%  COMPUTER LAB 1
%  ========================================================================
disp('--- Starting Lab 1 ---');

% --- Exercise 1A: Evaluate complex function via vectors ---
s_val = -3 + 4i;
num_1a = conv([1 1], [1 2]);     % (s+1)(s+2)
den_1a = conv([1 0], conv([1 3], [1 4])); % s(s+3)(s+4)
G_1a = tf(num_1a, den_1a);

% Calculate Magnitude and Angle manually/using MATLAB
G_at_s = polyval(num_1a, s_val) / polyval(den_1a, s_val);
mag_1a = abs(G_at_s);
phase_1a = rad2deg(angle(G_at_s));

fprintf('Lab 1A: Magnitude = %.4f, Phase = %.4f degrees\n', mag_1a, phase_1a);

% --- Exercise 1B: Root Locus Analysis ---
% 5.1 Root Locus for G(s)
figure(1);
rlocus(G_1a);
title('Lab 1B - 5.1: Root Locus of G(s)');
grid on;

% 5.2 Unity Feedback System
% G(s) = K(s-1)(s-2) / (s^2 + 4s + 16)
num_52 = conv([1 -1], [1 -2]);
den_52 = [1 4 16];
G_52 = tf(num_52, den_52);

figure(2);
rlocus(G_52);
title('Lab 1B - 5.2: Root Locus of G(s) with Unity Feedback');
grid on;

% Note: Use rlocfind(G_52) in command window to find crossings interactively
% [k, poles] = rlocfind(G_52); 

% Plot 0.45 damping ratio line
sgrid(0.45, []);

% Plot both 5.1 and 5.2(a) in the same diagram
figure(3);
hold on;
rlocus(G_1a);
rlocus(G_52);
title('Lab 1B - 5.2(e): Both Root Loci');
legend('System 5.1', 'System 5.2');
hold off;


%% ========================================================================
%  COMPUTER LAB 2
%  ========================================================================
disp('--- Starting Lab 2 ---');

% --- Exercise 2A: Analysis of Dynamic Models ---
% 3.1 Continuous model H(s) = (4s+1)/(s^2+3s+5)
num_H = [4 1];
den_H = [1 3 5];
H_sys = tf(num_H, den_H);
[wn, z] = damp(H_sys); 
% Note: damp() returns wn and zeta for the poles.
fprintf('Lab 2A - 3.1: Natural Frequencies and Damping Ratios found.\n');

% 3.2 MIMO System (Definition)
% H(s) = [1, (s-1)/(s^2+s+3); 1/(s+1), (s+2)/(s-3)]
% Defined using individual TFs
H11 = tf(1, 1);
H12 = tf([1 -1], [1 1 3]);
H21 = tf(1, [1 1]);
H22 = tf([1 2], [1 -3]);
H_mimo = [H11, H12; H21, H22];

% DC Gain
dc_gain_mimo = dcgain(H_mimo);
disp('Lab 2A - 3.2: DC Gain of MIMO system:');
disp(dc_gain_mimo);

% 3.3 Bode Plot
figure(4);
bode(H_mimo);
title('Lab 2A - 3.3: Bode Plot of MIMO System');
grid on;

% 3.4 Second Order System G(s)
zeta_req = 0.35;
wn_req = 3.4;
num_G_new = wn_req^2;
den_G_new = [1, 2*zeta_req*wn_req, wn_req^2];
G_new = tf(num_G_new, den_G_new);

% 3.5 Closed Loop Model (Fig 2: G forward, H feedback)
% Using H from 3.1 (scalar) and G from 3.4
sys_cl = feedback(G_new, H_sys);

% 3.6 Poles, Zeros and Impulse Response
figure(5);
pzmap(sys_cl);
title('Lab 2A - 3.6: Pole-Zero Map of Closed Loop System');
grid on;

figure(6);
impulse(sys_cl);
title('Lab 2A - 3.6: Impulse Response');
grid on;

% 3.7 Response to r = e^-0.5t
% We can use lsim for custom inputs
t = 0:0.01:10;
u = exp(-0.5*t);
figure(7);
lsim(sys_cl, u, t);
title('Lab 2A - 3.7: Response to r = e^{-0.5t}');
grid on;

% --- Exercise 2B: Electrical Networks (Symbolic Solver) ---
disp('Lab 2B: Solving Mesh Equations symbolically...');
syms s I1 I2 I3 V
% Based on visual inspection of T-network/Bridge in Figure 3
% Assumptions (Needs verification with diagram specific connectivity):
% Mesh 1 (Left): V, 2s, 1(shared with M2), 3s(shared with M3)
% Mesh 2 (Top Right): 1(shared with M1), 1, 4s(shared with M3)
% Mesh 3 (Bottom Right): 3s(shared with M1), 4s(shared with M2), 1/s
% WARNING: Topology assumed based on standard exercises.
% Mesh Eq Matrix Z * I = V_vec
% Loop 1: (2s + 1 + 3s)I1 - 1*I2 - 3s*I3 = V
% Loop 2: -1*I1 + (1 + 1 + 4s)I2 - 4s*I3 = 0
% Loop 3: -3s*I1 - 4s*I2 + (3s + 4s + 1/s)I3 = 0

Eq1 = (2*s + 1 + 3*s)*I1 - 1*I2 - 3*s*I3 == V;
Eq2 = -1*I1 + (2 + 4*s)*I2 - 4*s*I3 == 0;
Eq3 = -3*s*I1 - 4*s*I2 + (7*s + 1/s)*I3 == 0;

[Sol_I1, Sol_I2, Sol_I3] = solve([Eq1, Eq2, Eq3], [I1, I2, I3]);
TF_I3_V = simplify(Sol_I3 / V);
disp('Transfer Function I3(s)/V(s):');
pretty(TF_I3_V);


%% ========================================================================
%  COMPUTER LAB 3
%  ========================================================================
disp('--- Starting Lab 3 ---');

% --- Exercise 3A: State Space Representation ---
% TF: G(s) = (s+2)(s+4) / ( (s+1)(s+3)(s+5) )
num_3a = conv([1 2], [1 4]);
den_3a = conv([1 1], conv([1 3], [1 5]));

% 2.2 Define A, B, C, D manually or creates SS object
% Let's create the object from TF
sys_tf_3a = tf(num_3a, den_3a);
sys_ss_3a = ss(sys_tf_3a);

% 2.3 Convert to Controller Canonical Form
% MATLAB's 'canon' usually gives modal. For controller canonical, 
% we often construct it manually from the TF coefficients.
% Den = s^3 + 9s^2 + 23s + 15
% Num = s^2 + 6s + 8
[A_cc, B_cc, C_cc, D_cc] = tf2ss(num_3a, den_3a);
% Note: tf2ss gives Controller Canonical in Control Textbook convention
% (top row for Matlab usually, but standard form has bottom row coeffs).
% MATLAB tf2ss returns a form where A is companion matrix (top row).
sys_cc = ss(A_cc, B_cc, C_cc, D_cc);

% 2.4 Convert to Phase Variable Form
% Transformation P = [0 0 1; 0 1 0; 1 0 0] (reverse order of states)
P = [0 0 1; 0 1 0; 1 0 0];
Ap = inv(P)*A_cc*P;
Bp = inv(P)*B_cc;
Cp = C_cc*P;
Dp = D_cc;
sys_phase = ss(Ap, Bp, Cp, Dp);
disp('Lab 3A - 2.4: Phase Variable A matrix:');
disp(Ap);

% 2.5 Convert to Parallel Form (Modal Form)
sys_modal = canon(sys_cc, 'modal');

% 2.6/2.7 Observer Canonical
% Often A_obs = A_cont', B_obs = C_cont', C_obs = B_cont'
A_obs = A_cc';
B_obs = C_cc';
C_obs = B_cc';
D_obs = D_cc;
sys_obs = ss(A_obs, B_obs, C_obs, D_obs);

% --- Exercise 3A Part 3.0: SS to TF & Feedback ---
A_3 = [0 1 0; 0 0 1; -1 -2 -3];
B_3 = [10; 0; 0];
C_3 = [1 0 0];
D_3 = 0;
sys_3_ss = ss(A_3, B_3, C_3, D_3);
sys_3_tf = tf(sys_3_ss);

% 3.3 Pole Placement
% Desired poles: -2+4j, -2-4j, -10
des_poles = [-2+4i, -2-4i, -10];
K_place = place(A_3, B_3, des_poles);
disp('Lab 3A - 3.3: State Feedback Gain K:');
disp(K_place);


% --- Exercise 3B: Discrete-Time Analysis (Simulation) ---
disp('Lab 3B: Discrete Simulation running...');
% 4.1 Proportional Control
Ts = 1; % Assumption, sample time not specified, assume 1 or normalized
Gp_z = tf([3], [1 -0.6], Ts, 'Variable', 'z^-1');
Kp = 0.1;
% Closed loop T_cl = (Kp*Gp) / (1 + Kp*Gp)
sys_cl_d = feedback(Kp * Gp_z, 1);

t_d = 0:20; % 20 steps
ref = 300 * ones(size(t_d)); % Desired rate 300
[y_prop, t_out] = step(300 * sys_cl_d, 20); % Scaled step

% 4.4 Integral Control
% C(z) = kI / (1 - z^-1)
kI = 0.1;
C_int = tf(kI, [1 -1], Ts, 'Variable', 'z^-1');
sys_cl_int = feedback(C_int * Gp_z, 1);
[y_int, ~] = step(300 * sys_cl_int, 20);

figure(8);
subplot(2,1,1);
stairs(t_d, y_prop);
title('Lab 3B: Proportional Control Response');
ylabel('Ventilation Rate'); grid on;

subplot(2,1,2);
stairs(t_d, y_int);
title('Lab 3B: Integral Control Response');
ylabel('Ventilation Rate'); grid on;

disp('All exercises completed.');