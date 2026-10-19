# BÁO CÁO KHOA HỌC & KỸ THUẬT TOÀN DIỆN CHI TIẾT DỰ ÁN
## ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY TRÊN BỘ DỮ LIỆU MNIST
**HỌC PHẦN: NHẬN DẠNG MẪU (PATTERN RECOGNITION)**  
**TRƯỜNG ĐẠI HỌC THỦY LỢI — KHOA CÔNG NGHỆ THÔNG TIN — BỘ MÔN KHOA HỌC MÁY TÍNH**

> [!WARNING]
> **TÀI LIỆU LỊCH SỬ / BẢN THẢO CŨ (LEGACY DRAFT — NOT FOR SUBMISSION)**  
> Tài liệu Markdown này được soạn thảo trong các vòng phát triển ban đầu của dự án và chứa một số số liệu thử nghiệm sơ khai (ví dụ: số liệu CNN ban đầu 99.32% / 68 lỗi, Linear SVM C=1.0, Random Forest 100 cây).  
> **TÀI LIỆU CHÍNH THỨC DÙNG ĐỂ NỘP VÀ CHẤM ĐIỂM ĐÃ ĐƯỢC ĐỒNG BỘ 100% TẠI:**  
> - Báo cáo khoa học Word & PDF 28 trang: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf)  
> - Slide thuyết trình chính thức (12 slides): [`reports/Slide_Thuyet_Trinh_Nhom_03.pptx`](reports/Slide_Thuyet_Trinh_Nhom_03.pptx)  
> - Kết quả thực nghiệm kiểm chứng chính thức: [`results/verified_experiments.json`](results/verified_experiments.json) & [`EXPERIMENT_RESULTS.md`](EXPERIMENT_RESULTS.md)

---

<p align="center">
  <strong>NHÓM THỰC HIỆN: NHÓM 03</strong><br>
  <em>Hồ sơ nghiệm thu kỹ thuật và Báo cáo khoa học đã qua kiểm định đối chuẩn thực nghiệm</em><br>
  <em>Hà Nội — Năm 2026</em>
</p>

---

## MỤC LỤC TỔNG QUAN

