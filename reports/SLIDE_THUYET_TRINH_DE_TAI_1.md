# ĐỀ CƯƠNG SLIDE BÁO CÁO THUYẾT TRÌNH BÀI TẬP LỚN
## ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY (MNIST DATASET)
**Môn học: Nhận dạng mẫu (Pattern Recognition) — Nhóm 03**
**Trường Đại học Thủy Lợi — Khoa Công nghệ Thông tin**

> [!WARNING]
> **TÀI LIỆU LỊCH SỬ / BẢN THẢO CŨ (LEGACY DRAFT — NOT FOR SUBMISSION)**  
> File Markdown này là bản phác thảo slide ban đầu. Bộ slide trình chiếu chính thức đã được thiết kế hoàn thiện, chia tách khoa học 12 slide widescreen không tràn bảng tại:  
> **[`reports/Slide_Thuyet_Trinh_Nhom_03.pptx`](Slide_Thuyet_Trinh_Nhom_03.pptx)**.

---

### SLIDE 1: TRANG BÌA
- **Tiêu đề**: NGHIÊN CỨU & TRIỂN KHAI CÁC MÔ HÌNH NHẬN DẠNG CHỮ SỐ VIẾT TAY
- **Học phần**: Nhận dạng mẫu (*Pattern Recognition*)
- **Nhóm thực hiện**: Nhóm 03
- **Thành viên**: `[Họ tên SV 1]`, `[Họ tên SV 2]`, `[Họ tên SV 3]`
- **Giảng viên hướng dẫn**: `[Điền tên Giảng viên]`
- **Đơn vị**: Khoa Công nghệ Thông tin - Trường Đại học Thủy Lợi

---

### SLIDE 2: BỐI CẢNH & CÂU HỎI NGHIÊN CỨU
- **Bối cảnh thực tế**: Bài toán nhận dạng chữ số tự động trong phân loại bưu phẩm bưu chính, nhận dạng số tài khoản/séc ngân hàng, số hóa tài liệu hành chính.
- **Thách thức cốt lõi**:
  - Sự đa dạng về thói quen viết tay cá nhân (nét nghiêng, nét đứt, độ dày bút).
  - Độ tương đồng thị giác cao giữa các cặp số: $(4 \leftrightarrow 9)$, $(3 \leftrightarrow 5)$, $(7 \leftrightarrow 1)$.
- **Câu hỏi nghiên cứu trọng tâm**:
  > *"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"*

---

### SLIDE 3: BỘ DỮ LIỆU THỰC NGHIỆM (MNIST)
- Nguồn dữ liệu: Yann LeCun / TensorFlow Datasets Catalog.
- Quy mô: **70,000 ảnh xám** $28 \times 28$ điểm ảnh (784 chiều).
- Phân chia chuẩn học thuật:
  - **Train**: 60,000 mẫu (~85.7%).
  - **Test**: 10,000 mẫu (~14.3%).
- Đánh giá phân bố: Gần như cân bằng hoàn hảo giữa 10 lớp ($0 \to 9$), độ hỗn loạn thông tin Shannon Entropy đạt $3.32$ bits (tiệm cận cực đại $\log_2 10$).

---

### SLIDE 4: KHÁM PHÁ DỮ LIỆU CHUYÊN SÂU (EDA)
- **Mean Digit Images (Ảnh trung bình)**:
  - Thể hiện dạng hình học trung tâm của từng chữ số. Số '1' tập trung nét thẳng ở giữa, số '0' có vòng oval rỗng.
- **Variance Heatmaps (Ảnh phương sai)**:
  - Chỉ ra các vùng điểm ảnh có sự bất đồng thuận lớn nhất giữa các người viết.
  - Số '4' và '7' có phương sai cao ở nét ngang gạch chân; số '2' có phương sai cao ở vòng xoắn đáy.
- **Không gian tiềm ẩn t-SNE 2D**:
  - Các cụm số $0, 1, 6$ tách biệt rõ rệt. Cụm $4, 7, 9$ nằm gần nhau do có chung đặc trưng nét thẳng đứng và nét nghiêng.

---

