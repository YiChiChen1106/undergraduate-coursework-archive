import cv2
import numpy as np
import os
import glob


def apply_gamma_correction(img, gamma=1.2):
    """
    步骤 4: Gamma 变换
    构建一个查找表(LUT)将像素值映射到新的伽马校正值
    """
    # 归一化到 [0, 1] ->计算幂 -> 还原到 [0, 255]
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # 使用查找表应用变换
    return cv2.LUT(img, table)


def preprocess_image(image_path, output_path):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return

    # --- 步骤 1: 灰度化 (Graying)  ---
    # 论文中提到将彩色眼底图像转换为灰度图
    # 注意：在视网膜分割任务中，有时提取"绿色通道"比直接转灰度效果更好，
    # 但为了严格复现论文的"Graying"，这里使用标准的 BGR2GRAY。
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 步骤 2: 标准化 (Standardization)  ---
    # 论文中紧接着灰度化后进行了标准化。
    # 为了让后续的 CLAHE (通常处理 0-255 uint8 数据) 效果最佳，
    # 这里采用 Min-Max 标准化将像素拉伸覆盖整个 0-255 范围。
    # 如果你的图片本身对比度极低，这一步能确保数据分布在合理区间。
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # --- 步骤 3: 自适应直方图均衡化 (Adaptive Histogram Equalization)  ---
    # 使用 OpenCV 的 CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # clipLimit 和 tileGridSize 是常用参数，论文未详述具体数值，这里使用通用的经验值。
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(normalized)

    # --- 步骤 4: 伽马变换 (Gamma Transform)  ---
    # 调整图像亮度/对比度。Gamma > 1 会让暗部更暗（增强血管对比），Gamma < 1 会提亮。
    # 论文 Fig 6(e) 显示血管更清晰，通常使用 Gamma 1.2 左右较为合适。
    final_img = apply_gamma_correction(clahe_img, gamma=1.2)

    # 保存结果
    cv2.imwrite(output_path, final_img)
    print(f"已处理: {output_path}")


def batch_process(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 支持常见的图片格式
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tif']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))

    print(f"找到 {len(image_files)} 张图片，开始处理...")

    for img_path in image_files:
        filename = os.path.basename(img_path)
        save_path = os.path.join(output_folder, filename)
        preprocess_image(img_path, save_path)


# --- 使用示例 ---
if __name__ == "__main__":
    # 请修改这里的路径为你自己的数据集路径
    input_dir = r"F:\shiwangmo\shiwangmodata\drive"  # 输入文件夹
    output_dir = r"F:\shiwangmo\shiwangmodata\drive_PAnet_preprocessed"  # 输出文件夹

    # 运行批量处理
    # 如果你想测试单张图片，可以直接调用 preprocess_image('path/to/img.jpg', 'result.jpg')
    batch_process(input_dir, output_dir)

    # 模拟运行提示
    print("请配置 input_dir 和 output_dir 后运行脚本。")