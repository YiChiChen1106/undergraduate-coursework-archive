function AttackedImg = Attacking_4(Image)
% Image: 带水印的图像 (512x512x3 uint8)
disp('正在运行第4组的攻击函数 (Attacking_4) - [JPEG 压缩版]');

% --- [ 1. 设定关键参数 ] ---
% Q=95, 这是一个中等强度的攻击
Q = 95; 

% --- [ 2. 执行 JPEG 压缩攻击 ] ---
temp_filename = 'temp_attack_file.jpg';
try
    % 1. 将图像保存为 .jpg 文件 (这就是攻击)
    imwrite(Image, temp_filename, 'Quality', Q);
    
    % 2. 立即将这个被压缩过的文件重新读入
    AttackedImg = imread(temp_filename);
    
    % 3. 删除临时文件
    delete(temp_filename);
catch ME
    disp('JPEG 攻击失败:');
    disp(ME.message);
    AttackedImg = Image; % 如果失败, 返回原图
end
disp('Attacking_4 (JPEG 压缩) 运行完毕。');
end