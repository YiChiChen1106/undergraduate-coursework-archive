%% project2_spectrum_gui.m
% Interactive GUI for Task 1: Digital Spectrum Analysis Parameter Exploration
% Usage: save as project2_spectrum_gui.m and run project2_spectrum_gui in MATLAB.
function project2_spectrum_gui()
    % Create UI figure
    fig = uifigure('Name','Spectrum Design Tool','Position',[100 100 450 400]);

    % Window Type Dropdown
    uilabel(fig, 'Position', [20 360 120 22], 'Text', 'Window Type:');
    ddWin = uidropdown(fig, ...
        'Position', [[phone-redacted]], ...
        'Items', {'Rectangular','Hamming','Hann','Blackman'}, ...
        'Value', 'Hann');

    % Window Length Listbox
    uilabel(fig, 'Position', [20 320 120 22], 'Text', 'Window Length M:');
    lbM = uilistbox(fig, ...
        'Position', [140 240 200 100], ...
        'Items', {'256','512','1024','2048'}, ...
        'Value', '1024');

    % FFT Points Listbox
    uilabel(fig, 'Position', [20 200 120 22], 'Text', 'FFT Points NFFT:');
    lbN = uilistbox(fig, ...
        'Position', [140 120 200 100], ...
        'Items', {'1024','2048','4096','8192'}, ...
        'Value', '2048');

    % Generate Button
    uibutton(fig, 'Text', 'Generate Spectrum', ...
        'Position', [140 50 200 30], ...
        'ButtonPushedFcn', @(btn,event) onGenerate(ddWin.Value, lbM.Value, lbN.Value));
end

% Callback function to compute and plot spectrum
function onGenerate(winType, Mstr, NFFTstr)
    % Convert inputs
    M = str2double(Mstr);
    NFFT = str2double(NFFTstr);

    % Sampling and signal definition
    Fs = 1000;
    t = (0:1023)/Fs;
    x = 10*sin(2*pi*64*t) + 1*sin(2*pi*250*t) + 20*sin(2*pi*256*t) + 3*sin(2*pi*260*t) + 10*sin(2*pi*512*t);

    % Select window
    switch winType
        case 'Rectangular'
            w = rectwin(M)';
        case 'Hamming'
            w = hamming(M)';
        case 'Hann'
            w = hann(M)';
        case 'Blackman'
            w = blackman(M)';
        otherwise
            error('Unsupported window type %s', winType);
    end

    % Apply window and FFT
    xw = x(1:M) .* w;
    X = fft(xw, NFFT);
    f = (0:NFFT-1)*(Fs/NFFT);

    % Create result figure
    fig2 = uifigure('Name','Spectrum Result','Position',[600 150 600 400]);
    ax = uiaxes(fig2,'Position',[50 50 500 300]);
    plot(ax, f, 20*log10(abs(X)), 'LineWidth', 1.2);
    title(ax, sprintf('%s | M=%d | NFFT=%d', winType, M, NFFT));
    xlabel(ax, 'Frequency (Hz)'); ylabel(ax, 'Magnitude (dB)');
    xlim(ax, [0 Fs/2]); grid(ax, 'on');
end
