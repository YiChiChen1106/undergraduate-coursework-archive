function [WatermarkedImg nScale] = Encoding_4(Img, Wmk)
% ... (使用 "修正版 v2" 的代码) ...

% --- [ 1. 设定关键参数 ] ---
% !! 关键 !! 重新调高 alpha
% 我们必须先让信号强到能被嵌入, 并且强到能抗住 Q=95 的攻击
alpha = 2.9; % <-- 从 1.0 重新开始
nScale = alpha;
% 将图像转为 double 型用于计算
Img_double = double(Img);
Wmk_double = double(Wmk);

% --- [ 1b. (v2) 归一化水印 ] ---
Wmk_double_norm = (Wmk_double - 128) / 128; % 归一化到 [-1, 1]

% 获取水印尺寸
[wmk_h, wmk_w, ~] = size(Wmk);

% --- [ 2. 定义嵌入位置 (中频区) ] ---
start_row = 101;
start_col = 101;
end_row = start_row + wmk_h - 1;
end_col = start_col + wmk_w - 1;

if end_row > 512 || end_col > 512
    error('水印尺寸对于所选起始点来说太大了');
end

WatermarkedImg_double = Img_double;

% --- [ 3. 逐个通道进行 DCT 嵌入 ] ---
for channel = 1:3
    % 3a. 对原图和归一化水印进行 DCT
    Img_dct = dct2(Img_double(:, :, channel));
    Wmk_dct_norm = dct2(Wmk_double_norm(:, :, channel));
    
    % 3b. (v2) 嵌入水印: C_new = C + alpha * W_dct
    Img_dct_Region = Img_dct(start_row:end_row, start_col:end_col);
    Img_dct(start_row:end_row, start_col:end_col) = ...
        Img_dct_Region + alpha * Wmk_dct_norm;
    
    % 3c. 执行逆 DCT 恢复图像
    WatermarkedImg_double(:, :, channel) = idct2(Img_dct);
end

% --- [ 4. 转换回 uint8 ] ---
WatermarkedImg = uint8(WatermarkedImg_double);

disp('Encoding_4 (v2) 运行完毕。');
end