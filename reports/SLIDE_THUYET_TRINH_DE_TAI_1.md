# ĐỀ CƯƠNG SLIDE BÁO CÁO THUYẾT TRÌNH BÀI TẬP LỚN
## ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY (MNIST DATASET)
**Học phần: Nhận dạng mẫu (Pattern Recognition) — Nhóm 03**  
**Khoa Công nghệ Thông tin — Phân hiệu Trường Đại học Thủy Lợi**

---

### SLIDE 1: TRANG BÌA
- **Tiêu đề**: NGHIÊN CỨU & TRIỂN KHAI CÁC MÔ HÌNH NHẬN DẠNG CHỮ SỐ VIẾT TAY TRÊN BỘ DỮ LIỆU MNIST
- **Học phần**: Nhận dạng mẫu (*Pattern Recognition*)
- **Nhóm thực hiện**: Nhóm 03
- **Sinh viên thực hiện**: 
  - Đoàn Anh Vũ (MSV: `2351267280`)
  - Nguyễn Hồng Nguyên (MSV: `2351267273`)
- **Đơn vị đào tạo**: Khoa Công nghệ Thông tin — Phân hiệu Trường Đại học Thủy Lợi

---

### SLIDE 2: BỐI CẢNH & CÂU HỎI NGHIÊN CỨU
- **Bối cảnh thực tế**: Bài toán nhận dạng chữ số tự động trong bưu chính (Zip Codes), tài chính ngân hàng (séc, phiếu nộp tiền), số hóa tài liệu hồ sơ hành chính.
- **Thách thức cốt lõi**:
  - Sự biến thiên đa dạng trong thói quen viết tay cá nhân (nét nghiêng, nét đứt, độ dày bút).
  - Sự tương đồng thị giác cao giữa các cặp số: $(4 \leftrightarrow 9)$, $(3 \leftrightarrow 5)$, $(7 \leftrightarrow 1)$.
- **Câu hỏi nghiên cứu trọng tâm**:
  > *"Không gian đặc trưng nào và thuật toán học máy nào giúp nhận dạng chữ số viết tay trên MNIST hiệu quả và tối ưu nhất về độ chính xác lẫn độ trễ suy luận?"*

---

### SLIDE 3: BỘ DỮ LIỆU THỰC NGHIỆM (MNIST)
- **Nguồn dữ liệu**: Bộ dữ liệu chuẩn học thuật Yann LeCun / TensorFlow MNIST Dataset.
- **Quy mô**: **70.000 ảnh xám** kích thước $28 \times 28$ điểm ảnh (784 chiều).
- **Phân chia chuẩn học thuật**:
  - **Train**: 50.000 mẫu (~71.4%) dùng để huấn luyện mô hình.
  - **Validation**: 10.000 mẫu (~14.3%) dùng để kiểm chứng và dừng sớm (Early Stopping).
  - **Test**: 10.000 mẫu (~14.3%) dùng để đối chuẩn độc lập, khách quan 100%.
- **Đánh giá phân bố**: Phân bố nhãn cân bằng hoàn hảo giữa 10 lớp ($0 \to 9$), độ hỗn loạn thông tin Shannon Entropy đạt $3.32$ bits.

---

### SLIDE 4: KHÁM PHÁ DỮ LIỆU CHUYÊN SÂU (EDA)
- **Mean Digit Images (Ảnh trung bình)**:
  - Thể hiện dạng hình học đặc trưng trung tâm của từng chữ số. Chữ số '1' tập trung nét thẳng ở giữa; số '0' có vòng oval rỗng đặc trưng.
- **Variance Heatmaps (Bản đồ nhiệt phương sai)**:
  - Chỉ ra các vùng điểm ảnh có sự bất đồng thuận lớn nhất giữa người viết.
  - Chữ số '4' và '7' có phương sai cao ở nét ngang gạch chân; chữ số '2' có phương sai cao ở vòng xoắn đáy.
- **Không gian tiềm ẩn t-SNE 2D & PCA**:
  - Các cụm số $0, 1, 6$ tách biệt rất rõ rệt. Cụm $4, 7, 9$ nằm gần nhau do có chung đặc trưng nét thẳng đứng và nét nghiêng.

---

