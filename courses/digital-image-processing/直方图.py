# -*- coding: utf-8 -*-
# Plot original and 3x3-averaged histograms for two images (Windows paths filled in).
# Requirements: pip install pillow matplotlib numpy

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# ---------- Edit here if needed ----------
IMG_A = r"C:\Users\28100\Desktop\DIP\imga.jpg"
IMG_B = r"C:\Users\28100\Desktop\DIP\imgb.jpg"
SAVE_DIR = os.path.dirname(IMG_A) or "."
# ----------------------------------------

def load_grayscale(path: str) -> np.ndarray:
    img = Image.open(path).convert("L")
    return np.asarray(img, dtype=np.uint8)

def avg_blur_3x3(img: np.ndarray) -> np.ndarray:
    """3×3 average blur using numpy only, edge padding."""
    k = 3
    pad = k // 2
    padded = np.pad(img.astype(np.float32), ((pad, pad), (pad, pad)), mode="edge")
    out = np.zeros_like(img, dtype=np.float32)
    for dy in range(-pad, pad + 1):
        for dx in range(-pad, pad + 1):
            out += padded[pad + dy: pad + dy + img.shape[0],
                          pad + dx: pad + dx + img.shape[1]]
    out /= (k * k)
    return np.clip(out, 0, 255).astype(np.uint8)

def compute_hist(img: np.ndarray, bins: int = 256):
    hist, edges = np.histogram(img, bins=bins, range=(0, 256))
    centers = (edges[:-1] + edges[1:]) / 2.0
    return hist, centers

def plot_hist_pair(h1, b1, h2, b2, title, save_path):
    plt.figure(figsize=(10, 5))
    plt.plot(b1, h1, label="Image A")
    plt.plot(b2, h2, "--", label="Image B")
    plt.title(title)
    plt.xlabel("Gray Level (0–255)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=180)
    plt.close()
    print(f"Saved: {save_path}")

def main():
    # Load
    a = load_grayscale(IMG_A)
    b = load_grayscale(IMG_B)

    # Original histograms
    ha, ba = compute_hist(a)
    hb, bb = compute_hist(b)
    out1 = os.path.join(SAVE_DIR, "hist_original.png")
    plot_hist_pair(ha, ba, hb, bb, "Original Histograms", out1)

    # 3x3 average blur -> histograms
    a_blur = avg_blur_3x3(a)
    b_blur = avg_blur_3x3(b)
    ha2, ba2 = compute_hist(a_blur)
    hb2, bb2 = compute_hist(b_blur)
    out2 = os.path.join(SAVE_DIR, "hist_blurred_3x3.png")
    plot_hist_pair(ha2, ba2, hb2, bb2, "Histograms After 3×3 Average Blur", out2)

if __name__ == "__main__":
    main()
