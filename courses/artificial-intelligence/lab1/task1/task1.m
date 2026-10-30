% Load the T_junction_best.mat file and extract S-parameter and frequency data
data = load('T_junction_best.mat');
freq = data.freq;  % Frequency
S11_val = data.S11db;  % S11 in dB
S21_val = data.S21dB;  % S21 in dB
S31_val = data.S31db;  % S31 in dB

% Define the evaluation function
function perf = evaluate(f, S11_val, S21_val, S31_val)
    % Define frequency ranges and design specifications
    S11_spec1 = -20;  % S11 threshold for 12.5~12.75 GHz and 13~13.25 GHz
    S21_spec1 = -20;  % S21 threshold for 12~12.3 GHz
    S21_spec2 = -55;  % S21 threshold for 13~13.25 GHz
    S31_spec1 = -55;  % S31 threshold for 12.5~12.75 GHz
    S31_spec2 = -20;  % S31 threshold for 13.4~13.75 GHz

    % Initialize performance evaluation result
    perf = zeros(1, 6);

    % Calculate deviations for S11
    E1 = max(S11_val(f >= 12.5 & f <= 12.75) - S11_spec1);
    E2 = max(S11_val(f >= 13 & f <= 13.25) - S11_spec1);
    if E1 <= 0, E1 = 0; end
    if E2 <= 0, E2 = 0; end
    perf(1) = E1;  % Record deviation value
    perf(2) = E2;

    % Calculate deviations for S21
    E3 = max(S21_val(f >= 12 & f <= 12.3) - S21_spec1);
    E4 = max(S21_val(f >= 13 & f <= 13.25) - S21_spec2);
    if E3 <= 0, E3 = 0; end
    if E4 <= 0, E4 = 0; end
    perf(3) = E3;
    perf(4) = E4;

    % Calculate deviations for S31
    E5 = max(S31_val(f >= 12.5 & f <= 12.75) - S31_spec1);
    E6 = max(S31_val(f >= 13.4 & f <= 13.75) - S31_spec2);
    if E5 <= 0, E5 = 0; end
    if E6 <= 0, E6 = 0; end
    perf(5) = E5;
    perf(6) = E6;
end

% Run the evaluation function
perf = evaluate(freq, S11_val, S21_val, S31_val);
disp('Performance evaluation result:');
disp(perf);
