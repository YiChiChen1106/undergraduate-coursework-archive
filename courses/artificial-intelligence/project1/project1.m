% Main program with multiple runs
num_runs = 10; % Number of runs
num_generations = 2000; % Set number of generations
final_results = zeros(num_runs, 1); % Store the final best value for each run
all_best_values = zeros(num_generations, num_runs); % Store all best fitness values for each generation for all runs
best_components = zeros(num_runs, 8); % Store the best component values for each run

for run = 1:num_runs
    % Initialize parameters
    pop_size = 300; % Increase population size to 300
    crossover_rate = 0.9; % Increase crossover probability
    mutation_rate = 0.3; % Increase mutation probability
    penalty_coefficient = 1000; % Constraint penalty coefficient
    shrink_value = 0.5; % Reduce mutation shrink value
    SUBPOP = 1; % Number of subpopulations, set to 1 indicating no subpopulation division

    % Load Standard Component Values
    data = load('StandardComponentValues.mat'); % Load the standard component values for resistors and thermistors
    Res = data.Res; % Resistor values
    ThBeta = data.ThBeta; % Thermistor beta values
    ThVal = data.ThVal; % Thermistor resistance values
    Tdata = linspace(0, 100, 27); % Create Tdata with at least 27 points to ensure Vdata length matches requirement
    Vdata = linspace(0, 1, 27); % Create Vdata with enough length to match objective function requirement

    % Define variable bounds FieldDR using standard component values
    FieldDR = [1, 1, 1, 1, 1, 1, 1, 1; 
               length(Res), length(ThBeta), length(ThVal), length(Res), length(ThVal), length(ThBeta), length(ThVal), length(ThBeta)];
    % Use indices in FieldDR to match component arrays' sizes

    % Define mutation options MutOpt, including mutation rate and shrink value
    MutOpt = [mutation_rate, shrink_value];

    % Step 1: Initialize population
    population = crtrp(pop_size, FieldDR); 

    % Evolution main loop
    best_value = zeros(num_generations, 1); % To store the best fitness value of each generation
    for gen = 1:num_generations
        fitness_values = zeros(pop_size, 1);

       % Step 2: Fitness evaluation (call objectiveFunction)
        for i = 1:pop_size
            % Round values to ensure valid integer indices and bounds
            component_values = round(population(i, :));

            % Ensure indices are within valid bounds for each component array
            component_values(1:4) = max(1, min(component_values(1:4), length(Res)));
            component_values(5:6) = max(1, min(component_values(5:6), length(ThVal)));
            component_values(7:8) = max(1, min(component_values(7:8), length(ThBeta)));

            % Calculate voltage response for the current component values
            voltage_response = voltageCurve(Tdata, component_values, Res, ThVal, ThBeta); 

            % Adjust voltage_response length if necessary to match Vdata length
            if length(voltage_response) < length(Vdata)
                voltage_response = [voltage_response, zeros(1, length(Vdata) - length(voltage_response))];
            elseif length(voltage_response) > length(Vdata)
                voltage_response = voltage_response(1:length(Vdata));
            end

            % Evaluate fitness using the objective function
            fitness_values(i) = objectiveFunction(component_values, Res, ThVal, ThBeta, Tdata, voltage_response);

            % Apply penalty from component constraints
            penalty = componentConstraints(component_values, Res, ThVal, ThBeta);
            fitness_values(i) = fitness_values(i) + penalty; % Add penalty to fitness value
        end

        % Step 3: Apply penalty
        penalty_values = zeros(pop_size, 1);
        for i = 1:pop_size
            component_values = round(population(i, :));
            temp_curve = tempCompCurve(component_values, Tdata); 
            voltage_response = voltageCurve(Tdata, component_values, Res, ThVal, ThBeta);
            constraint_violations = max(0, temp_curve - voltage_response); 
            penalty_values(i) = penalty_coefficient * sum(constraint_violations);
        end

        % Final fitness values (with penalty)
        fitness_values = fitness_values + penalty_values;

        % Step 4: Fitness ranking
        ranked_fitness = ranking(fitness_values);

        % Step 5: Selection
        selected_indices = rws(ranked_fitness, pop_size); 
        selected_parents = population(selected_indices, :);

        % Step 6: Crossover
        offspring = xovmp(selected_parents, crossover_rate); 

        % Step 7: Mutation
        mutated_offspring = mutbga(offspring, FieldDR, MutOpt);

        % Step 8: Reinsertion
        population = reins(population, mutated_offspring, SUBPOP, [1, 1.0], fitness_values);

        % Record the best fitness value for each generation
        best_value(gen) = min(fitness_values);
    end

    % Record the final best value of each run
    [final_results(run), best_index] = min(best_value);
    best_components(run, :) = population(best_index, :); % Store the best component values for each run
    all_best_values(:, run) = best_value;

    fprintf('Run %d: Best Fitness Value = %f\n', run, final_results(run));
end

% Summarize the results of 10 runs
fprintf('\nSummary of 10 Runs:\n');
fprintf('Best Value: %f\n', min(final_results));
fprintf('Worst Value: %f\n', max(final_results));
fprintf('Mean Value: %f\n', mean(final_results));
fprintf('Median Value: %f\n', median(final_results));

% Plot convergence trend using the median value of the 10 runs
median_convergence = median(all_best_values, 2);
figure;
plot(1:num_generations, median_convergence);
xlabel('Generation');
ylabel('Median Best Fitness Value');
title('Convergence Trend of GA Using Median Value of 10 Runs');

% Plot the fitted curve using the best component values from all runs
[~, best_run] = min(final_results);
best_component_values = best_components(best_run, :);
voltage_response_best = voltageCurve(Tdata, best_component_values, Res, ThVal, ThBeta);

figure;
plot(Tdata, Vdata, 'b-', 'DisplayName', 'Target Curve'); % Plot target curve
hold on;
plot(Tdata, voltage_response_best, 'r--', 'DisplayName', 'Fitted Curve'); % Plot fitted curve
xlabel('Temperature (°C)');
ylabel('Voltage Response');
title('Fitted Curve vs Target Curve');
legend;
grid on;

% Constraint function: componentConstraints
function penalty = componentConstraints(x, Res, ThVal, ThBeta)
    % Ensure that each component value is a valid index within the standard component arrays.
    % Each variable should be an integer and within the valid range of available components.

    % Extract the number of standard components available
    numRes = length(Res);
    numThVal = length(ThVal);
    numThBeta = length(ThBeta);

    % Constraint violations: count how many indices are out of range
    penalty = 0;

    % Check resistor index ranges
    if any(x(1:4) < 1 | x(1:4) > numRes)
        penalty = penalty + 1; % Increment penalty for each resistor index out of range
    end

    % Check thermistor value index ranges
    if any(x(5:6) < 1 | x(5:6) > numThVal)
        penalty = penalty + 1; % Increment penalty for each thermistor value index out of range
    end

    % Check thermistor beta index ranges
    if any(x(7:8) < 1 | x(7:8) > numThBeta)
        penalty = penalty + 1; % Increment penalty for each thermistor beta index out of range
    end

    % You may also add other domain-specific constraints as required.
    
    % Multiply penalty by a high value (e.g., 1000) to discourage constraint violations.
    penalty = penalty * 1000;
end

