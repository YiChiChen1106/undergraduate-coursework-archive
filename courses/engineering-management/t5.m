% tornado_two_page_fixed.m
% Two‐page tornado plots with R6 label no longer overlapping left

%% 1. Define risk data
riskDesc = { ...
    'R8: Late discovery of major defects', ...
    'R3: Technology component validation failure', ...
    'R2: Key developer unavailable (illness)', ...
    'R4: Critical supplier late delivery', ...
    'R1: Ambiguous requirements → rework', ...
    'R5: Regulatory change requires redesign', ...
    'R7: Stakeholder turnover loses knowledge', ...
    'R6: Project budget cut' ...
    };

P     = [0.25; 0.20; 0.25; 0.40; 0.30; 0.15; 0.35; 0.10];
emv   = [4500; 4000; 3750; 3200; 3000; 1800; 1750; -2000];
delay = [2.25; 2.00; 1.75; 1.60; 1.50; 0.90; 0.70; 0.30];

fontSize = 12;
outputPDF = 'tornado_diagrams_fixed.pdf';

%% 2. Figure 1: Cost-Impact Tornado
fig1 = figure('Name','Cost Impact','Color','w');
% color shading
basePos = [0.2 0.6 0.8]; baseNeg = [0.85 0.33 0.10];
maxP = max(P);
cdata = zeros(numel(emv),3);
for i = 1:numel(emv)
    shade = 0.5 + 0.5*(P(i)/maxP);
    if emv(i) >= 0
        cdata(i,:) = basePos * shade;
    else
        cdata(i,:) = baseNeg * shade;
    end
end

barh(emv,'FaceColor','flat','EdgeColor','k','CData',cdata);
hold on;
% highlight R8, R3
for idx = [1,2]
    if emv(idx)>=0
        x0=0; w=emv(idx);
    else
        x0=emv(idx); w=-emv(idx);
    end
    rectangle('Position',[x0, idx-0.4, w, 0.8],...
              'EdgeColor','k','LineWidth',2);
end

% labels: positive outside, negative just left of zero
offset = max(abs(emv))*0.02;
for i = 1:numel(emv)
    x = emv(i); y = i;
    if x >= 0
        xt = x + offset;    ha = 'left';
    else
        xt = -offset;       ha = 'right';
    end
    text(xt, y, sprintf('£%.0f (%.0f%%)', x, P(i)*100), ...
         'FontSize',10,'VerticalAlignment','middle','HorizontalAlignment',ha);
end
hold off;

set(gca, 'YDir','reverse', 'YTick',1:8, 'YTickLabel',riskDesc, ...
         'FontSize',fontSize,'XGrid','on','YGrid','off');
xline(0,'k--','LineWidth',1);
xlim([min(emv)*1.1, max(emv)*1.1]);
xlabel('Expected Monetary Value (GBP)','FontSize',fontSize);
title('Figure B.1 Cost-Impact Tornado Diagram','FontSize',fontSize+2);

% export page 1
exportgraphics(fig1, outputPDF, 'ContentType','vector');

%% 3. Figure 2: Schedule-Impact Tornado
fig2 = figure('Name','Schedule Impact','Color','w');
barh(delay,'FaceColor',[0.8 0.4 0.4],'EdgeColor','k');
hold on;
for i = 1:numel(delay)
    xt = delay(i) + max(delay)*0.02;
    text(xt, i, sprintf('%.2f d (%.0f%%)', delay(i), P(i)*100), ...
         'FontSize',10,'VerticalAlignment','middle','HorizontalAlignment','left');
end
hold off;

set(gca, 'YDir','reverse', 'YTick',1:8, 'YTickLabel',riskDesc, ...
         'FontSize',fontSize,'XGrid','on','YGrid','off');
xlim([0, max(delay)*1.1]);
xlabel('Expected Delay (days)','FontSize',fontSize);
title('Figure B.2 Schedule-Impact Tornado Diagram','FontSize',fontSize+2);

% append page 2
exportgraphics(fig2, outputPDF, 'ContentType','vector','Append',true);

disp(['Two-page PDF written to: ', outputPDF]);
