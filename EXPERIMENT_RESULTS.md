# KẾT QUẢ THỰC NGHIỆM ĐỐI CHUẨN KHOA HỌC (EXPERIMENT_RESULTS.md)
**Học phần: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay (MNIST)**  
**Đơn vị: Trường Đại học Thủy Lợi — Khoa CNTT — Nhóm 03**

Tất cả các số liệu trong tài liệu này được trích xuất trực tiếp từ tệp cơ sở dữ liệu thực nghiệm đã xác minh `results/verified_experiments.json`, đo lường khách quan trên toàn bộ **10,000 mẫu Test Set** chuẩn của MNIST.

---

## 1. THỰC NGHIỆM ĐỐI CHỨNG CÓ KIỂM SOÁT (CONTROLLED SUBSET BENCHMARK - 10,000 MẪU TRAIN)

> **Nguyên tắc khoa học**: Tất cả các mô hình trong Mục 1 được huấn luyện trên **cùng một tập con 10,000 mẫu phân tầng cố định** (`random_state=42`, 1,000 mẫu/lớp) và đánh giá trên **10,000 mẫu Test Set độc lập**.  
> Điều này loại bỏ hoàn toàn biến nhiễu kích thước mẫu, cho phép phân tích nhân quả chính xác về vai trò của từng đặc trưng và từng thuật toán.

### 1.1. Bảng tổng hợp đối chuẩn kiểm soát (Cùng 10,000 mẫu Train)

| Xếp hạng | Phân nhóm | Mô hình / Thuật toán | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1-Score | Số mẫu sai (/10k test) | Ghi chú khoa học |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **#1** | **Nhóm A (Đặc trưng)** | **SVM (RBF Kernel, C=5.0)** | **Deskewed + PCA** | **112** | 10,000 | **97.97%** | **97.96%** | **203** | **Quán quân Nhóm A**: Nắn thẳng góc nghiêng kết hợp PCA nén thông tin |
| **#2** | Nhóm A (Đặc trưng) | **SVM (RBF Kernel, C=5.0)** | **Deskewed Pixels** | 784 | 10,000 | **97.77%** | **97.75%** | 223 | Nắn thẳng nét chữ tăng +0.91% so với Raw Pixels |
| **#3** | Nhóm C (Học sâu) | **Modern CNN (sub10k)** | **Learned Conv (28×28)** | 784 | 10,000 | **97.60%** | **97.60%** | 240 | CNN tự học biểu diễn từ ảnh thô trên 10k mẫu |
| **#4** | Nhóm A (Đặc trưng) | **SVM (RBF Kernel, C=5.0)** | **HOG Features** | 324 | 10,000 | **97.58%** | **97.57%** | 242 | Biểu đồ hướng gradient nắm bắt cấu trúc biên nét (+0.72%) |
| **#5** | Nhóm A (Đặc trưng) | **SVM (RBF Kernel, C=5.0)** | **PCA (95% Var)** | 152 | 10,000 | **97.22%** | **97.20%** | 278 | Nén chiều $5.1\times$, loại bỏ nhiễu biên (+0.36%) |
| **#6** | Nhóm A (Đặc trưng) | **SVM (RBF Kernel, C=5.0)** | **Raw Pixels** | 784 | 10,000 | **96.86%** | **96.83%** | 314 | Điểm ảnh thô mức xám chuẩn hóa [0, 1] |
| **#7** | Nhóm B (Thuật toán) | **k-NN (k=3, Euclidean)** | **PCA (95% Var)** | 152 | 10,000 | **95.44%** | **95.41%** | 456 | PCA giúp k-NN tăng độ chính xác và giảm $4\times$ độ trễ |
| **#8** | Nhóm B (Thuật toán) | **Random Forest (150 cây)** | **Raw Pixels** | 784 | 10,000 | **95.28%** | **95.23%** | 472 | Học kết hợp Bagging chống quá khớp (150 cây thắng Validation) |
| **#9** | Nhóm B (Thuật toán) | **k-NN (k=3, Euclidean)** | **Raw Pixels** | 784 | 10,000 | **95.17%** | **95.14%** | 483 | Bị ảnh hưởng bởi "lời nguyền số chiều" trên không gian 784D |
| **#10** | Nhóm B (Thuật toán) | **Linear SVM (C=0.01)** | **Raw Pixels** | 784 | 10,000 | **90.79%** | **90.64%** | 921 | Tối ưu điều chuẩn C=0.01 cải thiện từ 89.34% lên 90.79% |
| **#11** | Nhóm B (Thuật toán) | **Bernoulli Naive Bayes** | **Binarized Pixels** | 784 | 10,000 | **84.40%** | **84.20%** | 1,560 | Nhị phân hóa điểm ảnh phù hợp hơn giả định Gauss |
| **#12** | Nhóm B (Thuật toán) | **Gaussian Naive Bayes** | **Raw Pixels** | 784 | 10,000 | **55.80%** | **51.50%** | 4,420 | Vi phạm nghiêm trọng giả định phân phối chuẩn độc lập |

---

## 2. THỰC NGHIỆM MỞ RỘNG QUY MÔ TOÀN PHẦN (FULL DATASET BENCHMARK - 60,000 MẪU TRAIN)

Khi mở rộng quy mô dữ liệu huấn luyện lên tối đa $60,000$ mẫu (huấn luyện trên $50,000$ mẫu train, $10,000$ mẫu validation độc lập để chọn siêu tham số/early stopping, và kiểm thử khách quan trên $10,000$ mẫu test):

