% 主 GA 代码开始
% 初始化参数
pop_size = 100; % 种群大小
num_generations = 200; % 代数
crossover_rate = 0.8; % 交叉概率
mutation_rate = 0.05; % 变异概率
penalty_coefficient = 1000; % 约束惩罚系数
shrink_value = 1; % 变异收缩值
SUBPOP = 1; % 子种群数量，设为1表示没有子种群划分

% 定义变量范围 FieldDR
% 第一行是每个变量的下界，第二行是每个变量的上界
FieldDR = repmat([-10; 10], 1, 7); % 7 个变量的上下界，范围为 [-10, 10]

% 定义变异选项 MutOpt，包含变异率和缩放值
MutOpt = [mutation_rate, shrink_value];

% 第一步：初始化种群（使用 crtrp 创建实数值种群，范围为 [-10, 10]）
population = crtrp(pop_size, FieldDR); 
disp('Initial Population Size:');
disp(size(population)); % 显示种群维度信息

% 进化主循环
for gen = 1:num_generations
    % 第二步：适应度评估（调用 PrG9f 函数）
    fitness_values = PrG9f(population);
    
    % 第三步：约束评估并应用惩罚（调用 PrG9c 函数）
    penalty_values = zeros(pop_size, 1);
    for i = 1:pop_size
        constraint_violations = PrG9c(population(i, :));
        % 计算总的约束违反程度
        total_violation = sum(max(0, constraint_violations));
        % 应用惩罚
        penalty_values(i) = penalty_coefficient * total_violation;
    end
    
    % 最终适应度值（带惩罚）
    fitness_values = fitness_values + penalty_values;
    
    % 第四步：适应度排序
    ranked_fitness = ranking(fitness_values);
    
    % 第五步：选择
    num_parents = pop_size; % 保持父代的数量与种群数量一致
    selected_indices = rws(ranked_fitness, num_parents);
    disp('Selected Parents Indices Size:');
    disp(size(selected_indices)); % 显示父代索引维度信息
    
    % 使用选择的索引获取完整的个体
    selected_parents = population(selected_indices, :);
    disp('Selected Parents Size:');
    disp(size(selected_parents)); % 显示父代个体维度信息
    
    % 第六步：交叉
    offspring = xovsp(selected_parents, crossover_rate);
    disp('Offspring Size after Crossover:');
    disp(size(offspring)); % 显示后代维度信息

    % 确保交叉后的 `offspring` 和原始种群的列数一致
    [num_offspring, num_variables] = size(offspring);
    if num_variables ~= size(FieldDR, 2)
        error('Error: The number of variables in offspring does not match FieldDR.');
    end

    % 如果交叉后的 offspring 数量少于原始种群，进行补充
    if num_offspring < pop_size
        % 从原始种群中随机选取一些个体，直到满足原始种群数量
        num_additional = pop_size - num_offspring;
        additional_indices = randi([1, pop_size], num_additional, 1);
        additional_individuals = population(additional_indices, :);
        
        % 确保拼接时维度一致
        offspring = [offspring; additional_individuals];
    elseif num_offspring > pop_size
        % 如果 offspring 超过了 pop_size，随机去除一些个体
        offspring = offspring(1:pop_size, :);
    end
    
    disp('Offspring Size after Adjustment:');
    disp(size(offspring)); % 显示调整后的后代维度信息
    
    % 第七步：变异（使用 mutbga，提供 FieldDR 和 MutOpt 参数）
    mutated_offspring = mutbga(offspring, FieldDR, MutOpt);
    disp('Mutated Offspring Size:');
    disp(size(mutated_offspring)); % 显示变异后后代维度信息
    
    % 第八步：重插入
    InsOpt = [0, 1.0]; % 0 表示均匀插入，1.0 表示插入所有后代
    population = reins(population, mutated_offspring, SUBPOP, InsOpt, fitness_values);
    disp('New Population Size:');
    disp(size(population)); % 显示新种群维度信息
    
    % 记录每代的最佳适应度值
    best_value(gen) = min(fitness_values);
end

% 绘制收敛曲线
plot(1:num_generations, best_value);
xlabel('Generation');
ylabel('Best Fitness Value');
title('Convergence Trend of GA with Constraints');

% 主 GA 代码结束



% 目标函数：PrG9f
function y = PrG9f(x)
    % x: 种群矩阵，其中每一行是一个个体
    [N, ~] = size(x);
    y = zeros(N, 1);
    for i = 1:N
        xi = x(i, :);
        y(i) = (xi(1) - 10)^2 + 5 * (xi(2) - 12)^2 + xi(3)^4 + 3 * (xi(4) - 11)^2 + ...
                10 * xi(5)^6 + 7 * xi(6)^2 + xi(7)^4 - 4 * xi(6) * xi(7) - 10 * xi(6) - 8 * xi(7);
    end
end

% 约束函数：PrG9c
function y = PrG9c(x)
    % x: 单个个体（1x7 的向量）
    % 约束
    v1 = 2 * x(1)^2;
    v2 = x(2)^2;
    y(1) = v1 + 3 * v2^2 + x(3) + 4 * x(4)^2 + 5 * x(5) - 127;
    y(2) = 7 * x(1) + 3 * x(2) + 10 * x(3)^2 + x(4) - x(5) - 282;
    y(3) = 23 * x(1) + v2 + 6 * x(6)^2 - 8 * x(7) - 196;
    y(4) = 2 * v1 + v2 - 3 * x(1) * x(2) + 2 * x(3)^2 + 5 * x(6) - 11 * x(7);
    
    % 变量的下界
    for j = 1:7
        y(j + 4) = -x(j) - 10;
    end
    
    % 变量的上界
    for j = 1:7
        y(j + 11) = x(j) - 10;
    end

    % 将约束向量转置为列向量
    y = y';
end