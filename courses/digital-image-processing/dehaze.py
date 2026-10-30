import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import time # <<< NEW: 引入time模块

# --- 0. 新增：计时器与性能报告工具 ---

class CodeTimer:
    """一个简单的上下文管理器，用于代码块计时。"""
    def __init__(self, name, timings_dict):
        self.name = name
        self.timings = timings_dict
    
    def __enter__(self):
        self.start = time.perf_counter()
        return self
        
    def __exit__(self, type, value, traceback):
        self.elapsed = time.perf_counter() - self.start
        if self.name not in self.timings:
            self.timings[self.name] = []
        self.timings[self.name].append(self.elapsed)

def print_performance_report(timings, item_count, item_type="Image"):
    """打印格式化的性能报告"""
    print("\n--- Performance Analysis Report ---")
    if not timings:
        print("No timing data collected.")
        return

    total_time = sum(sum(v) for v in timings.values())
    if total_time == 0:
        print("Total execution time was zero. Cannot generate report.")
        return

    print(f"Processed {item_count} {item_type}(s).")
    print(f"Total Pipeline Time: {total_time:.4f} seconds.")
    print(f"Average Time per {item_type}: {total_time / item_count:.4f} seconds.")
    print("\nBreakdown of Average Time per Item:")

    avg_timings = {k: sum(v) / len(v) for k, v in timings.items()}
    total_avg_time = sum(avg_timings.values())

    for name, avg_time in sorted(avg_timings.items(), key=lambda item: item[1], reverse=True):
        percentage = (avg_time / total_avg_time) * 100
        print(f"  - {name:<25}: {avg_time:.4f}s ({percentage:5.1f}%)")
    print("-------------------------------------\n")


# --- 1. 用户配置区 ---
IMAGE_DIR = r"C:\Users\28100\Desktop\DIP\db\IEI2019"
VIDEO_DIR = r"C:\Users\28100\Desktop\DIP\db\IEV2022"
OUTPUT_DIR = r"C:\Users\28100\Desktop\DIP\db\ultimate_output2"


# --- 2. 核心算法与所有辅助函数 ---
# (此部分函数无需改动，为简洁省略，使用你原来的即可)
def get_dark_channel(image, patch_size=15):
    min_channel = np.min(image, axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (patch_size, patch_size))
    return cv2.erode(min_channel, kernel)
def get_atmospheric_light_improved(image, dark_channel):
    flat_image = image.reshape(-1, 3)
    flat_dark = dark_channel.flatten()
    num_pixels = flat_dark.shape[0]
    search_indices = (-flat_dark).argsort()[:int(num_pixels * 0.001)]
    candidate_pixels = flat_image[search_indices]
    return np.mean(candidate_pixels, axis=0).astype(np.float32)
def simplest_color_balance(image, percent=0.5):
    out_channels = []
    channels = cv2.split(image)
    total_pixels = image.shape[0] * image.shape[1]
    for channel in channels:
        hist = cv2.calcHist([channel], [0], None, [256], (0, 256))
        ignore_count = int(total_pixels * (percent / 100.0))
        low_val, high_val = 0, 255
        count = 0
        for i in range(256):
            count += hist[i]
            if count >= ignore_count:
                low_val = i
                break
        count = 0
        for i in range(255, -1, -1):
            count += hist[i]
            if count >= ignore_count:
                high_val = i
                break
        if high_val > low_val:
            saturated_channel = np.clip(channel, low_val, high_val)
            normalized_channel = ((saturated_channel.astype(np.float32) - low_val) / (high_val - low_val) * 255).astype(np.uint8)
            out_channels.append(normalized_channel)
        else:
            out_channels.append(channel)
    return cv2.merge(out_channels)
def apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl_l_channel = clahe.apply(l_channel)
    updated_lab_image = cv2.merge((cl_l_channel, a_channel, b_channel))
    return cv2.cvtColor(updated_lab_image, cv2.COLOR_LAB2BGR)
def unsharp_mask(image, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    return cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)