### SLIDE 5: KỸ THUẬT TRÍCH XUẤT ĐẶC TRƯNG
Nhóm thiết kế và so sánh **4 không gian đặc trưng**:
1. **Raw Pixels (784D)**: Điểm ảnh chuẩn hóa $[0.0, 1.0]$.
2. **Deskewing (Nắn góc nghiêng)**: Dùng mô-men quán tính ảnh trung tâm $\alpha = \mu_{11} / \mu_{02}$ để thực hiện biến đổi Affine, nắn thẳng chữ số bị viết xiên.
3. **PCA (Principal Component Analysis)**: Giảm từ 784 chiều xuống **154 chiều** giữ nguyên 95% phương sai (giảm $5.1\times$ dung lượng).
4. **HOG (Histogram of Oriented Gradients)**: Trích xuất 324 chiều đặc trưng hướng biên nét viết.

---

### SLIDE 6: CƠ SỞ TOÁN HỌC CÁC THUẬT TOÁN ML KINH ĐIỂN
- **Naive Bayes (Gaussian & Bernoulli)**:
  - Áp dụng định lý Bayes $P(Y|X) \propto P(Y) \prod P(X_j|Y)$. Giả định các pixel độc lập có điều kiện.
- **$k$-Nearest Neighbors ($k$-NN)**:
  - Phân loại phi tham số dựa trên khoảng cách Euclidean trong không gian nhiều chiều.
  - Kết hợp PCA giúp loại bỏ "lời nguyền số chiều" và tăng tốc độ tìm kiếm láng giềng.
- **Support Vector Machine (SVM)**:
  - Tìm siêu phẳng tối ưu cực đại hóa biên phân cách (Max-margin hyperplane).
  - Áp dụng **RBF Kernel** $K(x, z) = \exp(-\gamma \|x - z\|^2)$ chiếu phi tuyến vào không gian vô hạn chiều.

---

### SLIDE 7: MÔ HÌNH HỌC SÂU SÁNG TẠO (MODERN CNN)
- **Kiến trúc mạng tích chập LeNet-5 hiện đại hóa**:
  - 3 khối tích chập: `Conv2D(3x3) -> BatchNorm -> ReLU -> MaxPool(2x2)`.
  - Bộ phân loại: `Dropout(0.4) -> Linear(512 -> 128) -> ReLU -> Dropout(0.2) -> Linear(128 -> 10)`.
- **Cơ chế học đặc trưng tự động**:
  - Tầng nông: Học bộ lọc phát hiện cạnh, góc, viền.
  - Tầng sâu: Tổng hợp thành các cung tròn, vòng khép kín của số 8, 6, 0.

---

### SLIDE 8: BẢNG SO SÁNH ĐỐI CHUẨN HIỆU NĂNG (BENCHMARK)

| Thuật toán | Đặc trưng | Chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1 | Thời gian Train | Độ trễ suy luận |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Modern CNN** | Learned Conv | 784 | 60,000 | **99.32%** | **99.31%** | 198.55s | 0.079 ms |
| **SVM (RBF Kernel)** | **PCA (95% Var)** | 154 | 60,000 | **98.54%** | **98.53%** | 27.88s | 0.866 ms |
| **SVM (RBF Kernel)** | Deskewed + PCA | 154 | 10,000 | **97.91%** | 97.90% | 0.83s | 0.196 ms |
| **SVM (RBF Kernel)** | HOG Features | 324 | 10,000 | **97.46%** | 97.46% | 1.13s | 0.282 ms |
| **$k$-NN ($k=3$)** | PCA (95% Var) | 154 | 60,000 | **97.31%** | 97.29% | 0.00s | 0.077 ms |
| **Random Forest** | Raw Pixels | 784 | 10,000 | **95.26%** | 95.22% | 0.33s | 0.005 ms |
| **$k$-NN ($k=3$)** | Raw Pixels | 784 | 10,000 | **94.86%** | 94.85% | 0.01s | 0.074 ms |
| **Linear SVM** | Raw Pixels | 784 | 60,000 | **91.84%** | 91.71% | 28.02s | 0.002 ms |
| **Bernoulli NB** | Binarized Pixels | 784 | 60,000 | **84.46%** | 84.26% | 0.35s | 0.004 ms |
| **Gaussian NB** | Raw Pixels | 784 | 60,000 | **55.58%** | 50.90% | 0.21s | 0.023 ms |

---

### SLIDE 9: PHÂN TÍCH MA TRẬN NHẦM LẪN (CONFUSION MATRIX)
- **Cặp nhầm lẫn phổ biến nhất**:
  - $4 \to 9$: Nét gạch đỉnh của số 4 bị nối liền hoặc viết quá khép, giống vòng tròn của số 9.
  - $7 \to 2$ hoặc $7 \to 1$: Số 7 thiếu nét gạch ngang giữa thân hoặc viết thẳng như số 1.
  - $3 \to 5$: Phần móc cung tròn uốn lượn có cấu trúc hình học tương đồng cao.
