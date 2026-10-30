import os
import numpy as np
from PIL import Image
from sklearn.metrics import confusion_matrix
from glob import glob
from tqdm import tqdm

# --- 1. 配置路径和参数 ---

# [!] 包含你的模型预测结果的文件夹 (假设是黑白 PNG, 血管=255, 背景=0)
# prediction_dir = r"F:\shiwangmo\drive_prediction_images" # <-- 使用你认为方向正确的预测文件夹
prediction_dir = r"F:\shiwangmo\drive-clahe-focal100-prediction-images"  # 或者这个，或者你最新生成的那个
# prediction_dir = r"F:\shiwangmo\drive_prediction_images_rot_cw_flipped" # 或者这个

# [!] 包含你的真实分割标签 (Ground Truth) 的文件夹 (也假设是黑白 PNG)
ground_truth_dir = r"F:\shiwangmo\unet_clahe\labels"

# [!] 确认你的预测文件和真实标签文件的扩展名 (.png, .tif, .bmp ?)
# [!] 并且确保两个文件夹中的对应文件名是一致的
file_extension = ".png"


# --- 结束配置 ---


# --- 2. 定义函数来计算单个图像的指标 ---
def calculate_metrics_detailed(gt_path, pred_path, num_classes=2):
    """
    加载真值和预测图像，计算详细的分割指标。
    假设图像是黑白的，前景像素值 > 0, 背景 = 0。
    返回: 各类别的 IoU, 各类别的 Pixel Accuracy, Recall, Precision, Accuracy, F1(Dice)
    """
    try:
        gt_img = Image.open(gt_path).convert('L')
        pred_img = Image.open(pred_path).convert('L')

        gt_arr = np.array(gt_img)
        pred_arr = np.array(pred_img)

        if gt_arr.shape != pred_arr.shape:
            print(f"警告: 文件 {os.path.basename(gt_path)} 的形状不匹配，跳过。")
            return None

        # 转换为二值 (0=背景, 1=前景)
        gt_binary = (gt_arr > 0).astype(np.uint8)
        pred_binary = (pred_arr > 0).astype(np.uint8)

        gt_flat = gt_binary.flatten()
        pred_flat = pred_binary.flatten()

        # 计算混淆矩阵: cm[i, j] 表示真实为 i 但预测为 j 的像素数
        cm = confusion_matrix(gt_flat, pred_flat, labels=range(num_classes))

        # 从混淆矩阵计算指标
        tp = np.diag(cm)  # True Positives per class
        fp = np.sum(cm, axis=0) - tp  # False Positives per class
        fn = np.sum(cm, axis=1) - tp  # False Negatives per class
        tn = np.sum(cm) - (tp + fp + fn)  # True Negatives per class (虽然这里不太直接用)

        # 1. IoU per class (Intersection over Union)
        iou_per_class = (tp + 1e-6) / (tp + fp + fn + 1e-6)  # 加 epsilon 避免除以0

        # 2. Pixel Accuracy per class (PA)
        # PA_class_i = TP_i / (TP_i + FN_i) = Recall_i
        pa_per_class = (tp + 1e-6) / (np.sum(cm, axis=1) + 1e-6)

        # 3. Overall Accuracy (全局像素准确率)
        accuracy = np.sum(tp) / np.sum(cm)

        # 4. Precision, Recall, F1 for the foreground class (class 1)
        # (通常 Recall, Precision, F1 是针对前景类别计算的)
        tp_fg = tp[1]
        fp_fg = fp[1]
        fn_fg = fn[1]

        precision_fg = (tp_fg + 1e-6) / (tp_fg + fp_fg + 1e-6)
        recall_fg = (tp_fg + 1e-6) / (tp_fg + fn_fg + 1e-6)  # 等同于 pa_per_class[1]
        f1_fg = (2 * tp_fg + 1e-6) / (2 * tp_fg + fp_fg + fn_fg + 1e-6)  # Dice Score

        return iou_per_class, pa_per_class, recall_fg, precision_fg, accuracy, f1_fg

    except FileNotFoundError:
        print(f"错误: 找不到文件对 {gt_path} 或 {pred_path}")
        return None
    except Exception as e:
        print(f"处理文件 {os.path.basename(gt_path)} 时出错: {e}")
        return None


# --- 3. 查找所有预测文件并计算平均指标 ---
print(f"正在查找 {prediction_dir} 中的预测文件 (*{file_extension})...")
prediction_files = sorted(glob(os.path.join(prediction_dir, f"*{file_extension}")))

if not prediction_files:
    print("错误: 在预测文件夹中没有找到任何文件。请检查路径和扩展名。")
    exit()

print(f"找到了 {len(prediction_files)} 个预测文件。开始计算指标...")

# 存储每个文件计算出的指标数组/值
all_iou_arrays = []
all_pa_arrays = []
all_recall_fg = []
all_precision_fg = []
all_accuracy = []
all_f1_fg = []

processed_count = 0

for pred_path in tqdm(prediction_files):
    base_name = os.path.basename(pred_path)
    gt_path = os.path.join(ground_truth_dir, base_name)

    if not os.path.exists(gt_path):
        print(f"警告: 找不到对应的真值文件 {gt_path}，跳过 {base_name}。")
        continue

    metrics = calculate_metrics_detailed(gt_path, pred_path)

    if metrics is not None:
        iou_arr, pa_arr, rec_fg, prec_fg, acc, f1_fg = metrics
        all_iou_arrays.append(iou_arr)
        all_pa_arrays.append(pa_arr)
        all_recall_fg.append(rec_fg)
        all_precision_fg.append(prec_fg)
        all_accuracy.append(acc)
        all_f1_fg.append(f1_fg)
        processed_count += 1

# --- 4. 计算并打印平均指标 ---
if processed_count > 0:
    # --- 计算平均值 ---
    # 平均 IoU per class
    mean_iou_per_class = np.mean(all_iou_arrays, axis=0)
    # 平均 PA per class
    mean_pa_per_class = np.mean(all_pa_arrays, axis=0)

    # 从平均数组中提取所需指标
    iou_vessel = mean_iou_per_class[1]  # IoU for class 1 (vessel)
    mIoU = np.mean(mean_iou_per_class)  # Mean IoU across background (0) and vessel (1)

    recall = np.mean(all_recall_fg)  # Recall is typically for foreground
    precision = np.mean(all_precision_fg)  # Precision is typically for foreground

    accuracy = np.mean(all_accuracy)  # Overall pixel accuracy

    mPA = np.mean(mean_pa_per_class)  # Mean Pixel Accuracy across background (0) and vessel (1)

    f1_score = np.mean(all_f1_fg)  # F1/Dice is typically for foreground

    # --- 打印结果 ---
    print("\n---------------------- 评估结果 (平均值) ----------------------")
    print(f"成功处理了 {processed_count} / {len(prediction_files)} 个图像对。")
    print(f"指标          | 计算值")
    print(f"--------------|---------")
    print(f"IoU (血管)    | {iou_vessel:.4f}")
    print(f"mIoU          | {mIoU:.4f}")
    print(f"Recall        | {recall:.4f}")
    print(f"Precision     | {precision:.4f}")
    print(f"Accuracy      | {accuracy:.4f}")
    print(f"mPA           | {mPA:.4f}")
    print(f"F1-score      | {f1_score:.4f}")
    print("----------------------------------------------------------------")
    # print(f"(背景 IoU: {mean_iou_per_class[0]:.4f}, 背景 PA: {mean_pa_per_class[0]:.4f})") # 调试信息

else:
    print("\n错误: 未能成功处理任何图像对。请检查文件路径、格式和错误信息。")