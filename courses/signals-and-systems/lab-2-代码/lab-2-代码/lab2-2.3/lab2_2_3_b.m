clc;
clear;

% Define the time vector
t = 0:1:10;

% Define the transfer function parameters
b = 1; 
a = [1 0.5];

% Step and impulse responses
s = step(b, a, t);
h = impulse(b, a, t);

% Define symbolic variable for t
syms t_sym;
h2_sym = 2 * (1 - exp(-t_sym/2)) * heaviside(t_sym);

% Derivative of the symbolic function
h2_deriv_sym = diff(h2_sym, t_sym);

% Plot the step response
figure(1);
plot(t, s);
xlabel('t');
ylabel('s(t)');
title('The step response of dy(t)/dt = -0.5y(t) + x(t)');

% Plot the impulse response and the derivative of eq2.14
figure(2);
subplot(2, 1, 1);
plot(t, h);
xlabel('t');
ylabel('h(t)');
title('The impulse response of dy(t)/dt = -0.5y(t) + x(t)');

% Plot the symbolic derivative
subplot(2, 1, 2);
fplot(h2_deriv_sym, [0 10]);
xlabel('t');
ylabel('h2''(t)');
title('Plot of the derivative of eq2.14');