- Mô hình **CNN** gần như xóa bỏ sự nhầm lẫn này (độ chính xác từng lớp đều trên 99.0%).

---

### SLIDE 10: PHÂN TÍCH LỖI CHUYÊN SÂU (DEEP ERROR ANALYSIS)
- Lọc top 20 mẫu ảnh lỗi mà các mô hình dự đoán sai:
  - **Trường hợp 1: Nhãn gốc trong MNIST bị gán nhãn sai** (Label Noise).
  - **Trường hợp 2: Chữ số cực kỳ mơ hồ (Ambiguous Digits)**: Thậm chí con người khi nhìn bằng mắt thường cũng khó phân định đó là số 4 hay 9.
  - **Trường hợp 3: Nét đứt quãng hoặc mực bị loang**: Làm mất tính liên tục cấu trúc tô-pô.

---

### SLIDE 11: TRẢ LỜI CÂU HỎI NGHIÊN CỨU KHOA HỌC
> *"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"*
1. **Đặc trưng tối ưu nhất**:
   - **Learned Features (CNN)**: Vượt trội nhất vì không cần trích xuất thủ công, tự học theo cấu trúc không gian 2D.
   - **PCA (154D)**: Là biểu diễn đặc trưng nén hiệu quả nhất trong ML truyền thống (tiết kiệm $5\times$ bộ nhớ, cải thiện $k$-NN từ $94.86\% \to 97.31\%$).
2. **Thuật toán tối ưu nhất**:
   - **Modern CNN** (>99.32%) dẫn đầu về độ chính xác và khả năng thích nghi.
   - **SVM (RBF Kernel + PCA)** (>98.54%) là thuật toán ML cổ điển mạnh mẽ nhất, thời gian train chỉ 27 giây.

---

### SLIDE 12: DEMO ỨNG DỤNG WEB TƯƠNG TÁC (+0.5 ĐIỂM THƯỞNG)
- **Kiến trúc hệ thống**: Frontend Vanilla HTML5 Canvas + Backend FastAPI.
- **Tính năng nổi bật**:
  - Bảng vẽ tương tác mượt mà bằng chuột hoặc màn hình cảm ứng.
  - Cơ chế tiền xử lý quang học **Center of Mass** chuẩn hóa tọa độ tâm $(14, 14)$ như tập MNIST gốc.
  - Tùy chọn chuyển đổi tức thì giữa các mô hình (CNN, SVM, k-NN, GNB).
  - Hiển thị trực quan thanh xác suất 10 lớp và độ trễ suy luận thời gian thực (chỉ 10–15 ms).
  - Tích hợp sẵn thanh Palette 10 mẫu test chọn nhanh.

---

### SLIDE 13: ĐIỂM SÁNG TẠO & ĐÓNG GÓP CỦA DỰ ÁN
1. **Tính sáng tạo (+0.5đ)**:
   - Triển khai mạng nơ-ron tích chập Modern CNN với BatchNorm và Dropout.
   - Thực nghiệm kỹ thuật tiền xử lý hình học Deskewing dựa trên mô-men bậc hai.
2. **Sản phẩm hoàn thiện (+0.5đ)**:
   - Ứng dụng Web hoàn chỉnh, trực quan, thẩm mỹ cao theo chuẩn Glassmorphism.
3. **Quy chuẩn mã nguồn**:
   - Cấu trúc module hóa chuyên nghiệp, có file hướng dẫn cài đặt `requirements.txt`, Jupyter Notebook chi tiết và chạy được ngay với 1 lệnh `python run_app.py`.

---

### SLIDE 14: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
- **Kết luận**: Nhóm đã hoàn thành xuất sắc 100% mục tiêu bài tập lớn theo đúng thang điểm và hướng dẫn của bộ môn.
- **Hướng phát triển tương lai**:
  - Mở rộng bài toán sang nhận dạng chuỗi chữ số viết tay liên tục (như mã bưu điện, số điện thoại, biển số xe).
  - Triển khai mô hình Vision Transformer (ViT) nhẹ hoặc chuyển đổi sang định dạng ONNX/TensorRT để chạy trên thiết bị biên nhúng (Edge AI).

---

### SLIDE 15: HỎI VÀ ĐÁP (Q&A)
- **Cảm ơn Thầy/Cô và các bạn đã chú ý lắng nghe!**
- *Nhóm 03 xin trân trọng đón nhận các câu hỏi và ý kiến đóng góp của Hội đồng.*
