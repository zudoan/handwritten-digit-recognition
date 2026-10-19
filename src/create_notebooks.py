import sys
import json
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)



def make_code_cell(source: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip().split("\n")]
    }


def make_markdown_cell(source: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    }


def build_eda_notebook():
    cells = [
        make_markdown_cell(
            "# BÀI TẬP LỚN MÔN NHẬN DẠNG MẪU - ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY\n"
            "## NOTEBOOK 1: PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA) & TRÍCH XUẤT ĐẶC TRƯNG\n"
            "**Sinh viên thực hiện**: Nhóm 03\n"
            "**Bộ dữ liệu**: MNIST (Modified National Institute of Standards and Technology)\n"
            "---\n"
            "### Mục tiêu nghiên cứu:\n"
            "1. Phân tích cấu trúc dữ liệu, độ cân bằng giữa 10 lớp chữ số ($0 \\to 9$).\n"
            "2. Trực quan hóa ảnh trung bình (*Mean Digit*) và ảnh phương sai (*Variance Digit*).\n"
            "3. Giảm chiều dữ liệu và khám phá cụm tiềm ẩn bằng **PCA** và **t-SNE**.\n"
            "4. Đánh giá tác động của kỹ thuật nắn thẳng góc nghiêng (*Deskewing*) và trích xuất đặc trưng *HOG*."
        ),
        make_code_cell(
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "\n"
            "# Thêm thư mục gốc vào path\n"
            "sys.path.append(str(Path.cwd().parent))\n"
            "from src.data_loader import load_mnist_data\n"
            "from src.features import deskew_image, extract_hog_features, PCATransformer\n"
            "\n"
            "print('Đã nạp thành công các thư viện cốt lõi!')"
        ),
        make_markdown_cell(
            "### 1. Nạp dữ liệu và kiểm tra kích thước"
        ),
        make_code_cell(
            "(x_train, y_train), (x_test, y_test) = load_mnist_data(normalize=True, flatten=False)\n"
            "print(f'Tập huấn luyện (Train): {x_train.shape}, Nhãn: {y_train.shape}')\n"
            "print(f'Tập kiểm thử   (Test) : {x_test.shape},  Nhãn: {y_test.shape}')\n"
            "print(f'Miền giá trị pixel    : [{x_train.min():.1f}, {x_train.max():.1f}]')"
        ),
        make_markdown_cell(
            "### 2. Kiểm tra độ cân bằng giữa 10 lớp chữ số (Class Distribution)"
        ),
        make_code_cell(
            "train_counts = np.bincount(y_train, minlength=10)\n"
            "test_counts = np.bincount(y_test, minlength=10)\n"
            "\n"
            "plt.figure(figsize=(10, 4), dpi=150)\n"
            "x = np.arange(10)\n"
            "plt.bar(x - 0.2, train_counts, width=0.4, label='Train (60,000)', color='#1d3557')\n"
            "plt.bar(x + 0.2, test_counts, width=0.4, label='Test (10,000)', color='#e63946')\n"
            "plt.xlabel('Chữ số (0 - 9)')\n"
            "plt.ylabel('Số lượng mẫu')\n"
            "plt.title('Phân bố số lượng mẫu giữa các lớp MNIST')\n"
            "plt.xticks(x)\n"
            "plt.legend()\n"
            "plt.show()"
        ),
        make_markdown_cell(
            "### 3. Trực quan hóa ảnh trung bình và phương sai của từng chữ số\n"
            "- **Mean Digit Image**: Cho thấy hình dạng chuẩn mực, trung tâm của từng chữ số.\n"
            "- **Variance Image**: Vùng phát sáng mạnh đại diện cho những vị trí có sự biến thiên nét bút lớn nhất."
        ),
        make_code_cell(
            "fig, axes = plt.subplots(2, 10, figsize=(15, 3.5), dpi=150)\n"
            "for d in range(10):\n"
            "    imgs = x_train[y_train == d]\n"
            "    axes[0, d].imshow(np.mean(imgs, axis=0), cmap='viridis')\n"
            "    axes[0, d].set_title(f'Mean {d}')\n"
            "    axes[0, d].axis('off')\n"
            "    \n"
            "    axes[1, d].imshow(np.var(imgs, axis=0), cmap='magma')\n"
            "    axes[1, d].set_title(f'Var {d}')\n"
            "    axes[1, d].axis('off')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        make_markdown_cell(
            "### 4. Kỹ thuật tiền xử lý hình học: Nắn thẳng góc nghiêng (Deskewing)\n"
            "Sử dụng mô-men ảnh trung tâm để tính độ nghiêng nét viết và khử góc nghiêng bằng phép biến đổi Affine."
        ),
        make_code_cell(
            "fig, axes = plt.subplots(2, 6, figsize=(12, 4), dpi=150)\n"
            "for i in range(6):\n"
            "    orig = x_train[i]\n"
            "    desk = deskew_image(orig)\n"
            "    axes[0, i].imshow(orig, cmap='gray')\n"
            "    axes[0, i].set_title(f'Gốc (Lớp: {y_train[i]})')\n"
            "    axes[0, i].axis('off')\n"
            "    \n"
            "    axes[1, i].imshow(desk, cmap='gray')\n"
            "    axes[1, i].set_title('Sau nắn thẳng')\n"
            "    axes[1, i].axis('off')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        make_markdown_cell(
            "### 5. Phân tích thành phần chính (PCA) & Không gian tiềm ẩn t-SNE\n"
            "Khảo sát phương sai tích lũy và tìm số chiều tối ưu để giữ 95% thông tin."
        ),
        make_code_cell(
            "from sklearn.decomposition import PCA\n"
            "X_flat = x_train.reshape(len(x_train), -1)\n"
            "pca = PCA(n_components=150, random_state=42)\n"
            "pca.fit(X_flat[:10000])\n"
            "cum_var = np.cumsum(pca.explained_variance_ratio_)\n"
            "n_95 = np.searchsorted(cum_var, 0.95) + 1\n"
            "\n"
            "plt.figure(figsize=(7, 4), dpi=150)\n"
            "plt.plot(range(1, 151), cum_var * 100, color='#0284c7', lw=2)\n"
            "plt.axhline(95, color='r', linestyle='--', label=f'Ngưỡng 95% ({n_95} chiều)')\n"
            "plt.xlabel('Số thành phần chính (PC)')\n"
            "plt.ylabel('Phương sai tích lũy (%)')\n"
            "plt.title('Đường cong phương sai tích lũy của PCA')\n"
            "plt.legend()\n"
            "plt.show()"
        )
    ]

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    out_file = NOTEBOOKS_DIR / "01_eda_and_data_analysis.ipynb"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"[OK] Đã tạo notebook EDA: {out_file}")


