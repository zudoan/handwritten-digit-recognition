# GIAO THỨC THỰC NGHIỆM ĐỐI CHUẨN KIỂM SOÁT (EXPERIMENT_PROTOCOL.md)
**Học phần: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay (MNIST)**  
**Đơn vị: Trường Đại học Thủy Lợi — Nhóm 03**

---

## 1. MỤC TIÊU VÀ CÂU HỎI KHOA HỌC
Giải quyết câu hỏi nghiên cứu chính thức:
> **"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"**

Để trả lời thỏa đáng, toàn bộ các thực nghiệm phải tuân thủ nguyên tắc **đối chứng đơn biến (Controlled Single-variable Comparison)**:
- Khi khảo sát ảnh hưởng của **đặc trưng**, phải giữ cố định thuật toán và tập dữ liệu.
- Khi khảo sát ảnh hưởng của **thuật toán**, phải giữ cố định không gian đặc trưng và tập dữ liệu.
- Tách biệt rõ ràng thực nghiệm trên tập con kiểm soát (*Controlled Benchmark Subset*) với thực nghiệm trên toàn bộ dữ liệu (*Full Benchmark*).

---

## 2. QUY TRÌNH PHÂN CHIA VÀ KIỂM SOÁT DỮ LIỆU

### 2.1. Phân chia tập dữ liệu chuẩn
- **Tập kiểm thử (Test Set)**: Giữ nguyên $10,000$ mẫu chuẩn của MNIST do NIST/LeCun công bố. Tập này chỉ được sử dụng cho đánh giá độc lập cuối cùng. Tuyệt đối không fit transformer, không tinh chỉnh siêu tham số trên tập này.
- **Tập huấn luyện & kiểm định gốc**: $60,000$ mẫu từ `x_train`, `y_train`.
- **Phân chia 3-way split có phân tầng (Stratified Split, `random_state = 42`)**:
  - `Train Set` ($50,000$ mẫu - ~83.33%): Dùng để tối ưu tham số trọng số mô hình.
  - `Validation Set` ($10,000$ mẫu - ~16.67%): Dùng để thẩm định siêu tham số ($C, \gamma, k$) và chọn checkpoint tốt nhất.
  - `Test Set` ($10,000$ mẫu): Đánh giá tổng quát hóa.

### 2.2. Tập con đối chứng kiểm soát (Controlled Benchmark Subset - 10,000 mẫu)
Do các giải thuật như SVM kernel RBF và k-NN tính toán khoảng cách theo ma trận cặp ($O(N^2)$ đến $O(N \cdot D)$) trên CPU có thời gian chạy rất lớn với 50,000 mẫu, chúng tôi thiết kế một **tập con phân tầng chuẩn hóa cố định gồm 10,000 mẫu train** (mỗi lớp chính xác 1,000 mẫu, trích xuất từ 50,000 mẫu train gốc với `random_state = 42`).
- Tập con này được áp dụng **đồng nhất tuyệt đối** cho mọi phép so sánh trong Nhóm A và Nhóm B.
- Tập Validation ($10,000$ mẫu) và Tập Test ($10,000$ mẫu) được giữ nguyên vẹn.

### 2.3. Kiểm soát rò rỉ dữ liệu (Data Leakage Protocol)
1. **PCA Transformer**:
   - Chỉ được `fit` trên tập huấn luyện của thí nghiệm tương ứng.
   - Khi áp dụng cho đặc trưng nắn thẳng (*Deskewed*), PCA phải được `fit` trên tập ảnh đã nắn thẳng của tập train, sau đó mới `transform` cho validation và test.
2. **Min-Max Scaling & Chuẩn hóa**:
   - Ánh xạ chia $255.0$ là phép co dãn cố định không phụ thuộc tham số thống kê tập dữ liệu.
3. **Deskewing**:
   - Tính toán mô-men trung tâm quán tính độc lập trên từng ảnh, không phụ thuộc vào các mẫu xung quanh.
4. **HOG**:
   - Trích xuất độc lập từng ảnh với tham số cố định (9 hướng, cell $7 \times 7$, block $2 \times 2$).

---

## 3. THIẾT KẾ CÁC NHÓM ĐỐI CHUẨN CÓ KIỂM SOÁT

