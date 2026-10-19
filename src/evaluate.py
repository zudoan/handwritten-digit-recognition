"""
Evaluation and error analysis module for handwritten digit recognition.
Computes comprehensive metrics, plots normalized confusion matrices,
and extracts and visualizes misclassified samples for deep error analysis.
"""
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
)

from src.config import FIGURES_DIR, CLASS_NAMES


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "Model",
) -> Dict[str, Any]:
    """
    Compute full classification metrics.
    """
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    prec_per_class, rec_per_class, f1_per_class, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, zero_division=0
    )

    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    report_str = classification_report(
        y_true, y_pred, target_names=CLASS_NAMES, digits=4
    )

    return {
        "model_name": model_name,
        "accuracy": float(acc),
        "macro_precision": float(prec),
        "macro_recall": float(rec),
        "macro_f1": float(f1),
        "precision_per_class": prec_per_class.tolist(),
        "recall_per_class": rec_per_class.tolist(),
        "f1_per_class": f1_per_class.tolist(),
        "support": support.tolist(),
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_norm": cm_norm.tolist(),
        "classification_report": report_str,
    }


def plot_confusion_matrix_heatmap(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str,
    save_path: Optional[Path] = None,
    normalize: bool = True,
):
    """
    Plot and save confusion matrix heatmap with high aesthetics.
    """
    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm_display = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        fmt = ".2%"
        title = f"Ma trận nhầm lẫn chuẩn hóa - {model_name}"
    else:
        cm_display = cm
        fmt = "d"
        title = f"Ma trận nhầm lẫn (Số lượng mẫu) - {model_name}"

    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
    sns.heatmap(
        cm_display,
        annot=True,
        fmt=fmt,
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        cbar=True,
        ax=ax,
        linewidths=0.5,
        linecolor="#dddddd",
    )
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Chữ số dự đoán (Predicted Label)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Chữ số thực tế (True Label)", fontsize=11, fontweight="bold")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"[OK] Đã lưu ma trận nhầm lẫn: {save_path}")
    plt.close()


def find_top_misclassified(
    x_test: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    top_k: int = 25,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Identify misclassified samples. If prediction probabilities are provided,
    ranks errors by the model's highest overconfidence (maximum probability assigned to wrong class).
    """
    wrong_indices = np.where(y_true != y_pred)[0]

    if len(wrong_indices) == 0:
        return np.array([]), np.array([]), np.array([]), np.array([])

    if y_prob is not None:
        # Confidence score for the incorrect predicted class
        confidences = np.max(y_prob[wrong_indices], axis=1)
        sort_order = np.argsort(confidences)[::-1]  # Highest confidence first
        top_indices = wrong_indices[sort_order[:top_k]]
    else:
        top_indices = wrong_indices[:top_k]

    return (
        x_test[top_indices],
        y_true[top_indices],
        y_pred[top_indices],
        top_indices,
    )


def plot_misclassified_gallery(
    x_test: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    model_name: str = "Model",
    save_path: Optional[Path] = None,
    num_samples: int = 20,
):
    """
    Plot a grid gallery of misclassified digits with true vs predicted annotations.
    Vital for Section 4: Phân tích các trường hợp nhận dạng sai và nguyên nhân.
    """
    wrong_imgs, wrong_true, wrong_pred, _ = find_top_misclassified(
        x_test, y_true, y_pred, y_prob, top_k=num_samples
    )

    if len(wrong_imgs) == 0:
        print("[INFO] Không có mẫu nào bị nhận dạng sai!")
        return

    n_show = min(len(wrong_imgs), num_samples)
    cols = 5
    rows = int(np.ceil(n_show / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.2, rows * 2.5), dpi=300)
    axes = np.array(axes).reshape(-1)

    for i in range(len(axes)):
        if i < n_show:
            img = wrong_imgs[i]
            if img.ndim == 1:
                img = img.reshape(28, 28)
            axes[i].imshow(img, cmap="gray_r")
            t_label = wrong_true[i]
            p_label = wrong_pred[i]
            title_text = f"Thực: {t_label} -> Đoán: {p_label}"
            axes[i].set_title(title_text, fontsize=10, color="crimson", fontweight="bold")
            axes[i].axis("off")
        else:
            axes[i].axis("off")

    fig.suptitle(
        f"Phân tích lỗi (Error Analysis) - Các mẫu dự đoán sai tiêu biểu của {model_name}",
        fontsize=12,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"[OK] Đã lưu phòng tranh phân tích lỗi: {save_path}")
    plt.close()