### SLIDE 5: TIỀN XỬ LÝ ẢNH & TRÍCH XUẤT ĐẶC TRƯNG
Nhóm thiết kế và áp dụng các kỹ thuật biểu diễn dữ liệu:
1. **Raw Pixels (784D)**: Điểm ảnh chuẩn hóa $[0.0, 1.0]$.
2. **Deskewing (Nắn thẳng góc nghiêng nét viết)**:
   - Dùng mô-men quán tính ảnh trung tâm $\alpha = \mu_{11} / \mu_{02}$ để thực hiện biến đổi Affine, đưa nét chữ xiên về phương thẳng đứng.
3. **PCA (Principal Component Analysis 95% phương sai)**:
   - Áp dụng trên tập ảnh đã nắn thẳng Deskewing, giảm từ **784 chiều** xuống **113 chiều** (giảm 6.9 lần số chiều, loại bỏ nhiễu biên và tăng tốc suy luận).
4. **Binarization (Nhị phân hóa)**: Ngưỡng $0.2$ phục vụ mô hình Bernoulli Naive Bayes.

---

### SLIDE 6: CÁC THUẬT TOÁN HỌC MÁY KINH ĐIỂN
- **Bernoulli Naive Bayes**:
  - Áp dụng định lý Bayes trên không gian nhị phân, tốc độ cực nhanh ($1.66$ ms), phù hợp làm baseline khởi điểm.
- **Random Forest (150 cây quyết định)**:
  - Học tập hợp (Ensemble Learning) phương pháp Bagging với 150 Decision Trees, không bị overfit, đạt $96.99\%$.
- **$k$-Nearest Neighbors ($k$-NN, $k=3$, Trọng số khoảng cách nghịch đảo)**:
  - Huấn luyện trên không gian đặc trưng **Deskew + PCA (113D)** giúp triệt tiêu "lời nguyền số chiều", đạt độ chính xác cao $98.06\%$.
- **Support Vector Machine (SVM RBF Kernel)**:
  - Tìm siêu phẳng tối ưu cực đại hóa khoảng cách lề lồi trong không gian Hilbert tái tạo qua hàm nhân RBF ($C=5.0$, $\gamma=\text{scale}$), kết hợp **Deskew + PCA (113D)** đạt xuất sắc **$98.79\%$** (chỉ 121 lỗi).

---

### SLIDE 7: HỌC SÂU MẠNG TÍCH CHẬP (MODERN CNN)
- **Kiến trúc mạng tích chập hiện đại (3 khối Convolutional)**:
  - Khối 1: `Conv2D(32) -> BatchNorm -> ReLU -> Conv2D(32) -> MaxPool(2x2) -> Dropout(0.25)`
  - Khối 2: `Conv2D(64) -> BatchNorm -> ReLU -> Conv2D(64) -> MaxPool(2x2) -> Dropout(0.25)`
  - Khối 3: `Conv2D(128) -> BatchNorm -> ReLU -> Flatten -> Dropout(0.4)`
  - Khối phân loại: `Linear(128) -> ReLU -> Dropout(0.3) -> Linear(10)`
- **Chiến lược huấn luyện**:
  - Tối ưu bằng **Adam**, học trên 50.000 mẫu train, kiểm tra sau mỗi epoch trên 10.000 mẫu validation.
  - Áp dụng **Early Stopping** dừng tối ưu tại Epoch 17 với Validation Loss cực tiểu $0.0249$.
  - Đạt đỉnh cao hiệu năng **$99.42\%$** Accuracy (chỉ sai **58 ảnh** trên 10.000 ảnh test).

---

### SLIDE 8: BẢNG SO SÁNH ĐỐI CHUẨN HIỆU NĂNG TOÀN DIỆN (BENCHMARK)

| Xếp hạng | Mô hình | Không gian đặc trưng | Tập huấn luyện | Accuracy | Macro F1 | Số ảnh sai / 10k | Độ trễ suy luận |
|:---:|---|---|---|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN** | Learned Conv (28×28) | 50k train / 10k val | **99.42%** | **99.42%** | **58** | 8.85 ms |
| **#2** | **SVM** | Deskewed + PCA 95% (113D) | 50.000 mẫu | **98.79%** | **98.78%** | **121** | 20.03 ms |
| **#3** | **k-NN** | Deskewed + PCA 95% (113D) | 50.000 mẫu | **98.06%** | **98.05%** | **194** | 63.38 ms |
| **#4** | **Random Forest** | Raw Pixels (784D) | 50.000 mẫu | **96.99%** | **96.97%** | **301** | 56.72 ms |
| **#5** | **Bernoulli Naive Bayes** | Binarized Pixels (784D) | 50.000 mẫu | **84.46%** | **84.27%** | **1.554** | 1.66 ms |

