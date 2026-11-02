BỘ NÔNG NGHIỆP VÀ PHÁT TRIỂN NÔNG THÔN
PHÂN HIỆU TRƯỜNG ĐẠI HỌC THỦY LỢI
KHOA CÔNG NGHỆ THÔNG TIN

*****

BÁO CÁO BÀI TẬP LỚN CUỐI KỲ
HỌC PHẦN: NHẬN DẠNG MẪU (PATTERN RECOGNITION)

ĐỀ TÀI 1: NGHIÊN CỨU, THỰC NGHIỆM VÀ TRIỂN KHAI
HỆ THỐNG NHẬN DẠNG CHỮ SỐ VIẾT TAY TRÊN BỘ DỮ LIỆU MNIST

Giảng viên hướng dẫn: Bộ môn Khoa học Máy tính
Lớp học phần: Nhận dạng mẫu — S26-65TTNT
Nhóm sinh viên thực hiện: Nhóm 03
Thành viên nhóm:
  1. Đoàn Anh Vũ — MSSV: 2351267280
  2. Nguyễn Hồng Nguyên — MSSV: 2351267273

Năm 2026

# GIỚI THIỆU BÁO CÁO VÀ LỜI CẢM ƠN

Báo cáo trình bày chi tiết cơ sở lý thuyết, quy trình tiền xử lý, trích xuất đặc trưng, huấn luyện các thuật toán học máy kinh điển kết hợp mô hình học sâu mạng tích chập hiện đại (Modern CNN), và xây dựng ứng dụng web tương tác thời gian thực nhận dạng chữ số viết tay trên bộ dữ liệu chuẩn MNIST (70.000 ảnh).

Toàn bộ các bảng đánh giá thực nghiệm trong báo cáo được trích xuất trực tiếp từ các mô hình đã huấn luyện hoàn chỉnh, đối chuẩn khách quan 100% trên tập kiểm thử độc lập gồm 10.000 ảnh test của MNIST.

Nhóm 03 xin chân thành cảm ơn các thầy cô giảng viên Bộ môn Khoa học Máy tính — Khoa Công nghệ Thông tin, Phân hiệu Trường Đại học Thủy Lợi đã tận tình truyền đạt kiến thức nền tảng vững chắc về lý thuyết nhận dạng mẫu, trích xuất không gian đặc trưng và đánh giá mô hình học máy, làm kim chỉ nam giúp nhóm hoàn thành xuất sắc đề tài này.

## TÓM TẮT BÁO CÁO

Đề tài nghiên cứu toàn diện bài toán phân loại chữ số viết tay đơn lẻ từ 0 đến 9 trên tập dữ liệu chuẩn MNIST. Quy trình thực nghiệm áp dụng quy chuẩn phân chia khoa học: **50.000 mẫu huấn luyện (Train)**, **10.000 mẫu kiểm chứng (Validation)** để tinh chỉnh siêu tham số và dừng sớm (Early Stopping), cùng **10.000 mẫu kiểm thử độc lập (Test)** để đối chuẩn.

Nghiên cứu tập trung khảo sát 5 thuật toán học máy đại diện kết hợp các kỹ thuật xử lý hình thái học:
1. **Mạng nơ-ron tích chập hiện đại (Modern CNN)** với 3 khối Convolutional và cơ chế Early Stopping tại Epoch 17 (Validation Loss cực tiểu 0.0249) đạt hiệu năng xuất sắc nhất: **99.42% Test Accuracy**, chỉ mắc **58 lỗi trên 10.000 ảnh test**, độ trễ suy luận 8.85 ms.
2. **Support Vector Machine (SVM nhân RBF)** kết hợp quy trình tiền xử lý nắn thẳng góc nghiêng (**Deskewing**) và giảm chiều dữ liệu (**PCA 95% phương sai — 113 chiều**) đạt vị trí á quân với **98.79% Test Accuracy** (121 lỗi), vượt trội hoàn toàn so với mô hình huấn luyện trên điểm ảnh thô.
3. **k-Nearest Neighbors (k-NN, k=3, khoảng cách nghịch đảo)** trên không gian đặc trưng Deskew + PCA (113 chiều) đạt **98.06% Test Accuracy** (194 lỗi).
4. **Random Forest (150 cây quyết định)** trên 784 điểm ảnh thô đạt **96.99% Test Accuracy** (301 lỗi).
5. **Bernoulli Naive Bayes (ngưỡng nhị phân 0.2)** đạt **84.46% Test Accuracy** (1.554 lỗi) với tốc độ suy luận nhanh nhất (1.66 ms).

