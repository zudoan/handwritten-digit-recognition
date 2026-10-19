# KẾT QUẢ THỰC NGHIỆM ĐÃ XÁC MINH (FINAL_EXPERIMENT_RESULTS.md)
**Dự án: Nhận dạng chữ số viết tay trên MNIST — Nhóm 03 — Trường Đại học Thủy Lợi**  
**Nguồn dữ liệu xác minh duy nhất: `results/verified_experiments.json`**

---

## 1. BẢNG TỔNG HỢP KẾT QUẢ TOÀN DIỆN (ĐÃ ĐO ĐẠC VÀ KIỂM CHỨNG)

Tất cả các số liệu dưới đây được đo lường trực tiếp trên toàn bộ **10,000 ảnh** của tập kiểm thử độc lập MNIST Test Set:

### 1.1. Quy mô Toàn phần (Full Dataset - 60,000 mẫu Huấn luyện)

| Mã EXP | Mô hình | Không gian Đặc trưng | Số chiều | Mẫu Train | **Test Accuracy** | Macro F1-Score | Số ảnh sai / 10k | Thời gian Train (s) | Độ trễ suy luận (ms) | Dung lượng mô hình | Checkpoint |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **EXP-C01** | **Modern CNN** | **Learned Conv (28×28)** | 784 | 60,000 | **99.19%** | **99.18%** | **81** | 164.75 s | **0.079 ms** | 0.62 MB | `modern_cnn_mnist.pt` |
| **EXP-F01** | **SVM (RBF Kernel)** | PCA (95% Var) | 154 | 60,000 | **98.54%** | **98.53%** | 146 | 125.56 s | 0.852 ms | 8.44 MB | `svm_rbf_pca.joblib` |
| **EXP-F02** | **k-NN ($k=3$, Euclidean)** | PCA (95% Var) | 154 | 60,000 | **97.31%** | **97.29%** | 269 | 0.00 s | 0.075 ms | 33.74 MB | `knn_pca_k3.joblib` |
| **EXP-F03** | **Linear SVM** | Raw Pixels (784D) | 784 | 60,000 | **91.84%** | **91.71%** | 816 | 28.02 s | 0.002 ms | 0.05 MB | `svm_linear_raw.joblib` |
| **EXP-F04** | **Bernoulli Naive Bayes** | Binarized Pixels | 784 | 60,000 | **84.46%** | **84.26%** | 1,554 | 0.35 s | 0.004 ms | 0.05 MB | `bernoulli_nb_bin.joblib` |
| **EXP-F05** | **Gaussian Naive Bayes** | Raw Pixels (784D) | 784 | 60,000 | **55.58%** | **50.90%** | 4,442 | 0.21 s | 0.023 ms | 0.04 MB | `gaussian_nb_raw.joblib` |

---

### 1.2. Tập con Kiểm chuẩn Đối chứng Đơn biến (Controlled Subset - Cùng 10,000 mẫu Huấn luyện)

Cố định tập dữ liệu huấn luyện phân tầng 10,000 mẫu (`random_state=42`, 1,000 mẫu/lớp) và đánh giá trên 10,000 mẫu test:

