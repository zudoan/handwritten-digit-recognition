# NHẬN DẠNG CHỮ SỐ VIẾT TAY (MNIST DATASET)
### BÀI TẬP LỚN MÔN NHẬN DẠNG MẪU (PATTERN RECOGNITION) — ĐỀ TÀI 1
**Trường Đại học Thủy Lợi — Khoa Công nghệ Thông tin**  
**Nhóm thực hiện:** Nhóm 03  
**Kho lưu trữ chính thức:** [https://github.com/zudoan/handwritten-digit-recognition](https://github.com/zudoan/handwritten-digit-recognition)

---

<p align="center">
  <img src="reports/evidence/web/redesign_overview.png" alt="Giao diện Web Demo ChuSoVietTay" width="880"/>
</p>

<p align="center">
  <a href="https://github.com/zudoan/handwritten-digit-recognition"><img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub Repo"/></a>
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Deep%20Learning-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/Tests-28%20Passed%20(100%25)-brightgreen?style=for-the-badge" alt="Tests"/>
</p>

---

## 📌 MỤC LỤC
1. [Giới Thiệu Đề Tài](#1-giới-thiệu-đề-tài)
2. [Cơ Sở Dữ Liệu & Quy Chuẩn Tiền Xử Lý](#2-cơ-sở-dữ-liệu--quy-chuẩn-tiền-xử-lý)
3. [Phương Pháp & Kỹ Thuật Trích Xuất Đặc Trưng](#3-phương-pháp--kỹ-thuật-trích-xuất-đặc-trưng)
4. [Bảng Đối Chuẩn Thực Nghiệm Toàn Diện (Benchmark)](#4-bảng-đối-chuẩn-thực-nghiệm-toàn-diện-benchmark)
5. [Ứng Dụng Web Studio Tương Tác](#5-ứng-dụng-web-studio-tương-tác)
6. [Cấu Trúc Thư Mục Dự Án](#6-cấu-trúc-thư-mục-dự-án)
7. [Hướng Dẫn Cài Đặt & Khởi Chạy](#7-hướng-dẫn-cài-đặt--khởi-chạy)
8. [Hồ Sơ Báo Cáo Khoa Học & Slide](#8-hồ-sơ-báo-cáo-khoa-học--slide)
9. [Đội Ngũ Thực Hiện & Bản Quyền](#9-đội-ngũ-thực-hiện--bản-quyền)

---

## 1. GIỚI THIỆU ĐỀ TÀI

Nhận dạng chữ số viết tay (*Handwritten Digit Recognition*) là bài toán nền tảng kinh điển trong lĩnh vực **Nhận dạng mẫu (Pattern Recognition)** và **Thị giác máy tính (Computer Vision)**.

Mục tiêu của dự án:
- Nghiên cứu có hệ thống và đối chuẩn thực nghiệm đa thuật toán trên tập dữ liệu chuẩn **MNIST (70.000 mẫu)**.
- So sánh hiệu năng của hai trường phái:
  1. **Học máy thống kê cổ điển (Classical Pattern Recognition):** Support Vector Machine (Linear / RBF Kernel), $k$-Nearest Neighbors ($k$-NN), Random Forest, Gaussian & Bernoulli Naive Bayes kết hợp các kỹ thuật trích xuất đặc trưng (PCA, HOG, Deskewing).
  2. **Học sâu (Deep Learning):** Kiến trúc Modern Convolutional Neural Network (CNN) gồm 3 khối tích chập, Batch Normalization và Dropout chống quá khớp.
- Xây dựng ứng dụng Web tương tác thời gian thực (*Interactive Web Demo Studio*) đạt tiêu chuẩn giao diện cao cấp (*Soft Glass & Editorial Minimalism*), tích hợp bảng vẽ canvas tự động căn chỉnh quang học Center of Mass và so sánh độ trễ suy luận.

---

## 2. CƠ SỞ DỮ LIỆU & QUY CHUẨN TIỀN XỬ LÝ

### 2.1. Phân chia tập dữ liệu (Splits)
Dữ liệu sử dụng nguồn chuẩn **MNIST** từ TensorFlow Datasets / Yann LeCun:
- **Tập huấn luyện (Training Set):** 60.000 ảnh kích thước $28 \times 28$ mức xám.
- **Tập kiểm thử (Test Set):** 10.000 ảnh phân bố cân bằng đồng đều giữa 10 lớp ($0 \to 9$).
- **Chia tập kiểm định (Validation Tuning):** Để lựa chọn siêu tham số công bằng, một tập kiểm chuẩn gồm 50.000 train + 10.000 validation được thiết lập nhằm tránh rò rỉ dữ liệu (*data leakage*) từ tập test.

### 2.2. Chuẩn hóa quang học Center of Mass (NIST Standard)
Để đảm bảo ảnh người dùng vẽ tay trên canvas có phân bố tương đồng tuyệt đối với dữ liệu huấn luyện:
1. **Phát hiện vùng ký tự:** Bóc tách khung chữ nhật nhỏ nhất bao quanh nét vẽ (`cv2.boundingRect`).
2. **Co dãn bảo toàn tỷ lệ:** Nén tỷ lệ cạnh lớn nhất về đúng $20\text{px}$ (khung viền $20 \times 20$).
3. **Căn trọng tâm quang học:** Tính moment không gian ($\mu_{10}, \mu_{01}$) để xác định tâm khối lượng nét mực và tịnh tiến affine đưa trọng tâm về chính xác tọa độ $(14, 14)$ của khung chuẩn $28 \times 28$.
4. **Chuẩn hóa giá trị:** Đưa cường độ điểm ảnh từ $[0, 255]$ về $[0.0, 1.0]$.

---

## 3. PHƯƠNG PHÁP & KỸ THUẬT TRÍCH XUẤT ĐẶC TRƯNG

| Phương pháp đặc trưng | Kích thước | Mục đích & Cơ sở toán học |
|---|:---:|---|
| **Raw Pixels** | 784D | Vector hóa trực tiếp ma trận điểm ảnh phẳng hóa $28 \times 28$. |
| **PCA (Principal Component Analysis)** | 154D / 112D | Giảm số chiều bảo toàn $\ge 95\%$ phương sai dữ liệu, loại bỏ nhiễu biên và tăng tốc suy luận. |
| **Deskewing (Nắn thẳng góc nghiêng)** | 784D | Tính moment quán tính cấp 2 ($\mu_{11}, \mu_{02}$) để triệt tiêu độ nghiêng nét viết cá nhân. |
| **Deskewing + PCA** | **112D** | Kết hợp nắn thẳng hình học và nén phương sai, mang lại độ chính xác cao nhất nhóm học máy cổ điển. |
| **HOG (Histogram of Oriented Gradients)** | 324D | Trích xuất phân bố hướng gradient biên cạnh cục bộ với 9 bins góc và chuẩn hóa khối $2\times 2$. |
| **Binarized Pixels** | 784D | Nhị phân hóa điểm ảnh với ngưỡng $\theta = 0.2$ phục vụ mô hình xác suất Bernoulli Naive Bayes. |
| **Learned Conv Features (CNN)** | Không gian sâu | Tự động học trích xuất đặc trưng cục bộ đến toàn cục qua 3 tầng Conv2D + BatchNorm + ReLU. |

---

## 4. BẢNG ĐỐI CHUẨN THỰC NGHIỆM TOÀN DIỆN (BENCHMARK)

Tất cả kết quả đều được kiểm chứng độc lập trên **10.000 ảnh MNIST Test Set** từ các checkpoint đã lưu:

### 4.1. Quy mô toàn phần (Full Dataset — 60.000 mẫu Train)

| Xếp hạng | Thuật toán / Mô hình | Không gian Đặc trưng | Số chiều | Số mẫu Train | **Độ chính xác (Test Acc)** | Số ảnh sai / 10k | Độ trễ suy luận |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 🥇 **#1** | **Modern CNN Baseline** | **Learned Conv (28×28)** | 784 | 60.000 | **99.19%** | **81** | **0.516 ms** |
| 🥈 **#2** | **Modern CNN (Val Tuned)** | **Learned Conv (28×28)** | 784 | 50.000 | **99.00%** | **100** | 0.516 ms |
| 🥉 **#3** | **SVM (RBF Kernel, C=5.0)** | **PCA (95% Var)** | 154 | 60.000 | **98.54%** | **146** | 1.250 ms |
| **#4** | **$k$-NN ($k=3$, Distance)** | **PCA (95% Var)** | 154 | 60.000 | **97.31%** | **269** | 2.100 ms |
| **#5** | **Linear SVM** | Raw Pixels (784D) | 784 | 60.000 | **91.84%** | 816 | 0.008 ms |
| **#6** | **Bernoulli Naive Bayes** | Binarized Pixels | 784 | 60.000 | **84.46%** | 1.554 | 0.012 ms |
| **#7** | **Gaussian Naive Bayes** | Raw Pixels (784D) | 784 | 60.000 | **55.58%** | 4.442 | 0.035 ms |

### 4.2. Tập con kiểm chuẩn đối chứng (Controlled Subset — Cùng 10.000 mẫu Train)

| Mô hình / Thuật toán | Không gian Đặc trưng | Số chiều | **Độ chính xác (Test Acc)** | Ghi chú khoa học |
|:---|:---|:---:|:---:|:---|
| **SVM (RBF Kernel)** | **Deskewed + PCA** | **112** | **97.97%** | **Top 1 Nhóm A**: Nắn thẳng nét chữ + PCA |
| **SVM (RBF Kernel)** | Deskewed Pixels | 784 | **97.77%** | Nắn thẳng triệt tiêu độ nghiêng (+0.91% so với Raw) |
| **Modern CNN (sub10k)** | Learned Conv (28×28) | 784 | **97.60%** | CNN trên tập con 10.000 mẫu |
| **SVM (RBF Kernel)** | HOG Features | 324 | **97.58%** | Đặc trưng gradient hướng biên cạnh |
| **SVM (RBF Kernel)** | PCA (95% Var) | 152 | **97.22%** | Nén số chiều $5.1\times$, lọc nhiễu nền |
| **SVM (RBF Kernel)** | Raw Pixels | 784 | **96.86%** | Điểm ảnh thô [0, 1] |
| **$k$-NN ($k=3$, Distance)** | PCA (95% Var) | 152 | **95.44%** | PCA cải thiện khoảng cách Euclidean trong không gian nén |
| **Random Forest (150 cây)** | Raw Pixels | 784 | **95.28%** | Tối ưu số cây trên Validation Set (150 cây) |
| **$k$-NN ($k=3$, Distance)** | Raw Pixels | 784 | **95.17%** | Suy giảm nhẹ do hiện tượng bùng nổ số chiều |
| **Linear SVM ($C=0.01$)** | Raw Pixels | 784 | **90.79%** | Tối ưu $C$ qua Validation Set (tăng từ 89.34% lên 90.79%) |
| **Bernoulli Naive Bayes** | Binarized Pixels | 784 | **84.40%** | Mô hình xác suất Bernoulli nhị phân |
| **Gaussian Naive Bayes** | Raw Pixels | 784 | **55.80%** | Giả định độc lập có điều kiện bị vi phạm nghiêm trọng |

---

## 5. ỨNG DỤNG WEB STUDIO TƯƠNG TÁC

Hệ thống được trang bị giao diện web hiện đại theo ngôn ngữ **Premium Soft Glass + Editorial Minimalism**:

<p align="center">
  <img src="reports/evidence/web/sample_0_prediction.png" alt="Dự đoán mẫu số 0" width="880"/>
</p>

### Các tính năng nổi bật:
- **Studio Drawing Canvas:** Khung vẽ đen nhung với vạch căn góc cơ học (`corner-mark`), hỗ trợ mượt mà cả chuột và màn hình cảm ứng.
- **Stroke Presets:** 3 nấc nét bút thông minh (Mảnh 14, Chuẩn 20, Đậm 28) đồng bộ thanh trượt.
- **Live Model Metadata:** Tự động hiển thị không gian đặc trưng, số lượng mẫu huấn luyện và huy hiệu `VERIFIED BENCHMARK` khi chuyển mô hình.
- **Real-time Inference:** Nhận dạng tức thời kèm độ trễ tính bằng mili-giây (`latency_ms`), ảnh tiền xử lý $28 \times 28$ chuẩn NIST và phân bố xác suất trực quan trên 10 lớp.
- **Test Samples Palette:** Nạp trực tiếp 10 mẫu ảnh thực nghiệm từ tập MNIST Test để kiểm thử ngay lập tức.
- **Responsive & Accessibility:** Tương thích từ màn hình máy tính đến điện thoại di động, hỗ trợ `prefers-reduced-motion`.

---

## 6. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
ChuSoVietTay/
├── app/                                 # Ứng dụng Web Demo tương tác
│   ├── server.py                        # FastAPI Server & Model Registry
│   └── static/                          # Frontend Assets (HTML5, Vanilla CSS, JS)
│       ├── index.html                   # Giao diện Soft Glass Studio
│       ├── style.css                    # Design Tokens & Motion System
│       └── app.js                       # Logic vẽ canvas & API fetch
├── data/                                # Thư mục dữ liệu MNIST
│   ├── mnist.npz                        # Gói dữ liệu NumPy chuẩn nạp tốc độ cao
│   └── raw/                             # Tệp nhị phân thô IDX (được .gitignore loại trừ)
├── notebooks/                           # Jupyter Notebooks thực nghiệm
│   ├── 01_eda_and_data_analysis.ipynb   # Phân tích khám phá dữ liệu & đặc trưng
│   └── 02_models_and_benchmark.ipynb    # Huấn luyện mô hình & đối chuẩn chi tiết
├── reports/                             # Hồ sơ học thuật hoàn chỉnh
│   ├── BAO_CAO_KHOA_HOC_NHAN_DANG_CHU_SO_MNIST.md # Báo cáo khoa học 6 chương
│   ├── Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx # Báo cáo Word in ấn
│   ├── Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf  # Báo cáo PDF chính thức
│   ├── SLIDE_THUYET_TRINH_DE_TAI_1.md   # Đề cương slide thuyết trình
│   ├── Slide_Thuyet_Trinh_Nhom_03.pptx  # Slide thuyết trình PowerPoint
│   ├── BANG_PHAN_CONG_CONG_VIEC.md      # Bảng phân công nhiệm vụ thành viên
│   ├── figures/                         # Toàn bộ biểu đồ EDA, t-SNE, ma trận nhầm lẫn
│   ├── tables/                          # Bảng kết quả thực nghiệm JSON/Markdown
│   └── evidence/web/                    # Bằng chứng kiểm thử visual web app
├── results/                             # Nhật ký kiểm chứng thực nghiệm & tham số
│   ├── verified_experiments.json        # Dữ liệu đối chuẩn 12 cấu hình chính thức
│   └── hyperparameter_search_results.json # Bằng chứng chọn siêu tham số validation
├── saved_models/                        # Checkpoints các mô hình đã huấn luyện (.pt, .joblib)
├── src/                                 # Thư viện mã nguồn cốt lõi
│   ├── config.py                        # Cấu hình đường dẫn và hằng số
│   ├── data_loader.py                   # Nạp dữ liệu & kiểm tra tính toàn vẹn
│   ├── eda.py                           # Kịch bản sinh biểu đồ phân tích dữ liệu
│   ├── features.py                      # Pipeline PCA, HOG, Deskewing
│   ├── models.py                        # Định nghĩa ModernCNN & helper scikit-learn
│   ├── train_and_benchmark.py           # Huấn luyện và xuất kết quả đối chuẩn
│   ├── train_cnn_with_validation.py     # Huấn luyện CNN với tập kiểm định Early Stopping
│   └── tune_hyperparameters.py          # Lựa chọn siêu tham số công bằng trên Validation
├── tests/                               # Bộ kiểm thử tự động
│   └── test_pipeline.py                 # 28 bài test unit, integration & regression
├── requirements.txt                     # Danh mục thư viện phụ thuộc
├── run_app.py                           # Kịch bản khởi động Web Server
└── README.md                            # Tài liệu tổng quan dự án
```

---

## 7. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY

### 7.1. Cài đặt môi trường

Yêu cầu: **Python 3.10 trở lên** (khuyến nghị 3.10, 3.11 hoặc 3.12).

```bash
# 1. Clone kho lưu trữ
git clone https://github.com/zudoan/handwritten-digit-recognition.git
cd handwritten-digit-recognition

# 2. Tạo và kích hoạt môi trường ảo (khuyến nghị)
python -m venv .venv

# Trên Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Trên Linux / macOS:
source .venv/bin/activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 7.2. Khởi chạy Web Studio tương tác

Chạy một lệnh duy nhất:
```bash
python run_app.py
```
Sau đó mở trình duyệt tại: **`http://127.0.0.1:8000`**

### 7.3. Chạy bộ kiểm thử tự động (Unit & Integration Tests)

Dự án trang bị bộ kiểm thử toàn diện 28 test cases kiểm tra từ tiền xử lý, tính bất biến hình học, tải checkpoint và suy luận API:
```bash
python -m unittest tests/test_pipeline.py
```
*Kết quả:* `Ran 28 tests in ~1.9s — OK (100% PASS)`.

### 7.4. Tái hiện lại toàn bộ thực nghiệm

```bash
# 1. Chạy phân tích khám phá dữ liệu và sinh đồ thị:
python -m src.eda

# 2. Tinh chỉnh siêu tham số trên tập kiểm chuẩn Validation:
python -m src.tune_hyperparameters

# 3. Huấn luyện lại CNN với Early Stopping:
python -m src.train_cnn_with_validation

# 4. Đo độ trễ suy luận chi tiết:
python -m src.benchmark_latency
```

---

## 8. HỒ SƠ BÁO CÁO KHOA HỌC & SLIDE

Toàn bộ tài liệu báo cáo của Nhóm 03 được chuẩn bị đầy đủ và đồng bộ số liệu 100%:

1. **Báo cáo khoa học hoàn chỉnh (6 Chương):**
   - Định dạng Markdown: [reports/BAO_CAO_KHOA_HOC_NHAN_DANG_CHU_SO_MNIST.md](reports/BAO_CAO_KHOA_HOC_NHAN_DANG_CHU_SO_MNIST.md)
   - Định dạng Word: [reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx)
   - Định dạng PDF: [reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf)
2. **Slide thuyết trình bảo vệ trước hội đồng:**
   - Định dạng PowerPoint: [reports/Slide_Thuyet_Trinh_Nhom_03.pptx](reports/Slide_Thuyet_Trinh_Nhom_03.pptx)
   - Đề cương Markdown: [reports/SLIDE_THUYET_TRINH_DE_TAI_1.md](reports/SLIDE_THUYET_TRINH_DE_TAI_1.md)
3. **Phân công nhiệm vụ nhóm:** [reports/BANG_PHAN_CONG_CONG_VIEC.md](reports/BANG_PHAN_CONG_CONG_VIEC.md)

---

## 9. ĐỘI NGŨ THỰC HIỆN & BẢN QUYỀN

- **Đơn vị đào tạo:** Trường Đại học Thủy Lợi (TLU) — Khoa Công nghệ Thông tin.
- **Học phần:** Nhận dạng mẫu (*Pattern Recognition*).
- **Nhóm thực hiện:** **Nhóm 03**.
- **Chủ sở hữu kho lưu trữ:** [zudoan](https://github.com/zudoan) ([https://github.com/zudoan/handwritten-digit-recognition](https://github.com/zudoan/handwritten-digit-recognition)).
- **Giấy phép:** Phục vụ mục đích học thuật và nghiên cứu giáo dục.