Toàn bộ các mô hình và bộ biến đổi đã được tích hợp trọn vẹn vào ứng dụng **Web tương tác thời gian thực** (FastAPI + HTML5 Canvas), áp dụng thuật toán căn tâm khối lượng quang học (Center of Mass) đưa nét vẽ về khung chuẩn 28x28 NIST, đồng thời được nghiệm thu nghiêm ngặt bởi bộ kiểm thử tự động **28/28 Unit Tests Passed (100%)**.

## MỤC LỤC BÁO CÁO

CHƯƠNG 1  GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU
CHƯƠNG 2  CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC
CHƯƠNG 3  DỮ LIỆU MNIST VÀ QUY CHUẨN TIỀN XỬ LÝ
CHƯƠNG 4  THIẾT KẾ THỰC NGHIỆM VÀ ĐỐI CHUẨN MÔ HÌNH
CHƯƠNG 5  KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH LỖI
CHƯƠNG 6  TRIỂN KHAI WEB DEMO VÀ KIỂM THỬ HỆ THỐNG
CHƯƠNG 7  KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
TÀI LIỆU THAM KHẢO

---

# CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU

## 1.1. Bối cảnh thực tế và ý nghĩa bài toán
Nhận dạng chữ số viết tay (*Handwritten Digit Recognition*) là bài toán kinh điển đặt nền móng cho ngành **Nhận dạng mẫu (Pattern Recognition)** và **Thị giác máy tính (Computer Vision)**. Trong thời đại chuyển đổi số, nhận dạng tự động ký tự và chữ số đóng vai trò then chốt:
- **Tự động hóa bưu chính:** Tự động đọc mã bưu chính (Zip Codes) trên phong bì thư nhằm phân luồng bưu kiện tốc độ cao.
- **Ngành tài chính - ngân hàng:** Tự động số hóa số tiền viết tay, số tài khoản trên séc ngân hàng và chứng từ giao dịch.
- **Quản lý hành chính công và giáo dục:** Số hóa hồ sơ bệnh án, chấm thi trắc nghiệm, nhận diện số báo danh và điểm số viết tay.

## 1.2. Định nghĩa toán học bài toán nhận dạng chữ số
Bài toán được mô hình hóa dưới dạng phân lớp đa lớp có giám sát (Supervised Multi-class Classification):
- Không gian đầu vào: Ảnh xám kích thước $28 \times 28$ điểm ảnh, biểu diễn bằng véc-tơ $\mathbf{x} \in [0.0, 1.0]^{784}$ hoặc tensor ảnh $\mathbf{X} \in \mathbb{R}^{1 \times 28 \times 28}$.
- Không gian nhãn đầu ra: Tập nhãn rời rạc gồm 10 lớp chữ số: $\mathcal{Y} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$.
- Mục tiêu: Tìm hàm ánh xạ quyết định $f: \mathcal{X} \to \mathcal{Y}$ cực tiểu hóa rủi ro kỳ vọng (Expected Risk) dựa trên hàm tổn thất $0-1$:
$$R(f) = \mathbb{E}_{(\mathbf{x}, y) \sim \mathcal{D}} [\mathbb{I}(f(\mathbf{x}) \neq y)]$$

## 1.3. Thách thức kỹ thuật của bài toán
1. **Biến thiên nội lớp (Intra-class Variability):** Cùng một chữ số nhưng phong cách viết tay của mỗi người rất khác nhau về độ nghiêng nét, độ đậm nhạt, tỷ lệ dài/rộng và nét móc.
2. **Tương đồng liên lớp (Inter-class Similarity):** Một số cặp chữ số có cấu trúc hình học rất gần nhau khi viết ẩu: cặp $4 \leftrightarrow 9$ (khi số 4 bị khép đỉnh), cặp $3 \leftrightarrow 5$ (khi nét gạch trên của số 5 bị cong tròn), cặp $7 \leftrightarrow 1$ hoặc $8 \leftrightarrow 0$.
3. **Lời nguyền số chiều (Curse of Dimensionality):** Không gian điểm ảnh 784 chiều chứa nhiều vùng biên đen không mang thông tin phân lớp, dễ dẫn đến hiện tượng quá khớp (Overfitting) với các mô hình tham số nếu không được giảm chiều hiệu quả.

