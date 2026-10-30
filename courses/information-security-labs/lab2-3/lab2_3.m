% 主程序 - UESTC4036 信息安全实验（完整暴力破解范围）
clear; clc;
% ==================== 计算密钥 k ====================
guid1 = [student-id-redacted];
guid2 = [student-id-redacted];
sum_guid = guid1 + guid2;
fprintf('GUID相加结果: %d\n', sum_guid);
% 新计算方法：各位数字相加后取模26
digits = num2str(sum_guid) - '0';
k_sum = sum(digits);
k_mod = mod(k_sum, 26);
fprintf('各位数字之和 k = %d\n', k_sum);
fprintf('k_mod = mod(%d, 26) = %d\n\n', k_sum, k_mod);
k = k_mod; % 使用k_mod作为加密密钥
% ==================== 主程序执行部分 ====================
% 明文文本
plaintext = ['In this section and the next, we examine a sampling of what might be called classical ', ...
             'encryption techniques. A study of these techniques enables us to illustrate the basic ', ...
             'approaches to symmetric encryption used today and the types of cryptanalytic attacks ', ...
             'that must be anticipated. The two basic building blocks of all encryption techniques ', ...
             'are substitution and transposition. We examine these in the next two sections. Finally, ', ...
             'we discuss a system that combines both substitution and transposition.A substitution ', ...
             'technique is one in which the letters of plaintext are replaced by other letters or by ', ...
             'numbers or symbols. If the plaintext is viewed as a sequence of bits, then substitution ', ...
             'involves replacing plaintext bit patterns with ciphertext bit patterns.'];
% 任务1: 加密
fprintf('=== 任务1: 凯撒密码加密 ===\n');
ciphertext = caesar_encrypt(plaintext, k);
fprintf('加密结果(前200个字符):\n');
disp(ciphertext(1:200));
fprintf('\n');
% 任务2: 暴力破解（完整范围k=1到26）
fprintf('=== 任务2: 暴力破解凯撒密码 (k=1到26) ===\n');
brute_force_caesar(ciphertext(1:100),k);
fprintf('\n');
% 任务3: 频率分析和柱状图
fprintf('=== 任务3: 频率分析和柱状图 ===\n');
frequency_analysis_plot(plaintext, ciphertext);
fprintf('\n');
% 任务4: Playfair矩阵生成
fprintf('=== 任务4: Playfair矩阵生成 ===\n');
fprintf('关键词 "exceeding" 生成的Playfair矩阵:\n');
matrix1 = generate_playfair_matrix('exceeding');
disp(matrix1);
fprintf('\n');
fprintf('姓名 "JiangHaozhe" 生成的Playfair矩阵:\n');
matrix2 = generate_playfair_matrix('JiangHaozhe');
disp(matrix2);
fprintf('\n');
% 验证加密和解密
fprintf('=== 加密解密验证 ===\n');
test_text = 'hello world';
encrypted = caesar_encrypt(test_text, k);
decrypted = caesar_decrypt(encrypted, k);
fprintf('原文: %s\n', test_text);
fprintf('加密: %s\n', encrypted);
fprintf('解密: %s\n', decrypted);
fprintf('解密是否正确: %s\n', string(strcmp(test_text, decrypted)));
% ==================== 函数定义部分 ====================
function ciphertext = caesar_encrypt(plaintext, k)
    % 凯撒加密函数
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
    % 凯撒解密函数
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
function brute_force_caesar(ciphertext,k)
    % 暴力破解函数 - 完整范围k=1到26
    fprintf('开始暴力破解凯撒密码 (k=1到26)...\n\n');

    % 分两列显示，每列13个结果
    fprintf('%-30s %-30s\n', '第一列 (k=1-13)', '第二列 (k=14-26)');
    fprintf('%s\n', repmat('-', 1, 60));

    for row = 1:13
        % 第一列：k = 1到13
        k1 = row;
        decrypted_text1 = caesar_decrypt(ciphertext, k1);
        if length(decrypted_text1) > 25
            decrypted_text1 = [decrypted_text1(1:25) '...'];
        end

        % 第二列：k = 14到26
        k2 = row + 13;
        decrypted_text2 = caesar_decrypt(ciphertext, k2);
        if length(decrypted_text2) > 25
            decrypted_text2 = [decrypted_text2(1:25) '...'];
        end

        fprintf('k=%2d: %-25s  k=%2d: %-25s\n', k1, decrypted_text1, k2, decrypted_text2);
    end

    fprintf('\n暴力破解完成。请人工检查哪个k值能产生有意义的文本。\n');
    fprintf('提示：k=%d应该能产生有意义的英文文本（因为加密密钥k=%d）。\n', 26-k, k);
