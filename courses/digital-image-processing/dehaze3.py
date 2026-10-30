import cv2
import numpy as np
import os
import glob
import time
import matplotlib.pyplot as plt

# --- 0. 计时器与性能报告工具 ---

class CodeTimer:
    """A simple context manager for timing code blocks."""
    def __init__(self, name, timings_dict):
        self.name = name
        self.timings = timings_dict
    
    def __enter__(self):
        self.start = time.perf_counter()
    
    def __exit__(self, type, value, traceback):
        elapsed = time.perf_counter() - self.start
        if self.name not in self.timings:
            self.timings[self.name] = []
        self.timings[self.name].append(elapsed)

def print_performance_report(timings, item_count):
    """Prints a formatted performance report for the different pipelines."""
    print("\n--- Full Pipeline Performance Comparison Report ---")
    if not timings or item_count == 0:
        print("No timing data collected or no items processed.")
        return

    print(f"Compared {len(timings)} full pipelines on {item_count} images.")
    print("\nAverage Execution Time per Image (Core Algorithm + Post-Processing):")

    avg_timings = {k: sum(v) / len(v) for k, v in timings.items()}
    
    for name, avg_time in sorted(avg_timings.items(), key=lambda item: item[1]):
        print(f"  - {name:<30}: {avg_time:.4f}s")
    print("---------------------------------------------------\n")

# --- 1. 用户配置区 ---
IMAGE_DIR = r"C:\Users\28100\Desktop\DIP\db\IEI2019"
VIDEO_DIR = r"C:\Users\28100\Desktop\DIP\db\IEV2022"
OUTPUT_DIR = r"C:\Users\28100\Desktop\DIP\db\final_project_output"

# --- 2. 核心算法区 ---

# === 方法1: 暗通道先验 (DCP) - 包含一个为视频优化的快速版本 ===
def get_dark_channel(image, patch_size=15):
    min_channel = np.min(image, axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (patch_size, patch_size))
    return cv2.erode(min_channel, kernel)

def get_atmospheric_light(image, dark_channel):
    flat_image = image.reshape(-1, 3)
    flat_dark = dark_channel.flatten()
    search_indices = (-flat_dark).argsort()[:int(flat_dark.shape[0] * 0.001)]
    return np.mean(flat_image[search_indices], axis=0)

def core_dehaze_dcp(image, radius=60, eps=0.001, omega=0.95, t0=0.1):
    """Standard DCP for high-quality image processing."""
    img_float = image.astype(np.float32) / 255.0
    gray_image = cv2.cvtColor(img_float, cv2.COLOR_BGR2GRAY)
    dark_channel = get_dark_channel(img_float, 15)
    atmospheric_light = get_atmospheric_light(img_float, dark_channel)
    initial_transmission = 1 - omega * get_dark_channel(img_float / atmospheric_light, 15)
    try:
        refined_transmission = cv2.ximgproc.guidedFilter(gray_image, initial_transmission, radius, eps)
    except AttributeError:
        print("Warning: cv2.ximgproc not found. Using GaussianBlur as a fallback for DCP.")
        refined_transmission = cv2.GaussianBlur(initial_transmission, (radius*2+1, radius*2+1), radius)
    refined_transmission = np.maximum(refined_transmission, t0)
    recovered_image = np.zeros_like(img_float)
    for i in range(3):
        recovered_image[:, :, i] = (img_float[:, :, i] - atmospheric_light[i]) / refined_transmission + atmospheric_light[i]
    return (np.clip(recovered_image, 0, 1) * 255).astype(np.uint8)

def core_dehaze_dcp_fast(image, processing_width=480, radius=40):
    """Optimized DCP with downsampling for fast video processing."""
    h, w, _ = image.shape
    scale_factor = processing_width / w
    small_h, small_w = int(h * scale_factor), processing_width
    small_image = cv2.resize(image, (small_w, small_h), interpolation=cv2.INTER_AREA)
    # 在小图像上计算核心去雾
    small_result_img = core_dehaze_dcp(small_image, radius=radius)
    # 将结果放大回原始尺寸
    return cv2.resize(small_result_img, (w, h), interpolation=cv2.INTER_CUBIC)

