import argparse
import gzip
import json
import struct
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = Path(r"F:\shiwangmo\nnUNetFrame\nnUNet_results\Dataset505_PAnet_DRIVE")
LABELS_ROOT = Path(r"F:\shiwangmo\nnUNetFrame\nnUNet_raw\Dataset505_PAnet_DRIVE\labelsTr")
IMAGES_ROOT = Path(r"F:\shiwangmo\shiwangmodata\drive")

PANELS = [
    ("Original", None, None),
    ("Ground Truth", LABELS_ROOT, "#39a96b"),
    ("nnU-Net baseline", RESULTS_ROOT / "nnUNetTrainer_Baseline100__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4", "#e76f51"),
    ("MS-Modulated + CA", RESULTS_ROOT / "nnUNetTrainerPANet_MSDeformableLPT_CA_NoAFFM__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4", "#c77dff"),
    ("MS-DSConv + CA", RESULTS_ROOT / "nnUNetTrainerPANet_MSDSConvLPT_CA_NoAFFM__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4", "#2a9d8f"),
    ("MS-DSConv + CA\n(post-processed)", RESULTS_ROOT / "nnUNetTrainerPANet_MSDSConvLPT_CA_NoAFFM__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4" / "postprocessed", "#264653"),
]

SUMMARY_FILES = {
    "nnU-Net baseline": RESULTS_ROOT / "nnUNetTrainer_Baseline100__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4" / "summary.json",
    "MS-Modulated + CA": RESULTS_ROOT / "nnUNetTrainerPANet_MSDeformableLPT_CA_NoAFFM__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4" / "summary.json",
    "MS-DSConv + CA": RESULTS_ROOT / "nnUNetTrainerPANet_MSDSConvLPT_CA_NoAFFM__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4" / "summary.json",
    "MS-DSConv + CA\n(post-processed)": RESULTS_ROOT / "nnUNetTrainerPANet_MSDSConvLPT_CA_NoAFFM__nnUNetPlans__2d" / "crossval_results_folds_0_1_2_3_4" / "postprocessed" / "summary.json",
}

DTYPE_MAP = {
    2: np.uint8,
    4: np.int16,
    8: np.int32,
    16: np.float32,
    64: np.float64,
    256: np.int8,
    512: np.uint16,
    768: np.uint32,
}


def load_nifti(path: Path) -> np.ndarray:
    with gzip.open(path, "rb") as handle:
        header = handle.read(348)
        endian = "<" if struct.unpack("<I", header[:4])[0] == 348 else ">"
        dim = struct.unpack(endian + "8h", header[40:56])
        ndim = dim[0]
        shape = tuple(length for length in dim[1:1 + ndim] if length > 0)
        datatype = struct.unpack(endian + "h", header[70:72])[0]
        if datatype not in DTYPE_MAP:
            raise ValueError(f"Unsupported NIfTI datatype {datatype} for {path}")
        vox_offset = int(struct.unpack(endian + "f", header[108:112])[0])
        dtype = np.dtype(DTYPE_MAP[datatype]).newbyteorder(endian)
        handle.seek(vox_offset)
        flat = np.frombuffer(handle.read(), dtype=dtype)
    array = flat[: int(np.prod(shape))].reshape(shape)
    return np.squeeze(array)


def load_case_metrics(summary_path: Path) -> dict[str, float]:
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    metrics = {}
    for item in payload["metric_per_case"]:
        case_id = Path(item["prediction_file"]).name.split(".")[0]
        metrics[case_id] = item["metrics"]["1"]["Dice"]
    return metrics


def build_metrics_index() -> dict[str, dict[str, float]]:
    return {
        panel_name: load_case_metrics(summary_path)
        for panel_name, summary_path in SUMMARY_FILES.items()
        if summary_path.exists()
    }


def load_rgb_image(case_id: str) -> np.ndarray:
    image = Image.open(IMAGES_ROOT / f"{case_id}.jpg").convert("RGB")
    return np.asarray(image, dtype=np.uint8)


