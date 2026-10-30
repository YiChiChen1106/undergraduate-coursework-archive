% Lab 2: Genetic Algorithm for Constrained Optimization
% MATLAB Code for Lab 2 by User

% Load GA Toolbox (Assuming the toolbox is in the current directory)
 

% Define problem parameters
nVars = 7; % Number of variables (7 dimensions)
lb = -10 * ones(1, nVars); % Lower bounds
ub = 10 * ones(1, nVars); % Upper bounds

% Genetic Algorithm parameters
popSize = 300; % Population size (increased for better diversity)
maxGenerations = 500; % Maximum number of generations (increased for more thorough search)
crossoverRate = 0.9; % Increased crossover rate for more diversity
initialMutationRate = 0.1; % Increased initial mutation rate for more exploration
finalMutationRate = 0.05; % Increased final mutation rate for more exploration
initialPenaltyWeight = 0.1; % Initial penalty weight for constraint violations
finalPenaltyWeight = 2.0; % Final penalty weight for constraint violations
eliteCount = round(0.1 * popSize); % Number of elites to retain (increased to 10%)

% Initial population generation (randomized within bounds)
population = lb + (ub - lb) .* rand(popSize, nVars);

% Fitness calculation
fitness = zeros(popSize, 1);
for i = 1:popSize
    fitness(i) = PrG9f(population(i, :)) + initialPenaltyWeight * penaltyFunction(PrG9c(population(i, :))); % Include penalty for constraints with initial weight
end

% Main GA loop
for generation = 1:maxGenerations
    % Dynamic penalty weight and mutation rate
    penaltyWeight = initialPenaltyWeight + (finalPenaltyWeight - initialPenaltyWeight) * (generation / maxGenerations);
    mutationRate = initialMutationRate - (initialMutationRate - finalMutationRate) * (generation / maxGenerations);
    
    % Selection (Roulette Wheel Selection)
    selectedParentsIdx = rws(fitness, popSize); % Use roulette wheel selection for better diversity
    parents = population(selectedParentsIdx, :);
    
    % Crossover (Single-point Crossover)
    FieldDR = [lb; ub]; % Define boundaries for crossover
    offspring = xovsp(parents, crossoverRate);

    % Mutation
    FieldDR = [lb; ub]; % Define boundaries for mutation
    MutOpt = [mutationRate, 1]; % Define mutation rate and shrink value
    offspring = mutbga(offspring, FieldDR, MutOpt); % Use real-value mutation from toolbox
    
    % Fitness calculation for offspring
    offspringFitness = zeros(size(offspring, 1), 1);
    for i = 1:size(offspring, 1)
        offspringFitness(i) = PrG9f(offspring(i, :)) + penaltyWeight * penaltyFunction(PrG9c(offspring(i, :))); % Include penalty for constraints with dynamic weight
    end
    
    % Replacement (elitism with more elites)
    [population, fitness] = elitismReplacement(population, fitness, offspring, offspringFitness, eliteCount);
    
    % Save the current best value for convergence plot
    bestFitness(generation) = min(fitness);
end

% Plot convergence trend for a single run
figure;
plot(1:maxGenerations, bestFitness);
xlabel('Generation');
ylabel('Best Objective Function Value');
title('GA Convergence Trend');
grid on;

% Statistical Results (20 runs)
numRuns = 20;
finalResults = zeros(numRuns, 1);
bestFitnessHistory = zeros(maxGenerations, numRuns); % Track best fitness each generation for each run

for run = 1:numRuns
    % Run the GA and get the best objective value for each run
    bestFitnessRun = runGA(nVars, lb, ub, popSize, maxGenerations, crossoverRate, initialMutationRate, finalMutationRate, initialPenaltyWeight, finalPenaltyWeight, eliteCount);
    bestFitnessHistory(:, run) = bestFitnessRun;
    finalResults(run) = bestFitnessRun(end); % Store the final best result of this run
end

% Compute statistics for the 20 runs
bestResult = min(finalResults);
worstResult = max(finalResults);
meanResult = mean(finalResults);
medianResult = median(finalResults);

% Display statistics
disp(['Best Result: ', num2str(bestResult)]);
disp(['Worst Result: ', num2str(worstResult)]);
disp(['Mean Result: ', num2str(meanResult)]);
disp(['Median Result: ', num2str(medianResult)]);

% Plot median convergence trend across runs
medianBestFitness = median(bestFitnessHistory, 2);
figure;
plot(1:maxGenerations, medianBestFitness);
xlabel('Generation');
ylabel('Median Objective Function Value across 20 runs');
title('GA Convergence Trend (Median of 20 Runs)');
grid on;

