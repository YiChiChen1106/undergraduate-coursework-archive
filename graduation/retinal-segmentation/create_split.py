import json
import os

# --- 1. 定义文件路径 ---
# [!] 假设此脚本与 train.txt 和 val.txt 在同一目录
train_txt_path = "train.txt"
val_txt_path = "val.txt"

# [!] 这是关键：nnU-Net 存放预处理数据和 split 文件的位置
preprocessed_dir = r"F:\shiwangmo\nnUNet\nnUNetFrame\nnUNet_preprocessed\Dataset502_RetinaVessel"
output_json_path = os.path.join(preprocessed_dir, "splits_final.json")


# --- 2. 定义一个函数来读取 ID (已修正) ---
def load_ids_from_file(filepath):
    """
    读取文件，去除空白，并跳过空行和以 '[' 开头的行 (例如 )
    """
    try:
        with open(filepath, 'r') as f:
            ids = [line.strip() for line in f if line.strip() and not line.strip().startswith('[')]
            return ids
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filepath}")
        return None


# --- 3. 读取 ID ---
print(f"正在从 {train_txt_path} 读取训练 ID...")
train_ids = load_ids_from_file(train_txt_path)

print(f"正在从 {val_txt_path} 读取验证 ID...")
val_ids = load_ids_from_file(val_txt_path)

if train_ids is None or val_ids is None:
    print("脚本终止，因为文件未找到。")
    exit()

# --- 4. 构建 nnU-Net 期望的 JSON 结构 ---
# nnU-Net 期望一个 "列表 (list)"，列表中的每一项都是一个 "折" (fold)
# 我们这里只有一个固定的折 (它将被视为 fold 0)
split_data = [
    {
        "train": train_ids,
        "val": val_ids
    }
]

# --- 5. 确保目标文件夹存在并保存 JSON 文件 ---
os.makedirs(preprocessed_dir, exist_ok=True)

try:
    with open(output_json_path, 'w') as f:
        json.dump(split_data, f, indent=4)

    print("\n-------------------------------------------------")
    print(f"成功创建文件: {output_json_path}")
    print(f"此固定拆分包含: {len(train_ids)} 个训练样本, {len(val_ids)} 个验证样本。")
    print("-------------------------------------------------")

except PermissionError:
    print(f"\n错误: 权限不足，无法写入文件。")
    print(f"请检查你是否有权限写入: {output_json_path}")
except Exception as e:
    print(f"\n写入文件时发生未知错误: {e}")