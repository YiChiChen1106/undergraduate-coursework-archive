import nibabel as nib
import numpy as np
from PIL import Image
import os
from glob import glob
from tqdm import tqdm

# --- 1. 配置路径 ---

# [输入] 你的 nnU-Net 预测结果文件夹 (包含 0 和 1 的 .nii.gz)
nii_input_dir = r"F:\shiwangmo\drive-clahe-focal100-prediction"  # <-- 确认这是你的预测结果 .nii.gz 文件夹

# [输出] 你想保存 顺时针旋转90度+左右翻转后 的黑白 PNG 图像的文件夹
png_output_dir = r"F:\shiwangmo\drive-clahe-focal100-prediction-images"  # <-- 新建一个文件夹

# --- 结束配置 ---

# 确保输出文件夹存在
os.makedirs(png_output_dir, exist_ok=True)

print(f"正在查找 {nii_input_dir} 中的 .nii.gz 文件...")
nii_files = glob(os.path.join(nii_input_dir, "*.nii.gz"))
if not nii_files:
    print("错误：在输入文件夹中没有找到 .nii.gz 文件。")
    exit()

print(f"找到了 {len(nii_files)} 个文件。开始转换、顺时针旋转90度并进行左右翻转...")

for nii_path in tqdm(nii_files):
    try:
        # 1. 加载 NIfTI 文件
        nii_img = nib.load(nii_path)
        # 使用 get_fdata() 获取 NumPy 数组 (通常 W x H x D)
        data = nii_img.get_fdata()

        # 2. 压缩为 2D 数组
        data_2d = np.squeeze(data)

        # 3. 转换数值：0 -> 0 (黑色), 1 -> 255 (白色)
        processed_data = data_2d.copy()
        processed_data[processed_data == 1] = 255

        # 4. [关键] 进行顺时针旋转 90 度
        # np.rot90(m, k=-1) 表示顺时针旋转 90 度
        data_rotated = np.rot90(processed_data, k=-1)

        # 5. [关键] 对旋转后的结果进行左右翻转 (水平翻转)
        data_flipped = np.fliplr(data_rotated)

        # 6. 转换为 8位无符号整数
        data_uint8 = data_flipped.astype(np.uint8)

        # 7. 使用 PIL 创建图像
        # 'L' 模式表示 8位灰度图
        # Pillow 通常期望 H x W 顺序，需要检查 np.rot90 和 np.fliplr 后的数组维度顺序是否匹配
        # 如果保存的 PNG 方向不对，可能需要调整这里的数组或使用 PIL 的 transpose
        img_pil = Image.fromarray(data_uint8, mode='L')

        # 8. 保存为 PNG
        base_name = os.path.basename(nii_path).replace(".nii.gz", ".png")
        output_path = os.path.join(png_output_dir, base_name)
        img_pil.save(output_path)

    except Exception as e:
        print(f"处理文件 {nii_path} 时出错: {e}")

print("\n---------------------------------")
print("转换、旋转和翻转完成！")
print(f"所有处理后的黑白图像已保存到: {png_output_dir}")
print("---------------------------------")