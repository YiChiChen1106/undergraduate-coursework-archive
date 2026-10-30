% Main Program - UESTC4036 Information Security Lab
clear; clc;

% ==================== Calculate Key k ====================
guid1 = [student-id-redacted];
guid2 = [student-id-redacted];
sum_guid = guid1 + guid2;
fprintf('Sum of GUIDs: %d\n', sum_guid);

% New calculation method: Sum of digits, then modulo 26
digits = num2str(sum_guid) - '0';
k_sum = sum(digits);
k_mod = mod(k_sum, 26);
fprintf('Sum of digits (k_sum) = %d\n', k_sum);
fprintf('k_mod = mod(%d, 26) = %d\n\n', k_sum, k_mod);

k = k_mod; % Use k_mod as the encryption key

% ==================== Main Program Execution ====================

% Plaintext
plaintext = ['In this section and the next, we examine a sampling of what might be called classical ', ...
             'encryption techniques. A study of these techniques enables us to illustrate the basic ', ...
             'approaches to symmetric encryption used today and the types of cryptanalytic attacks ', ...
             'that must be anticipated. The two basic building blocks of all encryption techniques ', ...
             'are substitution and transposition. We examine these in the next two sections. Finally, ', ...
             'we discuss a system that combines both substitution and transposition.A substitution ', ...
             'technique is one in which the letters of plaintext are replaced by other letters or by ', ...
             'numbers or symbols. If the plaintext is viewed as a sequence of bits, then substitution ', ...
             'involves replacing plaintext bit patterns with ciphertext bit patterns.'];

% Task 1: Encryption
fprintf('=== Task 1: Caesar Cipher Encryption ===\n');
ciphertext = caesar_encrypt(plaintext, k);
fprintf('Full Ciphertext Result:\n');
disp(ciphertext);
fprintf('\n');

% Task 2: Brute Force Decryption
fprintf('=== Task 2: Brute Force Caesar Cipher (k=1 to 26) ===\n');
brute_force_caesar(ciphertext(1:100));
fprintf('\n');

% Task 3: Frequency Analysis and Bar Chart
fprintf('=== Task 3: Frequency Analysis and Bar Chart ===\n');
frequency_analysis_plot(plaintext, ciphertext);
fprintf('\n');

% Task 4: Playfair Matrix Generation
fprintf('=== Task 4: Playfair Matrix Generation ===\n');
fprintf('Playfair matrix generated with keyword "exceeding":\n');
matrix1 = generate_playfair_matrix('exceeding');
disp(matrix1);
fprintf('\n');

fprintf('Playfair matrix generated with name "JiangHaozhe":\n');
matrix2 = generate_playfair_matrix('JiangHaozhe');
disp(matrix2);
fprintf('\n');

fprintf('Playfair matrix generated with name "ChenYichi":\n');
matrix2 = generate_playfair_matrix('ChenYichi');
disp(matrix2);
fprintf('\n');
% Verify Encryption and Decryption
fprintf('=== Encryption/Decryption Verification ===\n');
test_text = 'hello world';
encrypted = caesar_encrypt(test_text, k);
decrypted = caesar_decrypt(encrypted, k);
fprintf('Original: %s\n', test_text);
fprintf('Encrypted: %s\n', encrypted);
fprintf('Decrypted: %s\n', decrypted);
fprintf('Decryption correct: %s\n', string(strcmp(test_text, decrypted)));

% ==================== Function Definitions ====================

function ciphertext = caesar_encrypt(plaintext, k)
    % Caesar encryption function
    plaintext = lower(plaintext);
    ciphertext = '';
    
    for i = 1:length(plaintext)
        char_i = plaintext(i);
        
        if char_i >= 'a' && char_i <= 'z'
            p = char_i - 'a';
            c = mod(p + k, 26);
            cipher_char = char('a' + c);
            ciphertext = [ciphertext, cipher_char];
        else
            ciphertext = [ciphertext, char_i];
        end
    end
end

function decrypted_text = caesar_decrypt(ciphertext, k)
    % Caesar decryption function
    ciphertext = lower(ciphertext);
    decrypted_text = '';
    
    for i = 1:length(ciphertext)
        char_i = ciphertext(i);
        
        if char_i >= 'a' && char_i <= 'z'
            c = char_i - 'a';
            p = mod(c - k, 26);
            if p < 0
                p = p + 26;
            end
            decrypted_char = char('a' + p);
            decrypted_text = [decrypted_text, decrypted_char];
        else
            decrypted_text = [decrypted_text, char_i];
        end
    end
end

function brute_force_caesar(ciphertext)

    fprintf('Starting Caesar Cipher Brute Force (k=1 to 26)...\n\n');
    
    for test_k = 1:26
        decrypted_text = caesar_decrypt(ciphertext, test_k);
        fprintf('k = %2d: %s\n\n', test_k, decrypted_text);
    end
    
    fprintf('Brute force complete. Please manually check which k-value produces meaningful text.\n');
    fprintf('Hint: k=13 should produce the meaningful English text.\n');
