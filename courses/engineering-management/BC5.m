%% Complete MATLAB Script: Risk Influence Diagrams with Severity Coloring

% Define colormap: High=red, Medium=yellow, Low=green
cmap = [1 0.5 0.5;   % 1 = High
        1 1   0.5;   % 2 = Medium
        0.5 1 0.5];  % 3 = Low

%% Part B: Cost Overrun Influence Diagram

% Node labels
costNodes = { ...
    'R1:Supplier Delay', ...
    'R3:Equipment Breakdown', ...
    'R4:Logistics Spike', ...
    'R5:FX Volatility', ...
    'R8:Regulatory Change', ...
    'Cost Overrun'};

nCostRisks = numel(costNodes)-1;

% Edges: each risk → Cost Overrun (node index nCostRisks+1)
sCost = 1:nCostRisks;
tCost = repmat(nCostRisks+1,1,nCostRisks);

% Probabilities and cost impacts
P_cost = [0.30, 0.15, 0.25, 0.40, 0.05];
C_imp  = [3000, 4000, 1500, 2000, 5000];

% Build edge labels like '£3000×0.30'
edgeLabelsCost = arrayfun(@(c,p) ['£' num2str(c) '×' num2str(p,'%.2f')], ...
                          C_imp, P_cost, 'UniformOutput',false);

% Construct digraph and plot
Gcost = digraph(sCost, tCost, [], costNodes);
figure('Name','Cost Overrun Influence Diagram','Color','w');
hCost = plot(Gcost, ...
    'Layout','force', ...
    'NodeLabel', costNodes, ...
    'EdgeLabel', edgeLabelsCost, ...
    'LineWidth', 1.5, ...
    'EdgeAlpha', 0.7, ...
    'ArrowSize', 12);

% Font sizes
hCost.NodeFontSize = 12;
hCost.EdgeFontSize = 10;

% Severity levels: (High, High, Medium, Medium, High, Low)
severityCost = [1, 1, 2, 2, 1, 3];  
hCost.NodeColor = cmap(severityCost,:);

% Manual node positions (fan out on left, outcome on right)
yCost = linspace(2,-2,nCostRisks)';
hCost.XData(1:nCostRisks) = -1;
hCost.YData(1:nCostRisks) = yCost;
hCost.XData(end) = 1.5;
hCost.YData(end) = 0;

title('Cost Overrun Influence Diagram');

% Annotate expected cost overrun
expCost = sum(P_cost .* C_imp);
annotation('textbox',[0.65 0.2 0.25 0.1], ...
    'String', sprintf('E[Cost Overrun] = £%.0f', expCost), ...
    'FontSize', 11, 'EdgeColor', 'none');


%% Part C: Schedule Slip Influence Diagram

% Node labels
schedNodes = { ...
    'R1:Supplier Delay', ...
    'R2:Quality Defect', ...
    'R3:Equipment Breakdown', ...
    'R6:Staff Turnover', ...
    'R7:Scope Change', ...
    'R8:Regulatory Change', ...
    'Schedule Slip'};

nSchedRisks = numel(schedNodes)-1;

% Edges: each risk → Schedule Slip (node index nSchedRisks+1)
sSched = 1:nSchedRisks;
tSched = repmat(nSchedRisks+1,1,nSchedRisks);

% Probabilities and time impacts
P_time = [0.30, 0.20, 0.15, 0.10, 0.20, 0.05];
T_imp  = [7, 5, 10, 3, 4, 14];

% Build edge labels like '7d×0.30'
edgeLabelsTime = arrayfun(@(d,p) [num2str(d) 'd×' num2str(p,'%.2f')], ...
                          T_imp, P_time, 'UniformOutput',false);

% Construct digraph and plot
Gtime = digraph(sSched, tSched, [], schedNodes);
figure('Name','Schedule Slip Influence Diagram','Color','w');
hTime = plot(Gtime, ...
    'Layout','force', ...
    'NodeLabel', schedNodes, ...
    'EdgeLabel', edgeLabelsTime, ...
    'LineWidth', 1.5, ...
    'EdgeAlpha', 0.7, ...
    'ArrowSize', 12);

% Font sizes
hTime.NodeFontSize = 12;
hTime.EdgeFontSize = 10;

% Severity levels: (High, Medium, High, Low, Medium, High, Low)
severityTime = [1, 2, 1, 3, 2, 1, 3];
hTime.NodeColor = cmap(severityTime,:);

% Manual node positions
yTime = linspace(2,-2,nSchedRisks)';
hTime.XData(1:nSchedRisks) = -1;
hTime.YData(1:nSchedRisks) = yTime;
hTime.XData(end) = 1.5;
hTime.YData(end) = 0;

title('Schedule Slip Influence Diagram');

% Annotate expected schedule slip
expTime = sum(P_time .* T_imp);
annotation('textbox',[0.65 0.2 0.25 0.1], ...
    'String', sprintf('E[Schedule Slip] = %.1f days', expTime), ...
    'FontSize', 11, 'EdgeColor', 'none');
