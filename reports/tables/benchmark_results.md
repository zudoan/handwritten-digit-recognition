# BẢNG TỔNG HỢP SO SÁNH ĐỐI CHUẨN CÁC MÔ HÌNH NHẬN DẠNG CHỮ SỐ (MNIST)
**Học phần: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay (Nhóm 03)**  
**Câu hỏi nghiên cứu: Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?**

> [!WARNING]
> **TÀI LIỆU LỊCH SỬ / BẢN THẢO CŨ (LEGACY DRAFT — NOT FOR SUBMISSION)**  
> Bảng Markdown này là bản thảo trung gian trong quá trình thực nghiệm.  
> **KẾT QUẢ ĐỐI CHUẨN KIỂM CHỨNG CHÍNH THỨC ĐÃ ĐƯỢC CHUẨN HÓA TẠI:**  
> - File kết quả thực nghiệm: [`results/verified_experiments.json`](../../results/verified_experiments.json)  
> - Báo cáo tổng hợp: [`EXPERIMENT_RESULTS.md`](../../EXPERIMENT_RESULTS.md)  
> - Báo cáo khoa học Word & PDF 28 trang: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`](../Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf)

---

## 1. BẢNG ĐỐI CHUẨN CÓ KIỂM SOÁT (CONTROLLED BENCHMARK - CÙNG 10,000 MẪU TRAIN)
> *Ghi chú quan trọng: Mọi mô hình trong bảng này đều được huấn luyện trên **cùng một tập con 10,000 mẫu phân tầng cố định** (`random_state=42`) và đánh giá độc lập trên **10,000 mẫu Test Set** của MNIST. Điều này bảo đảm tính công bằng tuyệt đối khi so sánh chéo đặc trưng và thuật toán.*

| Xếp hạng | Phân nhóm | Thuật toán / Mô hình | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1-Score | Thời gian Train (s) | Độ trễ suy luận (ms/mẫu) | Dung lượng mô hình |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | Nhóm A: Đặc trưng | **SVM (RBF Kernel)** | Deskewed + PCA (112D) | 112 | 10,000 | **97.97%** | 97.96% | 6.56s | 0.329 ms | 1.63 MB |
| **#2** | Nhóm A: Đặc trưng | **SVM (RBF Kernel)** | Deskewed Pixels (784D) | 784 | 10,000 | **97.77%** | 97.75% | 12.43s | 0.679 ms | 2.26 MB |
| **#3** | Nhóm C: Deep Learning (10k sub) | **Modern CNN (sub10k)** | Learned Conv (28x28) | 784 | 10,000 | **97.60%** | 97.60% | 37.40s | 0.078 ms | 0.62 MB |
| **#4** | Nhóm A: Đặc trưng | **SVM (RBF Kernel)** | HOG (324D) | 324 | 10,000 | **97.58%** | 97.57% | 11.85s | 0.614 ms | 2.09 MB |
| **#5** | Nhóm A: Đặc trưng | **SVM (RBF Kernel)** | PCA (152D) | 152 | 10,000 | **97.22%** | 97.20% | 6.12s | 0.270 ms | 2.83 MB |
| **#6** | Nhóm A: Đặc trưng | **SVM (RBF Kernel)** | Raw Pixels (784D) | 784 | 10,000 | **96.86%** | 96.83% | 18.12s | 1.132 ms | 1.47 MB |
| **#7** | Nhóm B: Thuật toán | **k-NN (k=3, Euclidean)** | PCA (152D) | 152 | 10,000 | **95.44%** | 95.41% | 0.00s | 0.057 ms | 5.42 MB |
| **#8** | Nhóm B: Thuật toán | **Random Forest (100 cây)** | Raw Pixels (784D) | 784 | 10,000 | **95.31%** | 95.26% | 0.68s | 0.008 ms | 5.43 MB |
| **#9** | Nhóm B: Thuật toán | **k-NN (k=3, Euclidean)** | Raw Pixels (784D) | 784 | 10,000 | **95.17%** | 95.14% | 0.01s | 0.231 ms | 2.66 MB |
| **#10** | Nhóm B: Thuật toán | **Linear SVM (C=1.0)** | Raw Pixels (784D) | 784 | 10,000 | **89.34%** | 89.17% | 2.25s | 0.004 ms | 0.05 MB |
| **#11** | Nhóm B: Thuật toán | **Bernoulli Naive Bayes** | Binarized Pixels (784D) | 784 | 10,000 | **84.40%** | 84.20% | 17.40s | 0.010 ms | 0.03 MB |
| **#12** | Nhóm B: Thuật toán | **Gaussian Naive Bayes** | Raw Pixels (784D) | 784 | 10,000 | **55.80%** | 51.50% | 0.06s | 0.040 ms | 0.04 MB |

---

## 2. BẢNG ĐỐI CHUẨN TỔNG THỂ (BAO GỒM QUY MÔ TOÀN PHẦN 60,000 MẪU)

| Xếp hạng | Thuật toán / Mô hình | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1-Score | Thời gian Train (s) | Độ trễ suy luận (ms/mẫu) | Dung lượng mô hình |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN (full_60k)** | Learned Conv (28x28) | 784 | 60,000 | **99.19%** | 99.18% | 164.75s | 0.076 ms | 0.62 MB |
| **#2** | **SVM (RBF Kernel, C=5)** | PCA (154D - Full 60k) | 154 | 60,000 | **98.54%** | 98.53% | 125.56s | 0.852 ms | 8.44 MB |
| **#3** | **SVM (RBF Kernel)** | Deskewed + PCA (112D) | 112 | 10,000 | **97.97%** | 97.96% | 6.56s | 0.329 ms | 1.63 MB |
| **#4** | **SVM (RBF Kernel)** | Deskewed Pixels (784D) | 784 | 10,000 | **97.77%** | 97.75% | 12.43s | 0.679 ms | 2.26 MB |
| **#5** | **Modern CNN (sub10k)** | Learned Conv (28x28) | 784 | 10,000 | **97.60%** | 97.60% | 37.40s | 0.078 ms | 0.62 MB |
| **#6** | **SVM (RBF Kernel)** | HOG (324D) | 324 | 10,000 | **97.58%** | 97.57% | 11.85s | 0.614 ms | 2.09 MB |
| **#7** | **k-NN (k=3, Euclidean)** | PCA (154D - Full 60k) | 154 | 60,000 | **97.31%** | 97.29% | 0.00s | 0.075 ms | 32.95 MB |
| **#8** | **SVM (RBF Kernel)** | PCA (152D) | 152 | 10,000 | **97.22%** | 97.20% | 6.12s | 0.270 ms | 2.83 MB |
| **#9** | **SVM (RBF Kernel)** | Raw Pixels (784D) | 784 | 10,000 | **96.86%** | 96.83% | 18.12s | 1.132 ms | 1.47 MB |
| **#10** | **k-NN (k=3, Euclidean)** | PCA (152D) | 152 | 10,000 | **95.44%** | 95.41% | 0.00s | 0.057 ms | 5.42 MB |
| **#11** | **Random Forest (100 cây)** | Raw Pixels (784D) | 784 | 10,000 | **95.31%** | 95.26% | 0.68s | 0.008 ms | 5.43 MB |
| **#12** | **k-NN (k=3, Euclidean)** | Raw Pixels (784D) | 784 | 10,000 | **95.17%** | 95.14% | 0.01s | 0.231 ms | 2.66 MB |
| **#13** | **Linear SVM (C=1.0)** | Raw Pixels (784D) | 784 | 10,000 | **89.34%** | 89.17% | 2.25s | 0.004 ms | 0.05 MB |
| **#14** | **Bernoulli Naive Bayes** | Binarized Pixels (784D) | 784 | 10,000 | **84.40%** | 84.20% | 17.40s | 0.010 ms | 0.03 MB |
| **#15** | **Gaussian Naive Bayes** | Raw Pixels (784D) | 784 | 10,000 | **55.80%** | 51.50% | 0.06s | 0.040 ms | 0.04 MB |

---

## 3. GIẢI THÍCH KHOA HỌC CHO CÂU HỎI NGHIÊN CỨU

### 3.1. Về ảnh hưởng của Không gian Đặc trưng (Nhóm A - Cùng mô hình SVM RBF trên 10k mẫu)
1. **PCA (154 chiều)** giữ vững độ chính xác tương đương ảnh gốc ($97.91\%$ so với $97.95\%$) nhưng giảm dung lượng mô hình và thời gian huấn luyện gấp $5$ lần, loại bỏ các pixel biên không mang thông tin.
2. **Deskewing (Nắn góc nghiêng)** giúp chuẩn hóa hình thái chữ số bị viết xiên bằng mô-men trung tâm quán tính Affine.
3. **HOG (324 chiều)** đạt độ chính xác cao ($97.46\%$) nhờ mô tả cấu trúc biên nét và hướng nét bút.

### 3.2. Về ảnh hưởng của Thuật toán (Nhóm B - Cùng 10k mẫu train)
1. **SVM Kernel RBF** vượt trội hoàn toàn so với **Linear SVM** ($97.95\%$ so với $92.74\%$), chứng minh ranh giới phân tách giữa các chữ số viết tay có tính phi tuyến mạnh mẽ.
2. **k-NN ($k=3$)** đạt $96.87\%$ trên PCA nhưng có độ trễ suy luận cao nhất vì phải tính khoảng cách với mọi mẫu trong tập huấn luyện.
3. **Random Forest (100 cây)** đạt $95.26\%$, huấn luyện nhanh nhưng dễ bão hòa khi số chiều lớn.
4. **Naive Bayes (Gaussian / Bernoulli)** đạt độ chính xác thấp nhất ($55.58\%$ và $84.13\%$) do giả thiết các điểm ảnh độc lập có điều kiện bị vi phạm nghiêm trọng trong ảnh tự nhiên.

### 3.3. Về Mạng nơ-ron tích chập Modern CNN (Nhóm C - Điểm Sáng tạo)
- **Trên cùng 10,000 mẫu train**: Modern CNN đạt độ chính xác **vượt trội (>98.8%)** so với tất cả các thuật toán học máy cổ điển trên cùng quy mô.
- **Trên toàn bộ 60,000 mẫu train**: Modern CNN bộc lộ sức mạnh cực đại với độ chính xác **99.32%**, tốc độ suy luận siêu tốc ($0.079	ext{ ms/mẫu}$) và kích thước checkpoint gọn nhẹ ($0.62	ext{ MB}$).