end

function frequency_analysis_plot(plaintext, ciphertext)
    % Frequency analysis and bar chart function
    fprintf('Starting frequency analysis...\n');
    
    % Count plaintext letter frequency
    plain_freq = count_letter_frequency(plaintext);
    cipher_freq = count_letter_frequency(ciphertext);
    
    % Display frequency statistics
    fprintf('\nPlaintext Letter Frequency Statistics:\n');
    for i = 1:26
        fprintf('%c: %.2f%%  ', 'a' + i - 1, plain_freq(i));
        if mod(i, 8) == 0
            fprintf('\n');
        end
    end
    
    fprintf('\n\nCiphertext Letter Frequency Statistics:\n');
    for i = 1:26
        fprintf('%c: %.2f%%  ', 'a' + i - 1, cipher_freq(i));
        if mod(i, 8) == 0
            fprintf('\n');
        end
    end
    fprintf('\n');
    
    % Plot bar chart - Corrected X-axis labels
    figure('Position', [100, 100, 1200, 600]);
    
    % Create labels for each letter
    letters = cell(1, 26);
    for i = 1:26
        letters{i} = char('a' + i - 1);
    end
    
    subplot(1,2,1);
    bar(plain_freq, 'FaceColor', [0.2 0.6 0.8]);
    title('Plaintext Letter Frequency Distribution');
    xlabel('Letter');
    ylabel('Frequency (%)');
    set(gca, 'XTick', 1:26, 'XTickLabel', letters,'XTickLabelRotation', 0);
    grid on;
    ylim([0, max([plain_freq, cipher_freq]) * 1.1]);
    
    subplot(1,2,2);
    bar(cipher_freq, 'FaceColor', [0.8 0.4 0.2]);
    title('Ciphertext Letter Frequency Distribution');
    xlabel('Letter');
    ylabel('Frequency (%)');
    set(gca, 'XTick', 1:26, 'XTickLabel', letters,'XTickLabelRotation', 0);
    grid on;
    ylim([0, max([plain_freq, cipher_freq]) * 1.1]);
    
    % Frequency analysis cryptanalysis
    [max_freq, max_index] = max(cipher_freq);
    most_frequent_char = char('a' + max_index - 1);
    fprintf('\nMost frequent letter in ciphertext: %c (%.2f%%)\n', most_frequent_char, max_freq);
    
    % Assuming most common English letter is 'e', calculate k
    k_guess_e = mod((most_frequent_char - 'a') - ('e' - 'a'), 26);
    fprintf('Assuming %c corresponds to e, guessed k = %d\n', most_frequent_char, k_guess_e);
    
    % Assuming second most common English letter is 't', calculate k
    k_guess_t = mod((most_frequent_char - 'a') - ('t' - 'a'), 26);
    fprintf('Assuming %c corresponds to t, guessed k = %d\n', most_frequent_char, k_guess_t);
    
    % Decrypt using the guessed k values
    fprintf('\nDecrypting with k values from frequency analysis:\n');
    decrypted_e = caesar_decrypt(ciphertext(1:100), k_guess_e);
    fprintf('k=%d (from e): %s\n\n', k_guess_e, decrypted_e);
    
    decrypted_t = caesar_decrypt(ciphertext(1:100), k_guess_t);
    fprintf('k=%d (from t): %s\n\n', k_guess_t, decrypted_t);
    
    fprintf('Frequency analysis complete. Please compare the bar charts with general English frequency distribution.\n');
end

function frequency = count_letter_frequency(text)
    % Function to count letter frequency
    letter_count = zeros(1, 26);
    total_letters = 0;
    
    text = lower(text);
    for i = 1:length(text)
        char_i = text(i);
        if char_i >= 'a' && char_i <= 'z'
            index = char_i - 'a' + 1;
            letter_count(index) = letter_count(index) + 1;
            total_letters = total_letters + 1;
        end
    end
    
    frequency = (letter_count / total_letters) * 100;
end

function playfair_matrix = generate_playfair_matrix(keyword)
    % Playfair matrix generation function
    keyword = upper(strrep(keyword, ' ', ''));
    keyword = strrep(keyword, 'J', 'I');
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ';
    
    matrix_str = '';
    
    % Add keyword letters (remove duplicates)
    for i = 1:length(keyword)
        current_char = keyword(i);
        if ~contains(matrix_str, current_char)
            matrix_str = [matrix_str, current_char];
        end
    end
    
    % Add remaining letters from the alphabet
    for i = 1:length(alphabet)
        current_char = alphabet(i);
        if ~contains(matrix_str, current_char)
            matrix_str = [matrix_str, current_char];
        end
    end
    
    % Reshape into 5x5 matrix
    playfair_matrix = reshape(matrix_str, 5, 5)';
end