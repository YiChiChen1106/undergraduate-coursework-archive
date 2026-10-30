#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JPG + PNG → nnUNet v2  2D 分割数据集一键转换脚本
Usage:
    python -m nnunetv2.utilities.jpg_process
        -i F:/nnunet/shiwangmodata
        -o F:/nnunet/Dataset/nnUNet_raw/Dataset501_ShiWangMo
        -d 501 -n ShiWangMo
"""
import argparse
import json
import os
import cv2
import numpy as np
import nibabel as nib
from tqdm import tqdm


def convert_one_case(img_file, lab_file, out_img, out_lab):
    import cv2, numpy as np, nibabel as nib

    # 读图
    img = cv2.imread(img_file, cv2.IMREAD_COLOR)        # H,W,3
    lab = cv2.imread(lab_file, cv2.IMREAD_GRAYSCALE)    # H,W

    # RGB → 灰度
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)         # H,W

    # 2D  nnUNet 要 (H, W, 1)
    img3 = img[..., np.newaxis]      # H,W,1
    # 标签保持 (H, W)

    # 统一 affine & spacing：px, py, 1
    spacing = np.array([1.0, 1.0, 1.0])
    affine  = np.diag(spacing.tolist() + [1.0])

    nii_img = nib.Nifti1Image(img3.astype(np.uint8), affine)
    nii_lab = nib.Nifti1Image(lab.astype(np.uint8), affine)

    nib.save(nii_img, out_img)
    nib.save(nii_lab, out_lab)

def run(input_folder, output_folder, dataset_id, dataset_name):
    imagesTr = os.path.join(output_folder, 'imagesTr')
    labelsTr = os.path.join(output_folder, 'labelsTr')
    os.makedirs(imagesTr, exist_ok=True)
    os.makedirs(labelsTr, exist_ok=True)

    jpg_dir = os.path.join(input_folder, 'JPEGImages')
    png_dir = os.path.join(input_folder, 'SegmentationClass')
    jpg_files = sorted([f for f in os.listdir(jpg_dir) if f.lower().endswith('.jpg')])
    png_files = sorted([f for f in os.listdir(png_dir) if f.lower().endswith('.png')])
    assert len(jpg_files) == len(png_files), '图片与标注数量不一致'

    for img_name, lab_name in tqdm(zip(jpg_files, png_files), total=len(jpg_files)):
        case = os.path.splitext(img_name)[0]
        convert_one_case(
            os.path.join(jpg_dir, img_name),
            os.path.join(png_dir, lab_name),
            os.path.join(imagesTr, f'{case}_0000.nii.gz'),
            os.path.join(labelsTr, f'{case}.nii.gz')
        )

    # ====== nnUNet v2 必填字段 ======
    dataset_json = {
        "channel_names": {"0": "RGB"},
        "labels": {"background": 0, "foreground": 1},
        "numTraining": len(jpg_files),
        "file_ending": ".nii.gz"
    }
    with open(os.path.join(output_folder, 'dataset.json'), 'w', encoding='utf-8') as f:
        json.dump(dataset_json, f, indent=4, ensure_ascii=False)
    print(f'Dataset{dataset_id}_{dataset_name} 已生成 → {output_folder}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JPG/PNG → nnUNet v2 NIfTI (2D)')
    parser.add_argument('-i', '--input', required=True,
                        help='Directory containing JPEGImages/ and SegmentationClass/')
    parser.add_argument('-o', '--output', required=True,
                        help='Output directory (will become DatasetXXX_YYY)')
    parser.add_argument('-d', '--dataset_id', type=int, required=True,
                        help='Dataset ID (≥ 500 for custom)')
    parser.add_argument('-n', '--dataset_name', required=True,
                        help='Dataset name (no spaces)')
    args = parser.parse_args()
    run(args.input, args.output, args.dataset_id, args.dataset_name)