### NHÓM A — KHẢO SÁT ẢNH HƯỞNG CỦA ĐẶC TRƯNG (FEATURE IMPACT)
- **Thuật toán cố định**: SVM Kernel RBF ($C = 5.0, \gamma = \text{'scale'}$).
- **Tập huấn luyện cố định**: Cùng tập con phân tầng 10,000 mẫu (`x_sub_train`, `y_sub_train`).
- **Tập đánh giá cố định**: $10,000$ mẫu Test chuẩn của MNIST.
- **Các không gian đặc trưng so sánh**:
  1. `A1`: **Raw Pixels (784 chiều)**: Điểm ảnh chuẩn hóa $[0, 1]$.
  2. `A2`: **Deskewed Pixels (784 chiều)**: Nắn thẳng góc nghiêng bằng mô-men quán tính Affine.
  3. `A3`: **PCA Features (152 chiều - 95% phương sai)**: Fit PCA trên 10,000 mẫu train subset.
  4. `A4`: **HOG Features (324 chiều)**: Lược đồ hướng gradient cục bộ.
  5. `A5`: **Deskewed + PCA (112 chiều - 95% phương sai)**: Nắn thẳng trước, sau đó fit PCA riêng trên ảnh đã nắn thẳng (cô đọng phương sai, nén còn 112 chiều).

### NHÓM B — KHẢO SÁT ẢNH HƯỞNG CỦA THUẬT TOÁN (ALGORITHM IMPACT)
- **Không gian đặc trưng cố định**: Raw Pixels (784 chiều) hoặc PCA 154 chiều.
- **Tập huấn luyện cố định**: Cùng tập con 10,000 mẫu (`x_sub_train`, `y_sub_train`).
- **Tập đánh giá cố định**: $10,000$ mẫu Test chuẩn của MNIST.
- **Các thuật toán so sánh**:
  1. `B1`: **Gaussian Naive Bayes** (Mô hình xác suất tham số, giả định phân phối Gauss).
  2. `B2`: **Bernoulli Naive Bayes** (Mô hình xác suất nhị phân, ngưỡng binarize $\theta = 0.2$). *Ghi chú: Đầu vào nhị phân hóa, không hoàn toàn đồng nhất với pixel liên tục nhưng đưa vào để so sánh trong họ Bayes.*
  3. `B3`: **k-Nearest Neighbors ($k=3$, Euclidean)** (Học không tham số).
  4. `B4`: **Linear SVM ($C=1.0$)** (Siêu phẳng phân tách tuyến tính cực đại lề).
  5. `B5`: **RBF SVM ($C=5.0$)** (Kernel phi tuyến chiếu vào không gian vô hạn chiều).
  6. `B6`: **Random Forest ($100$ cây)** (Ensemble bagging).

### NHÓM C — MÔ HÌNH HỌC SÂU NÂNG CAO (DEEP LEARNING / CREATIVE BONUS)
- **Kiến trúc**: Modern CNN (3 khối Conv2D $3\times3$ + BatchNorm + ReLU + MaxPool $2\times2$ + Dropout + Fully-Connected).
- **Đặc trưng**: Tự động học bộ lọc từ ảnh 2D ($28 \times 28$), không dùng đặc trưng thủ công.
- **Đánh giá đối chiếu**:
  - Đánh giá trên tập con 10,000 mẫu để so sánh công bằng với Nhóm A và B.
  - Đánh giá trên tập đầy đủ 60,000 mẫu (50k train, 10k val, 10k test) để kiểm tra năng lực tối đa của Deep Learning.

---

## 4. TIÊU CHÍ VÀ PHƯƠNG PHÁP ĐO HIỆU NĂNG

Mỗi mô hình được đánh giá qua các thước đo khoa học:
1. **Accuracy**: $\frac{\sum \mathbb{I}(\hat{y} = y)}{N}$.
2. **Macro Precision, Macro Recall, Macro F1-score**: Trung bình không trọng số giữa 10 lớp.
3. **Training Time (giây)**: Thời gian fit mô hình trên CPU.
4. **Inference Latency (mili-giây/mẫu)**: Đo trên toàn bộ $10,000$ mẫu test, chia cho $10,000$ để ra độ trễ từng mẫu.
5. **Model Checkpoint Size (MB)**: Dung lượng tệp lưu trữ trên đĩa cứng.
