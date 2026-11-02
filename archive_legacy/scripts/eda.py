"""
Exploratory Data Analysis (EDA) module for MNIST handwritten digits.
Generates:
1. Class distribution charts (Train vs Test).
2. Mean digit and variance heatmap per class (0-9).
3. Pixel intensity distribution (bimodal histogram).
4. Deskewing visual comparison (Original vs Deskewed).
5. PCA explained variance ratio curve and 2D/3D projection.
6. t-SNE 2D cluster visualization.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Reconfigure stdout for Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.config import FIGURES_DIR, TABLES_DIR, CLASS_NAMES, RANDOM_STATE
from src.data_loader import load_mnist_data
from src.features import deskew_image, extract_hog_features

# Configure matplotlib aesthetic styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 11


def plot_class_distribution(y_train: np.ndarray, y_test: np.ndarray, save_dir: Path = FIGURES_DIR):
    """Plot bar chart comparing train vs test class distribution."""
    train_counts = np.bincount(y_train, minlength=10)
    test_counts = np.bincount(y_test, minlength=10)

    x = np.arange(10)
    width = 0.38

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    rects1 = ax.bar(x - width / 2, train_counts, width, label="Tập huấn luyện (Train: 60,000)", color="#2b5c8f")
    rects2 = ax.bar(x + width / 2, test_counts, width, label="Tập kiểm thử (Test: 10,000)", color="#e07a5f")

    ax.set_ylabel("Số lượng mẫu (Samples)")
    ax.set_xlabel("Chữ số (Lớp 0 - 9)")
    ax.set_title("Phân bố số lượng mẫu giữa các lớp trong bộ dữ liệu MNIST", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(CLASS_NAMES)
    ax.legend(frameon=True)
    ax.set_ylim(0, 7500)

    # Add count labels on top of bars
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"{h}", xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h}", xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    out_path = save_dir / "01_class_distribution.png"
    plt.savefig(out_path)
    plt.close()
    print(f"[OK] Đã lưu biểu đồ phân bố lớp: {out_path}")


def plot_mean_and_variance_digits(x_train: np.ndarray, y_train: np.ndarray, save_dir: Path = FIGURES_DIR):
    """Plot mean digit image and variance heatmap for each digit class (0-9)."""
    fig, axes = plt.subplots(2, 10, figsize=(16, 4), dpi=300)

    for digit in range(10):
        digit_images = x_train[y_train == digit]
        mean_img = np.mean(digit_images, axis=0)
        var_img = np.var(digit_images, axis=0)

        # Row 0: Mean
        ax_mean = axes[0, digit]
        im_m = ax_mean.imshow(mean_img, cmap="viridis")
        ax_mean.set_title(f"Mean '{digit}'", fontsize=10, fontweight="bold")
        ax_mean.axis("off")

        # Row 1: Variance
        ax_var = axes[1, digit]
        im_v = ax_var.imshow(var_img, cmap="magma")
        ax_var.set_title(f"Var '{digit}'", fontsize=10, fontweight="bold")
        ax_var.axis("off")

    fig.suptitle("Ảnh trung bình (Mean) và Phương sai (Variance) của từng chữ số trong tập huấn luyện",
                 fontsize=13, fontweight="bold", y=1.03)
    plt.tight_layout()
    out_path = save_dir / "02_mean_variance_digits.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Đã lưu ảnh trung bình và phương sai: {out_path}")


def plot_pixel_intensity_distribution(x_train: np.ndarray, save_dir: Path = FIGURES_DIR):
    """Plot pixel intensity histogram demonstrating background vs stroke distributions."""
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    sample_pixels = x_train[:2000].ravel()

    ax.hist(sample_pixels, bins=50, color="#1d3557", edgecolor="black", alpha=0.8, log=True)
    ax.set_title("Phân bố cường độ điểm ảnh (Pixel Intensity Histogram) - Log Scale", fontsize=12, fontweight="bold")
    ax.set_xlabel("Giá trị điểm ảnh chuẩn hóa [0.0 (nền đen) - 1.0 (nét mực trắng)]")
    ax.set_ylabel("Tần suất xuất hiện (Log Scale)")
    ax.axvline(x=0.1, color="red", linestyle="--", label="Ngưỡng tách nền gợi ý (~0.1)")
    ax.legend()

    plt.tight_layout()
    out_path = save_dir / "03_pixel_distribution.png"
    plt.savefig(out_path)
    plt.close()
    print(f"[OK] Đã lưu biểu đồ phân bố cường độ pixel: {out_path}")


def plot_deskew_comparison(x_train: np.ndarray, y_train: np.ndarray, save_dir: Path = FIGURES_DIR):
    """Plot side-by-side comparison of original slanted digits and deskewed versions."""
    # Pick digits that typically have high tilt (like 1, 3, 4, 7, 9)
    fig, axes = plt.subplots(4, 10, figsize=(15, 6), dpi=300)

    sample_indices = []
    for d in range(10):
        idxs = np.where(y_train == d)[0]
        sample_indices.append(idxs[0])
        sample_indices.append(idxs[1])

    for col in range(10):
        idx1 = sample_indices[col * 2]
        idx2 = sample_indices[col * 2 + 1]

        # First sample
        orig1 = x_train[idx1]
        desk1 = deskew_image(orig1)
        axes[0, col].imshow(orig1, cmap="gray")
        axes[0, col].set_title(f"Gốc: {y_train[idx1]}", fontsize=9)
        axes[0, col].axis("off")

        axes[1, col].imshow(desk1, cmap="gray")
        axes[1, col].set_title(f"Nắn: {y_train[idx1]}", fontsize=9, color="blue")
        axes[1, col].axis("off")

        # Second sample
        orig2 = x_train[idx2]
        desk2 = deskew_image(orig2)
        axes[2, col].imshow(orig2, cmap="gray")
        axes[2, col].set_title(f"Gốc: {y_train[idx2]}", fontsize=9)
        axes[2, col].axis("off")

        axes[3, col].imshow(desk2, cmap="gray")
        axes[3, col].set_title(f"Nắn: {y_train[idx2]}", fontsize=9, color="blue")
        axes[3, col].axis("off")

    fig.suptitle("So sánh ảnh chữ số gốc và ảnh sau khi nắn thẳng góc nghiêng (Deskewing)",
                 fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    out_path = save_dir / "04_deskew_comparison.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Đã lưu ảnh so sánh Deskewing: {out_path}")


def plot_pca_variance_and_projections(x_train: np.ndarray, y_train: np.ndarray, save_dir: Path = FIGURES_DIR):
    """
    Plot PCA cumulative explained variance curve and 2D scatter projection.
    """
    X_flat = x_train.reshape(x_train.shape[0], -1)

    # 1. Cumulative Explained Variance
    pca_full = PCA(n_components=200, random_state=RANDOM_STATE)
    pca_full.fit(X_flat[:10000])  # Fit on subset for speed
    cum_var = np.cumsum(pca_full.explained_variance_ratio_)

    # Find components for 80%, 90%, 95% variance
    n_80 = np.searchsorted(cum_var, 0.80) + 1
    n_90 = np.searchsorted(cum_var, 0.90) + 1
    n_95 = np.searchsorted(cum_var, 0.95) + 1

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(range(1, 201), cum_var * 100, color="#0077b6", lw=2, label="Phương sai tích lũy (%)")
    ax.axhline(y=95, color="red", linestyle="--", label=f"95% Phương sai ({n_95} chiều)")
    ax.axvline(x=n_95, color="red", linestyle=":")
    ax.axhline(y=90, color="orange", linestyle="--", label=f"90% Phương sai ({n_90} chiều)")
    ax.axvline(x=n_90, color="orange", linestyle=":")
    ax.axhline(y=80, color="green", linestyle="--", label=f"80% Phương sai ({n_80} chiều)")
    ax.axvline(x=n_80, color="green", linestyle=":")

    ax.set_xlabel("Số lượng thành phần chính (Principal Components)")
    ax.set_ylabel("Tỷ lệ phương sai giải thích tích lũy (%)")
    ax.set_title("Đường cong phân tích phương sai tích lũy của PCA trên dữ liệu MNIST", fontsize=12, fontweight="bold")
    ax.legend(loc="lower right")
    ax.set_xlim(1, 200)
    ax.set_ylim(40, 101)

    plt.tight_layout()
    out_curve = save_dir / "05_pca_variance_curve.png"
    plt.savefig(out_curve)
    plt.close()
    print(f"[OK] Đã lưu đường cong PCA: {out_curve}")

    # 2. 2D Scatter Projection of Classes
    pca_2d = PCA(n_components=2, random_state=RANDOM_STATE)
    sub_X, sub_y = X_flat[:3000], y_train[:3000]
    X_pca_2d = pca_2d.fit_transform(sub_X)

    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    scatter = ax.scatter(
        X_pca_2d[:, 0],
        X_pca_2d[:, 1],
        c=sub_y,
        cmap="tab10",
        alpha=0.6,
        s=15,
        edgecolors="none",
    )
    cbar = plt.colorbar(scatter, ticks=range(10))
    cbar.set_label("Chữ số (Lớp 0 - 9)")
    ax.set_title("Chiếu không gian dữ liệu MNIST xuống 2D bằng PCA (PC1 vs PC2)", fontsize=12, fontweight="bold")
    ax.set_xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% variance)")

    plt.tight_layout()
    out_proj = save_dir / "06_pca_2d_projection.png"
    plt.savefig(out_proj)
    plt.close()
    print(f"[OK] Đã lưu PCA 2D projection: {out_proj}")


def plot_tsne_visualization(x_train: np.ndarray, y_train: np.ndarray, save_dir: Path = FIGURES_DIR):
    """
    Plot t-SNE 2D cluster visualization on sample digits.
    t-SNE reveals non-linear manifolds and natural cluster separations.
    """
    X_flat = x_train.reshape(x_train.shape[0], -1)
    # Take 2000 samples for high-quality, fast t-SNE
    sub_X, sub_y = X_flat[:2500], y_train[:2500]

    # Pre-reduce with PCA to 50 dims first (standard best practice for t-SNE)
    pca = PCA(n_components=50, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(sub_X)

    tsne = TSNE(n_components=2, perplexity=35, max_iter=1000, random_state=RANDOM_STATE)
    X_tsne = tsne.fit_transform(X_pca)

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    scatter = ax.scatter(
        X_tsne[:, 0],
        X_tsne[:, 1],
        c=sub_y,
        cmap="tab10",
        alpha=0.7,
        s=20,
        edgecolors="none",
    )
    cbar = plt.colorbar(scatter, ticks=range(10))
    cbar.set_label("Chữ số (Lớp 0 - 9)")
    ax.set_title("Trực quan hóa cụm không gian tiềm ẩn bằng t-SNE 2D (MNIST)", fontsize=13, fontweight="bold")
    ax.set_xlabel("t-SNE Dimension 1")
    ax.set_ylabel("t-SNE Dimension 2")

    # Annotate class centroids
    for digit in range(10):
        cls_points = X_tsne[sub_y == digit]
        centroid = np.median(cls_points, axis=0)
        ax.annotate(
            str(digit),
            xy=centroid,
            xytext=(0, 0),
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="black", lw=1.5, alpha=0.9),
        )

    plt.tight_layout()
    out_tsne = save_dir / "07_tsne_clustering.png"
    plt.savefig(out_tsne)
    plt.close()
    print(f"[OK] Đã lưu t-SNE 2D visualization: {out_tsne}")


def generate_eda_report():
    """Run full EDA pipeline and output all charts and tables."""
    print("=" * 60)
    print("BẮT ĐẦU QUY TRÌNH PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA)")
    print("=" * 60)

    (x_train, y_train), (x_test, y_test) = load_mnist_data(normalize=True, flatten=False)

    plot_class_distribution(y_train, y_test)
    plot_mean_and_variance_digits(x_train, y_train)
    plot_pixel_intensity_distribution(x_train)
    plot_deskew_comparison(x_train, y_train)
    plot_pca_variance_and_projections(x_train, y_train)
    plot_tsne_visualization(x_train, y_train)

    print("=" * 60)
    print("HOÀN TẤT EDA! TẤT CẢ BIỂU ĐỒ ĐÃ ĐƯỢC LƯU VÀO reports/figures/")
    print("=" * 60)


if __name__ == "__main__":
    generate_eda_report()
