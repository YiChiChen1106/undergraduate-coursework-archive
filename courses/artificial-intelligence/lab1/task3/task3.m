% Define Ackley function parameters
a = 20;
b = 0.2;
c = 2 * pi;

% Define the Ackley function for 10-dimensional optimization
ackleyFunc = @(x) -a * exp(-b * sqrt(sum(x.^2) / 10)) - exp(sum(cos(c * x)) / 10) + a + exp(1);

% Set the number of dimensions
n = 10;

% Define search range for each dimension
lb = -15 * ones(1, n);  % Lower bound
ub = 30 * ones(1, n);   % Upper bound

% Configure options for the genetic algorithm
options = optimoptions('ga', 'Display', 'iter', 'PlotFcn', @gaplotbestf);

% Use genetic algorithm to find the minimum value of the Ackley function
[x_opt, fval] = ga(ackleyFunc, n, [], [], [], [], lb, ub, [], options);

% Display the optimized results
disp('Optimal decision variables (x):');
disp(x_opt);  % Display optimal values for decision variables
disp('Optimal objective function value:');
disp(fval);  % Display the minimum value achieved for Ackley function
