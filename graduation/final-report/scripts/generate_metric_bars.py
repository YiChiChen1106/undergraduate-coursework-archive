import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


MODELS = [
    "nnU-Net\nbaseline",
    "Deformable LPT\n(No AFFM, 4 point)",
    "Modulated\nDeformable\n(4 point)",
    "MS-Modulated\n(4 point)",
    "MS-Modulated\n+ CA",
    "MS-DSConv\n+ CA",
]

COLORS = [
    "#9aa0a6",
    "#bfd7ea",
    "#9cc4df",
    "#7faecd",
    "#5d95bb",
    "#2f6da5",
]

METRICS = {
    "se": {
        "title": "Comparison of Sensitivity (SE)",
        "ylabel": "Sensitivity (SE)",
        "values": [0.7627, 0.7634, 0.7660, 0.7582, 0.7697, 0.8083],
        "filename": "comparion_of_se.png",
    },
    "f1": {
        "title": "Comparison of F1-score",
        "ylabel": "F1-score",
        "values": [0.7891, 0.7958, 0.7950, 0.7954, 0.7973, 0.8020],
        "filename": "Comparison of F1-score.png",
    },
    "auc": {
        "title": "Comparison of AUC",
        "ylabel": "AUC",
        "values": [0.8739, 0.8749, 0.8759, 0.8726, 0.8777, 0.8949],
        "filename": "comparison_of_auc.png",
    },
}


def nice_limits(values: list[float]) -> tuple[float, float]:
    vmin = min(values)
    vmax = max(values)
    span = vmax - vmin
    pad = max(span * 0.35, 0.0025)
    return round(vmin - pad, 4), round(vmax + pad, 4)


def plot_bar(metric_key: str, outdir: Path) -> Path:
    spec = METRICS[metric_key]
    values = spec["values"]
    x = np.arange(len(MODELS))

    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    bars = ax.bar(x, values, color=COLORS, width=0.72, edgecolor="#5a6772", linewidth=0.6)

    ymin, ymax = nice_limits(values)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(x, MODELS)
    ax.set_ylabel(spec["ylabel"], fontsize=14)
    ax.set_xlabel("Model", fontsize=14)
    ax.set_title(spec["title"], fontsize=18, pad=14)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.45)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=12)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + (ymax - ymin) * 0.01,
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
        )

    fig.tight_layout()
    outfile = outdir / spec["filename"]
    fig.savefig(outfile, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return outfile


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate thesis metric bar charts.")
    parser.add_argument(
        "--outdir",
        default=str(Path(__file__).resolve().parents[1] / "pic"),
        help="Output directory for generated PNG files.",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for key in ("se", "f1", "auc"):
        outfile = plot_bar(key, outdir)
        print(f"Saved: {outfile}")


if __name__ == "__main__":
    main()