| Xếp hạng | Mô hình / Thuật toán | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1-Score | Số mẫu sai (/10k test) | Tốc độ suy luận (ms/mẫu) | Dung lượng mô hình | Trạng thái Checkpoint |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN (Deep Learning)** | **Learned Conv (28×28)** | 784 | 60,000 | **99.19%** | **99.18%** | **81** | **0.079 ms** | **0.62 MB** | Đã xác minh (`modern_cnn_mnist.pt`) |
| **#2** | **SVM (RBF Kernel, C=5.0)** | **PCA (95% Var)** | 154 | 60,000 | **98.54%** | **98.53%** | **146** | 0.852 ms | 8.44 MB | Đã xác minh (`svm_rbf_pca.joblib`) |
| **#3** | **k-NN (k=3, Euclidean)** | **PCA (95% Var)** | 154 | 60,000 | **97.31%** | **97.29%** | **269** | 0.075 ms | 33.74 MB | Đã xác minh (`knn_pca_k3.joblib`) |
| **#4** | **Linear SVM (C=1.0)** | **Raw Pixels (784D)** | 784 | 60,000 | **91.84%** | **91.71%** | 816 | 0.002 ms | 0.05 MB | Đã xác minh (`svm_linear_raw.joblib`) |
| **#5** | **Bernoulli Naive Bayes** | **Binarized Pixels** | 784 | 60,000 | **84.46%** | **84.26%** | 1,554 | 0.004 ms | 0.05 MB | Đã xác minh (`bernoulli_nb_bin.joblib`) |
| **#6** | **Gaussian Naive Bayes** | **Raw Pixels (784D)** | 784 | 60,000 | **55.58%** | **50.90%** | 4,442 | 0.023 ms | 0.04 MB | Đã xác minh (`gaussian_nb_raw.joblib`) |

---

## 3. TRẢ LỜI CÂU HỎI NGHIÊN CỨU DỰA TRÊN BẰNG CHỨNG THỰC TẾ

### Câu hỏi: "Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"

#### 3.1. Phân tích ảnh hưởng của Không gian Đặc trưng (Nhóm A - Đối chứng đơn biến)
1. **Kết hợp Nắn thẳng và Nén chiều (Deskewed + PCA 112D)** là biểu diễn tối ưu nhất trong học máy truyền thống: Đạt **97.97%** (chỉ sai 203 ảnh trên 10k test, Macro F1: 97.96%). Việc nắn thẳng nét chữ giúp thu hẹp phương sai biến thiên nội lớp, cho phép PCA chỉ cần 112 chiều là lưu giữ đủ 95% thông tin, đồng thời tối ưu hóa bề mặt phân cách cho SVM.
2. **Nắn thẳng góc nghiêng (Deskewing 784D)**: Giúp SVM tăng độ chính xác từ **$96.86\% \to 97.77\%$** (+0.91% tuyệt đối, giảm 91 mẫu sai sót). Nguyên nhân: Loại bỏ biến thiên về thói quen viết nghiêng cá nhân.
3. **Lược đồ hướng gradient (HOG - 324D)**: Đạt độ chính xác **$97.58\%$** (+0.72% so với điểm ảnh thô), mô tả xuất sắc hướng viền nét chữ.
4. **Phân tích thành phần chính (PCA - 152D/154D)**: Giảm hơn $5\times$ số chiều nhưng độ chính xác tăng từ **$96.86\% \to 97.22\%$** trên SVM và từ **$95.17\% \to 95.44\%$** trên k-NN. Điều này chứng minh PCA lọc bỏ thành công các điểm ảnh viền tối không mang thông tin phân lớp.

#### 3.2. Phân tích ảnh hưởng của Thuật toán Phân lớp (Nhóm B - Đối chứng đơn biến)
1. **RBF SVM ($96.86\%$) vượt trội Linear SVM ($90.79\%$)**: Khoảng cách chênh lệch $+6.07\%$, chứng minh bề mặt quyết định của các chữ số viết tay trong không gian điểm ảnh có tính phi tuyến phức tạp. Điều chuẩn tối ưu $C=0.01$ trên Linear SVM đã giúp cải thiện rõ rệt từ 89.34% lên 90.79% (giảm 145 lỗi).
2. **Random Forest 150 cây ($95.28\%$) và k-NN ($95.44\%$)**: Cho hiệu năng tương đương nhau ở quy mô 10,000 mẫu. Tuy nhiên k-NN có nhược điểm lớn về dung lượng lưu trữ vector mẫu (33.7 MB) và độ trễ suy luận tăng tuyến tính theo số mẫu.
3. **Sự thất bại của Gaussian Naive Bayes ($55.80\%$)**: Giả định 784 điểm ảnh độc lập có điều kiện bị vi phạm nghiêm trọng trong hình ảnh chữ số tự nhiên. Khi nhị phân hóa pixel, Bernoulli Naive Bayes cải thiện đáng kể lên **$84.40\%$** (+28.6% tuyệt đối).

#### 3.3. Phân tích ưu thế của Deep Learning và Quy mô dữ liệu (Nhóm C)
1. **Modern CNN trên 60k mẫu đạt 99.19% (81 lỗi)**: Vượt qua tất cả các mô hình truyền thống tốt nhất.
2. **Hiện tượng đổi ngôi thú vị giữa quy mô 10k và 60k**:
   - Ở quy mô nhỏ 10k mẫu: SVM Deskew + PCA (97.97%) vượt qua Modern CNN 10k (97.60%) nhờ có tri thức chuyên gia hình học định hướng trước (Inductive Bias từ Deskewing).
   - Ở quy mô lớn 60k mẫu: Modern CNN (99.19%) bứt phá vượt qua SVM RBF + PCA (98.54%) nhờ năng lực tự học các bộ lọc tích chập phân cấp từ lượng lớn dữ liệu mà không cần trích xuất thủ công.