## 1.4. Mục tiêu nghiên cứu và các câu hỏi nghiên cứu (RQs)
- **Câu hỏi nghiên cứu 1 (RQ1):** Kỹ thuật nắn thẳng góc nghiêng (Deskewing) kết hợp phân tích thành phần chính (PCA) cải thiện độ chính xác phân loại của các thuật toán ML cổ điển (SVM, k-NN) như thế nào?
- **Câu hỏi nghiên cứu 2 (RQ2):** So sánh hiệu năng toàn diện giữa các trường phái học máy (Bayes, Khoảng cách láng giềng, Cây quyết định tập hợp, Siêu phẳng lề cực đại) trên cùng tập dữ liệu chuẩn?
- **Câu hỏi nghiên cứu 3 (RQ3):** Mạng nơ-ron tích chập hiện đại (Modern CNN) với cơ chế Early Stopping mang lại ưu thế vượt trội ra sao so với các mô hình học máy truyền thống về độ chính xác và độ trễ suy luận?

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC

## 2.1. Không gian biểu diễn và trích xuất đặc trưng

### 2.1.1. Kỹ thuật nắn thẳng nét nghiêng (Deskewing bằng Image Moments)
Để loại bỏ sự sai lệch do người viết thuận tay trái hoặc viết nghiêng, thuật toán tính toán mô-men trung tâm bậc 2 của ảnh:
$$\mu_{pq} = \sum_{x} \sum_{y} (x - \bar{x})^p (y - \bar{y})^q I(x, y)$$
Hệ số xiên (Skew coefficient) được xác định bởi tỷ số: $\alpha = \frac{\mu_{11}}{\mu_{02}}$. Phép biến đổi Affine sau đó được áp dụng để tịnh tiến các điểm ảnh đưa chữ số về phương thẳng đứng hoàn hảo:
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 1 & -\alpha \\ 0 & 1 \end{bmatrix} \begin{bmatrix} x - \bar{x} \\ y - \bar{y} \end{bmatrix} + \begin{bmatrix} \bar{x} \\ \bar{y} \end{bmatrix}$$

### 2.1.2. Phân tích thành phần chính (Principal Component Analysis - PCA)
PCA tìm kiếm ma trận chiếu trực giao $\mathbf{W} \in \mathbb{R}^{784 \times d}$ sang không gian $d$ chiều sao cho bảo toàn tỷ lệ phương sai tích lũy tối thiểu $95\%$:
$$\text{Tỷ lệ phương sai} = \frac{\sum_{i=1}^d \lambda_i}{\sum_{j=1}^{784} \lambda_j} \ge 0.95$$
Trên tập 50.000 mẫu ảnh đã nắn thẳng Deskewing, thuật toán xác định chính xác **$d = 113$ thành phần chính**, giảm số chiều từ 784 xuống 113 (giảm $6.9$ lần chiều dữ liệu) mà vẫn giữ trọn vẹn thông tin hình thái quan trọng nhất.

## 2.2. Các thuật toán học máy kinh điển

### 2.2.1. Support Vector Machine (SVM với nhân RBF)
SVM tìm siêu phẳng phân cách tối ưu cực đại hóa khoảng cách lề hình học. Với các bài toán phi tuyến tính như chữ số, hàm nhân Radial Basis Function (RBF) được áp dụng:
$$K(\mathbf{x}, \mathbf{z}) = \exp(-\gamma \|\mathbf{x} - \mathbf{z}\|^2), \quad \gamma = \frac{1}{d \cdot \text{Var}(X)}$$
Mô hình sử dụng chiến lược One-vs-Rest (OvR) và tham số điều hòa $C = 5.0$.

### 2.2.2. Thuật toán k-Láng giềng gần nhất (k-NN)
Phân loại dựa trên khoảng cách Euclidean trong không gian $113$ chiều Deskew+PCA. Nhóm áp dụng $k=3$ kết hợp trọng số khoảng cách nghịch đảo ($w_i = \frac{1}{d(\mathbf{x}, \mathbf{x}_i)}$), cho phép láng giềng gần hơn có tiếng nói quyết định mạnh mẽ hơn.