# 【终极处理流水线 - 已修改】
def ultimate_dehaze_pipeline(image, timings_dict, # <<< MODIFIED: 增加一个参数用于接收计时字典
                             patch_size=15, omega=0.95, t0=0.1, radius=81, eps=0.001,
                             balance_percent=0.5, 
                             denoise_strength=10,
                             clahe_clip=2.0, 
                             sharpen_strength=0.8):
    """ 整合去雾、色彩均衡、降噪、CLAHE和锐化的终极处理流水线 (带分步计时) """
    
    with CodeTimer("1. Core Dehazing", timings_dict):
        img_float = image.astype(np.float32) / 255.0
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        dark_channel = get_dark_channel(img_float, patch_size)
        atmospheric_light = get_atmospheric_light_improved(img_float, dark_channel)
        initial_transmission = 1 - omega * get_dark_channel(img_float / atmospheric_light, patch_size)
        refined_transmission = cv2.ximgproc.guidedFilter(guide=gray_image, src=initial_transmission, radius=radius, eps=eps)
        refined_transmission = np.maximum(refined_transmission, t0)
        
        recovered_image = np.zeros_like(img_float)
        for i in range(3):
            recovered_image[:, :, i] = (img_float[:, :, i] - atmospheric_light[i]) / refined_transmission + atmospheric_light[i]
        
        dehazed_image = (np.clip(recovered_image, 0, 1) * 255).astype(np.uint8)

    with CodeTimer("2. Color Balance", timings_dict):
        balanced_image = simplest_color_balance(dehazed_image, percent=balance_percent)
    
    with CodeTimer("3. Denoising", timings_dict):
        denoised_image = cv2.fastNlMeansDenoisingColored(balanced_image, None, h=denoise_strength, hColor=denoise_strength, templateWindowSize=7, searchWindowSize=21)

    with CodeTimer("4. Contrast (CLAHE)", timings_dict):
        contrasted_image = apply_clahe(denoised_image, clip_limit=clahe_clip)

    with CodeTimer("5. Sharpening", timings_dict):
        final_image = unsharp_mask(contrasted_image, strength=sharpen_strength)
    
    return final_image


# --- 3. 项目任务执行函数 (调用最终流水线) ---
# (此部分函数无需改动，为简洁省略)
def task_1_compute_histograms():
    print("--- 开始执行任务1：计算直方图 ---")
    image_files = ["H22.png", "H26.jpg", "R1.jpg"]
    colors = ('b', 'g', 'r')
    for filename in image_files:
        path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(path):
            print(f"警告：找不到文件 {path}，跳过。")
            continue
        image = cv2.imread(path)
        plt.figure(figsize=(10, 6))
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=color, label=f'{color.upper()} channel')
        plt.title(f'Histogram for {filename}')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Number of Pixels')
        plt.legend()
        plt.grid(True)
        plt.show()
    print("--- 任务1完成 ---\n")

def task_2_enhance_images(): # <<< MODIFIED: 整体修改以支持计时
    print("--- 开始执行任务2：处理所有图像 ---")
    image_paths = glob.glob(os.path.join(IMAGE_DIR, '*'))
    output_image_dir = os.path.join(OUTPUT_DIR, 'images')
    os.makedirs(output_image_dir, exist_ok=True)
    
    all_timings = {}
    processed_count = 0
    
    for path in image_paths:
        filename = os.path.basename(path)
        print(f"正在处理图像: {filename}...")
        image = cv2.imread(path)
        if image is None: continue
            
        if filename.upper().startswith('H'):
            final_result = ultimate_dehaze_pipeline(image, all_timings, denoise_strength=5)
            processed_count += 1
        else:
            final_result = image # 对于非H开头的图像，我们不计时
            
        output_path = os.path.join(output_image_dir, f"ultimate_{filename}")
        cv2.imwrite(output_path, final_result)
        
    print(f"--- 任务2完成，所有处理后的图像已保存至: {output_image_dir} ---")
    print_performance_report(all_timings, processed_count, "Image")
    
def task_3_enhance_video(): # <<< MODIFIED: 整体修改以支持计时
    print("--- 开始执行任务3：处理视频 ---")
    video_paths = glob.glob(os.path.join(VIDEO_DIR, '*.mp4')) + glob.glob(os.path.join(VIDEO_DIR, '*.avi'))
    if not video_paths:
        print("在指定目录下未找到视频文件。")
        return
        
    video_path = video_paths[0]
    filename = os.path.basename(video_path)
    print(f"正在处理视频: {filename} (这会非常耗时)...")
    
    output_video_dir = os.path.join(OUTPUT_DIR, 'videos')
    os.makedirs(output_video_dir, exist_ok=True)
    output_path = os.path.join(output_video_dir, f"ultimate_{filename}")
    
    cap = cv2.VideoCapture(video_path)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frame_count = cap.get(cv2.CAP_PROP_FPS), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    all_timings = {}
    current_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        current_frame += 1
        print(f"处理帧: {current_frame} / {frame_count}")
        
        final_frame = ultimate_dehaze_pipeline(frame, all_timings, denoise_strength=5)
        out.write(final_frame)
        
    cap.release(), out.release(), cv2.destroyAllWindows()
    print(f"--- 任务3完成，处理后的视频已保存至: {output_path} ---")
    print_performance_report(all_timings, frame_count, "Frame")

# --- 4. 主程序入口 ---
if __name__ == "__main__":
    try:
        cv2.ximgproc
    except AttributeError:
        print("错误：找不到 cv2.ximgproc。请确保安装了 opencv-contrib-python。")
        exit()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    task_1_compute_histograms()
    task_2_enhance_images()
    task_3_enhance_video()
    
    print("所有任务已执行完毕！")