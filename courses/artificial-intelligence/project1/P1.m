format long;  % Set display format to avoid scientific notation

% Main program for running GA over 10 runs with varying parameters
num_runs = 10;  % Number of runs
num_generations = 2500;  % Fixed number of generations
final_results = zeros(num_runs, 1);  % Store the final best value for each run
all_best_values = zeros(num_generations, num_runs);  % Store best fitness values for each generation for all runs
params_table = cell(num_runs, 6);  % Initialize a 10x6 cell array to store parameters and final fitness values

% Load required variables
load('StandardComponentValues.mat');  % Load Res, ThVal, ThBeta, etc.
Tdata = -40:5:85;
Vdata = 1.026e-1 + -1.125e-4 * Tdata + 1.125e-5 * Tdata.^2;

lb = [1 1 1 1 1 1];  % Lower bounds
ub = [70 70 70 70 9 9];  % Upper bounds

% Define constraint function (example)
function c = nonlcon(x)
    c = x(1) + x(2) - 100;  % Constraint: x(1) + x(2) <= 100
end

% Running GA for 10 runs with different options for each run
for run = 1:num_runs
    % Vary GA parameters for each run, but keep the number of generations fixed at 2500
    population_size = 200; 
    crossover_frac = 0.1;  
    mutation_frac = 0.9;  

    % Store the parameters for this run in the table
    params_table{run, 1} = population_size;
    params_table{run, 2} = num_generations;  % Fixed number of generations (2500)
    params_table{run, 3} = crossover_frac;
    params_table{run, 4} = mutation_frac;

    % Set options for this run
    options = struct('PopulationSize', population_size, 'Generations', num_generations, ...
        'CrossoverFrac', crossover_frac, 'MutationFrac', mutation_frac);

    % Call myGA function with the current parameters and nonlcon as the constraint
    [xOpt, fVal, best_values] = myGA(@(x)objectiveFunction(round(x), Res, ThVal, ThBeta, Tdata, Vdata), ...
        6, [], [], [], [], lb, ub, @nonlcon, [], options);

    % Store the final best value of the current run
    final_results(run) = fVal;

    % Store the best value for each generation for this run (for plotting convergence)
    all_best_values(:, run) = best_values;  % Save the best value for each generation

    % Store the convergence value at the 2500th generation in params_table
    params_table{run, 5} = best_values(end);

    % Calculate and store the standard deviation of best values over generations for this run
    params_table{run, 6} = std(best_values);
end

% Summarize results: best, worst, average, and standard deviation of fVals over 10 runs
best_result = min(final_results);
worst_result = max(final_results);
mean_result = mean(final_results);
std_result = std(final_results);

% Display the summary table in a clean, aligned format
disp('Summary of 10 Runs:');
fprintf('%-20s %-20s %-20s %-20s\n', 'Best_Result', 'Worst_Result', 'Mean_Result', 'Std_Result');
fprintf('%-20.7f %-20.7f %-20.7f %-20.7f\n', best_result, worst_result, mean_result, std_result);


% Find the best run and generate the fitted curve
[~, best_run_idx] = min(final_results);  % Find the index of the best run
best_xOpt = round(xOpt);  % Ensure best solution parameters are integers
V_fitted = voltageCurve(Tdata, best_xOpt, Res, ThVal, ThBeta);  % Generate fitted curve

% Plot target curve and fitted curve
figure;
plot(Tdata, Vdata, '-*', 'DisplayName', 'Target Curve');  % Target curve
hold on;
plot(Tdata, V_fitted, '-o', 'DisplayName', 'Fitted Curve');  % Fitted curve
legend;
title('Target and Fitted Curve');
xlabel('Temperature (°C)');
ylabel('Voltage (V)');
hold off;

% Calculate and plot convergence trend showing the average of best values from all runs for each generation
avg_best_values = mean(all_best_values, 2);  % Calculate the average best values for each generation across runs

% Plot the convergence curve showing the average of best values from all runs
figure;
plot(1:num_generations, avg_best_values);
xlabel('Generation');
ylabel('Average Best Fitness Value');
title('Convergence Curve of GA (Average of 10 Runs)');



% Genetic Algorithm Function
function [xOpt, fVal, best_values] = myGA(objectiveFunc, nvars, A, b, Aeq, beq, lb, ub, nonlcon, intCon, options, varargin)
    % Initialize parameters
    pop_size = options.PopulationSize;
    num_generations = options.Generations;
    crossover_rate = options.CrossoverFrac;
    mutation_rate = options.MutationFrac;
    penalty_coefficient = 1000;  % Constraint penalty coefficient
    shrink_value = 0.5;
    SUBPOP = 1;  % Number of subpopulations

    % Define FieldDR for crtrp function (real-value representation)
    FieldDR = [lb; ub];  % Bounds for variables: rows are lower and upper bounds

    % Use crtrp to generate the initial population within the bounds
    population = crtrp(pop_size, FieldDR);

    % Record the best value for each generation
    best_values = zeros(num_generations, 1);  % Initialize each generation's best value array
    for gen = 1:num_generations
        % Calculate fitness values
        fitness_values = arrayfun(@(i) objectiveFunc(population(i, :), varargin{:}), 1:pop_size)';

        % Constraint penalty
        penalty_values = zeros(pop_size, 1);
        for i = 1:pop_size
            if ~isempty(nonlcon)
                % Call nonlinear constraint function
                constraint_violations = nonlcon(population(i, :));
                % Calculate total constraint violation and apply penalty
                total_violation = sum(max(0, constraint_violations));
                penalty_values(i) = penalty_coefficient * total_violation;
            end
        end
        fitness_values = fitness_values + penalty_values;

        % Selection of parents
        num_parents = pop_size;
        ranked_fitness = ranking(fitness_values);  % Sort with ranking function
        selected_indices = rws(ranked_fitness, num_parents);  % Select with rws function
        selected_parents = population(selected_indices, :);

        % Crossover operation
        offspring = xovmp(selected_parents, crossover_rate);  % Multi-point crossover xovmp

        % If offspring are fewer than the population size, add more individuals
        if size(offspring, 1) < pop_size
            num_additional = pop_size - size(offspring, 1);
            additional_individuals = population(randi([1, pop_size], num_additional, 1), :);
            offspring = [offspring; additional_individuals];
        end

        % Mutation operation
        MutOpt = [mutation_rate, shrink_value];
        mutated_offspring = mutbga(offspring, FieldDR, MutOpt);

        % Reinsertion
        InsOpt = [1, 1.0];
        population = reins(population, mutated_offspring, SUBPOP, InsOpt, fitness_values);

        % Record the best fitness value for the current generation
        best_values(gen) = min(fitness_values);
    end

    % Return final optimal solution
    [fVal, idx] = min(fitness_values);
    xOpt = population(idx, :);
end