### 2.2.3. Rừng ngẫu nhiên (Random Forest)
Mô hình tập hợp (Ensemble Learning) phương pháp Bagging gồm **150 cây quyết định (Decision Trees)**. Mỗi cây được huấn luyện trên một tập mẫu con lấy mẫu có hoàn lại (Bootstrap sample) và tại mỗi nút chỉ xét tập con ngẫu nhiên $\sqrt{784} = 28$ đặc trưng. Kết quả phân loại là biểu quyết số đông (Majority Voting).

### 2.2.4. Phân lớp Naive Bayes (Bernoulli Naive Bayes)
Áp dụng định lý xác suất Bayes với giả định độc lập có điều kiện giữa các thuộc tính. Dữ liệu được nhị phân hóa với ngưỡng $\tau = 0.2$:
$$P(Y=k | \mathbf{x}) \propto P(Y=k) \prod_{j=1}^{784} p_{kj}^{x_j} (1 - p_{kj})^{(1 - x_j)}$$

## 2.3. Mạng nơ-ron tích chập hiện đại (Modern CNN)
Kiến trúc Modern CNN được thiết kế chuyên biệt cho ảnh MNIST với 3 khối tích chập chuẩn hóa:
- **Khối Conv 1:** $\text{Conv2D}(1 \to 32, 3\times 3) \to \text{BatchNorm} \to \text{ReLU} \to \text{Conv2D}(32 \to 32, 3\times 3) \to \text{MaxPool}(2\times 2) \to \text{Dropout}(0.25)$
- **Khối Conv 2:** $\text{Conv2D}(32 \to 64, 3\times 3) \to \text{BatchNorm} \to \text{ReLU} \to \text{Conv2D}(64 \to 64, 3\times 3) \to \text{MaxPool}(2\times 2) \to \text{Dropout}(0.25)$
- **Khối Conv 3:** $\text{Conv2D}(64 \to 128, 3\times 3) \to \text{BatchNorm} \to \text{ReLU} \to \text{Flatten} \to \text{Dropout}(0.4)$
- **Khối phân loại (Dense):** $\text{Linear}(128 \to 128) \to \text{ReLU} \to \text{Dropout}(0.3) \to \text{Linear}(128 \to 10)$
Tổng số tham số học được là **160.074 tham số**. Mô hình tối ưu hóa bằng Adam optimizer với learning rate khởi tạo $0.001$, tự động giảm learning rate (ReduceLROnPlateau) và dừng sớm (Early Stopping) sau 5 epoch không giảm Validation Loss.

---

# CHƯƠNG 3: DỮ LIỆU MNIST VÀ QUY CHUẨN TIỀN XỬ LÝ

## 3.1. Đặc tính bộ dữ liệu chuẩn MNIST
Bộ dữ liệu gồm 70.000 ảnh chữ số viết tay kích thước $28 \times 28$ do Viện Tiêu chuẩn và Công nghệ Quốc gia Hoa Kỳ (NIST) chuẩn hóa. Phân chia thực nghiệm:
- **Tập Train (Huấn luyện):** 50.000 mẫu
- **Tập Validation (Kiểm chứng):** 10.000 mẫu
- **Tập Test (Kiểm thử độc lập):** 10.000 mẫu

## 3.2. Quy trình tiền xử lý dữ liệu
1. **Chuẩn hóa biên độ pixel:** Ánh xạ từ $[0, 255]$ sang $[0.0, 1.0]$.
2. **Nắn thẳng Deskewing:** Áp dụng biến đổi Affine dựa trên mô-men bậc 2 cho toàn bộ tập train, val và test.
3. **Phân tích PCA:** Huấn luyện bộ biến đổi PCA trên 50.000 ảnh train đã nắn thẳng, cố định không gian 113 chiều và áp dụng chiếu nhất quán sang val và test.

---

# CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ ĐỐI CHUẨN MÔ HÌNH

## 4.1. Thiết kế thực nghiệm kiểm chứng khách quan
Toàn bộ 5 mô hình được huấn luyện trên cùng tập Train 50.000 mẫu (hoặc kết hợp 10.000 mẫu Validation cho CNN) và được đánh giá trên cùng tập Test 10.000 mẫu độc lập. Không có hiện tượng rò rỉ dữ liệu (Zero Data Leakage).

