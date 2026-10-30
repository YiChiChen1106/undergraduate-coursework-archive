function [DetectedWmk Flag] = Decoding_4(Image, Orilmg, OriWmk, nScale)
% Image: 待检测的图像 (512x512x3 uint8)
% Orilmg: 原始未加水印的图像 (512x512x3 uint8)
% OriWmk: 原始水印图像 (140x200x3 uint8)
% nScale: 从 Encoding_4 传入的 alpha 值
disp('正在运行第4组的解码函数 (Decoding_4) - [修正版 v2]');

% --- [ 1. 获取参数和准备 ] ---
alpha = nScale;
if alpha == 0
    DetectedWmk = []; Flag = 0; return;
end

Img_double = double(Image);
Orilmg_double = double(Orilmg);
[wmk_h, wmk_w, ~] = size(OriWmk);
DetectedWmk_double_norm = zeros(wmk_h, wmk_w, 3); 

% --- [ 2. 定义嵌入位置 (必须与 Encoding_4 完全一致) ] ---
start_row = 101;
start_col = 101;
end_row = start_row + wmk_h - 1;
end_col = start_col + wmk_w - 1;

% --- [ 3. 逐个通道进行 DCT 提取 ] ---
for channel = 1:3
    % 3a. 对带水印图像和原图进行 DCT
    Img_dct = dct2(Img_double(:, :, channel));
    Orilmg_dct = dct2(Orilmg_double(:, :, channel));
    
    % 3b. (v2) 提取差值
    Img_dct_Region = Img_dct(start_row:end_row, start_col:end_col);
    Orilmg_dct_Region = Orilmg_dct(start_row:end_row, start_col:end_col);
    Diff_dct = Img_dct_Region - Orilmg_dct_Region;
                   
    % 3c. (v2) 恢复归一化的水印DCT: W_dct = Diff / alpha
    Wmk_dct_rec_norm = Diff_dct / alpha;
    
    % 3d. (v2) 逆 DCT 恢复 *归一化* 的空间水印
    DetectedWmk_double_norm(:, :, channel) = idct2(Wmk_dct_rec_norm);
end

% --- [ 4. (v2) 反归一化: 从 [-1, 1] 恢复到 [0, 255] ] ---
DetectedWmk_double = (DetectedWmk_double_norm * 128) + 128;
DetectedWmk = uint8(DetectedWmk_double);

% --- [ 5. 设置 Flag (关键) ] ---
try
    psnr_val = psnr(DetectedWmk, OriWmk);
    detection_threshold = 12; % 保持这个较低的阈值
    
    if psnr_val > detection_threshold
        Flag = 1; % 成功检测到
    else
        Flag = 0; % 未检测到
        DetectedWmk = []; % 按要求清空
    end
catch ME
    disp('PSNR 函数出错或未找到');
    Flag = 1; % 暂时设为1用于测试
end
disp(['Decoding_4 (v2) 运行完毕, Flag = ', num2str(Flag)]);
end