def build_models_notebook():
    cells = [
        make_markdown_cell(
            "# BÀI TẬP LỚN MÔN NHẬN DẠNG MẪU - ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY\n"
            "## NOTEBOOK 2: THỰC NGHIỆM ĐA MÔ HÌNH & SO SÁNH ĐỐI CHUẨN\n"
            "**Nhóm thực hiện**: Nhóm 03\n"
            "---\n"
            "### Câu hỏi nghiên cứu trọng tâm:\n"
            "> *\"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?\"*\n\n"
            "Notebook này thực hiện huấn luyện và đối chuẩn trên 5 họ mô hình:\n"
            "1. **Naive Bayes**: GaussianNB & BernoulliNB\n"
            "2. **k-Nearest Neighbors (k-NN)**: Raw pixels vs PCA features\n"
            "3. **Support Vector Machines (SVM)**: Linear SVM, RBF SVM + PCA, RBF SVM + HOG\n"
            "4. **Random Forest (Ensemble)**\n"
            "5. **Modern CNN (Deep Learning - Điểm thưởng sáng tạo)**"
        ),
        make_code_cell(
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "sys.path.append(str(Path.cwd().parent))\n"
            "from src.data_loader import load_mnist_data\n"
            "from src.models import create_model, ModernCNN\n"
            "from src.evaluate import evaluate_predictions, plot_confusion_matrix_heatmap\n"
            "\n"
            "print('Đã sẵn sàng môi trường thực nghiệm!')"
        ),
        make_markdown_cell(
            "### 1. Hiển thị bảng tổng hợp kết quả đối chuẩn (Benchmark Results)"
        ),
        make_code_cell(
            "import pandas as pd\n"
            "results_path = Path.cwd().parent / 'reports' / 'tables' / 'benchmark_results.json'\n"
            "if results_path.exists():\n"
            "    df = pd.read_json(results_path)\n"
            "    display(df[['model_name', 'feature_type', 'accuracy', 'macro_f1', 'train_time_sec', 'inference_latency_ms', 'model_size_mb']])\n"
            "else:\n"
            "    print('Vui lòng chạy script src/train_and_benchmark.py để xem bảng kết quả!')"
        ),
        make_markdown_cell(
            "### 2. Trực quan hóa ma trận nhầm lẫn (Confusion Matrix)\n"
            "Ma trận nhầm lẫn giúp phân tích các cặp chữ số thường bị nhận dạng sai lệch."
        ),
        make_code_cell(
            "from PIL import Image\n"
            "fig_dir = Path.cwd().parent / 'reports' / 'figures'\n"
            "cm_files = list(fig_dir.glob('cm_*.png'))\n"
            "print(f'Tìm thấy {len(cm_files)} biểu đồ ma trận nhầm lẫn:')\n"
            "for f in cm_files[:3]:\n"
            "    print(' -', f.name)"
        )
    ]

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "python3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    out_file = NOTEBOOKS_DIR / "02_models_and_benchmark.ipynb"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"[OK] Đã tạo notebook Models: {out_file}")


if __name__ == "__main__":
    build_eda_notebook()
    build_models_notebook()
