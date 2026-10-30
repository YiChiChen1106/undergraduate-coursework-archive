import os
import glob
from PIL import Image
import numpy as np
import SimpleITK as sitk
import json
from collections import OrderedDict

# --- 1. 定义你的路径 ---

# 你的原始数据路径
image_dir = r"F:\nnunet\shiwangmodata\JPEGImages"
label_dir = r"F:\nnunet\shiwangmodata\SegmentationClass"

# nnU-Net 的 raw 数据库路径 (根据你的第一张截图)
nnunet_raw_dir = r"F:\nnunet\Dataset\nnUNet_raw"

# --- 2. 定义新任务的名称和ID ---
# 你可以自己定义 ID 和名称，ID 建议大于 100
TASK_ID = 101
TASK_NAME = "Task101_RetinaVessel" # 任务名：TaskID_任务描述

# --- 3. 创建目标文件夹 ---
task_dir = os.path.join(nnunet_raw_dir, TASK_NAME)
imagesTr_dir = os.path.join(task_dir, "imagesTr")
labelsTr_dir = os.path.join(task_dir, "labelsTr")

os.makedirs(imagesTr_dir, exist_ok=True)
os.makedirs(labelsTr_dir, exist_ok=True)

# --- 4. 核心转换逻辑 ---
print(f"开始处理数据集: {TASK_NAME}")

# 获取所有 jpg 图像
image_files = sorted(glob.glob(os.path.join(image_dir, "*.jpg")))

# 用来生成 dataset.json 的信息
training_cases = []
num_training = 0

for img_path in image_files:
    # 从文件名获取 case ID (例如 "883")
    case_id = os.path.basename(img_path).split('.')[0]
    
    # 找到对应的 png 标签文件
    label_path = os.path.join(label_dir, f"{case_id}.png")
    
    if not os.path.exists(label_path):
        print(f"警告: 找不到对应的标签 {label_path}，跳过 {img_path}")
        continue
        
    print(f"正在处理: {case_id}")
    num_training += 1
    
    # --- A. 处理图像 (JPG -> NIfTI) ---
    img_pil = Image.open(img_path)
    img_np = np.array(img_pil) # 形状 (H, W, 3)
    
    # nnU-Net 2D 需要 (C, H, W) 格式
    img_np = img_np.transpose((2, 0, 1)) # 变为 (3, H, W)
    
    # 转换为 SimpleITK 图像对象
    img_sitk = sitk.GetImageFromArray(img_np)
    img_sitk.SetSpacing([1.0, 1.0, 1.0]) # 设置默认 spacing
    
    # 定义输出文件名 (带模态 _0000)
    output_img_name = f"{case_id}_0000.nii.gz"
    sitk.WriteImage(img_sitk, os.path.join(imagesTr_dir, output_img_name))

    # --- B. 处理标签 (PNG -> NIfTI) ---
    label_pil = Image.open(label_path)
    label_np = np.array(label_pil) # 形状 (H, W)
    
    # !!! 关键步骤：检查你的标签值 !!!
    # 你的 PNG 截图是全黑的，但我猜目标(如血管)的值是 255 (白色)
    # nnU-Net 要求标签是从 0 (背景) 开始的连续整数，例如 0, 1, 2...
    # 假设你是二分类 (背景=0, 目标=255)，我们要把 255 映射为 1
    label_np[label_np == 255] = 1
    
    # (如果你的目标值已经是 1，请注释掉上一行)
    # (如果你有多个类别，例如 0, 100, 200，你需要把它们映射为 0, 1, 2)

    # 确保数据类型为整数
    label_np = label_np.astype(np.uint8) 
    
    # 转换为 SimpleITK 图像对象
    label_sitk = sitk.GetImageFromArray(label_np)
    label_sitk.SetSpacing([1.0, 1.0, 1.0])
    
    # 定义输出文件名 (不带模态)
    output_label_name = f"{case_id}.nii.gz"
    sitk.WriteImage(label_sitk, os.path.join(labelsTr_dir, output_label_name))
    
    # 记录用于 dataset.json
    training_cases.append({
        "image": f"./imagesTr/{output_img_name}",
        "label": f"./labelsTr/{output_label_name}"
    })


# --- 5. 创建 dataset.json 文件 ---
print("正在创建 dataset.json...")

# 使用 OrderedDict 保持键的顺序
dataset_json = OrderedDict()
dataset_json["name"] = TASK_NAME
dataset_json["description"] = "Retinal Vessel Segmentation" # (修改为你的描述)
dataset_json["tensorImageSize"] = "3D" # (nnU-Net v2 总是 3D，即使是 2D 图像)
dataset_json["reference"] = "N/A"
dataset_json["licence"] = "N/A"
dataset_json["release"] = "1.0"

# 模态: 0 是 RGB
dataset_json["channel_names"] = {
    "0": "RGB"
}

# 标签: 0 是背景, 1 是目标 (例如血管)
dataset_json["labels"] = {
    "background": 0,
    "vessel": 1  # (请修改为你的分割目标, 比如 'lesion' 或 'optic_disc')
}

dataset_json["numTraining"] = num_training
dataset_json["numTest"] = 0 # 我们暂时没有测试集
dataset_json["training"] = training_cases
dataset_json["test"] = []

# 写入 json 文件
with open(os.path.join(task_dir, "dataset.json"), 'w') as f:
    json.dump(dataset_json, f, indent=4)

print(f"--- 转换完成！ ---")
print(f"总共处理了 {num_training} 个训练样本。")
print(f"数据已存入: {task_dir}")