def find_crop_box(image: np.ndarray, pad: int = 10) -> tuple[int, int, int, int]:
    gray = image.mean(axis=2)
    foreground = gray > 8
    rows = np.where(foreground.any(axis=1))[0]
    cols = np.where(foreground.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return 0, image.shape[0], 0, image.shape[1]
    r0 = max(int(rows[0]) - pad, 0)
    r1 = min(int(rows[-1]) + pad + 1, image.shape[0])
    c0 = max(int(cols[0]) - pad, 0)
    c1 = min(int(cols[-1]) + pad + 1, image.shape[1])
    return r0, r1, c0, c1


def overlay_mask(image: np.ndarray, mask: np.ndarray, color: str, alpha: float = 0.42) -> np.ndarray:
    mask_bool = mask.astype(bool)
    overlay = image.astype(np.float32).copy()
    rgb = np.array(matplotlib.colors.to_rgb(color), dtype=np.float32) * 255.0
    overlay[mask_bool] = (1.0 - alpha) * overlay[mask_bool] + alpha * rgb

    edge = mask_bool.copy()
    edge[1:-1, 1:-1] = (
        mask_bool[1:-1, 1:-1]
        & (
            (~mask_bool[:-2, 1:-1])
            | (~mask_bool[2:, 1:-1])
            | (~mask_bool[1:-1, :-2])
            | (~mask_bool[1:-1, 2:])
        )
    )
    overlay[edge] = rgb
    return np.clip(overlay, 0, 255).astype(np.uint8)


def render_panel(ax: plt.Axes, image: np.ndarray, title: str, row_label: str, show_row_label: bool, title_fontsize: int) -> None:
    ax.imshow(image)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if show_row_label:
        ax.text(
            -0.08,
            0.5,
            row_label,
            transform=ax.transAxes,
            rotation=90,
            va="center",
            ha="center",
            fontsize=12,
            fontweight="bold",
        )


def compose_title(base_title: str, case_id: str, metrics_index: dict[str, dict[str, float]], show_dice: bool) -> str:
    if not show_dice:
        return base_title
    metric_by_case = metrics_index.get(base_title)
    if metric_by_case is None:
        return base_title
    dice = metric_by_case.get(case_id)
    if dice is None:
        return base_title
    return f"{base_title}\nDice={dice:.4f}"


def create_figure(case_ids: list[str], outpath: Path, show_dice: bool) -> None:
    metrics_index = build_metrics_index()
    n_rows = len(case_ids)
    n_cols = len(PANELS)
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(3.2 * n_cols, 3.2 * n_rows),
        squeeze=False,
    )

    for row_idx, case_id in enumerate(case_ids):
        base_image = load_rgb_image(case_id)
        r0, r1, c0, c1 = find_crop_box(base_image)
        row_label = f"Case {case_id}"

        for col_idx, (panel_title, folder, color) in enumerate(PANELS):
            panel_image = base_image
            if folder is not None:
                mask = load_nifti(folder / f"{case_id}.nii.gz") > 0
                panel_image = overlay_mask(base_image, mask, color)

            cropped = panel_image[r0:r1, c0:c1]
            title = compose_title(panel_title, case_id, metrics_index, show_dice)
            if not show_dice and row_idx > 0:
                title = ""
            title_fontsize = 10 if show_dice else 12
            render_panel(
                axes[row_idx, col_idx],
                cropped,
                title,
                row_label,
                col_idx == 0,
                title_fontsize,
            )

    fig.subplots_adjust(wspace=0.02, hspace=0.08 if not show_dice else 0.22, left=0.05, right=0.995, top=0.95, bottom=0.03)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate overlay comparison figures for DRIVE cases.")
    parser.add_argument(
        "--cases",
        nargs="+",
        required=True,
        help="Case ids to visualize, for example: 24 34",
    )
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "pic" / "overlay_case_comparison.png"),
        help="Output PNG path.",
    )
    parser.add_argument(
        "--show-dice",
        action="store_true",
        help="Append per-case Dice scores to model titles for easier inspection.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    case_ids = [str(int(case_id)) for case_id in args.cases]
    create_figure(case_ids, Path(args.out), show_dice=args.show_dice)
    print(f"Saved: {Path(args.out)}")


if __name__ == "__main__":
    main()
