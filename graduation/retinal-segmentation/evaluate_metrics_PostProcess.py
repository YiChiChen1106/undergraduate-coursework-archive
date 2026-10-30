import os
import numpy as np
import nibabel as nib
from sklearn.metrics import confusion_matrix, roc_auc_score
from glob import glob
from tqdm import tqdm
from skimage import morphology

# ================= 配置区域 =================
# 1. 真实标签文件夹
gt_folder = os.environ.get(
    "NNUNET_GT_FOLDER",
    "/mnt/f/shiwangmo/nnUNetFrame/nnUNet_raw/Dataset505_PAnet_DRIVE/labelsTr",
)

# 2. 预测结果文件夹
# 默认评估 nnUNetv2_find_best_configuration 生成的 postprocessed 结果。
pred_folder = os.environ.get(
    "NNUNET_PRED_FOLDER",
    "/mnt/f/shiwangmo/nnUNetFrame/nnUNet_results/"
    "Dataset505_PAnet_DRIVE/"
    "nnUNetTrainer_MSDSConv_clDice__nnUNetPlans__2d/"
    "crossval_results_folds_0_1_2_3_4/postprocessed",
)
# ============================================

def calculate_metrics_with_postprocess(threshold):
    pred_files = glob(os.path.join(pred_folder, "*.nii.gz"))
    pred_files = [f for f in pred_files if not f.endswith("_probabilities.nii.gz")]

    if len(pred_files) == 0:
        print(f"❌ 错误: 路径下没有找到文件")
        return

    print(f"\n🔎 正在评估 (阈值: {threshold})...")
    metrics = {"SE": [], "SP": [], "ACC": [], "AUC": [], "PR": [], "F1": []}

    for pred_path in tqdm(pred_files):
        filename = os.path.basename(pred_path)
        
        # 1. 读取并进行面积滤波
        pred_nii = nib.load(pred_path)
        pred_data = pred_nii.get_fdata().astype(np.uint8)
        
        if threshold > 0:
            pred_data = morphology.remove_small_objects(
                pred_data.astype(bool), 
                min_size=threshold, 
                connectivity=2
            ).astype(np.uint8)

        pred_binary = pred_data.flatten()

        # 2. 读取标签
        gt_path = os.path.join(gt_folder, filename)
        if not os.path.exists(gt_path):
            alt_name = filename.replace("_0000.nii.gz", ".nii.gz")
            gt_path = os.path.join(gt_folder, alt_name)
        if not os.path.exists(gt_path): continue

        gt_data = nib.load(gt_path).get_fdata().flatten().astype(int)
        gt_data[gt_data > 0] = 1

        # 3. 计算 AUC (尝试读取概率图)
        try:
            npz_path = pred_path.replace(".nii.gz", ".npz")
            if os.path.exists(npz_path):
                probs = np.load(npz_path)['probabilities'][1].flatten().astype(np.float32)
                auc = roc_auc_score(gt_data, probs)
            else:
                auc = roc_auc_score(gt_data, pred_binary)
        except:
            auc = 0.0

        # 4. 计算混淆矩阵与各项指标
        tn, fp, fn, tp = confusion_matrix(gt_data, pred_binary, labels=[0, 1]).ravel()
        epsilon = 1e-6

        se = tp / (tp + fn + epsilon)
        sp = tn / (tn + fp + epsilon)
        acc = (tp + tn) / (tp + tn + fp + fn + epsilon)
        pr = tp / (tp + fp + epsilon)
        f1 = 2 * pr * se / (pr + se + epsilon)

        metrics["SE"].append(se); metrics["SP"].append(sp); metrics["ACC"].append(acc)
        metrics["AUC"].append(auc); metrics["PR"].append(pr); metrics["F1"].append(f1)

    # --- 5. 格式化输出 (带标准差) ---
    print("\n" + "=" * 50)
    print(f"📊 5折交叉验证汇总 (面积阈值: {threshold})")
    print("=" * 50)
    print(f"{'Metric':<10} | {'Mean':<10} | {'Std Dev':<10}")
    print("-" * 34)

    for k, v in metrics.items():
        if len(v) > 0:
            mean_val = np.mean(v)
            std_val = np.std(v) # 这里增加了标准差的计算
            print(f"{k:<10} | {mean_val:.4f}     | {std_val:.4f}")
    
    print("=" * 50)

if __name__ == "__main__":
    # 你可以只跑你最看好的那个阈值
    target_thresholds = [0, 20, 30, 50, 90]
    for t in target_thresholds:
        calculate_metrics_with_postprocess(t)