# === 方法2: Retinex (MSRCR) ===
def single_scale_retinex(image, sigma):
    retinex = np.log10(image + 1e-5) - np.log10(cv2.GaussianBlur(image, (0, 0), sigma) + 1e-5)
    return retinex

def core_enhance_msrcr(image, sigmas=[15, 80, 250]):
    img_float = image.astype(np.float32) + 1.0
    msr = np.zeros_like(img_float)
    for sigma in sigmas:
        msr += single_scale_retinex(img_float, sigma)
    msr /= len(sigmas)
    color_sum = np.sum(img_float, axis=2, keepdims=True)
    alpha, beta, g = 125, 46, 5
    color_restoration = beta * (np.log10(alpha * img_float) - np.log10(color_sum))
    img_msrcr = g * (msr * color_restoration)
    min_val, max_val = np.min(img_msrcr), np.max(img_msrcr)
    return ((img_msrcr - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)

# === 方法3: 同态滤波 (Homomorphic Filtering) ===
def core_enhance_homomorphic(image, cutoff=30, g_low=0.5, g_high=2.0):
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y = img_yuv[:, :, 0]
    y_log = np.log1p(y.astype(np.float32))
    y_fft = np.fft.fftshift(np.fft.fft2(y_log))
    rows, cols = y.shape
    u, v = np.meshgrid(np.arange(cols), np.arange(rows))
    dist = np.sqrt((u - cols//2)**2 + (v - rows//2)**2)
    filter_kernel = (g_high - g_low) * (1 - np.exp(-(dist**2) / (cutoff**2))) + g_low
    y_fft_filtered = filter_kernel * y_fft
    y_ifft = np.fft.ifft2(np.fft.ifftshift(y_fft_filtered))
    y_exp = np.expm1(np.real(y_ifft))
    img_yuv[:, :, 0] = np.clip(y_exp, 0, 255).astype(np.uint8)
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

# --- 3. 共享的后处理流水线 ---
def apply_post_processing(image):
    balanced = simplest_color_balance(image)
    denoised = cv2.bilateralFilter(balanced, d=9, sigmaColor=75, sigmaSpace=75)
    contrasted = apply_clahe(denoised)
    return unsharp_mask(contrasted, strength=0.8)

# Helper functions for post-processing
def simplest_color_balance(image, percent=0.5):
    out_channels = []
    for channel in cv2.split(image):
        hist = cv2.calcHist([channel], [0], None, [256], (0, 256))
        ignore_count = int(image.shape[0] * image.shape[1] * (percent / 100.0))
        low_val, high_val = 0, 255
        count = 0;
        for i in range(256):
            if count >= ignore_count: low_val = i; break
            count += hist[i]
        count = 0;
        for i in range(255, -1, -1):
            if count >= ignore_count: high_val = i; break
            count += hist[i]
        if high_val > low_val:
            channel = np.clip(channel, low_val, high_val)
            channel = ((channel.astype(np.float32) - low_val) / (high_val - low_val) * 255).astype(np.uint8)
        out_channels.append(channel)
    return cv2.merge(out_channels)

def apply_clahe(image, clip_limit=2.0):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    return cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)

def unsharp_mask(image, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    return cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)

# --- 4. 任务执行函数 ---

def task_1_histogram_analysis():
    print("--- Starting Task 1: Histogram Analysis ---")
    image_files_to_analyze = ["H22.png", "H26.jpg", "R1.jpg"] #
    hist_dir = os.path.join(OUTPUT_DIR, 'histograms')
    os.makedirs(hist_dir, exist_ok=True)
    colors = ('blue', 'green', 'red')
    for filename in image_files_to_analyze:
        path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(path): continue
        print(f"  - Computing histogram for {filename}...")
        image = cv2.imread(path)
        plt.figure(figsize=(10, 6))
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=color, label=f'{color.capitalize()} Channel')
        plt.title(f'Color Histogram for {filename}')
        plt.xlabel('Pixel Intensity'); plt.ylabel('Number of Pixels')
        plt.legend(); plt.grid(True); plt.xlim([0, 256])
        plt.savefig(os.path.join(hist_dir, f"histogram_{filename}.png"))
        plt.close()
    print("--- Task 1 Finished ---\n")

def task_2_compare_image_pipelines():
    print("--- Starting Task 2: Compare 3 Full Enhancement Pipelines on Images ---")
    output_dirs = {
        "DCP": os.path.join(OUTPUT_DIR, 'dcp_enhanced_output'),
        "Retinex": os.path.join(OUTPUT_DIR, 'retinex_enhanced_output'),
        "Homomorphic": os.path.join(OUTPUT_DIR, 'homomorphic_enhanced_output')
    }
    for d in output_dirs.values(): os.makedirs(d, exist_ok=True)

    image_paths = [p for p in glob.glob(os.path.join(IMAGE_DIR, '*')) if os.path.basename(p).upper().startswith('H')] #
    all_timings = {}
    
    for i, path in enumerate(image_paths):
        filename = os.path.basename(path)
        print(f"Processing image {i+1}/{len(image_paths)}: {filename}...")
        image = cv2.imread(path)
        if image is None: continue

        pipelines = {
            "Pipeline: Dark Channel Prior": (core_dehaze_dcp, output_dirs["DCP"]),
            "Pipeline: Retinex (MSRCR)": (core_enhance_msrcr, output_dirs["Retinex"]),
            "Pipeline: Homomorphic Filter": (core_enhance_homomorphic, output_dirs["Homomorphic"])
        }

        for name, (core_func, out_dir) in pipelines.items():
            with CodeTimer(name, all_timings):
                final_result = apply_post_processing(core_func(image))
            cv2.imwrite(os.path.join(out_dir, f"final_{filename}"), final_result)
            
    print(f"--- Task 2 complete. Image results saved to subfolders in: {OUTPUT_DIR} ---")
    print_performance_report(all_timings, len(image_paths))


# <<< MODIFIED TASK FOR VIDEO >>>
def task_3_enhance_video_with_all_methods():
    """Enhances one video using all three methods, creating three separate output files."""
    print("\n--- Starting Task 3: Enhance One Video Clip with All 3 Methods ---")
    print("!!! WARNING: This is a very time-consuming process. Please be patient. !!!")
    
    video_paths = glob.glob(os.path.join(VIDEO_DIR, '*.mp4')) + glob.glob(os.path.join(VIDEO_DIR, '*.avi'))
    if not video_paths:
        print("  - No video files found. Skipping video task.")
        return
        
    video_path = video_paths[0]
    filename = os.path.basename(video_path)
    video_out_dir = os.path.join(OUTPUT_DIR, 'video_output_comparison')
    os.makedirs(video_out_dir, exist_ok=True)

    print(f"  - Processing video: {filename}...")
    
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Create three separate video writers
    out_dcp = cv2.VideoWriter(os.path.join(video_out_dir, f"dcp_{filename}"), fourcc, fps, (width, height))
    out_retinex = cv2.VideoWriter(os.path.join(video_out_dir, f"retinex_{filename}"), fourcc, fps, (width, height))
    out_homomorphic = cv2.VideoWriter(os.path.join(video_out_dir, f"homomorphic_{filename}"), fourcc, fps, (width, height))
    
    current_frame = 0
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # Process with all three pipelines
        # 1. DCP (Fast version for video)
        dcp_result = apply_post_processing(core_dehaze_dcp_fast(frame))
        out_dcp.write(dcp_result)
        
        # 2. Retinex
        retinex_result = apply_post_processing(core_enhance_msrcr(frame))
        out_retinex.write(retinex_result)
        
        # 3. Homomorphic
        homomorphic_result = apply_post_processing(core_enhance_homomorphic(frame))
        out_homomorphic.write(homomorphic_result)
        
        current_frame += 1
        elapsed = time.time() - start_time
        fps_current = current_frame / elapsed if elapsed > 0 else 0
        print(f"    - Processing frame: {current_frame}/{frame_count} ({fps_current:.2f} frames/sec)", end='\r')

    end_time = time.time()
    cap.release()
    out_dcp.release()
    out_retinex.release()
    out_homomorphic.release()
    cv2.destroyAllWindows()
    
    print(f"\n  - Video processing finished in {end_time - start_time:.2f} seconds.")
    print(f"--- Task 3 complete. Enhanced videos saved to: {video_out_dir} ---")


# --- 5. 主程序入口 ---
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Execute all project tasks in order
    task_1_histogram_analysis()
    task_2_compare_image_pipelines()
    task_3_enhance_video_with_all_methods()
    
    print("\nAll project tasks finished!")