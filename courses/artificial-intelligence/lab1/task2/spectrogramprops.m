function [Spec_image, labels] = spectrogramprops(Clipping, Hamming, TW, OF, Te, Diff, Comb1, Comb2, Comb3, Comb4, Comb5, Comb6)

% 文件路径
Load_path = strcat(pwd, '\1 December 2017 Dataset\');
Files = dir(fullfile(Load_path, '*.dat')); % 获取文件夹下所有.dat文件
Files = natsortfiles({Files.name}); % 对文件进行自然排序
LengthFiles = length(Files); % 获取文件数量

% 预分配labels矩阵
labels = zeros(LengthFiles, 1);

% 遍历文件
for i = 1:LengthFiles
    % 打开文件并读取数据
    fileID = fopen(strcat(Load_path, Files{i}));
    
    % 文件名第一个字符代表活动类型，将其转换为数字并存入labels
    labels(i, 1) = str2num(Files{i}(1));  % 提取文件名的第一个字符并转为数字

    % 读取文件内容，dataArray包含所有数据
    dataArray = textscan(fileID, '%f');
    fclose(fileID);
    radarData = dataArray{1};  % 将数据提取为一列

    % 提取雷达参数
    fc = radarData(1);         % 第一行是中心频率
    Tsweep = radarData(2);     % 第二行是扫频时间（ms）
    Tsweep = Tsweep / 1000;    % 转换为秒
    NTS = radarData(3);        % 第三行是每次扫描的时间采样点数
    Bw = radarData(4);         % 第四行是FMCW带宽

    % 从第五行开始提取数据，I+jQ格式的复数数据
    Data = radarData(5:end);

    % 计算记录的时长和脉冲数量
    record_length = length(Data) / NTS * Tsweep;
    nc = record_length / Tsweep;

    % 将数据重塑为 [NTS x nc] 矩阵
    Data_timebis = reshape(Data, NTS, nc);

    % 运动目标检测，计算差分
    Data_time = Data_timebis(:, 2:end) - Data_timebis(:, 1:end-1);

    % 应用汉明窗
    if Hamming == 1
        win = repmat(hamming(NTS), 1, size(Data_time, 2));
    else
        win = ones(NTS, size(Data_time, 2));  % 无窗函数
    end

    % 对数据应用窗函数
    Data_time = Data_time .* win;

    % 进行FFT并计算距离维
    tmp = fft(Data_time, NTS, 1);
    Data_range_MTI = tmp(1:NTS/2, :);  % 只保留正频率部分

    %% 第二次FFT计算（多普勒维）
    bin_indl = 10;  % 范围单元的下边界
    bin_indu = 60;  % 范围单元的上边界

    % 设置频谱图参数
    MD_PRF = 1 / Tsweep;
    MD_TimeWindowLength = TW;
    MD_OverlapFactor = OF;
    MD_OverlapLength = round(MD_TimeWindowLength * MD_OverlapFactor);
    PF = 4;
    MD_Pad_Factor = PF;
    MD_FFTPoints = MD_Pad_Factor * MD_TimeWindowLength;
    MD_DopplerBin = MD_PRF / (MD_FFTPoints);
    MD_DopplerAxis = -MD_PRF / 2 : MD_DopplerBin : MD_PRF / 2 - MD_DopplerBin;
    MD_WholeDuration = size(Data_range_MTI, 2) / MD_PRF;

    % 累加计算多普勒频谱图
    myvec_MTI = sum(Data_range_MTI(bin_indl:bin_indu, :));
    Data_spec_MTI2 = fftshift(spectrogram(myvec_MTI, MD_TimeWindowLength, MD_OverlapLength, MD_FFTPoints), 1);

    % 归一化并翻转多普勒频谱图
    Data_spec_MTI2 = flipud(Data_spec_MTI2);
    Data_spec_MTI2 = Data_spec_MTI2 ./ max(max(Data_spec_MTI2));

    % 裁剪频谱图
    Time_Lim = MD_DopplerAxis .* 3e8 / 2 / 5.8e9;
    Lim = find(abs(Time_Lim) < 6);
    max_Dop = max(Lim);
    min_Dop = min(Lim);
    Data_spec_MTI2 = Data_spec_MTI2(min_Dop:max_Dop, :);
    MD_DopplerAxis = MD_DopplerAxis(min_Dop:max_Dop);

    %% 根据Clipping参数处理
    Time = max(linspace(0, MD_WholeDuration, size(Data_spec_MTI2, 2)));
    spec_Shape = size(Data_spec_MTI2);
    each = floor(spec_Shape(2) / Time);
    p = floor(Time / Clipping);

    if Clipping == 0
        feature{i} = nodivision(Data_spec_MTI2, MD_DopplerAxis, linspace(0, MD_WholeDuration, size(Data_spec_MTI2, 2)), Te, Diff, Comb1, Comb2, Comb3, Comb4, Comb5, Comb6, OF, TW, PF, Files{i});
    else
        feature{i} = division(p, Clipping, each, Data_spec_MTI2, MD_DopplerAxis, linspace(0, MD_WholeDuration, size(Data_spec_MTI2, 2)), Te, Diff, Comb1, Comb2, Comb3, Comb4, Comb5, Comb6, OF, TW, PF, Files{i});
    end
end

%% 将特征cell转换为矩阵
cell_size = size(feature);
matrix_sample = feature{1};  % 将第一个特征单元转换为矩阵
sample_size = size(matrix_sample);
matrix_sample = zeros(1, sample_size(2));  % 初始化矩阵
for u = 1:cell_size(2)
    matrix_feature = feature{u};  % 将每个特征单元转换为矩阵
    matrix_sample = vertcat(matrix_sample, matrix_feature);  % 纵向拼接
end
matrix_sample(1,:) = [];  % 删除初始化的第一行
Spec_image = matrix_sample;  % 赋值给输出变量 Spec_image

end