---

### SLIDE 9: MA TRẬN NHẦM LẪN & ĐÁNH GIÁ TỪNG LỚP
- **Phân bố nhầm lẫn của Modern CNN**:
  - Lớp nhận dạng tốt nhất: Chữ số **0** ($99.80\%$ Recall, chỉ sai 2 ảnh) và chữ số **1** ($99.56\%$ Recall).
  - Lớp gặp thách thức nhất: Chữ số **5** ($98.09\%$ Recall, 17 ảnh nhầm sang 3 do cùng nét cong bụng dưới).
- **Phân tích 58 mẫu dự đoán sai**:
  - Nhóm 1: Nét viết bất thường, dị biệt (Outliers) từ người viết tự do.
  - Nhóm 2: Nhầm lẫn cặp số tương đồng hình thái học: $(4 \leftrightarrow 9)$, $(3 \leftrightarrow 5)$, $(7 \leftrightarrow 2)$.

---

### SLIDE 10: ỨNG DỤNG WEB DEMO TƯƠNG TÁC THỜI GIAN THỰC
- **Kiến trúc ứng dụng**:
  - Backend: **FastAPI** hiệu năng cao, nạp sẵn trọng số vào RAM, xử lý phi đồng bộ (Async/Await).
  - Frontend: HTML5 Canvas vẽ tay độ phân giải cao, hỗ trợ chuột và màn hình cảm ứng.
- **Pipeline tiền xử lý Center of Mass quang học**:
  - Bóc tách nét chữ bằng `cv2.boundingRect()` $\to$ Thu phóng bảo toàn tỷ lệ vào khung $20 \times 20$ $\to$ Tịnh tiến trọng tâm quang học khối lượng về chính giữa tọa độ chuẩn $(14.0, 14.0)$ của khung ảnh $28 \times 28$ NIST.
- **Trải nghiệm người dùng**:
  - Hiển thị phân bố xác suất thời gian thực 10 lớp chữ số $(0 \to 9)$.
  - Tích hợp 10 mẫu kiểm thử chuẩn NIST từ tập test để thử nghiệm tức thì.
  - Footer tối giản, chỉn chu: *Phân hiệu Đại học Thủy Lợi*.

---

### SLIDE 11: BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)
- Thiết kế **28 ca kiểm thử tự động (Unit & Integration Tests)** trong `tests/test_pipeline.py`.
- Bảo đảm 100% không rò rỉ dữ liệu (Zero Data Leakage giữa Train và Test).
- Kiểm tra toàn diện kích thước ma trận, hàm trích xuất Deskewing, PCA 113D, lan truyền tiến CNN và các API endpoints của Web Server.
- Tỷ lệ vượt qua: **28 / 28 Tests Passed (100%)**.

---

### SLIDE 12: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
- **Kết luận khoa học**:
  1. Kỹ thuật **Deskewing + PCA (113 chiều)** tăng cường vượt bậc độ chính xác của các thuật toán ML kinh điển (SVM vọt lên $98.79\%$, k-NN vọt lên $98.06\%$).
  2. **Modern CNN** là kiến trúc ưu việt nhất với khả năng tự động học biểu diễn đặc trưng không gian, đạt đỉnh cao **$99.42\%$** Accuracy.
- **Đóng góp thực tiễn**:
  - Xây dựng thành công hệ sinh thái hoàn chỉnh từ Notebook nghiên cứu, kho mô hình chuẩn, bộ test tự động đến Web Demo phục vụ giảng dạy và ứng dụng thực tế.
- **Hướng phát triển**:
  - Mở rộng nhận dạng chuỗi nhiều chữ số liên tục bằng kiến trúc CRNN + CTC Loss.
  - Lượng tử hóa mô hình INT8 / ONNX để nhúng lên thiết bị di động và camera AI biên.