## 4.2. Quá trình huấn luyện Modern CNN với Early Stopping
Quá trình huấn luyện diễn ra qua 17 epoch:
- Epoch 1: Train Loss 0.4079, Val Loss 0.0818, Val Acc 97.43%
- Epoch 5: Train Loss 0.0401, Val Loss 0.0385, Val Acc 98.79%
- Epoch 10: Train Loss 0.0210, Val Loss 0.0294, Val Acc 99.11%
- Epoch 14: Train Loss 0.0076, Val Loss 0.0249, Val Acc 99.23%
- Epoch 17: Train Loss 0.0051, Val Loss 0.0249 (cực tiểu), Val Acc **99.32%**
Mô hình đạt điểm dừng sớm tối ưu và tự động lưu checkpoint trọng số tốt nhất tại `saved_models/CNN.pt`.

---

# CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH LỖI

## 5.1. Bảng đối chuẩn kết quả toàn diện trên 10.000 ảnh MNIST Test Set

| Xếp hạng | Mô hình | Không gian đặc trưng | Tập huấn luyện | Test Accuracy | Macro F1 | Số ảnh sai / 10k | Độ trễ suy luận |
|:---:|---|---|---|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN** | Learned Conv (28×28) | 50k train / 10k val | **99.42%** | **99.42%** | **58** | 8.85 ms |
| **#2** | **SVM** | Deskewed + PCA 95% (113D) | 50.000 train | **98.79%** | **98.78%** | **121** | 20.03 ms |
| **#3** | **k-NN** | Deskewed + PCA 95% (113D) | 50.000 train | **98.06%** | **98.05%** | **194** | 63.38 ms |
| **#4** | **Random Forest** | Raw Pixels (784D) | 50.000 train | **96.99%** | **96.97%** | **301** | 56.72 ms |
| **#5** | **Bernoulli Naive Bayes** | Binarized Pixels (784D, bin=0.2) | 50.000 train | **84.46%** | **84.27%** | **1.554** | 1.66 ms |

## 5.2. Hiệu năng chi tiết trên từng lớp chữ số của Modern CNN (99.42%)

| Lớp chữ số | Số mẫu test | Precision (%) | Recall (%) | F1-Score (%) | Số ảnh đoán sai |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 980 | 99.49% | 99.80% | 99.64% | 2 |
| **1** | 1.135 | 99.74% | 99.56% | 99.65% | 5 |
| **2** | 1.032 | 99.42% | 99.42% | 99.42% | 6 |
| **3** | 1.010 | 99.41% | 99.70% | 99.55% | 3 |
| **4** | 982 | 99.19% | 99.59% | 99.39% | 4 |
| **5** | 892 | 99.44% | 98.99% | 99.21% | 9 |
| **6** | 958 | 99.38% | 99.48% | 99.43% | 5 |
| **7** | 1.028 | 99.42% | 99.42% | 99.42% | 6 |
| **8** | 974 | 99.38% | 99.08% | 99.23% | 9 |
| **9** | 1.009 | 99.31% | 99.11% | 99.21% | 9 |
| **Trung bình (Macro Avg)** | **10.000** | **99.42%** | **99.41%** | **99.42%** | **Tổng: 58** |

## 5.3. Phân tích chuyên sâu 58 mẫu dự đoán sai của Modern CNN
Trên toàn bộ 10.000 ảnh kiểm thử, mô hình chỉ đoán sai đúng 58 mẫu (tỷ lệ lỗi cực thấp $0.58\%$). Danh sách chi tiết được lưu trữ tại `reports/tables/cnn_error_samples.csv` và trực quan hóa tại `reports/figures/08_cnn_error_samples.png`.
- **Nhóm nhầm lẫn do tương đồng nét cong (3 và 5):** Chữ số 5 viết ẩu nét ngang trên bị cụt, nét cong dưới uốn sâu khiến mạng nhận diện nhầm thành số 3.
- **Nhóm nhầm lẫn do khép vòng (4 và 9):** Chữ số 4 viết nét gạch chéo vô tình chạm vào nét thẳng đứng tạo thành hình tam giác khép kín giống số 9.
- **Nhóm nét viết dị biệt (Outliers):** Một số ảnh nét chữ bị mờ, đứt đoạn hoặc quá dày khiến ngay cả mắt người bình thường cũng rất khó phân định chuẩn xác.

---

