import os
import json
from glob import glob

# --- 配置 ---
# 必须和脚本 1 中的 target_base_dir 保持一致
target_base_dir = r"F:\shiwangmo\nnUNet\nnUNetFrame\nnUNet_raw\Dataset505_PAnet_DRIVE"
output_json_file = os.path.join(target_base_dir, "dataset.json")


def generate_dataset_json():
    imagesTr_dir = os.path.join(target_base_dir, "imagesTr")

    # 获取所有的训练图像文件名 (不包含 _0000.nii.gz 后缀)
    # nnU-Net 的 json 只需要文件名，不需要路径
    image_files = sorted(glob(os.path.join(imagesTr_dir, "*_0000.nii.gz")))

    training_list = []
    for img_path in image_files:
        file_name = os.path.basename(img_path)
        # 移除 _0000.nii.gz 得到 Case Identifier
        case_id = file_name.replace("_0000.nii.gz", "")

        # 添加到列表
        training_list.append({
            "image": f"./imagesTr/{case_id}.nii.gz",
            "label": f"./labelsTr/{case_id}.nii.gz"
        })

    # 构建 JSON 结构
    json_dict = {
        "channel_names": {
            "0": "Grayscale_PANet"  # 通道名称，名字可以随便取
        },
        "labels": {
            "background": 0,
            "vessel": 1
        },
        "numTraining": len(training_list),
        "file_ending": ".nii.gz",
        "name": "Dataset505_PAnet_DRIVE",
        "reference": "DRIVE Dataset processed with PA-Net preprocessing",
        "description": "Retinal vessel segmentation",
        "release": "1.0",
        "tensorImageSize": "3D",  # 虽然是 2D 数据，但我们保存成了 (W,H,1) 的伪 3D
        "training": training_list
    }

    # 写入文件
    with open(output_json_file, 'w') as f:
        json.dump(json_dict, f, indent=4)

    print(f"dataset.json 已生成: {output_json_file}")
    print(f"共包含 {len(training_list)} 个训练样本。")


if __name__ == "__main__":
    generate_dataset_json()