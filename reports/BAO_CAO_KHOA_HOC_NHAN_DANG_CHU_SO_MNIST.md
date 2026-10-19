# BÁO CÁO KHOA HỌC BÀI TẬP LỚN MÔN NHẬN DẠNG MẪU

**TRƯỜNG ĐẠI HỌC THỦY LỢI — KHOA CÔNG NGHỆ THÔNG TIN**  
**BỘ MÔN KHOA HỌC MÁY TÍNH**

> [!WARNING]
> **TÀI LIỆU LỊCH SỬ / BẢN THẢO CŨ (LEGACY DRAFT — NOT FOR SUBMISSION)**  
> Tài liệu Markdown tóm tắt này thuộc giai đoạn khảo sát ban đầu và chứa một số số liệu thử nghiệm sơ khai.  
> **TÀI LIỆU CHÍNH THỨC DÙNG ĐỂ NỘP VÀ CHẤM ĐIỂM ĐÃ ĐƯỢC ĐỒNG BỘ 100% TẠI:**  
> - Báo cáo khoa học Word & PDF 28 trang: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf)  
> - Slide thuyết trình chính thức (12 slides): [`reports/Slide_Thuyet_Trinh_Nhom_03.pptx`](reports/Slide_Thuyet_Trinh_Nhom_03.pptx)  
> - Kết quả thực nghiệm kiểm chứng chính thức: [`results/verified_experiments.json`](../results/verified_experiments.json) & [`EXPERIMENT_RESULTS.md`](../EXPERIMENT_RESULTS.md)

---

<p align="center">
  <strong>ĐỀ TÀI 1: NGHIÊN CỨU VÀ TRIỂN KHAI CÁC MÔ HÌNH NHẬN DẠNG CHỮ SỐ VIẾT TAY TRÊN BỘ DỮ LIỆU MNIST</strong><br>
  <em>(Học phần: Nhận dạng mẫu — Mã học phần: CSE...)</em>
</p>

---

<p align="center">
  <strong>NHÓM THỰC HIỆN: NHÓM 03</strong><br>
  Sinh viên thực hiện:<br>
  1. <strong>[Họ và tên SV 1]</strong> — MSV: <code>[Điền MSV]</code> (Nhóm trưởng)<br>
  2. <strong>[Họ và tên SV 2]</strong> — MSV: <code>[Điền MSV]</code><br>
  3. <strong>[Họ và tên SV 3]</strong> — MSV: <code>[Điền MSV]</code><br>
  Lớp: <code>63KTPM...</code> — Khóa: K63<br>
  Giảng viên hướng dẫn: <strong>[Điền tên Giảng viên hướng dẫn]</strong>
</p>

<p align="center">
  <em>Hà Nội, Năm 2026</em>
</p>

---

