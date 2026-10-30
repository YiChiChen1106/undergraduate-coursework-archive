import os
import numpy as np
import nibabel as nib
from sklearn.metrics import confusion_matrix, roc_auc_score
from glob import glob
from tqdm import tqdm

# ================= 配置区域 (请修改这里) =================

# 1. 真实标签文件夹 (Ground Truth, labelsTr)
# 指向你 dataset.json 里定义的 labelsTr 文件夹
gt_folder = r"F:\shiwangmo\nnUNetFrame\nnUNet_raw\Dataset505_PAnet_DRIVE\labelsTr"

# 2. 预测结果文件夹 (Predictions)
# 指向 nnUNetv2_find_best_configuration 生成的 cv_niftis_raw 文件夹
# 路径通常很长，请确保复制完全
pred_folder = r"F:\shiwangmo\nnUNetFrame\nnUNet_results\Dataset505_PAnet_DRIVE\nnUNetTrainerPANet_MSDeformableLPT_CA_NoAFFM__nnUNetPlans__2d\crossval_results_folds_0_1_2_3_4"


# ==========================================================

def calculate_metrics():
    # 查找所有 .nii.gz 预测文件
    # 排除 .npz (概率文件) 和 .json (元数据)
    pred_files = glob(os.path.join(pred_folder, "*.nii.gz"))
    pred_files = [f for f in pred_files if not f.endswith("_probabilities.nii.gz")]

    if len(pred_files) == 0:
        print(f"❌ 错误: 在 {pred_folder} 中没有找到 .nii.gz 文件。请检查路径是否正确。")
        return

    print(f"🔎 找到 {len(pred_files)} 个预测文件，开始评估...")

    # 初始化指标列表
    metrics = {
        "SE": [], "SP": [], "ACC": [], "AUC": [], "PR": [], "F1": []
    }

    # 使用 tqdm 显示进度条
    for pred_path in tqdm(pred_files):
        filename = os.path.basename(pred_path)

        # --- 1. 读取预测结果 ---
        pred_nii = nib.load(pred_path)
        pred_data = pred_nii.get_fdata().flatten()  # 展平为一维数组
        # 强制二值化 (确保只有 0 和 1)
        pred_binary = (pred_data > 0).astype(int)

        # --- 2. 读取真实标签 ---
        gt_path = os.path.join(gt_folder, filename)

        # 容错处理：有时 nnU-Net 会去掉 _0000 后缀，有时不会，确保能找到对应的 label
        if not os.path.exists(gt_path):
            # 尝试去掉 _0000 (如果有)
            alt_name = filename.replace("_0000.nii.gz", ".nii.gz")
            gt_path = os.path.join(gt_folder, alt_name)

        if not os.path.exists(gt_path):
            print(f"\n⚠️ 警告: 找不到对应的标签文件: {filename}，已跳过。")
            continue

        gt_nii = nib.load(gt_path)
        gt_data = gt_nii.get_fdata().flatten().astype(int)

        # 确保 GT 也是二值的 (0和1)
        gt_data[gt_data > 0] = 1

        # --- 3. 计算 AUC ---
        # 优先尝试读取 .npz 概率文件以获得精确 AUC
        # nnU-Net 的 cv_niftis_raw 文件夹里通常只包含 .nii.gz (二值图)
        # 除非你之前重新跑了带 --npz 的验证。
        # 如果没有概率图，我们基于二值图计算 AUC (虽不完美，但可运行)
        try:
            npz_path = pred_path.replace(".nii.gz", ".npz")
            if os.path.exists(npz_path):
                npz_content = np.load(npz_path)
                # 关键点：[1]代表血管类，必须 flatten 并转为 float32
                probs = npz_content['probabilities'][1].flatten().astype(np.float32)
                auc = roc_auc_score(gt_data, probs)
            else:
                # 如果找不到 .npz，说明推理时没加 --save_probabilities
                print(f"⚠️ 警告: {filename} 缺失 .npz，AUC 将回落至二值计算")
                auc = roc_auc_score(gt_data, pred_binary)
        except Exception as e:
            # 如果出错（例如只有一个类别），AUC 设为 NaN 或 0
            auc = 0.0

        # --- 4. 计算混淆矩阵 ---
        # labels=[0, 1] 确保即使某张图没有血管也能正确返回 2x2 矩阵
        try:
            tn, fp, fn, tp = confusion_matrix(gt_data, pred_binary, labels=[0, 1]).ravel()
        except ValueError:
            # 极少数情况可能出现 shape 不匹配
            print(f"Skipping {filename} due to shape mismatch.")
            continue

        # --- 5. 根据论文公式计算指标 ---
        # 加上 1e-6 防止除以 0
        epsilon = 1e-6

        # SE (Sensitivity) = TP / (TP + FN)
        se = tp / (tp + fn + epsilon)

        # SP (Specificity) = TN / (TN + FP)
        sp = tn / (tn + fp + epsilon)

        # ACC (Accuracy)
        acc = (tp + tn) / (tp + tn + fp + fn + epsilon)

        # PR (Precision) = TP / (TP + FP)
        pr = tp / (tp + fp + epsilon)

        # F1 Score = 2 * PR * SE / (PR + SE)
        f1 = 2 * pr * se / (pr + se + epsilon)

        # 存入字典
        metrics["SE"].append(se)
        metrics["SP"].append(sp)
        metrics["ACC"].append(acc)
        metrics["AUC"].append(auc)
        metrics["PR"].append(pr)
        metrics["F1"].append(f1)

    # --- 6. 输出最终结果 ---
    print("\n" + "=" * 40)
    print("📊 最终 5折交叉验证 平均指标 (Mean Metrics)")
    print("=" * 40)

    # 格式化输出，方便复制
    print(f"{'Metric':<10} | {'Mean':<10} | {'Std Dev':<10}")
    print("-" * 34)

    for k, v in metrics.items():
        if len(v) > 0:
            mean_val = np.mean(v)
            std_val = np.std(v)
            print(f"{k:<10} | {mean_val:.4f}     | {std_val:.4f}")
        else:
            print(f"{k:<10} | N/A")

    print("=" * 40)
    print("✅ 完成！以上数值即为对应论文 Table 1 的复现结果。")


if __name__ == "__main__":
    calculate_metrics()