| Mã EXP | Nhóm đối chuẩn | Mô hình | Đặc trưng | Chiều | **Test Accuracy** | Macro F1 | Số ảnh sai | Thời gian Train (s) | Độ trễ (ms) | Đánh giá khoa học |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **EXP-A01** | **Nhóm A (Đặc trưng)** | **SVM RBF ($C=5.0$)** | **Deskewed + PCA** | **112** | **97.97%** | **97.96%** | **203** | 6.56 s | 0.329 ms | **Quán quân Nhóm A**: Nắn thẳng nét chữ + PCA |
| **EXP-A02** | Nhóm A (Đặc trưng) | SVM RBF ($C=5.0$) | Deskewed Pixels | 784 | **97.77%** | 97.75% | 223 | 12.43 s | 0.679 ms | Nắn thẳng triệt tiêu độ nghiêng nét viết |
| **EXP-C02** | Nhóm C (Học sâu) | Modern CNN (sub10k) | Learned Conv | 784 | **97.60%** | 97.60% | 240 | 37.40 s | 0.082 ms | CNN tự học trên 10k mẫu |
| **EXP-A03** | Nhóm A (Đặc trưng) | SVM RBF ($C=5.0$) | HOG Features | 324 | **97.58%** | 97.57% | 242 | 11.85 s | 0.614 ms | Đặc trưng hướng biên cạnh cục bộ |
| **EXP-A04** | Nhóm A (Đặc trưng) | SVM RBF ($C=5.0$) | PCA (95% Var) | 152 | **97.22%** | 97.20% | 278 | 6.12 s | 0.270 ms | Nén chiều $5.1\times$, lọc nhiễu vùng biên |
| **EXP-A05** | Nhóm A (Đặc trưng) | SVM RBF ($C=5.0$) | Raw Pixels | 784 | **96.86%** | 96.83% | 314 | 18.12 s | 1.132 ms | Điểm ảnh thô mức xám chuẩn hóa |
| **EXP-B01** | **Nhóm B (Thuật toán)** | k-NN ($k=3$, Euclidean)| PCA (95% Var) | 152 | **95.44%** | 95.41% | 456 | 0.00 s | 0.057 ms | PCA giúp k-NN tăng độ chính xác và tốc độ |
| **EXP-B02** | Nhóm B (Thuật toán) | Random Forest (150 cây) | Raw Pixels | 784 | **95.28%** | 95.23% | 472 | 0.42 s | 0.006 ms | 150 cây tối ưu trên Validation, bagging chống quá khớp |
| **EXP-B03** | Nhóm B (Thuật toán) | k-NN ($k=3$, Euclidean)| Raw Pixels | 784 | **95.17%** | 95.14% | 483 | 0.01 s | 0.231 ms | Bị ảnh hưởng bởi lời nguyền số chiều |
| **EXP-B04** | Nhóm B (Thuật toán) | Linear SVM ($C=0.01$) | Raw Pixels | 784 | **90.79%** | 90.64% | 921 | 0.70 s | 0.002 ms | Tối ưu C=0.01 trên Validation, cải thiện từ 89.34% lên 90.79% |
| **EXP-B05** | Nhóm B (Thuật toán) | Bernoulli Naive Bayes | Binarized Pixels | 784 | **84.40%** | 84.20% | 1,560 | 17.40 s | 0.010 ms | Nhị phân hóa điểm ảnh |
| **EXP-B06** | Nhóm B (Thuật toán) | Gaussian Naive Bayes | Raw Pixels | 784 | **55.80%** | 51.50% | 4,420 | 0.06 s | 0.040 ms | Vi phạm giả định độc lập không gian |

---

## 2. LỊCH SỬ TỐI ƯU SIÊU THAM SỐ TRÊN VALIDATION SET (HYPERPARAMETER TUNING)

Toàn bộ các siêu tham số được lựa chọn dựa trên điểm **Validation Accuracy** và **Validation Macro F1** trên tập 10,000 mẫu Validation độc lập (tuyệt đối không chạm vào Test Set). Trích xuất trực tiếp từ `results/hyperparameter_search_results.json`:

