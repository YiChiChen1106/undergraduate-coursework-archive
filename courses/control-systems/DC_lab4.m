% DC_lab4.m
% Exercise 1: Analysis of L(s) = (s+1)(s+2) / [ s^2 (s+3)(s+4)(s+10) ]

%% 1. 定义开环传递函数 L(s)
num = conv([1,1], [1,2]);                             % (s+1)(s+2)
den = conv([1,0,0], conv([1,3], conv([1,4], [1,10])));% s^2*(s+3)*(s+4)*(s+10)
L = tf(num, den);

%% 2. 根轨迹 (root locus)
figure('Name','Root Locus');
rlocus(L);
grid on;
title('Root Locus of L(s)');

%% 3. Bode 幅相特性及稳定性裕度
figure('Name','Bode Plot with Margins');
margin(L);                % 绘制 Bode 并自动标出 GM/PM
grid on;
title('Bode Plot of L(s) with Stability Margins');

% 打开 Data Cursor 模式，方便在图上点击读取数值
dcm = datacursormode(gcf);
set(dcm,'Enable','on','SnapToDataVertex','on');

% 用 margin() 提取增益/相位裕度及对应频率
[Gm, Pm, Wcg, Wcp] = margin(L);
GainMargin_dB = 20*log10(Gm);  % 转为 dB
GMFrequency   = Wcp;            % 对应增益裕度的频率 (rad/s)
PhaseMargin   = Pm;             % 相位裕度 (°)
PMFrequency   = Wcg;            % 对应相位裕度的频率 (rad/s)

%% 4. Nyquist 图 & 全部裕度
figure('Name','Nyquist Plot');
nyquist(L);
grid on;
title('Nyquist Plot of L(s)');
% 如需去掉负频率：右键 → Show → 取消 “Negative frequencies”
% 如需标出裕度 ：右键 → Characteristics → All Stability Margins

% 用 allmargin() 提取 Delay Margin 和稳定性标志
AM = allmargin(L);
DelayMargin = AM.DelayMargin;   % 时延裕度 (s)
DMFrequency = AM.DMFrequency;   % 对应频率 (rad/s)
isStable    = AM.Stable;        % 布尔：1=Stable, 0=Unstable

%% 5. 闭环稳定性校验 (K=1)
CL = feedback(L, 1);
if isstable(CL)
    ClosedLoopStatus = 'Stable';
else
    ClosedLoopStatus = 'Unstable';
end

%% 6. 输出所有结果，方便拷贝到报告
fprintf('\n---- Results ----\n');
fprintf('GainMargin   = %.2f dB\n',             GainMargin_dB);
fprintf('GMFrequency  = %.2f rad/s\n',         GMFrequency);
fprintf('PhaseMargin  = %.2f°\n',              PhaseMargin);
fprintf('PMFrequency  = %.2f rad/s\n',         PMFrequency);
fprintf('DelayMargin  = %.4f s\n',             DelayMargin);
fprintf('DMFrequency  = %.2f rad/s\n',         DMFrequency);
fprintf('Closed-loop  = %s\n',                  ClosedLoopStatus);
fprintf('allmargin-> Stable flag = %d (1=Stable,0=Unstable)\n', isStable);

