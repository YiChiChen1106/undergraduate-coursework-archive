import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. 修改这里的路径 ---

# 包含你的 "原始" .nii.gz 图像的文件夹 (用来和结果对比)
original_images_dir = r"F:\shiwangmo\images_to_predict"

# 包含你的 "预测结果" .nii.gz 掩码的文件夹
predictions_dir = r"F:\shiwangmo\my_predictions"

# 你想查看的文件名 (不带 .nii.gz 或 _0000.nii.gz)
file_name_to_check = "538"  # <--- 只需要把这里改成 "1"

# --- 2. 构建完整文件路径 ---
# (后面的代码不用动)
original_img_path = os.path.join(original_images_dir, f"{file_name_to_check}_0000.nii.gz")
predicted_mask_path = os.path.join(predictions_dir, f"{file_name_to_check}.nii.gz")

# --- 3. 加载 NIfTI 文件 ---
try:
    img_nii = nib.load(original_img_path)
    mask_nii = nib.load(predicted_mask_path)
except FileNotFoundError:
    print(f"错误：找不到文件，请检查你的路径和文件名 '{file_name_to_check}' 是否正确。")
    print(f"尝试加载: {original_img_path}")
    print(f"和: {predicted_mask_path}")
    exit()

# --- 4. 将 NIfTI 数据转为 Numpy 数组 ---
img_data_2d = np.squeeze(img_nii.get_fdata())
mask_data_2d = np.squeeze(mask_nii.get_fdata())

# --- 5. (关键) 创建一个“透明”的掩码 ---
mask_data_masked = np.ma.masked_where(mask_data_2d == 0, mask_data_2d)

# --- 6. 使用 Matplotlib 绘图 ---
print(f"正在为 {file_name_to_check} 生成可视化图像...")

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# 6.1. 绘制底图 (你的原始视网膜图片)
ax.imshow(img_data_2d, cmap='gray')

# 6.2. 叠加绘制掩码 (你的预测结果)
ax.imshow(mask_data_masked, cmap='Reds_r', alpha=0.6)

ax.set_title(f"预测结果: {file_name_to_check}")
ax.axis('off')  # 关闭坐标轴

plt.show() # 显示图像

print("完成！")