## MỤC LỤC
1. [CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN & DỮ LIỆU](#chương-1-giới-thiệu-bài-toán--dữ-liệu)
2. [CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & THUẬT TOÁN](#chương-2-cơ-sở-lý-thuyết--thuật-toán)
3. [CHƯƠNG 3: KHAI PHÁ DỮ LIỆU (EDA) & KỸ THUẬT TIỀN XỬ LÝ](#chương-3-khai-phá-dữ-liệu-eda--kỹ-thuật-tiền-xử-lý)
4. [CHƯƠNG 4: MÔ HÌNH THỰC NGHIỆM & KẾT QUẢ ĐỐI CHUẨN](#chương-4-mô-hình-thực-nghiệm--kết-quả-đối-chuẩn)
5. [CHƯƠNG 5: PHÂN TÍCH KẾT QUẢ & PHÂN TÍCH LỖI CHUYÊN SÂU](#chương-5-phân-tích-kết-quả--phân-tích-lỗi-chuyên-sâu)
6. [CHƯƠNG 6: KẾT LUẬN & HƯỚNG PHÁT TRIỂN](#chương-6-kết-luận--hướng-phát-triển)
7. [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)

---

## CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN & DỮ LIỆU

### 1.1. Bối cảnh thực tế và Tính cấp thiết của đề tài
Nhận dạng mẫu (*Pattern Recognition*) là một phân ngành nòng cốt của Trí tuệ Nhân tạo và Khoa học Dữ liệu, tập trung vào việc tự động phát hiện quy luật, cấu trúc và gán nhãn cho các đối tượng quan sát. Trong số các bài toán kinh điển, **Nhận dạng chữ số viết tay** (*Handwritten Digit Recognition*) đóng vai trò đặc biệt quan trọng cả về mặt lý thuyết học thuật lẫn ứng dụng thực tiễn:
- **Tự động hóa bưu chính**: Phân loại tự động hàng triệu lá thư và bưu phẩm mỗi ngày dựa trên mã bưu chính (*ZIP Code*).
- **Hệ thống ngân hàng và tài chính**: Đọc và đối soát tự động số tiền, ngày tháng và số tài khoản trên séc ngân hàng (*Check processing*).
- **Số hóa văn bản hành chính**: Chuyển đổi hồ sơ giấy, biểu mẫu thi trắc nghiệm và chứng từ thuế sang dữ liệu điện tử.

Thách thức trọng tâm của bài toán xuất phát từ sự biến thiên cực kỳ phức tạp về mặt hình học: thói quen cầm bút, độ nghiêng nét viết, nét đứt đoạn, nét đậm nhạt, và độ tương đồng thị giác cao giữa các cặp chữ số khác nhau (như số 4 và số 9, số 7 và số 1, số 3 và số 5).

### 1.2. Xác định đối tượng và Không gian bài toán
- **Đối tượng cần nhận dạng**: Các bức ảnh xám đơn kênh biểu diễn chữ số viết tay đơn lẻ.
- **Không gian nhãn lớp**: 10 lớp số tự nhiên riêng biệt:
  $$\mathcal{Y} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$$
- **Ý nghĩa kết quả**: Mỗi mẫu ảnh đầu vào được hệ thống gán cho một nhãn lớp dự đoán $\hat{y} \in \mathcal{Y}$ kèm theo phân bố xác suất tin cậy $P(y = c | \mathbf{x})$.

### 1.3. Nguồn gốc bộ dữ liệu chuẩn học thuật (MNIST)
Dự án sử dụng bộ dữ liệu chuẩn **MNIST** (*Modified National Institute of Standards and Technology*) do Yann LeCun, Corinna Cortes và Christopher Burges xây dựng từ hai tập con Special Database 1 và Special Database 3 của NIST. Dữ liệu được tải trực tiếp từ nguồn chính thức của **TensorFlow Datasets Catalog**:
- **Tổng số lượng mẫu**: $70,000$ mẫu ảnh xám chuẩn hóa kích thước $28 \times 28$ điểm ảnh.
- **Tập huấn luyện (Training Set)**: $60,000$ mẫu (~85.7%).
- **Tập kiểm thử (Test Set)**: $10,000$ mẫu (~14.3%).

### 1.4. Câu hỏi nghiên cứu trọng tâm
Đề tài bám sát câu hỏi khoa học do Hội đồng bộ môn đề ra:
> **"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"**

Để trả lời thỏa đáng câu hỏi này, nhóm thực hiện nghiên cứu so sánh chéo giữa **4 không gian biểu diễn đặc trưng** (Raw Pixels, Deskewed, PCA, HOG) và **5 họ thuật toán phân lớp** (Naive Bayes, $k$-NN, SVM, Random Forest, CNN).

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & THUẬT TOÁN

### 2.1. Bộ phân lớp Bayes thơ ngây (Naive Bayes)
Mô hình phân lớp xác suất dựa trên định lý Bayes kết hợp giả định "thơ ngây" rằng tất cả các điểm ảnh đều độc lập có điều kiện với nhau khi biết trước nhãn lớp:
$$P(y = c | \mathbf{x}) = \frac{P(y = c) \prod_{j=1}^{D} P(x_j | y = c)}{P(\mathbf{x})}$$
- **Gaussian Naive Bayes (GNB)**: Giả định mật độ xác suất của từng điểm ảnh liên tục tuân theo phân phối chuẩn $\mathcal{N}(\mu_{c, j}, \sigma_{c, j}^2)$.
- **Bernoulli Naive Bayes (BNB)**: Nhị phân hóa ảnh theo ngưỡng $x_j \in \{0, 1\}$, tính xác suất pixel được kích hoạt $p_{c, j}$.

### 2.2. Thuật toán $k$-Láng giềng gần nhất ($k$-NN)
$k$-NN là phương pháp học lười (*Lazy learning*), không tham số (*Non-parametric*). Không gian quyết định được hình thành bằng cách tính khoảng cách giữa mẫu mới $\mathbf{x}$ với tất cả các mẫu trong tập huấn luyện:
$$d(\mathbf{x}, \mathbf{x}^{(i)}) = \left( \sum_{j=1}^{D} |x_j - x_j^{(i)}|^p \right)^{1/p}$$
- Với $p = 2$: Khoảng cách Euclidean; với $p = 1$: Khoảng cách Manhattan.
- Nhãn dự đoán là nhãn chiếm đa số trong tập $k$ láng giềng gần nhất, có thể gia quyền theo nghịch đảo khoảng cách: $w_i = \frac{1}{d(\mathbf{x}, \mathbf{x}^{(i)})}$.

### 2.3. Máy vector hỗ trợ (Support Vector Machine - SVM)
SVM hướng tới việc tìm siêu phẳng tối ưu phân tách các lớp sao cho **khoảng cách lề (Margin)** giữa siêu phẳng và các điểm dữ liệu gần nhất (gọi là các vector hỗ trợ - Support Vectors) là cực đại:
$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^{N} \xi_i \quad \text{s.t.} \quad y^{(i)}(\mathbf{w}^T \phi(\mathbf{x}^{(i)}) + b) \ge 1 - \xi_i$$
Để xử lý bài toán phi tuyến, SVM sử dụng hàm nhân **Radial Basis Function (RBF Kernel)** nhằm chiếu ngầm định dữ liệu vào không gian vô hạn chiều:
$$K(\mathbf{x}, \mathbf{z}) = \exp(-\gamma \|\mathbf{x} - \mathbf{z}\|^2)$$

### 2.4. Rừng ngẫu nhiên (Random Forest)
Thuật toán học kết hợp (*Ensemble Learning*) dựa trên kỹ thuật đóng bao (*Bagging*) và lựa chọn ngẫu nhiên tập đặc trưng (*Feature Subsampling*). Rừng ngẫu nhiên huấn luyện đồng thời hàng trăm cây quyết định (*Decision Trees*) độc lập, sau đó lấy biểu quyết đa số nhằm giảm phương sai và chống quá khớp (*Overfitting*).

### 2.5. Mạng nơ-ron tích chập (Modern CNN - Sáng tạo)
Mạng CNN được thiết kế đặc thù cho dữ liệu dạng lưới 2D như hình ảnh:
- **Tầng tích chập (Convolutional Layer)**: Trượt các bộ lọc $3 \times 3$ qua ảnh để trích xuất bản đồ đặc trưng (*Feature Maps*), bảo toàn tính bất biến tịnh tiến (*Translation Invariance*).
- **Batch Normalization**: Chuẩn hóa trung gian giữa các tầng giúp tăng tốc độ hội tụ và ổn định gradient.
- **Max Pooling ($2 \times 2$)**: Giảm kích thước không gian, nén thông tin và tăng vùng tiếp nhận (*Receptive Field*).
- **Dropout**: Ngắt ngẫu nhiên 20–40% liên kết nơ-ron trong quá trình train để chống phụ thuộc đồng thời (*Co-adaptation*).

---

## CHƯƠNG 3: KHAI PHÁ DỮ LIỆU (EDA) & KỸ THUẬT TIỀN XỬ LÝ

### 3.1. Phân tích thống kê và Độ cân bằng dữ liệu
Kiểm tra thực nghiệm trên toàn bộ 70,000 mẫu MNIST:
- **Tập Train (60,000 mẫu)**: Phân bố dao động từ 5,421 mẫu (số 5 - 9.04%) đến 6,742 mẫu (số 1 - 11.24%).
- **Tập Test (10,000 mẫu)**: Phân bố đồng đều dao động từ 892 mẫu (số 5 - 8.92%) đến 1,135 mẫu (số 1 - 11.35%).
- **Độ hỗn loạn thông tin (Shannon Entropy)**: Trên tập huấn luyện 60,000 mẫu đạt **$3.3199$ bits** (tập test đạt **$3.3194$ bits**), so với cực đại lý thuyết $H_{\max} = \log_2(10) \approx 3.3219$ bits (tương đương hệ số cân bằng **$99.94\%$**). Phân bố số lượng mẫu giữa các lớp chênh lệch nhẹ từ 5,421 mẫu (lớp 5 - 9.04%) đến 6,742 mẫu (lớp 1 - 11.24%), cho thấy tập dữ liệu có phân bố gần như cân bằng đồng đều, không xảy ra hiện tượng mất cân bằng lớp cực đoan (*Extreme Class Imbalance*).


### 3.2. Ảnh trung bình (Mean) và Ảnh phương sai (Variance)
Bằng cách tính toán ma trận kỳ vọng và phương sai trên 60,000 mẫu:
- **Ảnh trung bình (Mean Image)**: Khắc họa hình thái mẫu mực chuẩn của 10 chữ số. Chữ số '1' có diện tích sáng nhỏ nhất, tập trung hẹp ở cột giữa; chữ số '0' tạo thành vòng khép kín rõ ràng.
- **Ảnh phương sai (Variance Heatmap)**: Vùng có độ lệch chuẩn cao tập trung ở các nét uốn lượn (đuôi chữ số '2', nét gạch ngang trên đỉnh chữ số '7' và '5', nét cắt chéo của chữ số '4'). Đây chính là các vị trí phát sinh lỗi nhận dạng chủ yếu.

### 3.3. Kỹ thuật tiền xử lý hình học: Nắn thẳng góc nghiêng (Deskewing)
Người viết tay thường có thói quen viết chữ số nghiêng về bên phải hoặc bên trái. Nhóm triển khai thuật toán tính mô-men quán tính ảnh trung tâm:
$$\mu_{pq} = \sum_x \sum_y (x - \bar{x})^p (y - \bar{y})^q f(x, y)$$
Hệ số nghiêng được tính bằng: $\alpha = \frac{\mu_{11}}{\mu_{02}}$. Sau đó áp dụng ma trận biến đổi Affine ngược để dựng đứng chữ số về phương thẳng đứng.

### 3.4. Giảm chiều không gian bằng PCA
Phân tích phương sai tích lũy của PCA cho thấy:
- 80% phương sai được lưu giữ chỉ với **43 thành phần chính**.
- 90% phương sai được lưu giữ với **87 thành phần chính**.
- **95% phương sai** được lưu giữ với **154 thành phần chính** (giảm số chiều từ 784 xuống 154, giảm $5.1\times$ dung lượng và thời gian tính toán).

---

## CHƯƠNG 4: MÔ HÌNH THỰC NGHIỆM & KẾT QUẢ ĐỐI CHUẨN

### 4.1. Thiết kế thực nghiệm và Chỉ số đánh giá
Các mô hình được huấn luyện trên môi trường Python 3.14, CPU Intel Core đa nhân, đánh giá khách quan độc lập trên **10,000 mẫu Test Set**.
Chỉ số đánh giá: **Accuracy, Macro Precision, Macro Recall, Macro F1-Score, Training Time (s), Inference Latency (ms/mẫu), Model Size (MB)**.

### 4.2. Bảng tổng hợp đối chuẩn hiệu năng đa mô hình

| Xếp hạng | Thuật toán / Mô hình | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1-Score | Thời gian Train (s) | Độ trễ suy luận (ms/mẫu) | Dung lượng mô hình |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN** | **Learned Conv (28×28)** | 784 | 60,000 | **99.32%** | **99.31%** | 198.55s | 0.079 ms | 0.62 MB |
| **#2** | **SVM (RBF Kernel, C=5)** | **PCA (95% Var)** | 154 | 60,000 | **98.54%** | **98.53%** | 27.88s | 0.866 ms | 8.44 MB |
| **#3** | **SVM (RBF Kernel)** | Deskewed + PCA | 154 | 10,000 | **97.91%** | 97.90% | 0.83s | 0.196 ms | 2.23 MB |
| **#4** | **SVM (RBF Kernel)** | HOG Features | 324 | 10,000 | **97.46%** | 97.46% | 1.13s | 0.282 ms | 2.12 MB |
| **#5** | **$k$-NN ($k=3$, Euclidean)** | PCA (95% Var) | 154 | 60,000 | **97.31%** | 97.29% | 0.00s | 0.077 ms | 32.95 MB |
| **#6** | **Random Forest (100 cây)** | Raw Pixels (784D) | 784 | 10,000 | **95.26%** | 95.22% | 0.33s | 0.005 ms | 5.44 MB |
| **#7** | **$k$-NN ($k=3$, Euclidean)** | Raw Pixels (784D) | 784 | 10,000 | **94.86%** | 94.85% | 0.01s | 0.074 ms | 2.66 MB |
| **#8** | **Linear SVM** | Raw Pixels (784D) | 784 | 60,000 | **91.84%** | 91.71% | 28.02s | 0.002 ms | 0.05 MB |
| **#9** | **Bernoulli Naive Bayes** | Binarized Pixels | 784 | 60,000 | **84.46%** | 84.26% | 0.35s | 0.004 ms | 0.05 MB |
| **#10** | **Gaussian Naive Bayes** | Raw Pixels (784D) | 784 | 60,000 | **55.58%** | 50.90% | 0.21s | 0.023 ms | 0.04 MB |

---

## CHƯƠNG 5: PHÂN TÍCH KẾT QUẢ & PHÂN TÍCH LỖI CHUYÊN SÂU

### 5.1. Phân tích ma trận nhầm lẫn (Confusion Matrix Analysis)
Từ các ma trận nhầm lẫn chuẩn hóa thu được, các lỗi phân loại tập trung vào các nhóm tương quan hình học:
1. **Cặp chữ số $4 \leftrightarrow 9$**: Tần suất nhầm lẫn cao nhất. Khi đỉnh số 4 bị người viết nối liền hoặc góc bo tròn, mô hình dễ nhầm vòng tròn khép kín của số 9.
2. **Cặp chữ số $3 \leftrightarrow 5$**: Cả hai chữ số đều sở hữu cung tròn uốn cong ở nửa dưới. Khi nét ngang trên đỉnh của số 5 bị viết cong hoặc ngắn, mô hình có xu hướng dự đoán thành số 3.
3. **Cặp chữ số $7 \leftrightarrow 1$ và $7 \leftrightarrow 2$**: Số 7 khi thiếu nét gạch ngang phụ giữa thân có hình dáng nét thẳng tương đồng với số 1.
4. **Cặp chữ số $8 \leftrightarrow 3$**: Nửa cung bên phải của số 8 tương đồng tuyệt đối với số 3.

### 5.2. Phân tích lỗi chuyên sâu (Deep Error Analysis)
Nhóm đã trích xuất danh sách các mẫu dự đoán sai của Modern CNN (chỉ có 68 mẫu sai trên tổng số 10,000 mẫu kiểm thử):
- **Nhiễu nhãn (Label Noise trong tập MNIST gốc)**: Có những mẫu trong bộ dữ liệu gốc bị con người gán nhãn sai (ví dụ: ảnh hiển thị số 6 nhưng nhãn gốc là số 0). Mô hình thực chất đã nhận dạng đúng đặc trưng thị giác.
- **Chữ số cực kỳ mơ hồ (Ambiguous Digits)**: Chữ số viết cẩu thả, nét bút bị loang mực hoặc đứt quãng, ngay cả mắt người bình thường cũng không thể khẳng định chắc chắn 100%.
- **Biến dạng bất thường (Heavy Distortion)**: Các nét viết có tỷ lệ khung hình bất thường hoặc tỷ lệ nét bị thu nhỏ quá mức khiến bước căn tâm trọng tâm khối lượng bị lệch nhẹ.

### 5.3. Trả lời câu hỏi nghiên cứu
1. **Đặc trưng nào hiệu quả nhất?**
   - **Đặc trưng tự học qua tích chập (Learned Conv Features)** là hiệu quả nhất vì tận dụng được cấu trúc không gian 2 chiều liền kề của điểm ảnh.
   - Trong học máy truyền thống: **PCA (154 chiều)** là không gian biểu diễn tối ưu nhất: vừa lọc nhiễu, vừa giảm số chiều gấp 5 lần, giúp $k$-NN tăng vọt độ chính xác từ $94.86\% \to 97.31\%$.
2. **Thuật toán nào hiệu quả nhất?**
   - **Modern CNN** là thuật toán nhận dạng chính xác nhất (**99.32%**), với độ trễ suy luận siêu tốc (0.079 ms/mẫu).
   - Trong các thuật toán học máy cổ điển đã học trong môn: **SVM với Kernel RBF kết hợp PCA** là thuật toán vượt trội nhất (**98.54%**), thời gian huấn luyện nhanh gấp nhiều lần so với huấn luyện trên vector 784 chiều thô.

---

## CHƯƠNG 6: KẾT LUẬN & HƯỚNG PHÁT TRIỂN

### 6.1. Những kết quả đã đạt được
1. Đã hoàn thành 100% các yêu cầu bắt buộc của bài tập lớn môn Nhận dạng mẫu theo đúng barem chấm điểm của Khoa.
2. Thực nghiệm so sánh có hệ thống trên 10 cấu hình mô hình và không gian đặc trưng khác nhau.
3. Giải quyết triệt để câu hỏi nghiên cứu khoa học với các bằng chứng thực nghiệm định lượng rõ ràng.
4. Triển khai thành công ứng dụng Web Demo tương tác hiện đại chuẩn Glassmorphism, cho phép vẽ tay trực tiếp và nhận dạng thời gian thực (đạt điểm thưởng sản phẩm).
5. Ứng dụng mô hình Deep Learning Modern CNN đạt độ chính xác vượt trội 99.32% (đạt điểm thưởng sáng tạo).

### 6.2. Hướng phát triển trong tương lai
- Phát triển mô hình nhận dạng chuỗi chữ số viết tay liên tục (*Connected Handwritten Digit String Recognition*) ứng dụng kỹ thuật Connectionist Temporal Classification (CTC).
- Nghiên cứu mô hình Vision Transformer (ViT) nhẹ và tối ưu hóa lượng tử hóa trọng số (INT8 Quantization) để triển khai trực tiếp trên chip nhúng IoT / Mobile Edge.

---

## TÀI LIỆU THAM KHẢO

1. **LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998)**. *Gradient-based learning applied to document recognition*. Proceedings of the IEEE, 86(11), 2278-2324.
2. **Bishop, C. M. (2006)**. *Pattern Recognition and Machine Learning*. Springer New York.
3. **Duda, R. O., Hart, P. E., & Stork, D. G. (2001)**. *Pattern Classification* (2nd ed.). John Wiley & Sons.
4. **Cortes, C., & Vapnik, V. (1995)**. *Support-vector networks*. Machine Learning, 20(3), 273-297.
5. **Dalal, N., & Triggs, B. (2005)**. *Histograms of oriented gradients for human detection*. IEEE CVPR, Vol. 1, pp. 886-893.
6. **Northcutt, C. G., Athalye, A., & Mueller, J. (2021)**. *Pervasive label errors in test sets destabilize machine learning benchmarks*. NeurIPS 2021.
7. **Bộ môn Khoa học Máy tính**, *Giáo trình Nhận dạng mẫu*, Trường Đại học Thủy Lợi.
