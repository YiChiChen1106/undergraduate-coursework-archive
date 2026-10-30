format long;  % 防止科学计数法

% 主程序参数
num_settings = 11;  % GA设置的组数（大于10）
num_runs = 10;  % 每组设置运行10次
num_generations = 2500;  % 固定代数
results_table = cell(num_settings, 7);  % 用于存储最终结果，每行对应一个设置

% 目标函数和约束函数
load('StandardComponentValues.mat');  % 加载电阻、热敏电阻等数据
Tdata = -40:5:85;
Vdata = 1.026e-1 + -1.125e-4 * Tdata + 1.125e-5 * Tdata.^2;
lb = [1 1 1 1 1 1];  % 下限
ub = [70 70 70 70 9 9];  % 上限
function c = nonlcon(x)
    c = x(1) + x(2) - 100;  % x(1) + x(2) <= 100
end

% 定义多个GA参数设置
settings = cell(num_settings, 1);
for i = 1:num_settings
    settings{i} = struct( ...
        'PopulationSize', randi([200, 400]), ...
        'CrossoverFrac', rand(), ...
        'MutationFrac', rand(), ...
        'Generations', num_generations ...
    );
end

% 存储每组设置的统计数据和收敛曲线
all_convergence_curves = zeros(num_generations, num_settings);  % 存储每组的收敛曲线
for setting_idx = 1:num_settings
    setting = settings{setting_idx};
    final_values = zeros(num_runs, 1);  % 每次运行的最终值
    convergence_curves = zeros(num_generations, num_runs);  % 每次运行的收敛曲线
    
    % 当前组设置的多次运行
    for run_idx = 1:num_runs
        [~, fVal, best_values] = myGA(@(x)objectiveFunction(round(x), Res, ThVal, ThBeta, Tdata, Vdata), ...
            6, [], [], [], [], lb, ub, @nonlcon, [], setting);
        final_values(run_idx) = fVal;  % 记录最终目标函数值
        convergence_curves(:, run_idx) = best_values;  % 记录每代的最优值
    end
    
    % 统计分析
    best_result = min(final_values);
    worst_result = max(final_values);
    mean_result = mean(final_values);
    std_result = std(final_values);
    avg_convergence = mean(convergence_curves, 2);  % 计算每代的平均收敛曲线
    all_convergence_curves(:, setting_idx) = avg_convergence;  % 存储每组的收敛曲线
    
    % 保存到表格
    results_table{setting_idx, 1} = setting.PopulationSize;
    results_table{setting_idx, 2} = setting.CrossoverFrac;
    results_table{setting_idx, 3} = setting.MutationFrac;
    results_table{setting_idx, 4} = best_result;
    results_table{setting_idx, 5} = worst_result;
    results_table{setting_idx, 6} = mean_result;
    results_table{setting_idx, 7} = std_result;
end

% 输出表格
disp('Summary of Results for Each GA Setting:');
fprintf('%-15s %-15s %-15s %-15s %-15s %-15s %-15s\n', ...
    'PopSize', 'CrossoverFrac', 'MutationFrac', 'Best', 'Worst', 'Mean', 'StdDev');
for i = 1:num_settings
    fprintf('%-15d %-15.5f %-15.5f %-15.7f %-15.7f %-15.7f %-15.7f\n', ...
        results_table{i, 1}, results_table{i, 2}, results_table{i, 3}, ...
        results_table{i, 4}, results_table{i, 5}, results_table{i, 6}, results_table{i, 7});
end

% 绘制收敛曲线
figure;
for setting_idx = 1:num_settings
    plot(1:num_generations, all_convergence_curves(:, setting_idx), 'DisplayName', ...
        sprintf('Setting %d', setting_idx));
    hold on;
end
xlabel('Generations');
ylabel('Average Best Fitness Value');
title('Convergence Curve for Different GA Settings');
legend show;
hold off;

% Genetic Algorithm Function
function [xOpt, fVal, best_values] = myGA(objectiveFunc, nvars, A, b, Aeq, beq, lb, ub, nonlcon, intCon, options, varargin)
    pop_size = options.PopulationSize;
    num_generations = options.Generations;
    crossover_rate = options.CrossoverFrac;
    mutation_rate = options.MutationFrac;
    FieldDR = repmat([-10; 10], 1, nvars);
    population = crtrp(pop_size, FieldDR);
    best_values = zeros(num_generations, 1);
    
    for gen = 1:num_generations
        fitness_values = arrayfun(@(i) objectiveFunc(population(i, :), varargin{:}), 1:pop_size)';
        best_values(gen) = min(fitness_values);
        selected_parents = select('sus', population, ranking(fitness_values), 1);
        offspring = recombin('xovsp', selected_parents, crossover_rate);
        offspring = mutate('mut', offspring, [], mutation_rate);
        population = reins(population, offspring, 1, 1, fitness_values, fitness_values);
    end
    
    [fVal, idx] = min(fitness_values);
    xOpt = population(idx, :);
end
