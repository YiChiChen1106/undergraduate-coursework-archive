import nibabel as nib
import numpy as np
import os
import glob

# 你的 labelsTr 路径
label_dir = r"F:\shiwangmo\nnUNet\nnUNetFrame\nnUNet_raw\Dataset505_PAnet_DRIVE\labelsTr"
nii_files = glob.glob(os.path.join(label_dir, "*.nii.gz"))

if not nii_files:
    print("找不到文件，请检查路径！")
else:
    # 只检查前 3 个文件
    for f in nii_files[:3]:
        nii = nib.load(f)
        data = nii.get_fdata()
        unique = np.unique(data)
        print(f"文件: {os.path.basename(f)} | 包含的标签值: {unique}")

    # 如果打印结果是 [0. 1.]，那就是修好了。
    # 如果打印结果是 [0.]，说明转换还是有问题。