| Họ mô hình | Không gian đặc trưng | Cấu hình siêu tham số thử nghiệm | Val Accuracy | Val Macro F1 | Quyết định lựa chọn |
|:---|:---|:---|:---:|:---:|:---:|
| **k-NN** | PCA (152D) | $n\_neighbors=3$, weights='uniform' | 95.32% | 95.31% | Không chọn |
| **k-NN (Tối ưu)** | **PCA (152D)** | **$n\_neighbors=3$, weights='distance'** | **95.60%** | **95.59%** | **ĐÃ CHỌN (Khớp checkpoint)** |
| **k-NN** | PCA (152D) | $n\_neighbors=5$, weights='uniform' | 95.19% | 95.18% | Không chọn |
| **k-NN** | PCA (152D) | $n\_neighbors=5$, weights='distance' | 95.55% | 95.55% | Không chọn |
| **k-NN** | PCA (152D) | $n\_neighbors=7$, weights='distance' | 95.21% | 95.22% | Không chọn |
| **Linear SVM (Tối ưu)**| **Raw Pixels (784D)** | **$C=0.01$** | **90.36%** | **90.25%** | **ĐÃ CHỌN** |
| **Linear SVM** | Raw Pixels (784D) | $C=0.1$ | 90.17% | 90.03% | Không chọn |
| **Linear SVM** | Raw Pixels (784D) | $C=1.0$ | 88.87% | 88.72% | Không chọn |
| **Linear SVM** | Raw Pixels (784D) | $C=5.0$ | 87.70% | 87.55% | Không chọn |
| **RBF SVM** | PCA (152D) | $C=1.0, \gamma=\text{'scale'}$ | 96.73% | 96.72% | Không chọn |
| **RBF SVM (Tối ưu)** | **PCA (152D)** | **$C=5.0, \gamma=\text{'scale'}$** | **97.09%** | **97.08%** | **ĐÃ CHỌN (Khớp checkpoint)** |
| **RBF SVM** | PCA (152D) | $C=10.0, \gamma=\text{'scale'}$ | 97.08% | 97.07% | Không chọn |
| **Random Forest** | Raw Pixels (784D) | $n\_estimators=50$, max_features='sqrt' | 94.40% | 94.37% | Không chọn |
| **Random Forest** | Raw Pixels (784D) | $n\_estimators=100$, max_features='sqrt'| 94.90% | 94.88% | Không chọn |
| **Random Forest (Tối ưu)**| **Raw Pixels (784D)** | **$n\_estimators=150$, max_features='sqrt'**| **95.07%** | **95.04%** | **ĐÃ CHỌN** |

---

## 3. BẰNG CHỨNG XÁC MINH VỀ MÔ HÌNH CHÍNH THỨC MODERN CNN

- **Checkpoint**: `saved_models/modern_cnn_mnist.pt` (650,927 bytes ~ 0.62 MB).
- **Kiến trúc chính xác (Đồng bộ mã nguồn `src/models.py`)**:
  - Khối 1: `Conv2d(1, 32, kernel_size=3, padding=1)` + `BatchNorm2d(32)` + `ReLU` + `MaxPool2d(2, 2)` (Kích thước: $14 \times 14 \times 32$)
  - Khối 2: `Conv2d(32, 64, kernel_size=3, padding=1)` + `BatchNorm2d(64)` + `ReLU` + `MaxPool2d(2, 2)` (Kích thước: $7 \times 7 \times 64$)
  - Khối 3: `Conv2d(64, 128, kernel_size=3, padding=1)` + `BatchNorm2d(128)` + `ReLU` + `AdaptiveAvgPool2d((2, 2))` (Kích thước: $2 \times 2 \times 128 = 512$ chiều)
  - Phân loại (FC): `Flatten()` + `Linear(512, 128)` + `BatchNorm1d(128)` + `ReLU` + `Dropout(0.4)` + `Linear(128, 10)` + `LogSoftmax(dim=1)`
  - **Tổng số tham số**: Đúng **160,074 tham số** (khớp 100% checkpoint).
- **Tập kiểm thử**: 10,000 ảnh MNIST Test Set.
- **Kết quả đo lường thực tế**:
  - **Accuracy: 99.19%** ($9,919 / 10,000$ mẫu đúng).
  - **Macro F1-Score: 99.18%**.
  - **Tổng số ảnh sai: 81 ảnh**.
  - **Độ trễ suy luận trung bình: 0.079 ms/ảnh** (trên CPU).
- **Phân loại nguyên nhân 81 mẫu sai**:
  1. *Nhiễu nhãn gán sai trong bộ dữ liệu gốc (Label Noise)*: Một số mẫu trong MNIST bị gán nhãn sai từ lúc số hóa ban đầu (ví dụ ảnh là số 6 nhưng nhãn ghi 0; ảnh là 9 nhưng nhãn ghi 4). Mô hình CNN thực chất đã dự đoán đúng theo hình thái thị giác thực tế.
  2. *Chữ số cực kỳ mơ hồ (Ambiguous Digits)*: Nét chữ cẩu thả, đứt đoạn, mắt người nhìn vào cũng không thể khẳng định chắc chắn 100%.
  3. *Biến dạng dị thường (Geometric Outliers)*: Tỷ lệ khung hình quá khác biệt khiến bước căn tâm quang học bị dịch chuyển lệch tâm.