end
function frequency_analysis_plot(plaintext, ciphertext)
    % 频率分析和柱状图函数
    fprintf('开始频率分析...\n');

    % 统计明文字母频率
    plain_freq = count_letter_frequency(plaintext);
    cipher_freq = count_letter_frequency(ciphertext);

    % 显示频率统计
    fprintf('\n明文字母频率统计:\n');
    for i = 1:26
        fprintf('%c: %.2f%%  ', 'a' + i - 1, plain_freq(i));
        if mod(i, 8) == 0
            fprintf('\n');
        end
    end

    fprintf('\n\n密文字母频率统计:\n');
    for i = 1:26
        fprintf('%c: %.2f%%  ', 'a' + i - 1, cipher_freq(i));
        if mod(i, 8) == 0
            fprintf('\n');
        end
    end
    fprintf('\n');

    % 绘制柱状图
    figure('Position', [100, 100, 1200, 600]);

    % 创建单个字母的标签
    letters = cell(1, 26);
    for i = 1:26
        letters{i} = char('a' + i - 1);
    end

    subplot(1,2,1);
    bar(plain_freq, 'FaceColor', [0.2 0.6 0.8]);
    title('明文字母频率分布');
    xlabel('字母');
    ylabel('频率 (%)');
    set(gca, 'XTick', 1:26, 'XTickLabel', letters);
    grid on;
    ylim([0, max([plain_freq, cipher_freq]) * 1.1]);

    subplot(1,2,2);
    bar(cipher_freq, 'FaceColor', [0.8 0.4 0.2]);
    title('密文字母频率分布');
    xlabel('字母');
    ylabel('频率 (%)');
    set(gca, 'XTick', 1:26, 'XTickLabel', letters);
    grid on;
    ylim([0, max([plain_freq, cipher_freq]) * 1.1]);

    % 频率分析破解
    [max_freq, max_index] = max(cipher_freq);
    most_frequent_char = char('a' + max_index - 1);
    fprintf('\n密文中出现频率最高的字母: %c (%.2f%%)\n', most_frequent_char, max_freq);

    % 假设英语中最常见的字母是'e'，计算k值
    k_guess_e = mod((most_frequent_char - 'a') - ('e' - 'a'), 26);
    fprintf('假设 %c 对应 e, 推测 k = %d\n', most_frequent_char, k_guess_e);

    % 假设英语中第二常见的字母是't'，计算k值
    k_guess_t = mod((most_frequent_char - 'a') - ('t' - 'a'), 26);
    fprintf('假设 %c 对应 t, 推测 k = %d\n', most_frequent_char, k_guess_t);

    % 使用推测的k值进行解密
    fprintf('\n使用频率分析推测的k值解密:\n');
    decrypted_e = caesar_decrypt(ciphertext(1:100), k_guess_e);
    fprintf('k=%d (对应e): %s\n\n', k_guess_e, decrypted_e);

    decrypted_t = caesar_decrypt(ciphertext(1:100), k_guess_t);
    fprintf('k=%d (对应t): %s\n\n', k_guess_t, decrypted_t);

    fprintf('频率分析完成。请比较柱状图并与英语一般频率分布对比。\n');
end
function frequency = count_letter_frequency(text)
    % 统计字母频率函数
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
    % Playfair矩阵生成函数
    keyword = upper(strrep(keyword, ' ', ''));
    keyword = strrep(keyword, 'J', 'I');
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ';

    matrix_str = '';

    % 添加关键词字母（去除重复）
    for i = 1:length(keyword)
        current_char = keyword(i);
        if ~contains(matrix_str, current_char)
            matrix_str = [matrix_str, current_char];
        end
    end

    % 添加字母表中剩余的字母
    for i = 1:length(alphabet)
        current_char = alphabet(i);
        if ~contains(matrix_str, current_char)
            matrix_str = [matrix_str, current_char];
        end
    end

    % 重塑为5x5矩阵
    playfair_matrix = reshape(matrix_str, 5, 5)';
end
