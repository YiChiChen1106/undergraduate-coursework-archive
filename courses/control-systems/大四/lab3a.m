%% Exercise 3A: State Space Representation & Pole Placement
clc; clear; close all;

disp('==============================================');
disp('          Exercise 3A: MATLAB Results         ');
disp('==============================================');

%% --- Part 2.1 - 2.3: Controller Canonical Form ---
% Transfer Function: G(s) = (s^2 + 6s + 8) / (s^3 + 9s^2 + 23s + 15)
num = [1 6 8];
den = [1 9 23 15];

disp(' ');
disp('--- Part 2.3: Controller Canonical Form Matrices (tf2ss) ---');
[A_c, B_c, C_c, D_c] = tf2ss(num, den);
sys_ss_controller = ss(A_c, B_c, C_c, D_c);

disp('A_c = '); disp(A_c);
disp('B_c = '); disp(B_c);
disp('C_c = '); disp(C_c);
disp('D_c = '); disp(D_c);

%% --- Part 2.5: Parallel Form (Modal Form) ---
disp(' ');
disp('--- Part 2.5: Parallel Form Matrices (Jordan/Modal) ---');
% Using 'modal' to diagonalize the system
sys_parallel = canon(sys_ss_controller, 'modal');
[A_p, B_p, C_p, D_p] = ssdata(sys_parallel);

disp('A_p = '); disp(A_p);
disp('B_p = '); disp(B_p);
disp('C_p = '); disp(C_p);

%% --- Part 2.6: Observer Canonical Form ---
disp(' ');
disp('--- Part 2.6: Observer Canonical Form Matrices ---');
% Observer form is the transpose of Controller form
A_o = A_c';
B_o = C_c';
C_o = B_c';
D_o = D_c;

disp('A_o = '); disp(A_o);
disp('B_o = '); disp(B_o);
disp('C_o = '); disp(C_o);

%% --- Part 3.0 - 3.2: System Definition & SS to TF ---
disp(' ');
disp('==============================================');
disp('       Part 3.0 - 3.3: Pole Placement         ');
disp('==============================================');

A_3 = [0 1 0; 0 0 1; -1 -2 -3];
B_3 = [10; 0; 0];
C_3 = [1 0 0];
D_3 = 0;
sys_3_ss = ss(A_3, B_3, C_3, D_3);

% Part 3.2: Convert SS object to Transfer Function
disp(' ');
disp('--- Part 3.2: Converted Transfer Function ---');
sys_3_tf = tf(sys_3_ss);
sys_3_tf % Display the transfer function

%% --- Part 3.3: Pole Placement ---
disp(' ');
disp('--- Part 3.3: Calculated State Feedback Gain K ---');
% Desired poles: -2+4j, -2-4j, -10
des_poles = [-2+4i, -2-4i, -10];
K_place = place(A_3, B_3, des_poles);

disp('K = '); disp(K_place);