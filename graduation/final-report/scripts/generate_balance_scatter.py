import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


POINTS = [
    ("nnU-Net baseline", 0.8238, 0.7627, "#8f969d", 90),
    ("MS-Modulated (4 point)", 0.8419, 0.7582, "#9e6a7d", 90),
    ("MS-Modulated + CA", 0.8324, 0.7697, "#4d908e", 95),
    ("MS-DSConv + CA", 0.7997, 0.8083, "#6f9e9c", 95),
    ("MS-DSConv + CA (X=20)", 0.8035, 0.8059, "#274d95", 135),
]

# Manual label offsets to avoid overlap while keeping marker positions exact.
OFFSETS = {
    "nnU-Net baseline": (-55, -6),
    "MS-Modulated (4 point)": (14, -8),
    "MS-Modulated + CA": (14, 10),
    "MS-DSConv + CA": (-52, 8),
    "MS-DSConv + CA (X=20)": (12, 12),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate thesis performance-balance scatter chart.")
    parser.add_argument(
        "--outdir",
        default=str(Path(__file__).resolve().parents[1] / "pic"),
        help="Output directory for generated PNG file.",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "performace_balance_comparison.png"

    fig, ax = plt.subplots(figsize=(9.8, 6.5))

    x_values = [p[1] for p in POINTS]
    y_values = [p[2] for p in POINTS]
    ax.set_xlim(min(x_values) - 0.015, max(x_values) + 0.015)
    ax.set_ylim(min(y_values) - 0.01, max(y_values) + 0.015)

    ax.set_xlabel("Precision (PR)", fontsize=14)
    ax.set_ylabel("Sensitivity (SE)", fontsize=14)
    ax.set_title("Performance Balance Comparison", fontsize=18, pad=14)
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.45)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=12)

    for label, x, y, color, size in POINTS:
        ax.scatter(x, y, s=size, c=color, edgecolors="white", linewidths=1.2, zorder=3)
        if label == "MS-DSConv + CA (X=20)":
            ax.scatter(x, y, s=size + 90, facecolors="none", edgecolors="#274d95", linewidths=1.4, zorder=2)

        dx, dy = OFFSETS[label]
        ax.annotate(
            f"{label}\n({x:.4f}, {y:.4f})",
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=10,
            ha="left" if dx >= 0 else "right",
            va="bottom" if dy >= 0 else "top",
            arrowprops=dict(arrowstyle="-", color="#999999", lw=0.7, shrinkA=0, shrinkB=5),
        )

    fig.tight_layout()
    fig.savefig(outfile, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outfile}")


if __name__ == "__main__":
    main()
