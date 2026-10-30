import os
import numpy as np
import nibabel as nib
from PIL import Image
from glob import glob
from tqdm import tqdm

# --- 1. 配置路径 ---
# 预处理后的图片路径 (灰度图)
preprocessed_images_folder = r"F:\shiwangmo\shiwangmodata\drive_PAnet_preprocessed"
# 原始标签路径
original_masks_folder = r"F:\shiwangmo\shiwangmodata\driveSegmentationClass"

# nnU-Net 目标文件夹 (建议使用一个新的 Dataset ID，例如 505)
# 注意：nnU-Net 要求文件夹名格式必须是 DatasetXXX_Name
target_base_dir = r"F:\shiwangmo\nnUNet\nnUNetFrame\nnUNet_raw\Dataset505_PAnet_DRIVE"
target_imagesTr = os.path.join(target_base_dir, "imagesTr")
target_labelsTr = os.path.join(target_base_dir, "labelsTr")

# 确保目标文件夹存在
os.makedirs(target_imagesTr, exist_ok=True)
os.makedirs(target_labelsTr, exist_ok=True)

# 扩展名匹配 (根据你的实际文件修改，DRIVE 标签通常是 .gif 或 .png)
IMG_EXTENSION_SEARCH = [".jpg", ".png", ".tif"]
MASK_EXTENSION = ".png"  # 如果你的标签是 gif，请改为 .gif

# --- 2. 定义 NIfTI 元数据 ---
# 保持和你之前脚本一致的 spacing 和方向
standard_affine = np.array([
    [1, 0, 0, 0],  # X
    [0, 1, 0, 0],  # Y
    [0, 0, 1, 0],  # Z
    [0, 0, 0, 1]
], dtype=np.float32)


def find_image_file(base_folder, extensions):
    """辅助函数：查找文件夹下任意后缀的同名文件"""
    all_files = os.listdir(base_folder)
    for f in all_files:
        for ext in extensions:
            if f.endswith(ext):
                return os.path.join(base_folder, f)
    return sorted(glob(os.path.join(base_folder, "*.*")))


# --- 3. 开始转换 ---
# 获取所有图片文件
image_files = []
for ext in IMG_EXTENSION_SEARCH:
    image_files.extend(glob(os.path.join(preprocessed_images_folder, f"*{ext}")))

# 去重并排序
image_files = sorted(list(set(image_files)))
print(f"在预处理文件夹中找到了 {len(image_files)} 个图像...")

for img_path in tqdm(image_files):
    try:
        # 获取文件名（不含后缀）
        file_name_with_ext = os.path.basename(img_path)
        base_name = os.path.splitext(file_name_with_ext)[0]

        # --- A. 处理图像 (灰度图) ---
        # 预处理后的图片已经是单通道灰度图
        img_pil = Image.open(img_path).convert("L")
        img_data_hw = np.array(img_pil)  # Shape (H, W)

        # 转换为 NIfTI (W, H, D=1) 格式
        # 1. Transpose: (H, W) -> (W, H)
        img_data_wh = np.transpose(img_data_hw, (1, 0))
        # 2. Add Z dimension: (W, H, 1)
        img_data_3d = np.expand_dims(img_data_wh, axis=2)

        # 保存为 _0000.nii.gz (nnU-Net 规范：单模态/单通道)
        img_nii = nib.Nifti1Image(img_data_3d, standard_affine)
        nib.save(img_nii, os.path.join(target_imagesTr, f"{base_name}_0000.nii.gz"))

        # --- B. 处理标签 ---
        # 尝试匹配标签文件
        mask_path = os.path.join(original_masks_folder, f"{base_name}{MASK_EXTENSION}")

        # 针对 DRIVE 数据集的特殊情况：如果是 gif 且上方配置没改
        if not os.path.exists(mask_path):
            mask_path = os.path.join(original_masks_folder, f"{base_name}.gif")

        if not os.path.exists(mask_path):
            # 如果文件名不完全匹配（例如 image_01.jpg 对应 image_01_manual1.gif）
            # 这里做一个简单的容错尝试，尝试找包含 base_name 的文件
            potential_masks = glob(os.path.join(original_masks_folder, f"*{base_name}*"))
            if potential_masks:
                mask_path = potential_masks[0]
            else:
                print(f"警告: 找不到对应的标签 {base_name}，跳过...")
                continue

        mask_pil = Image.open(mask_path).convert("L")
        mask_data_hw = np.array(mask_pil)

        # !!! 关键步骤：二值化标签 !!!
        # 更安全的写法：将所有非 0 的像素都视为血管（Label 1）
        mask_data_hw[mask_data_hw > 0] = 1
        mask_data_hw = mask_data_hw.astype(np.uint8)

        # 调试打印：检查一下当前图片里到底有没有血管
        unique_vals = np.unique(mask_data_hw)
        if 1 not in unique_vals:
            print(f"⚠️ 警告: {base_name} 的标签全是 0！原始最大值是: {np.max(np.array(mask_pil))}")

        # 转换为 NIfTI (W, H, D=1)
        mask_data_wh = np.transpose(mask_data_hw, (1, 0))
        mask_data_3d = np.expand_dims(mask_data_wh, axis=2)

        mask_nii = nib.Nifti1Image(mask_data_3d, standard_affine)
        nib.save(mask_nii, os.path.join(target_labelsTr, f"{base_name}.nii.gz"))

    except Exception as e:
        print(f"处理 {base_name} 时出错: {e}")

print(f"转换完成！数据保存在: {target_base_dir}")