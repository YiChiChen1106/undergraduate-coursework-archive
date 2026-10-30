% DTMF GUI 综合系统：三种生成+三种检测+双音识别整合
function dtmf_gui()
    % 创建主窗口
    f = figure('Name', 'DTMF Signal Generator & Analyzer', 'Position', [200 100 850 650]);

    %% Task 1: 生成 DTMF 信号
    uicontrol(f, 'Style', 'text', 'Position', [20 600 180 20], 'String', 'Task 1: Signal Generation');
    uicontrol(f, 'Style', 'text', 'Position', [20 570 150 20], 'String', 'Enter DTMF key:');
    key_input = uicontrol(f, 'Style', 'edit', 'Position', [170 570 60 25]);

    uicontrol(f, 'Style', 'text', 'Position', [250 570 120 20], 'String', 'Generation Method:');
    method_menu = uicontrol(f, 'Style', 'popupmenu', 'Position', [370 570 120 25], ...
        'String', {'Cosine', 'Look-up Table', 'Digital Oscillator'});

    uicontrol(f, 'Style', 'pushbutton', 'Position', [510 570 120 25], 'String', 'Generate & Plot', ...
        'Callback', @(src,event)generate_signal());

    ax1 = axes(f, 'Units', 'pixels', 'Position', [50 400 350 140]);
    title(ax1, 'Generated Signal');

    %% Task 2: DTMF 检测
    uicontrol(f, 'Style', 'text', 'Position', [20 370 200 20], 'String', 'Task 2: DTMF Detection');
    uicontrol(f, 'Style', 'text', 'Position', [20 340 150 20], 'String', 'Detection Method:');
    detection_method_menu = uicontrol(f, 'Style', 'popupmenu', 'Position', [[phone-redacted]], ...
        'String', {'FFT', 'Goertzel', 'LPC'});

    uicontrol(f, 'Style', 'pushbutton', 'Position', [330 340 100 30], 'String', 'Detect Key', ...
        'Callback', @(src,event)detect_signal());
    result_text = uicontrol(f, 'Style', 'text', 'Position', [450 340 250 25], 'FontSize', 12, 'String', 'Detected key: ');
    ax2 = axes(f, 'Units', 'pixels', 'Position', [430 400 350 140]);
    title(ax2, 'Spectrum');

    %% Task 3: 双音识别
    uicontrol(f, 'Style', 'text', 'Position', [20 300 200 20], 'String', 'Task 3: Piano Double Tone');
    uicontrol(f, 'Style', 'text', 'Position', [20 270 120 20], 'String', 'Select Notes:');
    notes = {'C', 'D', 'E', 'F', 'G', 'A', 'B'};
    note_input_1 = uicontrol(f, 'Style', 'popupmenu', 'Position', [140 270 80 25], 'String', notes);
    note_input_2 = uicontrol(f, 'Style', 'popupmenu', 'Position', [230 270 80 25], 'String', notes);

    uicontrol(f, 'Style', 'pushbutton', 'Position', [320 270 80 25], 'String', 'Play', ...
        'Callback', @(src,event)play_piano_notes());
    uicontrol(f, 'Style', 'pushbutton', 'Position', [410 270 100 25], 'String', 'Analyze', ...
        'Callback', @(src,event)analyze_notes());
    note_result = uicontrol(f, 'Style', 'text', 'Position', [520 270 300 25], 'FontSize', 12, 'String', '');

    ax3 = axes(f, 'Units', 'pixels', 'Position', [50 100 350 140]);
    title(ax3, 'Piano Signal');
    ax4 = axes(f, 'Units', 'pixels', 'Position', [430 100 350 140]);
    title(ax4, 'Frequency Spectrum');

    %% 全局变量
    signal = [];
    fs = 8000;
    piano_signal = [];

    %% Task 1: 生成函数
    function generate_signal()
        key = get(key_input, 'String');
        method = get(method_menu, 'Value');
        duration = 0.5;
        switch method
            case 1
                signal = generate_dtmf_cos(key, fs, duration);
            case 2
                signal = generate_dtmf_table(key, fs, duration);
            case 3
                signal = generate_dtmf_oscillator(key, fs, duration);
        end
        sound(signal, fs);
        t = (0:length(signal)-1)/fs;
        plot(ax1, t, signal);
        xlabel(ax1, 'Time (s)'); ylabel(ax1, 'Amplitude');
    end

    %% Task 2: 检测函数
    function detect_signal()
        if isempty(signal), errordlg('No signal'); return; end
        method = get(detection_method_menu, 'Value');
        switch method
            case 1
                key = detect_dtmf_fft(signal, fs);
            case 2
                key = detect_dtmf_goertzel(signal, fs);
            case 3
                key = detect_dtmf_lpc(signal, fs);
        end
        set(result_text, 'String', ['Detected key: ', key]);
        Y = abs(fft(signal));
        f = (0:length(signal)-1)*(fs/length(signal));
        plot(ax2, f(1:floor(end/2)), Y(1:floor(end/2)));
        xlabel(ax2, 'Frequency (Hz)'); ylabel(ax2, 'Magnitude');
    end

    %% Task 3: 双音检测函数
    function play_piano_notes()
        % 钢琴音符频率表 (C4-B4)
        freqs_table = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88];
        
        % 获取选择的音符
        idx1 = get(note_input_1, 'Value');
        idx2 = get(note_input_2, 'Value');
        f1 = freqs_table(idx1);
        f2 = freqs_table(idx2);
        
        % 生成带包络的钢琴音色
        fs = 44100; % 提高采样率获得更好音质
        t = 0:1/fs:1.0; % 1秒持续时间
        
        % 钢琴音色模拟（带谐波）
        tone1 = 0.5*sin(2*pi*f1*t) + 0.3*sin(2*pi*2*f1*t) + 0.2*sin(2*pi*3*f1*t);
        tone2 = 0.5*sin(2*pi*f2*t) + 0.3*sin(2*pi*2*f2*t) + 0.2*sin(2*pi*3*f2*t);
        
        % 添加指数衰减包络
        envelope = exp(-5*t);
        s = (tone1 + tone2) .* envelope;
        
        % 播放音频
        sound(s, fs);
        
        % 在ax3显示波形（前200ms）
        plot(ax3, t(1:round(0.2*fs)), s(1:round(0.2*fs)));
        title(ax3, sprintf('Piano: %.1fHz + %.1fHz', f1, f2));
        xlabel(ax3, 'Time (s)'); ylabel(ax3, 'Amplitude');
        grid(ax3, 'on');
        
        % 保存信号用于后续分析
        piano_signal = s;
    end

    function analyze_notes()
        if isempty(piano_signal)
            errordlg('Please play the notes first!');
            return;
        end
        
        freqs_table = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88];
        names = {'C','D','E','F','G','A','B'};
        fs = 44100;
        
        % 获取检测方法
        method = get(detection_method_menu, 'Value');
        
        % 执行检测
        switch method
            case 1 % FFT
                [freqs, note_names] = detect_dual_note_fft(piano_signal, fs);
                Y = abs(fft(piano_signal));
                f = (0:length(piano_signal)-1)*(fs/length(piano_signal));
                stem(ax4, f(1:floor(end/2)), Y(1:floor(end/2)));
                
            case 2 % Goertzel
                [freqs, note_names] = detect_dual_note_goertzel(piano_signal, fs);
                responses = arrayfun(@(f) goertzel_response(piano_signal, fs, f), freqs_table);
                stem(ax4, freqs_table, responses);
                
            case 3 % LPC
                [freqs, note_names] = detect_dual_note_lpc(piano_signal, fs);
                [H, w] = freqz(1, lpc(piano_signal, 12), 1024, fs);
                plot(ax4, w, abs(H));
        end
        
        title(ax4, 'Frequency Analysis');
        xlabel(ax4, 'Frequency (Hz)'); ylabel(ax4, 'Magnitude');
        grid(ax4, 'on');
        
        % 显示结果
        set(note_result, 'String', sprintf('Detected: %s (%.1fHz) + %s (%.1fHz)',...
            note_names{1}, freqs(1), note_names{2}, freqs(2)));
        % 频率分析后添加格式调整
        xlim(ax4, [0 2000]);                    % 限制频率范围
        
    end

    %% ====== 支持函数实现 ======
    function signal = generate_dtmf_cos(key, fs, duration)
        row_freqs = [697, 770, 852, 941];
        col_freqs = [1209, 1336, 1477, 1633];
        keys = ['1','2','3','A'; '4','5','6','B'; '7','8','9','C'; '*','0','#','D'];
        [row, col] = find(keys == upper(key));
        if isempty(row), error('Invalid key'); end
        f1 = row_freqs(row); f2 = col_freqs(col);
        t = 0:1/fs:duration;
        signal = cos(2*pi*f1*t) + cos(2*pi*f2*t);
    end

    function signal = generate_dtmf_table(key, fs, duration)
        dtmf_map = containers.Map(...
            {'1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D'}, ...
            {[697,1209],[697,1336],[697,1477],[697,1633],...
             [770,1209],[770,1336],[770,1477],[770,1633],...
             [852,1209],[852,1336],[852,1477],[852,1633],...
             [941,1209],[941,1336],[941,1477],[941,1633]});
        if ~isKey(dtmf_map, upper(key)), error('Invalid key'); end
        freqs = dtmf_map(upper(key));
        t = 0:1/fs:duration;
        signal = cos(2*pi*freqs(1)*t) + cos(2*pi*freqs(2)*t);
    end

    function signal = generate_dtmf_oscillator(key, fs, duration)
        [f1, f2] = get_dtmf_freqs(key);
        t = 0:1/fs:duration;
        s1 = digital_oscillator(f1, fs, t);
        s2 = digital_oscillator(f2, fs, t);
        signal = s1 + s2;
    end

    function x = digital_oscillator(f, fs, t)
        N = length(t);
        w = 2 * pi * f / fs;
        x = zeros(1, N);
        x(1:2) = [0, sin(w)];
        for n = 3:N
            x(n) = 2*cos(w)*x(n-1) - x(n-2);
        end
    end

    function [f1, f2] = get_dtmf_freqs(key)
        row_freqs = [697, 770, 852, 941];
        col_freqs = [1209, 1336, 1477, 1633];
        keys = ['1','2','3','A'; '4','5','6','B'; '7','8','9','C'; '*','0','#','D'];
        [row, col] = find(keys == upper(key));
        if isempty(row), error('Invalid key'); end
        f1 = row_freqs(row); f2 = col_freqs(col);
    end

    function key = detect_dtmf_fft(signal, fs)
        dtmf_freqs = [697,770,852,941,1209,1336,1477,1633];
        keys = ['1','2','3','A'; '4','5','6','B'; '7','8','9','C'; '*','0','#','D'];
        N = length(signal);
        f_axis = (0:N-1)*(fs/N);
        Y = abs(fft(signal));
        powers = zeros(1,length(dtmf_freqs));
        for i = 1:length(dtmf_freqs)
            [~, idx] = min(abs(f_axis - dtmf_freqs(i)));
            powers(i) = Y(idx);
        end
        [~, idxs] = maxk(powers, 2);
        row = min(idxs); col = max(idxs);
        row_idx = find([697,770,852,941] == dtmf_freqs(row));
        col_idx = find([1209,1336,1477,1633] == dtmf_freqs(col));
        key = keys(row_idx, col_idx);
    end

    function key = detect_dtmf_goertzel(signal, fs)
        dtmf_freqs = [697,770,852,941,1209,1336,1477,1633];
        keys = ['1','2','3','A'; '4','5','6','B'; '7','8','9','C'; '*','0','#','D'];
        N = length(signal);
        powers = zeros(1, length(dtmf_freqs));
        for i = 1:length(dtmf_freqs)
            k = round(dtmf_freqs(i)*N/fs);
            omega = 2*pi*k/N;
            coeff = 2*cos(omega);
            s_prev = 0; s_prev2 = 0;
            for n = 1:N
                s = signal(n) + coeff*s_prev - s_prev2;
                s_prev2 = s_prev; s_prev = s;
            end
            powers(i) = s_prev2^2 + s_prev^2 - coeff*s_prev*s_prev2;
        end
        [~, idxs] = maxk(powers,2);
        row = min(idxs); col = max(idxs);
        row_idx = find([697,770,852,941] == dtmf_freqs(row));
        col_idx = find([1209,1336,1477,1633] == dtmf_freqs(col));
        key = keys(row_idx, col_idx);
    end

    function key = detect_dtmf_lpc(signal, fs)
    % DTMF频率定义
    row_freqs = [697, 770, 852, 941];
    col_freqs = [1209, 1336, 1477, 1633];
    keys = ['1','2','3','A'; '4','5','6','B'; '7','8','9','C'; '*','0','#','D'];
    
    % 预处理
    signal = filter([1 -0.95], 1, signal); % 预加重
    win = hamming(length(signal));         % 加窗
    signal = signal .* win';
    
    % 自适应LPC阶数（每个频率至少2个极点）
    order = min(40, round(fs/1000 * 2 * 8)); % 8个频率×2极点/频率
    
    % 计算LPC
    a = lpc(signal, order);
    
    % 高分辨率频谱分析
    [h, f] = freqz(1, a, 4096, fs);
    h = 20*log10(abs(h));
    
    % 峰值检测（带约束条件）
    [pks, locs] = findpeaks(h, 'MinPeakHeight', -20, 'MinPeakDistance', 50);
    freqs = f(locs);
    
    % DTMF特定检测逻辑
    row_candidates = [];
    col_candidates = [];
    for i = 1:length(freqs)
        % 行频匹配（带3%容差）
        [min_diff, idx] = min(abs(freqs(i) - row_freqs));
        if min_diff/freqs(i) < 0.03
            row_candidates = [row_candidates; row_freqs(idx), pks(i)];
        end
        
        % 列频匹配
        [min_diff, idx] = min(abs(freqs(i) - col_freqs));
        if min_diff/freqs(i) < 0.03
            col_candidates = [col_candidates; col_freqs(idx), pks(i)];
        end
    end
    
    % 验证有效性
    if isempty(row_candidates) || isempty(col_candidates)
        key = '?';
        return;
    end
    
    % 选择幅度最大的有效频率对
    [~, row_idx] = max(row_candidates(:,2));
    [~, col_idx] = max(col_candidates(:,2));
    row_freq = row_candidates(row_idx,1);
    col_freq = col_candidates(col_idx,1);
    
    % 查找对应按键
    row_idx = find(row_freqs == row_freq);
    col_idx = find(col_freqs == col_freq);
    key = keys(row_idx, col_idx);
