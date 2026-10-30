clc;
clearvars;
%% Temperature and Voltage Data
Tdata = -40:5:85;
Vdata_Object = 1.026E-1 + -1.125E-4 * Tdata + 1.125E-5 * Tdata.^2;

%% Plot the Ideal Curve
subplot(2,2,1)
plot(Tdata,Vdata_Object,'-*');
title('Target Curve','FontSize',12); 
xlabel('Temperature (^oC)'); ylabel('Voltage (V)')

%% Load Component Values
load('StandardComponentValues.mat')

%% Check first 15 Resistor Values
disp('Sample of Available Resistor Sizes:')
disp(Res(1:15));

%% Parameter setting
pop_size = 1000;         % Number of individuals
RecOpt = 0.5;           % Probability of recombination and crossover
num_generations = 200; % The number of generations
GGAP = 1;               % Generation gap
NVAR = 6;               % The number of dimensions for inputs of the G9 function
PRECI = 50;             % The precision of the Binary representation of the Chromosome
Lind = NVAR*PRECI;      % The length of each chromosome
Pm = 0.2/Lind;         % The probability of mutation
SEL_OP = 'sus';         % Selection operator
XOV_OP = 'xovsp';       % Crossover operator
MUT_OP = 'mut';         % Mutation operator

%The input has 7 dimensions and in each dimension the range is [-10,10]
FieldD_1 = rep([PRECI, 1, 70, 1, 0, 1, 1]', [1, NVAR-2]);
FieldD_2 = rep([PRECI, 1, 9, 1, 0, 1, 1]', [1, 2]);
FieldD = [FieldD_1,FieldD_2];

% create matrices to store the output values for each generation
Best = zeros(num_generations,1);      % store the best values for each generation
Med = zeros(num_generations,1);       % store the median values for each generation
Worst = zeros(num_generations,1);     % store the worst values for each generation
Mean = zeros(num_generations,1);      % store the average values for each generation

% generate the binary representation for the Chromosomes
Chrom = crtbp(pop_size, Lind, 2);

x = round(bs2rv(Chrom, FieldD));


% calculate the objective function value for the initial generation
ObjV = zeros(pop_size,1);
for i = 1:pop_size
    ObjV(i,:) = Curve(x(i,:),Tdata,Res,ThVal,ThBeta,Vdata_Object);
end

% loop calculating the output for each generations
for gen = 1:num_generations
    fprintf('gen: %f\n',gen);
    % calculate the fitness for each individual
    FitnV = ranking(ObjV);
    % select the individuals as parents
    SelCh = select(SEL_OP, Chrom, FitnV, GGAP);
    % crossover the selected Chromosomes
    SelCh = recombin(XOV_OP, SelCh, RecOpt);
    % implement mutation
    SelCh = mutate(MUT_OP, SelCh, [], Pm);
    % insert the Chromosome of the offsprings
    [Chrom, ObjV] = reins(Chrom, SelCh, 1, 1, ObjV, ObjV);
    % convert the chromosomes of this generation into real numbers
    x = round(bs2rv(Chrom, FieldD));
    % calculate the objective function value for the initial generation
    for i = 1:pop_size
        ObjV(i,:) = Curve(x(i,:),Tdata,Res,ThVal,ThBeta,Vdata_Object);
    end
    
    Best_penalty(gen) = min(ObjV);  % store the best value of penalty function for the generation
    Worst_penalty(gen) = max(ObjV); % store the worst value of penalty function for the generation
    Mean_penalty(gen) = mean(ObjV); % store the average value of penalty function for the generation
    Med_penalty(gen) = median(ObjV);% store the median value of penalty function for the geeneration
    
    end
%%
% The Plot of Median Value
subplot(2,2,2);
generation = 1:num_generations;
plot(generation,Med_penalty);
xlabel('Generations');
ylabel('The Median Value of the results');
title('The Plot of Median Value');
subplot(2,2,3);
last_x = median(x);
omptimized_line = voltageCurve(Tdata,last_x,Res,ThVal,ThBeta);
plot(Tdata,omptimized_line,'ro-')
hold on
plot(Tdata,Vdata_Object,'bo-')
hold off