% Helper function: Run GA once
function bestFitnessRun = runGA(nVars, lb, ub, popSize, maxGenerations, crossoverRate, initialMutationRate, finalMutationRate, initialPenaltyWeight, finalPenaltyWeight, eliteCount)
    % Initialize population
    population = lb + (ub - lb) .* rand(popSize, nVars);
    fitness = zeros(popSize, 1);
    bestFitnessRun = zeros(maxGenerations, 1); % Track best fitness per generation
    for i = 1:popSize
        fitness(i) = PrG9f(population(i, :)) + initialPenaltyWeight * penaltyFunction(PrG9c(population(i, :))); % Include penalty for constraints with initial weight
    end
    
    % Main GA loop
    for generation = 1:maxGenerations
        % Dynamic penalty weight and mutation rate
        penaltyWeight = initialPenaltyWeight + (finalPenaltyWeight - initialPenaltyWeight) * (generation / maxGenerations);
        mutationRate = initialMutationRate - (initialMutationRate - finalMutationRate) * (generation / maxGenerations);
        
        % Selection (Roulette Wheel Selection)
        selectedParentsIdx = rws(fitness, popSize); % Use roulette wheel selection
        parents = population(selectedParentsIdx, :);
        
        % Crossover (Single-point Crossover)
        offspring = xovsp(parents, crossoverRate);

        % Mutation
        FieldDR = [lb; ub]; % Define boundaries for mutation
        MutOpt = [mutationRate, 1];
        offspring = mutbga(offspring, FieldDR, MutOpt);

        % Fitness calculation for offspring
        offspringFitness = zeros(size(offspring, 1), 1);
        for i = 1:size(offspring, 1)
            offspringFitness(i) = PrG9f(offspring(i, :)) + penaltyWeight * penaltyFunction(PrG9c(offspring(i, :)));
        end

        % Replacement (elitism with more elites)
        [population, fitness] = elitismReplacement(population, fitness, offspring, offspringFitness, eliteCount);
        
        % Save the current best value for this generation
        bestFitnessRun(generation) = min(fitness);
    end
end

% Objective function (PrG9f)
function y = PrG9f(x)
    % Matlab Code by A. Hedar (Nov. 23, 2005).
    y = (x(1)-10)^2 + 5*(x(2)-12)^2 + x(3)^4 + 3*(x(4)-11)^2 + ...
        10*x(5)^6 + 7*x(6)^2 + x(7)^4 - 4*x(6)*x(7) - 10*x(6) - 8*x(7);
end

% Constraints function (PrG9c)
function y = PrG9c(x)
    % Matlab Code by A. Hedar (Nov. 23, 2005).
    % Constraints
    v1 = 2*x(1)^2;
    v2 = x(2)^2;
    y(1) = v1 + 3*v2^2 + x(3) + 4*x(4)^2 + 5*x(5) - 127;
    y(2) = 7*x(1) + 3*x(2) + 10*x(3)^2 + x(4) - x(5) - 282;
    y(3) = 23*x(1) + v2 + 6*x(6)^2 - 8*x(7) - 196;
    y(4) = 2*v1 + v2 - 3*x(1)*x(2) + 2*x(3)^2 + 5*x(6) - 11*x(7);
    % Variable lower bounds
    for j = 1:7
        y(j+4) = -x(j) - 10;
    end
    % Variable upper bounds
    for j = 1:7
        y(j+11) = x(j) - 10;
    end
    % *************************************************************************
    y = y';
end

% Penalty Function
function penalty = penaltyFunction(constraints)
    % Penalty function for constraint violations
    penalty = sum(max(0, constraints).^2); % Penalize positive constraint values (violations)
end

% Roulette Wheel Selection function
function idx = rws(fitness, popSize)
    fitnessSum = sum(fitness);
    probabilities = fitness / fitnessSum;
    cumProbs = cumsum(probabilities);
    idx = zeros(popSize, 1);
    for i = 1:popSize
        r = rand;
        idx(i) = find(cumProbs >= r, 1, 'first');
    end
end

% Elitism Replacement function
function [population, fitness] = elitismReplacement(population, fitness, offspring, offspringFitness, eliteCount)
    combinedPopulation = [population; offspring];
    combinedFitness = [fitness; offspringFitness];
    [~, sortedIdx] = sort(combinedFitness);
    population = combinedPopulation(sortedIdx(1:size(population, 1)), :);
    fitness = combinedFitness(sortedIdx(1:size(fitness, 1)));
    % Retain elites
    population(1:eliteCount, :) = combinedPopulation(sortedIdx(1:eliteCount), :);
    fitness(1:eliteCount) = combinedFitness(sortedIdx(1:eliteCount));
end
