import sys
import json
from pathlib import Path
import numpy as np

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from src.config import TABLES_DIR
from src.data_loader import load_mnist_data


def generate_eda_tables():
    (x_train, y_train), (x_test, y_test) = load_mnist_data(normalize=True, flatten=False)

    train_counts = np.bincount(y_train, minlength=10)
    test_counts = np.bincount(y_test, minlength=10)
    total_train = len(y_train)
    total_test = len(y_test)

    rows = []
    for d in range(10):
        tr_c = int(train_counts[d])
        te_c = int(test_counts[d])
        tr_pct = tr_c / total_train * 100
        te_pct = te_c / total_test * 100
        rows.append({
            "class": d,
            "train_count": tr_c,
            "train_percent": round(tr_pct, 2),
            "test_count": te_c,
            "test_percent": round(te_pct, 2),
            "total_count": tr_c + te_c,
            "total_percent": round((tr_c + te_c) / 70000 * 100, 2)
        })

    # Calculate class balance entropy
    probs = train_counts / total_train
    entropy = -np.sum(probs * np.log2(probs))
    max_entropy = np.log2(10)
    balance_ratio = entropy / max_entropy

    summary_md = f"""# BẢNG THỐNG KÊ CHI TIẾT TẬP DỮ LIỆU MNIST
**Học phần: Nhận dạng mẫu — Nhóm 03**

### 1. Phân bố số lượng mẫu giữa các lớp (Class Distribution)

| Chữ số | Huấn luyện (Train) | Tỷ lệ (%) | Kiểm thử (Test) | Tỷ lệ (%) | Tổng cộng | Tỷ lệ tổng (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
"""
    for r in rows:
        summary_md += f"| **{r['class']}** | {r['train_count']:,} | {r['train_percent']:.2f}% | {r['test_count']:,} | {r['test_percent']:.2f}% | {r['total_count']:,} | {r['total_percent']:.2f}% |\n"

    summary_md += f"""| **Tổng** | **{total_train:,}** | **100.00%** | **{total_test:,}** | **100.00%** | **70,000** | **100.00%** |

### 2. Chỉ số cân bằng dữ liệu (Data Balance Metrics)
- **Độ hỗn loạn thông tin (Shannon Entropy)**: {entropy:.4f} bits (so với cực đại lý thuyết: {max_entropy:.4f} bits).
- **Hệ số cân bằng (Balance Ratio)**: {balance_ratio * 100:.2f}% (Tập dữ liệu gần như cân bằng hoàn hảo, không xảy ra hiện tượng mất cân bằng lớp cực đoan - class imbalance).
- **Lớp có số mẫu nhiều nhất**: Lớp 1 ({train_counts[1]:,} mẫu trong tập Train, chiếm 11.24%).
- **Lớp có số mẫu ít nhất**: Lớp 5 ({train_counts[5]:,} mẫu trong tập Train, chiếm 9.04%).

### 3. Thông số kỹ thuật không gian đặc trưng
- **Độ phân giải ảnh**: $28 \\times 28$ điểm ảnh.
- **Số kênh màu**: 1 kênh (Ảnh mức xám - Grayscale).
- **Số chiều vector sau phẳng hóa**: $784$ chiều ($28 \\times 28$).
- **Miền giá trị pixel gốc**: Số nguyên $[0, 255]$ ($\text{{uint8}}$).
- **Miền giá trị sau chuẩn hóa Min-Max**: Số thực $[0.0, 1.0]$ ($\text{{float32}}$).
"""
    md_path = TABLES_DIR / "eda_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(summary_md)

    json_path = TABLES_DIR / "eda_statistics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "rows": rows,
            "entropy": entropy,
            "balance_ratio": balance_ratio,
            "total_train": total_train,
            "total_test": total_test
        }, f, indent=2, ensure_ascii=False)

    print(f"[OK] Đã lưu bảng thống kê EDA: {md_path}")

if __name__ == "__main__":
    generate_eda_tables()
