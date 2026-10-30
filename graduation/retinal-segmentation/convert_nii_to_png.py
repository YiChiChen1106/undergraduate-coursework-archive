import nibabel as nib
import numpy as np
from PIL import Image
import os
from glob import glob
from tqdm import tqdm

# --- 1. 配置路径 ---

# [输入] 你的 nnU-Net 预测结果文件夹 (包含 0 和 1 的 .nii.gz)
nii_input_dir = r"F:\shiwangmo\drive-prediction"

# [输出] 你想保存黑白 PNG 图像的文件夹
png_output_dir = r"F:\shiwangmo\drive_prediction_images"

# --- 结束配置 ---

# 确保输出文件夹存在
os.makedirs(png_output_dir, exist_ok=True)

print(f"正在查找 {nii_input_dir} 中的 .nii.gz 文件...")

# 找到所有 .nii.gz 文件
nii_files = glob(os.path.join(nii_input_dir, "*.nii.gz"))

if not nii_files:
    print("错误：在输入文件夹中没有找到 .nii.gz 文件。")
    exit()

print(f"找到了 {len(nii_files)} 个文件。开始转换...")

for nii_path in tqdm(nii_files):
    try:
        # 1. 加载 NIfTI 文件
        nii_img = nib.load(nii_path)
        data = nii_img.get_fdata()

        # 2. 将 (W, H, D) 压缩为 (W, H)
        data_2d = np.squeeze(data)

        # 3. [关键] 转换数值：
        # 0 (背景) -> 0 (黑色)
        # 1 (血管) -> 255 (白色)
        data_2d[data_2d == 1] = 255

        # 4. 转换为 8位无符号整数 (图像的标准格式)
        data_uint8 = data_2d.astype(np.uint8)

        # 5. 使用 PIL (Pillow) 创建图像
        # 'L' 模式表示 8位灰度图
        img_pil = Image.fromarray(data_uint8, mode='L')

        # 6. 保存为 PNG
        base_name = os.path.basename(nii_path).replace(".nii.gz", ".png")
        output_path = os.path.join(png_output_dir, base_name)
        img_pil.save(output_path)

    except Exception as e:
        print(f"处理文件 {nii_path} 时出错: {e}")

print("\n---------------------------------")
print("转换完成！")
print(f"所有黑白图像已保存到: {png_output_dir}")
print("---------------------------------")