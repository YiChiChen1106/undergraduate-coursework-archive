%% project2_doppler_gui.m
% Interactive GUI for Task 2: Doppler Shift Detection System Design
% Only select predefined Param Sets A–P; parameters displayed read-only.
function project2_doppler_gui()
    % Part A: Display fixed Doppler calculation process
    c    = 3e8;    % Speed of light (m/s)
    fc   = 3e9;    % Carrier frequency (Hz)
    df0  = 500;    % Given Doppler shift (Hz)
    v0   = (df0/fc)*c;
    fprintf('=== Doppler Calculation Process ===\n');
    fprintf('Formula: Δf = (v / c) * f_c\n');
    fprintf('⇒ v = (Δf / f_c) * c\n');
    fprintf('Given Δf = %d Hz, f_c = %.1e Hz, c = %.1e m/s\n', df0, fc, c);
    fprintf('Compute: v = (%d / %.1e) * %.1e ≈ %.2f m/s\n\n', df0, fc, c, v0);

    % Define Param Sets: {Label, Fs, T_obs, Window, M, NFFT, v_true, SNR}
    sets = { ...
      'A', 500,  0.005, 'Rectangular', 128,  256, 50,  Inf;  
      'B', 1000, 0.01,  'Hann',        256,  512, 80,  Inf;  
      'C', 2000, 0.02,  'Hamming',     512, 1024, 100, 30;   
      'D', 5000, 0.005, 'Blackman',    256,  512, 100, 10;   
      'E', 2000, 0.005, 'Hann',        512, 1024, 50,  20;   
      'F', 1000, 0.02,  'Blackman',   1024, 2048, 60,   0;   
      'G', 500,  0.05,  'Rectangular',256,  256, 100, Inf;  
      'H', 5000, 0.02,  'Hamming',     512, 2048, 75,  10;   
      'I', 2000, 0.01,  'Hann',       1024,  512, 90,  30;   
      'J', 5000, 0.05,  'Blackman',   1024, 2048,100,  Inf;  
      'K', 1000, 0.005, 'Hamming',     128,  256, 70,  20;   
      'L', 1000, 0.05,  'Hann',        512,  512, 55,  Inf;  
      'M', 2000, 0.005, 'Blackman',   1024, 2048, 85,   0;   
      'N', 500,  0.01,  'Hann',        256, 1024, 60,  30;   
      'O', 5000, 0.01,  'Rectangular',512, 1024, 95,  20;   
      'P', 2000, 0.05,  'Hamming',    1024, 2048,100,  Inf};

    % Create UI
    fig = uifigure('Name','Doppler Detection Tool','Position',[100 100 500 550]);
    uilabel(fig,'Position',[20 500 300 22], 'Text',sprintf('Fixed result: v ≈ %.2f m/s', v0));

    % Param Set dropdown
    uilabel(fig,'Position',[20 460 100 22],'Text','Param Set:');
    ddSet = uidropdown(fig,'Position',[120 460 100 22], 'Items',sets(:,1), 'Value','A', 'ValueChangedFcn',@refreshDisplay);

    % Display parameters read-only
    labels = {'Fs (Hz):','T_{obs} (s):','Window:','M:','NFFT:','v_{true} (m/s):','SNR (dB):'}; y=420;
    for i=1:numel(labels)
        uilabel(fig,'Position',[20 y 120 22],'Text',labels{i});
        txt(i) = uilabel(fig,'Position',[140 y 200 22],'Text','');
        y = y - 30;
    end

    % Generate button
    uibutton(fig,'Text','Generate Spectrum','Position',[[phone-redacted]],'ButtonPushedFcn',@runCase);

    % Initialize display
    refreshDisplay();

    % Nested: update displayed fields
    function refreshDisplay(~,~)
        idx = find(strcmp(sets(:,1), ddSet.Value));
        vals = sets(idx,2:8);
        for k=1:numel(vals)
            txt(k).Text = string(vals{k});
        end
    end

    % Nested: execute selected case
    function runCase(~,~)
        idx = find(strcmp(sets(:,1), ddSet.Value));
        label   = sets{idx,1};
        [Fs,T_obs,winType,M,NFFT,v_true,SNR] = sets{idx,2:8};
        onGenerateDoppler(label, Fs, T_obs, winType, M, NFFT, v_true, SNR);
    end
end

function onGenerateDoppler(label, Fs, T_obs, winType, M, NFFT, v_true, SNR)
    c = 3e8; fc = 3e9;
    L = floor(Fs * T_obs); t = (0:L-1)/Fs;
    tx = exp(1j*2*pi*fc*t); fd_true = (v_true/c)*fc;
    rx = exp(1j*2*pi*(fc+fd_true)*t);
    bb = rx .* conj(tx);
    if isfinite(SNR), bb = awgn(bb, SNR, 'measured'); end

    seg_len = min(M, numel(bb));
    switch winType
        case 'Rectangular', w_full = rectwin(M)';
        case 'Hamming',    w_full = hamming(M)';
        case 'Hann',       w_full = hann(M)';
        case 'Blackman',   w_full = blackman(M)';
    end
    w = w_full(1:seg_len);

    X = fft(bb(1:seg_len).*w, NFFT);
    f = (0:NFFT-1)*(Fs/NFFT);
    [~,idx] = max(abs(X)); fd_est = f(idx); v_est = (fd_est/fc)*c;

    figure('Name','Doppler Spectrum','NumberTitle','off');
    plot(f,abs(X),'LineWidth',1.2);
    xlabel('Frequency (Hz)'); ylabel('Magnitude'); title(sprintf('Spectrum: Case %s', label));
    grid on; xlim([0 Fs/2]);

    fprintf('Case %s: True Δf=%.2f Hz, Est Δf=%.2f Hz\n', label, fd_true, fd_est);
    fprintf('         True v=%.2f m/s,    Est v=%.2f m/s\n\n', v_true, v_est);
end