end

    function [freqs, notes] = detect_dual_note_fft(signal, fs)
        % 钢琴音符频率范围 (C4=261.63Hz 到 B4=493.88Hz)
        ref_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88];
        names = {'C','D','E','F','G','A','B'};
        
        % 计算FFT并限制在有效频率范围
        N = length(signal);
        Y = abs(fft(signal));
        f = (0:N-1)*(fs/N);
        
        % 关键修复：只分析200Hz-600Hz范围（避免直流和高频干扰）
        valid_range = (f >= 200) & (f <= 600);
        Y = Y(valid_range);
        f = f(valid_range);
        
        % 找频谱中最高的两个峰
        [~, idx] = maxk(Y, 2);
        freqs = f(idx);
        
        % 匹配到最近的音符（允许±10Hz容差）
        notes = cell(1,2);
        for i = 1:2
            [~, n] = min(abs(ref_freqs - freqs(i)));
            notes{i} = names{n};
        end
        
        % 按频率排序
        [freqs, idx] = sort(freqs);
        notes = notes(idx);
    end

    function [freqs, notes] = detect_dual_note_goertzel(signal, fs)
        % 钢琴音符频率表 (C4到B4)
        piano_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88];
        note_names = {'C', 'D', 'E', 'F', 'G', 'A', 'B'};
        
        N = length(signal);
        powers = zeros(1, length(piano_freqs));
        
        % 对每个钢琴音符频率应用Goertzel算法
        for i = 1:length(piano_freqs)
            % 计算Goertzel算法的参数
            k = round(piano_freqs(i) * N / fs);
            omega = 2 * pi * k / N;
            coeff = 2 * cos(omega);
            
            % Goertzel算法实现
            s_prev = 0;
            s_prev2 = 0;
            for n = 1:N
                s = signal(n) + coeff * s_prev - s_prev2;
                s_prev2 = s_prev;
                s_prev = s;
            end
            
            % 计算功率
            powers(i) = s_prev2^2 + s_prev^2 - coeff * s_prev * s_prev2;
        end
        
        % 找到两个最强频率
        [~, idxs] = maxk(powers, 2);
        freqs = piano_freqs(idxs);
        notes = note_names(idxs);
        
        % 按频率排序(从低到高)
        [freqs, sort_idx] = sort(freqs);
        notes = notes(sort_idx);
    end

    function [freqs, notes] = detect_dual_note_lpc(signal, fs)
    piano_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88];
    note_names = {'C','D','E','F','G','A','B'};
    
    % ====== 输入加固 ======
    signal = signal(:)';
    if isempty(signal) || length(signal) < 512
        freqs = [261.63, 261.63];
        notes = {'C','C'};
        return
    end
    
    % ====== 信号预处理 ======
    signal = signal / (max(abs(signal)) + eps);
    signal = filter([1 -0.999], 1, signal); % 极强预加重
    win = kaiser(length(signal), 10)';
    signal = signal .* win;
    
    % ====== LPC计算 ======
    order = min(80, max(16, round(fs/200 * 6)));
    try
        a = lpc(signal, order);
    catch
        a = [1 zeros(1,order)];
    end
    
    % ====== 频谱生成 ======
    [h, f] = freqz(1, a, 32768, fs);
    h_power = abs(h).^2 * 1e6;
    
    % ====== 频率范围限制 ======
    valid_range = (f >= 200) & (f <= 600);
    f = f(valid_range);
    h_power = h_power(valid_range);
    
    % ====== 鲁棒峰值检测 ======
    freq_weight = 1./(f.^0.1 + 1);
    weighted_spectrum = h_power .* freq_weight;
    
    [~, locs] = findpeaks(weighted_spectrum,...
        'MinPeakHeight', max(weighted_spectrum)*0.01,...
        'MinPeakDistance', 100/(fs/32768),...
        'NPeaks',4);
    
    % ====== 强制有效输出 ======
    candidate_freqs = f(locs);
    
    % 填充保证至少2个频率
    min_freqs = 2;
    valid_freqs = [candidate_freqs, 261.63*ones(1,min_freqs-length(candidate_freqs))];
    valid_freqs = valid_freqs(1:min_freqs);
    
    % 频率有效性验证
    valid_mask = (valid_freqs >= 200) & (valid_freqs <= 600);
    valid_freqs(~valid_mask) = 261.63; % 替换无效值为C4
    
    % ====== 频率匹配 ======
    [freqs, notes] = deal(zeros(1,2), cell(1,2));
    for k = 1:2
        [min_diff, idx] = min(abs(piano_freqs - valid_freqs(k)));
        if min_diff > 15 % 15Hz绝对容差
            idx = 1; % 默认C4
        end
        freqs(k) = piano_freqs(idx);
        notes{k} = note_names{idx};
    end
    [freqs, idx] = sort(freqs);
    notes = notes(idx);
end

    function response = goertzel_response(signal, fs, target_freq)
        N = length(signal);
        k = round(target_freq * N / fs);
        omega = 2 * pi * k / N;
        coeff = 2 * cos(omega);
        
        s_prev = 0;
        s_prev2 = 0;
        for n = 1:N
            s = signal(n) + coeff * s_prev - s_prev2;
            s_prev2 = s_prev;
            s_prev = s;
        end
        response = s_prev2^2 + s_prev^2 - coeff * s_prev * s_prev2;
    end
end