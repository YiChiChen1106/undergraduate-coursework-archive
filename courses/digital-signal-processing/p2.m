% Interactive GUI for Task 1: Digital Spectrum Analysis Parameter Exploration
% Usage: save as project2_spectrum_gui.m and call project2_spectrum_gui in MATLAB command window.
function project2_spectrum_gui()
    % Create UI figure
    fig = uifigure('Name','Spectrum Design Tool','Position',[100 100 450 400]);

    % Window Type Dropdown
    uilabel(fig,'Position',[20 360 100 22],'Text','Window Type:');
    ddWin = uidropdown(fig, ...
        'Position',[[phone-redacted]], ...
        'Items',{'Rectangular','Hamming','Blackman','Kaiser(β=4)'}, ...
        'Value','Hamming');

    % Window Length Listbox
    uilabel(fig,'Position',[20 300 22],'Text','Window Length M:');
    lbM = uilistbox(fig, ...
        'Position',[140 240 200 100], ...
        'Items',{'256','512','1024','2048'}, ...
        'Value','1024');

    % FFT Points Listbox
    uilabel(fig,'Position',[20 160 100 22],'Text','FFT Points NFFT:');
    lbN = uilistbox(fig, ...
        'Position',[140 100 200 100], ...
        'Items',{'1024','2048','4096','8192'}, ...
        'Value','2048');

    % Generate Button
    uibutton(fig, ...
        'Text','Generate Spectrum', ...
        'Position',[140 40 200 30], ...
        'ButtonPushedFcn',@(btn,event)onGenerate(ddWin.Value, lbM.Value, lbN.Value));
end

function onGenerate(winType, Mstr, NFFTstr)
    % Parse numeric values
    M = str2double(Mstr);
    NFFT = str2double(NFFTstr);

    % Signal definition (fixed length 1024)
    Fs = 1000;
    t = (0:1023)/Fs;
    x = 10*sin(2*pi*64*t) + 1*sin(2*pi*250*t) + 20*sin(2*pi*256*t) + 3*sin(2*pi*260*t) + 10*sin(2*pi*512*t);

    % Window selection
    switch winType
        case 'Rectangular'
            w = rectwin(M)';
        case 'Hamming'
            w = hamming(M)';
        case 'Blackman'
            w = blackman(M)';
        case 'Kaiser(β=4)'
            w = kaiser(M,4)';
    end

    % Apply window and compute FFT
    xw = x(1:M) .* w;
    X = fft(xw, NFFT);
    f = (0:NFFT-1)*(Fs/NFFT);

    % Plot in new UI figure
    fig2 = uifigure('Name','Spectrum Result','Position',[600 150 600 400]);
    ax = uiaxes(fig2,'Position',[50 50 500 300]);
    plot(ax, f, 20*log10(abs(X)), 'LineWidth', 1.2);
    title(ax, sprintf('%s | M=%d | NFFT=%d', winType, M, NFFT));
    xlabel(ax, 'Frequency (Hz)'); ylabel(ax, 'Magnitude (dB)');
    xlim(ax, [0 Fs/2]); grid(ax, 'on');
end


%% Task 2: Doppler Frequency Shift Detection
% 1. 基本参数
c  = 3e8;      % 光速 (m/s)
fc = 3e9;      % 载波频率 (Hz)
v  = 80;       % 目标速度 (m/s) —— 可取 50~100 测试
fd = (v/c)*fc; % 多普勒频移 (Hz)

% 2. 模拟发射与接收信号
t2 = 0:T:0.01-T;                       % 观测时间 10 ms
tx = exp(1j*2*pi*fc*t2);              % 发射信号（载波）
rx = exp(1j*2*pi*(fc+fd)*t2);         % 接收信号（含多普勒偏移）

% 3. 基带化（混频至零中频）
baseband = rx .* conj(tx);            % 下变频

% 4. 加窗并 FFT
w2   = hann(length(baseband))';
Xb   = fft(baseband .* w2, NFFT);
fbb  = (-NFFT/2:NFFT/2-1)*(Fs/NFFT);  % 双边频谱

figure('Name','Task 2: Baseband Spectrum','NumberTitle','off');
plot(fbb, abs(fftshift(Xb)));
xlabel('Frequency (Hz)'); ylabel('Magnitude');
title('Baseband Spectrum for Doppler Estimation'); grid on;

% 5. 多普勒偏移与速度估计
[~, idx] = max(abs(fftshift(Xb)));
fd_est   = fbb(idx);
v_est    = (fd_est/fc)*c;

fprintf('理论多普勒频移: %.2f Hz\n', fd);
fprintf('估计多普勒频移: %.2f Hz\n', fd_est);
fprintf('估计目标速度  : %.2f m/s\n', v_est);