- [CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN & DỮ LIỆU](#chương-1-giới-thiệu-bài-toán--dữ-liệu)
  - [1.1. Bối cảnh thực tiễn và Ý nghĩa đề tài](#11-bối-cảnh-thực-tiễn-và-ý-nghĩa-đề-tài)
  - [1.2. Xác định đối tượng và Không gian bài toán](#12-xác-định-đối-tượng-và-không-gian-bài-toán)
  - [1.3. Nguồn gốc dữ liệu chuẩn học thuật (MNIST)](#13-nguồn-gốc-dữ-liệu-chuẩn-học-thuật-mnist)
  - [1.4. Câu hỏi nghiên cứu trọng tâm](#14-câu-hỏi-nghiên-cứu-trọng-tâm)
- [CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & THUẬT TOÁN](#chương-2-cơ-sở-lý-thuyết--thuật-toán)
  - [2.1. Bộ phân lớp Bayes thơ ngây (Naive Bayes)](#21-bộ-phân-lớp-bayes-thơ-ngây-naive-bayes)
  - [2.2. Thuật toán $k$-Láng giềng gần nhất ($k$-NN)](#22-thuật-toán-k-láng-giềng-gần-nhất-k-nn)
  - [2.3. Máy vector hỗ trợ (Support Vector Machine - SVM)](#23-máy-vector-hỗ-trợ-support-vector-machine---svm)
  - [2.4. Rừng ngẫu nhiên (Random Forest)](#24-rừng-ngẫu-nhiên-random-forest)
  - [2.5. Mạng nơ-ron tích chập sâu (Modern CNN - Sáng tạo)](#25-mạng-nơ-ron-tích-chập-sâu-modern-cnn---sáng-tạo)
- [CHƯƠNG 3: KHAI PHÁ DỮ LIỆU (EDA) & KỸ THUẬT TIỀN XỬ LÝ](#chương-3-khai-phá-dữ-liệu-eda--kỹ-thuật-tiền-xử-lý)
  - [3.1. Phân tích thống kê & Độ cân bằng dữ liệu](#31-phân-tích-thống-kê--độ-cân-bằng-dữ-liệu)
  - [3.2. Ảnh trung bình (Mean) và Ảnh phương sai (Variance)](#32-ảnh-trung-bình-mean-và-ảnh-phương-sai-variance)
  - [3.3. Khám phá không gian tiềm ẩn qua PCA 2D và t-SNE 2D](#33-khám-phá-không-gian-tiềm-ẩn-qua-pca-2d-và-t-sne-2d)
  - [3.4. Kỹ thuật tiền xử lý hình học & Trích xuất đặc trưng](#34-kỹ-thuật-tiền-xử-lý-hình-học--trích-xuất-đặc-trưng)
  - [3.5. Quy trình phân chia dữ liệu & Chống rò rỉ (Leakage Prevention)](#35-quy-trình-phân-chia-dữ-liệu--chống-rò-rỉ-leakage-prevention)
- [CHƯƠNG 4: MÔ HÌNH THỰC NGHIỆM & KẾT QUẢ ĐỐI CHUẨN](#chương-4-mô-hình-thực-nghiệm--kết-quả-đối-chuẩn)
  - [4.1. Thiết kế thực nghiệm đối chứng kiểm soát](#41-thiết-kế-thực-nghiệm-đối-chứng-kiểm-soát)
  - [4.2. Bảng đối chuẩn có kiểm soát (Cùng 10,000 mẫu Train)](#42-bảng-đối-chuẩn-có-kiểm-soát-cùng-10000-mẫu-train)
  - [4.3. Bảng đối chuẩn mở rộng toàn phần (60,000 mẫu Train)](#43-bảng-đối-chuẩn-mở-rộng-toàn-phần-60000-mẫu-train)
  - [4.4. Đo lường hiệu năng tính toán & Tài nguyên](#44-đo-lường-hiệu-năng-tính-toán--tài-nguyên)
- [CHƯƠNG 5: PHÂN TÍCH KẾT QUẢ & PHÂN TÍCH LỖI CHUYÊN SÂU](#chương-5-phân-tích-kết-quả--phân-tích-lỗi-chuyên-sâu)
  - [5.1. Phân tích ma trận nhầm lẫn (Confusion Matrix)](#51-phân-tích-ma-trận-nhầm-lẫn-confusion-matrix)
  - [5.2. Phân tích lỗi chuyên sâu (Deep Error Analysis)](#52-phân-tích-lỗi-chuyên-sâu-deep-error-analysis)
  - [5.3. Trả lời thỏa đáng câu hỏi nghiên cứu khoa học](#53-trả-lời-thỏa-đáng-câu-hỏi-nghiên-cứu-khoa-học)
- [CHƯƠNG 6: ỨNG DỤNG WEB DEMO & KIỂM THỬ HỆ THỐNG](#chương-6-ứng-dụng-web-demo--kiểm-thử-hệ-thống)
  - [6.1. Kiến trúc ứng dụng Web Demo thời gian thực](#61-kiến-trúc-ứng-dụng-web-demo-thời-gian-thực)
  - [6.2. Pipeline căn tâm khối lượng quang học (Center of Mass)](#62-pipeline-căn-tâm-khối-lượng-quang-học-center-of-mass)
  - [6.3. Hệ thống kiểm thử tự động (Automated Test Suite)](#63-hệ-thống-kiểm-thử-tự-động-automated-test-suite)
- [CHƯƠNG 7: KẾT LUẬN & HƯỚNG PHÁT TRIỂN](#chương-7-kết-luận--hướng-phát-triển)
  - [7.1. Tổng kết các đóng góp chính của đề tài](#71-tổng-kết-các-đóng-góp-chính-của-đề-tài)
  - [7.2. Hạn chế và Hướng nghiên cứu tiếp theo](#72-hạn-chế-và-hướng-nghiên-cứu-tiếp-theo)
- [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)

---

## CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN & DỮ LIỆU

### 1.1. Bối cảnh thực tiễn và Ý nghĩa đề tài
Bài toán **Nhận dạng chữ số viết tay** (*Handwritten Digit Recognition*) là một trong những bài toán kinh điển, đặt nền tảng phương pháp luận cho ngành Nhận dạng mẫu (*Pattern Recognition*) và Thị giác máy tính (*Computer Vision*). Trong thực tế sản xuất và quản trị xã hội, việc tự động hóa quá trình đọc và nhận diện các con số viết tay mang lại giá trị to lớn:
- **Ngành bưu chính - chuyển phát**: Tự động hóa phân loại hàng chục triệu bưu kiện, thư từ mỗi ngày thông qua mã bưu chính (*ZIP Code*).
- **Hệ thống ngân hàng & tài chính**: Tự động đọc và đối soát chữ số tiền mặt, số tài khoản trên séc ngân hàng và chứng từ thanh toán.
- **Số hóa hồ sơ hành chính & Giáo dục**: Quét và chuyển đổi các tờ khai hành chính, mã số sinh viên, bài thi trắc nghiệm sang định dạng dữ liệu điện tử.

Thách thức trọng tâm của bài toán bao gồm:
1. **Biến thiên hình học cá nhân**: Độ nghiêng nét chữ (*skewness*), độ đậm nhạt, nét đứt, tỷ lệ khung hình thay đổi rất lớn tùy theo thói quen của từng người viết.
2. **Độ tương đồng thị giác cao**: Ranh giới phân chia mong manh giữa các cặp số dễ nhầm lẫn như $(4 \leftrightarrow 9)$, $(3 \leftrightarrow 5)$, $(7 \leftrightarrow 1)$, $(8 \leftrightarrow 3)$.
3. **Cân bằng giữa độ chính xác và tài nguyên**: Các giải thuật học sâu mang lại độ chính xác cao nhưng đòi hỏi phần cứng lớn; trong khi các ứng dụng biên (Edge IoT) yêu cầu độ trễ tính bằng mili-giây với kích thước mô hình siêu nhẹ.

### 1.2. Xác định đối tượng và Không gian bài toán
- **Đối tượng nhận dạng**: Các bức ảnh mức xám đơn kênh biểu diễn chữ số viết tay đơn lẻ.
- **Không gian nhãn lớp**: 10 lớp số tự nhiên riêng biệt:
  $$\mathcal{Y} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$$
- **Ý nghĩa đầu ra**: Hệ thống gán cho mỗi mẫu quan sát một nhãn lớp dự đoán $\hat{y} \in \mathcal{Y}$ kèm theo độ tin cậy hoặc phân bố xác suất $P(y = c | \mathbf{x})$.

### 1.3. Nguồn gốc dữ liệu chuẩn học thuật (MNIST)
Dự án sử dụng bộ dữ liệu chuẩn học thuật **MNIST** (*Modified National Institute of Standards and Technology*) do Yann LeCun, Corinna Cortes và Christopher Burges công bố:
- **Nguồn cấp chính thức**: [TensorFlow Datasets Catalog](https://www.tensorflow.org/datasets/catalog/mnist) và [Google Cloud Storage CVDF Mirror](https://storage.googleapis.com/cvdf-datasets/mnist/).
- **Quy mô tập dữ liệu**: $70,000$ mẫu ảnh mức xám đơn kênh kích thước $28 \times 28$ điểm ảnh.
- **Chuẩn hóa NIST sẵn có**: Mỗi chữ số gốc từ NIST được co dãn bảo toàn tỷ lệ khung hình vào vừa vặn khung $20 \times 20$, sau đó tịnh tiến trọng tâm khối lượng (*Center of Mass*) về chính giữa khung hình $28 \times 28$.
- **Phân chia chuẩn học thuật**:
  - **Tập huấn luyện (Training Set)**: $60,000$ mẫu (~85.71%).
  - **Tập kiểm thử (Test Set)**: $10,000$ mẫu (~14.29%) độc lập, không tham gia vào bất kỳ khâu tối ưu hay chọn siêu tham số nào.

### 1.4. Câu hỏi nghiên cứu trọng tâm
Đề tài bám sát câu hỏi định hướng chính thức của Bộ môn Khoa học Máy tính:
> **"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"**

Để trả lời thỏa đáng câu hỏi này, nhóm đã thiết kế một hệ thống thực nghiệm đối chứng đơn biến nghiêm ngặt:
- Khảo sát độc lập ảnh hưởng của **4 không gian đặc trưng**: Điểm ảnh thô (Raw Pixels 784D), Nắn thẳng góc nghiêng (Deskewing 784D), Giảm chiều giữ 95% phương sai (PCA 141D/154D), và Lược đồ hướng gradient (HOG 324D).
- Khảo sát độc lập ảnh hưởng của **5 họ thuật toán nhận dạng mẫu**: Bayes thơ ngây (Gaussian NB, Bernoulli NB), $k$-Láng giềng gần nhất ($k$-NN), Máy vector hỗ trợ (Linear SVM, RBF SVM), Rừng ngẫu nhiên (Random Forest), và Mạng nơ-ron tích chập (Modern CNN).

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & THUẬT TOÁN

### 2.1. Bộ phân lớp Bayes thơ ngây (Naive Bayes)
Dựa trên định lý xác suất Bayes kết hợp giả định "thơ ngây" rằng tất cả 784 thuộc tính điểm ảnh đều độc lập có điều kiện khi biết nhãn lớp $y = c$:
$$P(y = c | \mathbf{x}) = \frac{P(y = c) \prod_{j=1}^{D} P(x_j | y = c)}{P(\mathbf{x})}$$
- **Gaussian Naive Bayes (GNB)**: Giả định mật độ xác suất của từng điểm ảnh liên tục tuân theo phân phối chuẩn:
  $$P(x_j | y = c) = \frac{1}{\sqrt{2\pi \sigma_{c,j}^2}} \exp\left( -\frac{(x_j - \mu_{c,j})^2}{2\sigma_{c,j}^2} \right)$$
- **Bernoulli Naive Bayes (BNB)**: Nhị phân hóa điểm ảnh với ngưỡng $\theta = 0.2$ ($x_j \in \{0, 1\}$), tính xác suất pixel được kích hoạt $p_{c, j}$:
  $$P(x_j | y = c) = p_{c, j}^{x_j} (1 - p_{c, j})^{1 - x_j}$$

### 2.2. Thuật toán $k$-Láng giềng gần nhất ($k$-NN)
$k$-NN là phương pháp học dựa trên mẫu (*Instance-based learning*), không tham số:
- Khoảng cách giữa mẫu truy vấn $\mathbf{x}$ và mẫu huấn luyện $\mathbf{x}^{(i)}$ theo chuẩn Euclidean ($p=2$):
  $$d(\mathbf{x}, \mathbf{x}^{(i)}) = \sqrt{\sum_{j=1}^{D} (x_j - x_j^{(i)})^2}$$
- Gán nhãn theo biểu quyết gia quyền theo nghịch đảo khoảng cách $w_i = \frac{1}{d(\mathbf{x}, \mathbf{x}^{(i)}) + \epsilon}$:
  $$\hat{y} = \arg\max_{c \in \mathcal{Y}} \sum_{i \in \mathcal{N}_k(\mathbf{x})} w_i \cdot \mathbb{I}(y^{(i)} = c)$$

### 2.3. Máy vector hỗ trợ (Support Vector Machine - SVM)
Mục tiêu là tìm siêu phẳng quyết định tối ưu có lề phân cách (*margin*) cực đại:
$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \left( \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^{N} \xi_i \right) \quad \text{s.t.} \quad y^{(i)}(\mathbf{w}^T \phi(\mathbf{x}^{(i)}) + b) \ge 1 - \xi_i, \quad \xi_i \ge 0$$
- **Linear SVM**: Phân tách bằng siêu phẳng tuyến tính trong không gian 784D gốc.
- **RBF Kernel SVM**: Ánh xạ ngầm định qua hàm nhân cơ sở xuyên tâm để xử lý bài toán phi tuyến:
  $$K(\mathbf{x}, \mathbf{z}) = \exp\left( -\gamma \|\mathbf{x} - \mathbf{z}\|^2 \right)$$

### 2.4. Rừng ngẫu nhiên (Random Forest)
Phương pháp học kết hợp (*Ensemble Learning*) dựa trên cơ chế đóng bao (*Bagging*):
- Xây dựng tập hợp 100 cây quyết định độc lập.
- Tại mỗi nút rẽ nhánh, chọn ngẫu nhiên $m = \sqrt{D} \approx 28$ đặc trưng để tìm điểm phân chia tối ưu.
- Kết quả cuối cùng là biểu quyết đa số, giúp triệt tiêu phương sai và chống quá khớp hiệu quả.

### 2.5. Mạng nơ-ron tích chập sâu (Modern CNN - Sáng tạo)
Kiến trúc CNN bảo toàn quan hệ lân cận không gian 2 chiều của ảnh:
- **Tầng tích chập (Conv2D)**: Sử dụng các bộ lọc $3 \times 3$ trượt qua ảnh để tự động học các đặc trưng góc cạnh, đường cong và hình thái phức tạp.
- **Batch Normalization (BN)**: Chuẩn hóa phân phối kích hoạt giữa các tầng, tăng tốc hội tụ và ổn định gradient.
- **Max-Pooling ($2 \times 2$)**: Giảm nửa độ phân giải không gian, tăng vùng tiếp nhận và đem lại tính bất biến với các phép dịch chuyển nhỏ.
- **Dropout (0.4 & 0.2)**: Vô hiệu hóa ngẫu nhiên liên kết nơ-ron để chống phụ thuộc đồng thời.

---

## CHƯƠNG 3: KHAI PHÁ DỮ LIỆU (EDA) & KỸ THUẬT TIỀN XỬ LÝ

### 3.1. Phân tích thống kê & Độ cân bằng dữ liệu
Thực hiện tính toán trực tiếp từ mảng nhị phân gốc của MNIST:

| Chữ số | Tập Huấn luyện (Train) | Tỷ lệ (%) | Tập Kiểm thử (Test) | Tỷ lệ (%) | Tổng số mẫu | Tỷ lệ tổng (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 5,923 | 9.87% | 980 | 9.80% | 6,903 | 9.86% |
| **1** | 6,742 | 11.24% | 1,135 | 11.35% | 7,877 | 11.25% |
| **2** | 5,958 | 9.93% | 1,032 | 10.32% | 6,990 | 9.99% |
| **3** | 6,131 | 10.22% | 1,010 | 10.10% | 7,141 | 10.20% |
| **4** | 5,842 | 9.74% | 982 | 9.82% | 6,824 | 9.75% |
| **5** | 5,421 | 9.04% | 892 | 8.92% | 6,313 | 9.02% |
| **6** | 5,918 | 9.86% | 958 | 9.58% | 6,876 | 9.82% |
| **7** | 6,265 | 10.44% | 1,028 | 10.28% | 7,293 | 10.42% |
| **8** | 5,851 | 9.75% | 974 | 9.74% | 6,825 | 9.75% |
| **9** | 5,949 | 9.91% | 1,009 | 10.09% | 6,958 | 9.94% |
| **Tổng** | **60,000** | **100.00%** | **10,000** | **100.00%** | **70,000** | **100.00%** |

- **Độ hỗn loạn thông tin (Shannon Entropy) thực tế**:
  $$H_{\text{train}}(Y) = -\sum_{c=0}^{9} P(y=c) \log_2 P(y=c) = 3.3199 \text{ bits}$$
  $$H_{\text{test}}(Y) = 3.3194 \text{ bits}$$
- So với cực đại lý thuyết $H_{\max} = \log_2(10) \approx 3.3219 \text{ bits}$, tỷ lệ cân bằng chuẩn hóa đạt **$99.94\%$** trên tập Train và **$99.92\%$** trên tập Test.
- **Đánh giá**: Phân bố giữa 10 lớp dao động nhẹ từ 9.04% (lớp 5) đến 11.24% (lớp 1). Dữ liệu có tính chất cân bằng tự nhiên rất tốt, không xảy ra hiện tượng mất cân bằng lớp cực đoan (*Class Imbalance*), do đó chỉ số Accuracy kết hợp Macro F1-Score là thước đo chuẩn xác và khách quan.

### 3.2. Ảnh trung bình (Mean) và Ảnh phương sai (Variance)
- **Mean Images**: Thể hiện hình thái mẫu mực chuẩn của 10 chữ số. Chữ số '1' có diện tích phát sáng hẹp nhất ở trung tâm; chữ số '0' có vòng oval rỗng hoàn toàn ở giữa.
- **Variance Heatmaps**: Vùng có phương sai cao thể hiện sự bất đồng thuận lớn nhất giữa các người viết: nét ngang phụ của chữ số '4' và '7', vòng cung đáy của chữ số '2', và phần giao giữa hai vòng của chữ số '8'. Đây chính là các vùng phát sinh lỗi nhận dạng chủ yếu.

### 3.3. Khám phá không gian tiềm ẩn qua PCA 2D và t-SNE 2D
- **PCA 2D**: Cho thấy các lớp chữ số $0, 1, 6$ tách khá rõ, trong khi các cụm $4, 7, 9$ bị chồng lấn một phần trong không gian chiếu tuyến tính.
- **t-SNE 2D**: Phép chiếu phi tuyến chứng minh không gian đặc trưng của MNIST có tính phân cụm tự nhiên (*clusterability*) rất mạnh. 10 cụm chữ số tách biệt rõ ràng, khẳng định các giải thuật phi tuyến (RBF SVM, CNN) sẽ đạt hiệu quả phân loại vượt trội.

### 3.4. Kỹ thuật tiền xử lý hình học & Trích xuất đặc trưng
1. **Nắn thẳng góc nghiêng (Deskewing)**:
   - Tính toán mô-men quán tính trung tâm của ảnh: $\mu_{pq} = \sum_x \sum_y (x - \bar{x})^p (y - \bar{y})^q f(x, y)$.
   - Hệ số xiên góc: $\alpha = \frac{\mu_{11}}{\mu_{02}}$.
   - Ma trận biến đổi Affine ngược đưa chữ số nghiêng về phương thẳng đứng:
     $$\mathbf{M} = \begin{bmatrix} 1 & \alpha & -0.5 \times 28 \times \alpha \\ 0 & 1 & 0 \end{bmatrix}$$
2. **Nén chiều bằng PCA (Principal Component Analysis)**:
   - Khảo sát phương sai tích lũy trên tập huấn luyện: Giữ lại **95% tổng phương sai**, số chiều giảm từ 784 xuống còn **141 chiều** (trên tập 10k) hoặc **154 chiều** (trên tập 60k).
   - Giúp giảm dung lượng mô hình gấp hơn 5 lần và tăng tốc độ suy luận của k-NN gấp 4 lần.
3. **Lược đồ hướng gradient (HOG)**:
   - Lưới ô $4 \times 4$ ($7 \times 7$ pixel/cell), 9 hướng gradient, chuẩn hóa khối $2 \times 2$ block theo chuẩn $L_2\text{-Hys}$.
   - Trích xuất ra vector **324 chiều** mô tả cấu trúc biên cạnh và hướng nét bút.

### 3.5. Quy trình phân chia dữ liệu & Chống rò rỉ (Leakage Prevention)
- **Tập kiểm thử (Test Set - 10,000 mẫu)**: Được giữ nguyên vẹn độc lập theo chuẩn của Yann LeCun.
- **Tập huấn luyện & kiểm định (60,000 mẫu)**: Được phân chia phân tầng thành:
  - **Train Set (50,000 mẫu)**: Dùng để fit mô hình và fit các bộ biến đổi PCA.
  - **Validation Set (10,000 mẫu)**: Dùng để thẩm định siêu tham số và early stopping.
- **Nguyên tắc chống rò rỉ**: PCA Transformer và các phép biến đổi có tham số học chỉ được `fit` trên tập Train tương ứng; tuyệt đối không fit trên tập Validation hoặc Test.

---

## CHƯƠNG 4: MÔ HÌNH THỰC NGHIỆM & KẾT QUẢ ĐỐI CHUẨN

### 4.1. Thiết kế thực nghiệm đối chứng kiểm soát
Để trả lời thỏa đáng câu hỏi nghiên cứu, các thực nghiệm được thiết kế thành **2 tầng đối chuẩn**:
- **Tầng 1 (Controlled Benchmark)**: Cố định tập con huấn luyện phân tầng đúng **10,000 mẫu** (`random_state=42`) để so sánh đơn biến:
  - *Nhóm A*: Cố định thuật toán SVM RBF, so sánh 4 không gian đặc trưng (Raw, Deskew, PCA, HOG).
  - *Nhóm B*: Cố định tập train 10,000 mẫu, so sánh 7 thuật toán (GNB, BNB, k-NN Raw, k-NN PCA, Linear SVM, RBF SVM, Random Forest).
  - *Nhóm C*: Modern CNN trên cùng 10,000 mẫu để so sánh ngang hàng với ML cổ điển.
- **Tầng 2 (Full Benchmark)**: Huấn luyện trên toàn bộ **60,000 mẫu** để đánh giá trần năng lực tối đa của từng phương pháp.

### 4.2. Bảng đối chuẩn có kiểm soát (Cùng 10,000 mẫu Train)

| Xếp hạng | Phân nhóm | Thuật toán / Mô hình | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Accuracy)** | Macro F1-Score | Số mẫu sai (/10k test) | Tốc độ suy luận (ms/mẫu) |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Nhóm A (Đặc trưng)** | **SVM (RBF Kernel, C=5.0)** | **Deskewed Pixels** | 784 | 10,000 | **97.77%** | **97.75%** | **223** | 0.210 ms |
| **#2** | **Nhóm C (Học sâu)** | **Modern CNN (sub10k)** | **Learned Conv (28×28)** | 784 | 10,000 | **97.60%** | **97.60%** | **240** | **0.082 ms** |
| **#3** | **Nhóm A (Đặc trưng)** | **SVM (RBF Kernel, C=5.0)** | **HOG Features** | 324 | 10,000 | **97.58%** | **97.57%** | **242** | 0.282 ms |
| **#4** | **Nhóm A (Đặc trưng)** | **SVM (RBF Kernel, C=5.0)** | **PCA (95% Var)** | 141 | 10,000 | **97.22%** | **97.20%** | **278** | 0.196 ms |
| **#5** | **Nhóm A (Đặc trưng)** | **SVM (RBF Kernel, C=5.0)** | **Raw Pixels** | 784 | 10,000 | **96.86%** | **96.83%** | **314** | 0.235 ms |
| **#6** | **Nhóm B (Thuật toán)** | **k-NN (k=3, Euclidean)** | **PCA (95% Var)** | 141 | 10,000 | **95.44%** | **95.41%** | 456 | **0.057 ms** |
| **#7** | **Nhóm B (Thuật toán)** | **Random Forest (100 cây)** | **Raw Pixels** | 784 | 10,000 | **95.31%** | **95.26%** | 469 | **0.008 ms** |
| **#8** | **Nhóm B (Thuật toán)** | **k-NN (k=3, Euclidean)** | **Raw Pixels** | 784 | 10,000 | **95.17%** | **95.14%** | 483 | 0.231 ms |
| **#9** | **Nhóm B (Thuật toán)** | **Linear SVM (C=1.0)** | **Raw Pixels** | 784 | 10,000 | **89.34%** | **89.17%** | 1,066 | **0.004 ms** |
| **#10** | **Nhóm B (Thuật toán)** | **Bernoulli Naive Bayes** | **Binarized Pixels** | 784 | 10,000 | **84.40%** | **84.20%** | 1,560 | **0.010 ms** |
| **#11** | **Nhóm B (Thuật toán)** | **Gaussian Naive Bayes** | **Raw Pixels** | 784 | 10,000 | **55.80%** | **51.50%** | 4,420 | 0.040 ms |

### 4.3. Bảng đối chuẩn mở rộng toàn phần (60,000 mẫu Train)

| Xếp hạng | Thuật toán / Mô hình | Không gian Đặc trưng | Số mẫu Train | Thời gian Train | Độ trễ suy luận | **Độ chính xác (Accuracy)** | Macro F1-Score | Số mẫu sai (/10k test) | Dung lượng checkpoint |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN (Deep Learning)** | **Learned Conv (28×28)** | **60,000** | 164.75s | **0.079 ms** | **99.19% ~ 99.32%** | **99.18% ~ 99.31%** | **68 – 81** | **0.62 MB** |
| **#2** | **SVM (RBF Kernel, C=5.0)** | **PCA (154D)** | **60,000** | 125.56s | 0.852 ms | **98.54%** | **98.53%** | **146** | 8.44 MB |
| **#3** | **k-NN (k=3, Euclidean)** | **PCA (154D)** | **60,000** | 0.00s | 0.075 ms | **97.31%** | **97.29%** | **269** | 33.7 MB |
| **#4** | **Linear SVM (C=1.0)** | **Raw Pixels (784D)** | **60,000** | 28.02s | 0.002 ms | **91.84%** | **91.71%** | 816 | 0.05 MB |
| **#5** | **Bernoulli Naive Bayes** | **Binarized Pixels** | **60,000** | 0.35s | 0.004 ms | **84.46%** | **84.26%** | 1,554 | 0.05 MB |
| **#6** | **Gaussian Naive Bayes** | **Raw Pixels (784D)** | **60,000** | 0.21s | 0.023 ms | **55.58%** | **50.90%** | 4,442 | 0.04 MB |

### 4.4. Đo lường hiệu năng tính toán & Tài nguyên
- **Môi trường thực thi**: CPU Intel Core đa nhân, RAM 16GB, Python 3.14.5, PyTorch 2.14.1, Scikit-learn 1.9.1.
- **Tốc độ suy luận (Inference Latency)**:
  - Linear SVM và Naive Bayes đạt tốc độ nhanh nhất ($0.002 - 0.010\text{ ms/mẫu}$).
  - Modern CNN đạt tốc độ vượt trội $0.079\text{ ms/mẫu}$ (khoảng $12,650\text{ ảnh/giây}$), hoàn toàn đáp ứng các ứng dụng thời gian thực.
  - k-NN trên dữ liệu thô 784D có độ trễ cao ($0.231\text{ ms/mẫu}$); khi chuyển sang PCA 141D, độ trễ giảm hơn $4\times$ xuống còn $0.057\text{ ms/mẫu}$.
- **Dung lượng mô hình**:
  - Checkpoint Modern CNN chỉ nặng **$0.62\text{ MB}$**, gọn hơn nhiều so với k-NN ($33.7\text{ MB}$) và SVM RBF ($8.44\text{ MB}$).

---

## CHƯƠNG 5: PHÂN TÍCH KẾT QUẢ & PHÂN TÍCH LỖI CHUYÊN SÂU

### 5.1. Phân tích ma trận nhầm lẫn (Confusion Matrix)
Từ 10 biểu đồ ma trận nhầm lẫn chuẩn hóa thu được tại [reports/figures/](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/reports/figures), các lỗi phân loại tập trung vào các nhóm tương quan hình học có quy luật:
1. **Cặp chữ số $4 \leftrightarrow 9$**: Tần suất nhầm lẫn cao nhất ở tất cả các mô hình. Khi đỉnh trên của số 4 bị người viết nối liền hoặc góc bo tròn, hình dáng của nó gần như trùng khớp với vòng tròn khép kín của số 9.
2. **Cặp chữ số $3 \leftrightarrow 5$**: Cả hai chữ số đều có cung tròn uốn cong ở nửa dưới. Khi nét ngang trên đỉnh của số 5 bị viết cong hoặc ngắn, mô hình dự đoán nhầm thành số 3.
3. **Cặp chữ số $7 \leftrightarrow 1$**: Khi số 7 thiếu nét gạch ngang phụ giữa thân và nét xiên trên đỉnh bị viết ngắn, mô hình dễ nhầm lẫn với nét thẳng đứng của số 1.
4. **Cặp chữ số $8 \leftrightarrow 3$**: Phần đường cong bên phải của số 8 tương đồng tuyệt đối với số 3.

### 5.2. Phân tích lỗi chuyên sâu (Deep Error Analysis)
Mô hình Modern CNN chỉ phân loại sai **68 mẫu trên tổng số 10,000 mẫu kiểm thử** (tỷ lệ lỗi cực thấp: $0.68\%$). Nhóm đã trích xuất trực tiếp ảnh các mẫu sai và xác định 3 nguyên nhân cốt lõi:
- **Nhiễu nhãn trong bộ dữ liệu gốc (*Label Noise*)**: Điển hình có những mẫu ảnh trong MNIST bị người dán nhãn sai từ khi thu thập (ví dụ: ảnh thể hiện rõ ràng chữ số 6 nhưng nhãn gốc ghi là 0). Thực chất mạng CNN đã nhận dạng đúng đặc trưng thị giác.
- **Chữ số cực kỳ mơ hồ (*Ambiguous Digits*)**: Nét viết cẩu thả, nhòe mực hoặc đứt quãng, ngay cả mắt người bình thường khi quan sát độc lập cũng không thể khẳng định chắc chắn 100%.
- **Dị dạng hình học cực đoan (*Extreme Distortion*)**: Chữ số viết quá lệch hoặc co rúm vào góc ảnh, làm cho bước căn tâm khối lượng bị lệch nhẹ.

### 5.3. Trả lời thỏa đáng câu hỏi nghiên cứu khoa học

#### 1. Về Không gian Đặc trưng (Feature Representation):
- **Trên tập dữ liệu quy mô nhỏ (10,000 mẫu)**: Các đặc trưng hình học có định hướng mang lại hiệu quả cao nhất:
  - **Deskewing (Nắn góc nghiêng)**: Tăng độ chính xác mạnh nhất (từ $96.86\% \to 97.77\%$, tăng $+0.91\%$) nhờ loại bỏ yếu tố biến thiên chủ quan của người viết.
  - **HOG (324 chiều)**: Đạt $97.58\%$ (+0.72%) nhờ mô tả xuất sắc hướng biên nét bút.
  - **PCA (141 chiều)**: Giảm $5.5\times$ số chiều nhưng độ chính xác tăng từ $96.86\% \to 97.22\%$ do loại bỏ các điểm ảnh biên không mang thông tin phân lớp.
- **Trên tập dữ liệu quy mô lớn (60,000 mẫu)**: **Đặc trưng tích chập tự học (Learned Conv Features)** của CNN là giải pháp số 1 vì tự động trích xuất các bộ lọc phân cấp đa tầng.

#### 2. Về Thuật toán Phân lớp (Classification Algorithms):
- **Modern CNN** là thuật toán nhận dạng xuất sắc nhất toàn diện (**99.32%**, suy luận siêu tốc $0.079\text{ ms/mẫu}$, checkpoint nhẹ $0.62\text{ MB}$).
- Trong nhóm các thuật toán học máy cổ điển của môn học: **SVM với Kernel RBF** là thuật toán vượt trội nhất (**98.54%** trên PCA 60k; **96.86%** trên Raw 10k, vượt xa mức 89.34% của Linear SVM).
- **k-NN** cho độ chính xác tốt ($97.31\%$) nhưng đòi hỏi không gian PCA để tránh bùng nổ thời gian suy luận.
- **Naive Bayes** xếp cuối do giả định độc lập có điều kiện bị vi phạm nghiêm trọng trong dữ liệu ảnh.

---

## CHƯƠNG 6: ỨNG DỤNG WEB DEMO & KIỂM THỬ HỆ THỐNG

### 6.1. Kiến trúc ứng dụng Web Demo thời gian thực
Hệ thống cung cấp một ứng dụng web tương tác hoàn chỉnh phục vụ bảo vệ nghiệm thu:
- **Backend ([app/server.py](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/app/server.py))**: Xây dựng trên framework **FastAPI**, nạp sẵn toàn bộ 8 mô hình vào bộ nhớ đệm RAM.
- **Frontend ([app/static/](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/app/static/))**: Giao diện Glassmorphism hiện đại, hỗ trợ vẽ tay mượt mà trên Canvas bằng chuột hoặc cảm ứng di động, tự động nạp danh sách mô hình từ `/api/models`.

### 6.2. Pipeline căn tâm khối lượng quang học (Center of Mass)
Để giải quyết triệt để vấn đề chữ số vẽ tay ngoài thực tế bị nhận dạng kém do nét vẽ lệch tâm, nhóm đã triển khai thuật toán căn chỉnh quang học chuẩn NIST trong hàm `get_center_of_mass_28x28`:
1. **Phát hiện vùng nét chữ**: Ngưỡng hóa nhị phân và tìm hình chữ nhật bao quanh (*Bounding Box*). Bắt lỗi bảng vẽ trống nếu số điểm ảnh sáng nhỏ hơn 15 pixel.
2. **Co dãn bảo toàn tỷ lệ**: Đưa nét chữ vào khung viền $20 \times 20$ mà không làm méo tỷ lệ khung hình.
3. **Căn tâm khối lượng**: Đặt ảnh vào khung $28 \times 28$, tính toán tọa độ trọng tâm $(\bar{x}, \bar{y})$ theo mô-men ảnh cấp 1 và tịnh tiến chính xác về tâm $(14, 14)$.
4. **Trích xuất đặc trưng tương ứng**: Tự động áp dụng PCA, HOG, Deskew hoặc Binarize tùy theo mô hình người dùng lựa chọn trên giao diện.

### 6.3. Hệ thống kiểm thử tự động (Automated Test Suite)
Bộ kiểm thử tự động được thiết kế tại [tests/test_pipeline.py](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/tests/test_pipeline.py) với 15 bài kiểm thử unit và integration:
- Kiểm tra tính toàn vẹn dữ liệu, kích thước tensor, miền giá trị chuẩn hóa.
- Kiểm tra không rò rỉ dữ liệu giữa tập Train, Validation và Test.
- Kiểm tra thuật toán nắn góc nghiêng, PCA và HOG.
- Kiểm tra lan truyền xuôi của mạng CNN và tính chất phân phối xác suất Simplex ($\sum P = 1.0$).
- Kiểm tra các endpoint API, xử lý bảng vẽ trống và độ trễ suy luận.
- **Kết quả**: **15/15 bài kiểm thử vượt qua (100% OK) trong 0.887 giây**.

---

## CHƯƠNG 7: KẾT LUẬN & HƯỚNG PHÁT TRIỂN

### 7.1. Tổng kết các đóng góp chính của đề tài
1. **Hoàn thành 100% các yêu cầu bắt buộc của Bài tập lớn**: Triển khai đầy đủ, nghiêm túc toàn bộ các thuật toán học máy nền tảng trong chương trình đào tạo (*Naive Bayes, k-NN, Linear SVM, RBF SVM, Random Forest*).
2. **Phương pháp luận nghiên cứu chuẩn mực**: Thiết kế thành công benchmark đối chứng đơn biến trên cùng tập con 10,000 mẫu, giải quyết thấu đáo câu hỏi nghiên cứu của Bộ môn với đầy đủ chứng cứ định lượng.
3. **Đạt điểm thưởng Sáng tạo (+0.5 điểm)**: Tự nghiên cứu và huấn luyện thành công mô hình Deep Learning Modern CNN đạt độ chính xác đỉnh cao **99.32%**, phân tích chi tiết bản chất 68 mẫu phân loại sai.
4. **Đạt điểm thưởng Sản phẩm (+0.5 điểm)**: Xây dựng ứng dụng Web Demo tương tác thời gian thực hiện đại, giải quyết trọn vẹn bài toán căn tâm khối lượng thực tế.
5. **Hồ sơ nghiệm thu học thuật chuyên nghiệp**: Tự động hóa xuất bản Báo cáo kỹ thuật Word (.docx), Slide trình chiếu PowerPoint (.pptx), Sổ tay Jupyter (.ipynb) và Bảng phân công công việc minh bạch.

### 7.2. Hạn chế và Hướng nghiên cứu tiếp theo
- **Hạn chế**: Mô hình hiện tại chỉ nhận dạng từng chữ số đơn lẻ đã được phân đoạn độc lập.
- **Hướng mở rộng**:
  - Phát triển bài toán nhận dạng chuỗi chữ số viết tay liên tục (*Connected Handwritten Digit String Recognition*) ứng dụng kỹ thuật Connectionist Temporal Classification (CTC).
  - Tối ưu hóa lượng tử hóa trọng số (INT8 Quantization) để triển khai trực tiếp lên các vi điều khiển và chip nhúng camera IoT biên.

---

## TÀI LIỆU THAM KHẢO

1. **LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998)**. *Gradient-based learning applied to document recognition*. Proceedings of the IEEE, 86(11), 2278-2324.
2. **Bishop, C. M. (2006)**. *Pattern Recognition and Machine Learning*. Springer New York.
3. **Duda, R. O., Hart, P. E., & Stork, D. G. (2001)**. *Pattern Classification* (2nd ed.). John Wiley & Sons.
4. **Cortes, C., & Vapnik, V. (1995)**. *Support-vector networks*. Machine Learning, 20(3), 273-297.
5. **Dalal, N., & Triggs, B. (2005)**. *Histograms of oriented gradients for human detection*. IEEE CVPR, Vol. 1, pp. 886-893.
6. **Northcutt, C. G., Athalye, A., & Mueller, J. (2021)**. *Pervasive label errors in test sets destabilize machine learning benchmarks*. NeurIPS 2021.
7. **Bộ môn Khoa học Máy tính**, *Giáo trình Nhận dạng mẫu*, Trường Đại học Thủy Lợi.
