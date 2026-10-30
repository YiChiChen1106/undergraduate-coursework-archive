clear; clc;

%% 1. 读取风能数据 [cite: 18]
% 读取 CSV 文件 (确保文件在当前目录下)
raw_data = readmatrix('gridwatch wind data.csv');
wind_power_kW = raw_data(:, 3); % 提取第3列数据

% 创建时间轴 (24小时 = 86400秒)
num_points = length(wind_power_kW);
time_seconds = linspace(0, 24*3600, num_points)'; % 注意：这里用了 ' 转置为列向量

% 创建 Simulink 专用输入变量
wind_input = timeseries(wind_power_kW, time_seconds);

%% 2. 定义负载参数
% Case 1: 恒定负载 450 kW 
Base_Load = 450; 

% Case 2: 扰动参数 [cite: 22]
% 中午 12:00 (43200秒) 突增，持续 5分钟 (300秒)
Disturbance_Start = 12 * 3600;
Disturbance_Duration = 5 * 60;
Disturbance_Height = 300; % 450 -> 750 kW, 所以增量是 300

% 开关变量：设为 1 开启扰动(Case 2)，设为 0 关闭扰动(Case 1)
Enable_Disturbance = 0; 

%% 3. 储能设备参数 (试错法优化处) [cite: 20, 24]
% 电池参数
Bat_Capacity_kWh = 6000;         % 容量 (Case 1 重点试错参数)
Bat_Capacity_J = Bat_Capacity_kWh * 3.6e6; 
Bat_Init_SoC = 50;               % 初始电量 50%

% 超级电容参数
SC_Capacitance = 500;            % 法拉 (F)
SC_Rated_V = 270;                % 额定电压 (V)
SC_Init_V = 270;                 % 初始电压
SC_Init_Energy = 0.5 * SC_Capacitance * SC_Init_V^2;

%% 4. 控制器参数 (核心)
% 时间常数 Tau。决定多少功率分给电池，多少分给超容。
% Case 2 重点试错参数。建议从 100 试到 500。
Tau = 2000;