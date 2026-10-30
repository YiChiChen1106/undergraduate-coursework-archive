clc; clear; close all;

% 坐标参数
w = 3; h = 0.9;      % 节点宽高
x0 = 0;              % 横坐标基线
y0 = 10;             % 纵坐标起点
dy = 1.6;            % 节点间距

% 节点文本
steps = {
    'Start'
    'Read waypoints from point.txt'
    'Takeoff'
    'For each waypoint'
    'Publish (X, Y, Z)'
    'Wait (hover time)'
    'All waypoints finished?'
    'Land'
    'End'
};

% 每个节点坐标（横坐标一致，纵坐标等距）
x = x0 * ones(length(steps),1);
y = y0 - (0:(length(steps)-1))'*dy;

figure('color','w','Position',[500,80,650,720]); hold on; axis off equal;

% 方框节点
boxidx = [1:6 8:9];
for i = boxidx
    rectangle('Position',[x(i)-w/2, y(i)-h/2, w, h],...
        'Curvature',0.08, 'FaceColor',[0.85 0.94 1], 'EdgeColor','k','LineWidth',2)
    text(x(i), y(i), steps{i}, 'FontSize',13, 'HorizontalAlignment','center')
end

% 菱形决策点
d = h*1.1;
plot([x(7) x(7)-d x(7) x(7)+d x(7)], [y(7)-d y(7) y(7)+d y(7) y(7)-d], ...
    'k', 'LineWidth',2)
text(x(7), y(7), steps{7}, 'FontSize',13, 'HorizontalAlignment','center')

% 正向箭头
for i = 1:6
    annotation('arrow',...
        'X',[0.5 0.5],'Y',[(y(i)-h/2-0.04)/y0 (y(i+1)+h/2+0.04)/y0],...
        'HeadLength',8,'HeadWidth',8)
end
% 决策Yes
annotation('arrow',...
    'X',[0.5 0.5],'Y',[(y(7)-d-0.01)/y0 (y(8)+h/2+0.04)/y0],'HeadLength',8,'HeadWidth',8)
text(x(7)-w*0.22, (y(7)-d+y(8)+h/2)/2+0.05, '\bf\color[rgb]{0,0.6,0}Yes','FontSize',13)
% Land->End
annotation('arrow','X',[0.5 0.5],'Y',[(y(8)-h/2-0.01)/y0 (y(9)+h/2+0.04)/y0],'HeadLength',8,'HeadWidth',8)

% 回环分支（No），绕开所有节点（右-上-左-下折线）
loop_x = [x(7)+d, x(7)+w*1.6, x(4)+w*1.6, x(4), x(4)];
loop_y = [y(7), y(7)+dy*0.2, y(4)+dy*0.6, y(4)+h/2+0.02, y(4)-h/2-0.04];
plot(loop_x, loop_y, 'k-', 'LineWidth',1.4)
annotation('arrow',...
    'X',[0.83 0.82],'Y',[(y(4)+h/2+0.07)/y0 (y(4)-h/2-0.01)/y0],...
    'HeadLength',8,'HeadWidth',8)
text(x(7)+d+0.5, y(7)+0.1, '\bf\color[rgb]{1,0.35,0}No','FontSize',13)

% 标题
title('\bf Workflow of VortexEdge.py Autonomous Waypoint Navigation','FontSize',15)
xlim([-2 5]); ylim([y0-10  y0+2]);

hold off