# CHƯƠNG 6: TRIỂN KHAI WEB DEMO VÀ KIỂM THỬ HỆ THỐNG

## 6.1. Kiến trúc hệ thống Web tương tác
Hệ thống demo được xây dựng theo kiến trúc hiện đại:
- **Backend:** FastAPI (Python), tải sẵn toàn bộ 5 mô hình vào bộ nhớ RAM, cung cấp API dự đoán độ trễ mili-giây (`/api/predict`) và API danh mục mô hình (`/api/models`).
- **Frontend:** Thiết kế theo phong cách Soft Glassmorphism tinh tế, bảng vẽ HTML5 Canvas mượt mà, hỗ trợ cả chuột máy tính lẫn bút cảm ứng.
- **Footer:** Chân trang tinh gọn chuẩn mực hiển thị thông tin duy nhất: **"Phân hiệu Đại học Thủy Lợi"**.

## 6.2. Pipeline tiền xử lý quang học Center of Mass thời gian thực
Để nét vẽ tự do từ người dùng có tỷ lệ tương đồng cao nhất với dữ liệu chuẩn MNIST, hệ thống áp dụng pipeline quang học 5 bước:
1. Cắt hộp bao (`cv2.boundingRect`) phát hiện vùng có nét chữ.
2. Thu phóng bảo toàn tỷ lệ khung hình vào ô vuông $20 \times 20$ điểm ảnh.
3. Tính toán trọng tâm khối lượng quang học (Center of Mass): $c_x = \frac{\sum x I(x, y)}{\sum I(x, y)}$, $c_y = \frac{\sum y I(x, y)}{\sum I(x, y)}$.
4. Áp dụng phép tịnh tiến đưa trọng tâm $(c_x, c_y)$ về chính xác tâm $(14.0, 14.0)$ của khung chuẩn $28 \times 28$ NIST.
5. Chuẩn hóa dải giá trị $[0.0, 1.0]$ trước khi đưa vào mô hình suy luận.

## 6.3. Kiểm thử tự động hệ thống (28 Test Cases)
Hệ thống tích hợp bộ kiểm thử tự động toàn diện trong `tests/test_pipeline.py`. Toàn bộ 28 bài kiểm tra từ tính toàn vẹn dữ liệu, kiểm tra rò rỉ, kiến trúc Modern CNN 160.074 tham số đến các endpoint API đều đạt **100% PASS**.

---

# CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 7.1. Kết luận khoa học
1. **Vai trò của biểu diễn đặc trưng:** Kỹ thuật nắn thẳng góc nghiêng Deskewing kết hợp giảm chiều PCA (113 chiều) đã tạo ra bước đột phá cho các thuật toán học máy kinh điển, đưa SVM RBF đạt đến $98.79\%$ và k-NN đạt $98.06\%$.
2. **Ưu thế tuyệt đối của Deep Learning:** Modern CNN với khả năng trích xuất đặc trưng tích chập đa tầng kết hợp cơ chế dừng sớm Early Stopping trên tập Validation độc lập đã chứng minh sức mạnh vượt trội với độ chính xác đỉnh cao **99.42%** (chỉ sai 58/10.000 ảnh).
3. **Tính ứng dụng thực tiễn:** Hệ thống đã được đóng gói hoàn chỉnh thành giải pháp phần mềm hoàn chỉnh, sẵn sàng ứng dụng vào thực tế giảng dạy và số hóa tài liệu.

## 7.2. Hướng phát triển trong tương lai
- Nghiên cứu mở rộng sang nhận dạng chuỗi chữ số và văn bản viết tay liên tục ứng dụng mô hình CRNN (Convolutional Recurrent Neural Network) kết hợp CTC Loss.
- Tối ưu hóa mô hình bằng kỹ thuật Lượng tử hóa (Quantization INT8) và xuất sang ONNX Runtime để triển khai trên các thiết bị nhúng IoT và camera thông minh.

---

# TÀI LIỆU THAM KHẢO
1. LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. *Proceedings of the IEEE*, 86(11), 2278-2324.
2. Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273-297.
3. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.
4. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer Science+Business Media, LLC.
5. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
6. Paszke, A., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. *NeurIPS 2019*, 32.
7. Bộ môn Khoa học Máy tính — Khoa Công nghệ Thông tin. Giáo trình Nhận dạng mẫu. Phân hiệu Trường Đại học Thủy Lợi, 2026.
