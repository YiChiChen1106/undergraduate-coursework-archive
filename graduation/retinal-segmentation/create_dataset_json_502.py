import json
import os
from glob import glob
from collections import OrderedDict # 保持 JSON 顺序，更易读

# --- 配置 ---
# [!] 新数据集在 nnUNet_raw 中的路径
dataset_base_dir = r"F:\shiwangmo\nnUNet\nnUNetFrame\nnUNet_raw\Dataset502_RetinaVessel"
output_json_path = os.path.join(dataset_base_dir, "dataset.json")

# [!] 通道名称 (因为是RGB分离的，保持不变)
channel_names = {
    "0": "Red",
    "1": "Green",
    "2": "Blue"
}

# [!] 标签名称 (0 通常是背景，1 是前景)
labels = {
    "background": 0,
    "vessel": 1 # 确认你的标签文件中血管的值是 1
}

# [!] 文件扩展名
file_ending = ".nii.gz"

# --- 自动计算训练样本数量 ---
# 假设 imagesTr 中的 _0000 文件代表一个样本
num_training = len(glob(os.path.join(dataset_base_dir, "imagesTr", "*_0000" + file_ending)))

# --- 构建 dataset.json 内容 ---
json_content = OrderedDict() # 使用 OrderedDict 保持顺序
json_content["channel_names"] = channel_names
json_content["labels"] = labels
json_content["numTraining"] = num_training
json_content["file_ending"] = file_ending
# 你可以添加其他可选字段，如 "description", "name" 等，但以上是必需的

# --- 保存 JSON 文件 ---
os.makedirs(dataset_base_dir, exist_ok=True)
with open(output_json_path, 'w') as f:
    json.dump(json_content, f, indent=4)

print(f"成功创建 dataset.json 文件于: {output_json_path}")
print(f"检测到 {num_training} 个训练样本。")
print(f"通道: {channel_names}")
print(f"标签: {labels}")