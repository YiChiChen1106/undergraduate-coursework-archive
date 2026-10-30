import os
import numpy as np
import nibabel as nib
from PIL import Image
from glob import glob
from tqdm import tqdm

# --- 1. 配置路径 ---
# !!! 修改为你存放原始 JPG/PNG 的真实路径 !!!

# 存放原始彩色 JPG 图像的文件夹
original_images_folder = r"F:\shiwangmo\unet_clahe\images"
# 存放原始黑白 PNG 标签的文件夹
original_masks_folder = r"F:\shiwangmo\unet_clahe\labels"

# nnU-Net 目标文件夹 (这些不用改)
target_base_dir = r"F:\shiwangmo\nnUNet\nnUNetFrame\nnUNet_raw\Dataset502_RetinaVessel"
target_imagesTr = os.path.join(target_base_dir, "imagesTr")
target_labelsTr = os.path.join(target_base_dir, "labelsTr")

# 确保目标文件夹存在
os.makedirs(target_imagesTr, exist_ok=True)
os.makedirs(target_labelsTr, exist_ok=True)

# !!! 你的原始图像和标签的文件扩展名是什么? (例如 .jpg, .png)
IMG_EXTENSION = ".jpg"
MASK_EXTENSION = ".png"  # 标签通常是 png

# --- 2. 定义 NIfTI 元数据 (关键) ---
# 这保证了 spacing = (1.0, 1.0, 1.0)
# NIfTI 格式 (X, Y, Z) 对应 (Width, Height, Depth)
standard_affine = np.array([
    [1, 0, 0, 0],  # X (Width)
    [0, 1, 0, 0],  # Y (Height)
    [0, 0, 1, 0],  # Z (Depth)
    [0, 0, 0, 1]
], dtype=np.float32)

# --- 3. 开始转换 ---
image_paths = sorted(glob(os.path.join(original_images_folder, f"*{IMG_EXTENSION}")))
print(f"找到了 {len(image_paths)} 个原始图像...")

for img_path in tqdm(image_paths):
    try:
        base_name = os.path.basename(img_path).replace(IMG_EXTENSION, "")

        # --- A. 处理图像 (JPG/PNG) ---
        img_pil = Image.open(img_path).convert("RGB")  # Shape (Height, Width)
        img_data_hwc = np.array(img_pil)  # Shape (H, W, C) -> (512, 512, 3)

        # 转换为 NIfTI (W, H, C) 格式
        img_data_whc = np.transpose(img_data_hwc, (1, 0, 2))  # Shape (W, H, C) -> (512, 512, 3)

        # 拆分为 3 个 NIfTI 文件
        # (注意: 我们添加一个 Z 轴，使其变为 (W, H, D=1) )
        r_data_3d = np.expand_dims(img_data_whc[:, :, 0], axis=2)  # Shape (512, 512, 1)
        g_data_3d = np.expand_dims(img_data_whc[:, :, 1], axis=2)  # Shape (512, 512, 1)
        b_data_3d = np.expand_dims(img_data_whc[:, :, 2], axis=2)  # Shape (512, 512, 1)

        # 使用标准 affine 保存
        r_nii = nib.Nifti1Image(r_data_3d, standard_affine)
        g_nii = nib.Nifti1Image(g_data_3d, standard_affine)
        b_nii = nib.Nifti1Image(b_data_3d, standard_affine)

        nib.save(r_nii, os.path.join(target_imagesTr, f"{base_name}_0000.nii.gz"))
        nib.save(g_nii, os.path.join(target_imagesTr, f"{base_name}_0001.nii.gz"))
        nib.save(b_nii, os.path.join(target_imagesTr, f"{base_name}_0002.nii.gz"))

        # --- B. 处理标签 (PNG) ---
        mask_path = os.path.join(original_masks_folder, f"{base_name}{MASK_EXTENSION}")
        if not os.path.exists(mask_path):
            print(f"警告: 找不到对应的标签 {mask_path}，跳过...")
            continue

        mask_pil = Image.open(mask_path).convert("L")  # 灰度图
        mask_data_hw = np.array(mask_pil)  # Shape (H, W) -> (512, 512)

        # 转换为 NIfTI (W, H) 格式
        mask_data_wh = np.transpose(mask_data_hw, (1, 0))  # Shape (W, H) -> (512, 512)

        # 添加 Z 轴 (Depth)，使其变为 (W, H, D=1)
        mask_data_3d = np.expand_dims(mask_data_wh, axis=2)  # Shape (512, 512, 1)

        # 使用与图像完全相同的 standard_affine 保存
        mask_nii = nib.Nifti1Image(mask_data_3d, standard_affine)
        mask_nii.set_data_dtype(np.uint8)

        nib.save(mask_nii, os.path.join(target_labelsTr, f"{base_name}.nii.gz"))

    except Exception as e:
        print(f"处理 {base_name} 时出错: {e}")

print("转换完成！")