# BẢNG ĐỐI CHIẾU TIÊU CHÍ CHẤM ĐIỂM (RUBRIC_FINAL_CHECK.md)
**Môn học: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay trên MNIST**  
**Nhóm thực hiện: Nhóm 03 — Trường Đại học Thủy Lợi**  
**Thang điểm: 9.0 điểm bắt buộc + 1.0 điểm thưởng tối đa**

---

## 1. BẢNG TỔNG HỢP ĐỐI CHIẾU TIÊU CHÍ RUBRIC

| STT | Tiêu chí đánh giá theo Rubric | Điểm tối đa | Yêu cầu kỹ thuật chi tiết | Tệp/Mã nguồn chứng minh | Kết quả kiểm tra thực tế | Trạng thái |
|:---:|:---|:---:|:---|:---|:---|:---:|
| **1** | **Xác định bài toán, mô tả và phân tích dữ liệu** | **1.5 đ** | • Định nghĩa bài toán OCR, đầu vào ma trận 2D và véc-tơ 1D.<br>• Phân tích thống kê MNIST, phân bố 10 lớp, Shannon Entropy.<br>• Khám phá ảnh trung bình (Mean) và độ lệch chuẩn (Variance). | • `src/eda.py`<br>• `reports/figures/01_class_distribution.png`<br>• `reports/figures/02_mean_variance_digits.png`<br>• Báo cáo Word (Chương 1 & 3) | Đã phân tích 70,000 ảnh, chứng minh độ cân bằng qua Shannon Entropy ($H = 3.3199$ bits, 99.94%), trực quan hóa mean/variance đầy đủ. | **DONE** |
| **2** | **Tiền xử lý và biểu diễn đặc trưng** | **1.5 đ** | • Chuẩn hóa cường độ sáng $[0, 1]$.<br>• Cài đặt nắn thẳng chữ số (Deskewing) bằng mô-men trung tâm.<br>• Giảm chiều PCA giữ 95% phương sai.<br>• Trích xuất đặc trưng biên cạnh HOG.<br>• Tuân thủ nghiêm ngặt nguyên tắc Zero Data Leakage. | • `src/features.py`<br>• `src/data_loader.py`<br>• `saved_models/pca_transformer.joblib` (154D)<br>• `saved_models/pca_transformer_deskew_sub10k.joblib` (112D)<br>• Báo cáo Word (Chương 2 & 3) | Đã triển khai đầy đủ 4 không gian đặc trưng. Chứng minh bằng unit test rằng train/val không trùng lặp index và PCA chỉ fit trên train. | **DONE** |
| **3** | **Xây dựng và giải thích mô hình** | **3.5 đ** | • Triển khai tối thiểu 4 thuật toán kinh điển trong học phần: Naive Bayes, k-NN, SVM (Linear & RBF), Random Forest.<br>• Xây dựng mạng nơ-ron sâu Modern CNN.<br>• Giải thích công thức toán học, hàm mất mát và tối ưu siêu tham số trên tập Validation độc lập. | • `src/models.py`<br>• `src/train_and_benchmark.py`<br>• Báo cáo Word (Chương 2 & 4)<br>• Bảng 4.1 trong Báo cáo Word | Đã xây dựng 10 cấu hình mô hình thực nghiệm, lưu đầy đủ checkpoint trong `saved_models/`. Có bảng lịch sử dò tìm siêu tham số trên Validation Set. | **DONE** |
| **4** | **Đánh giá, so sánh, phân tích lỗi** | **2.0 đ** | • Bảng tổng hợp đối chuẩn đa mô hình.<br>• Đo lường Accuracy, Macro F1, độ trễ suy luận và dung lượng.<br>• Ma trận nhầm lẫn (Confusion Matrix).<br>• Phân tích chi tiết từng lớp và Error Gallery giải mã nguyên nhân sai sót. | • `results/verified_experiments.json`<br>• `EXPERIMENT_RESULTS.md`<br>• `reports/figures/cm_modern_cnn.png`<br>• `reports/figures/errors_modern_cnn.png`<br>• Báo cáo Word (Chương 5) | Đã đo đạc thực tế trên 10,000 ảnh test. Phân tích chi tiết 81 mẫu sai của CNN thành 3 nhóm (Label noise, Ambiguity, Outliers). Bảng per-class đầy đủ. | **DONE** |
| **5** | **Chương trình kiểm tra thực nghiệm (Testing)** | **0.5 đ** | • Mã nguồn tổ chức module hóa, dễ tái lập kết quả.<br>• Bộ kiểm thử tự động (Unit test, Integration test, E2E, Regression test).<br>• Hướng dẫn cài đặt và thực thi rõ ràng trên Windows/Linux. | • `tests/test_pipeline.py`<br>• `README.md`<br>• `requirements.txt` | Đã thiết kế bộ kiểm thử 24 test cases. Chạy lệnh thực tế `pytest tests/ -v` đạt tỷ lệ 24/24 PASS (100%). | **DONE** |
| **+** | **Điểm thưởng Sáng tạo (Creative Bonus)** | **+0.5 đ** | • Triển khai mô hình nâng cao vượt ra ngoài nội dung bài giảng cơ bản (Deep Learning CNN / ResNet).<br>• Ứng dụng kỹ thuật nắn thẳng Deskewing tối ưu hóa hình học. | • `src/models.py` (`ModernCNN`)<br>• `src/features.py` (`deskew_dataset`, `DeskewTransformer`)<br>• `saved_models/modern_cnn_mnist.pt`<br>• `saved_models/svm_rbf_deskew_pca_pipeline.joblib`<br>• `saved_models/svm_rbf_deskew_pca_sub10k.joblib` | Mạng Modern CNN đạt **99.19%** trên full 60k (81 lỗi); Mô hình SVM kết hợp Deskewing + PCA đạt **97.97%** trên tập con 10k mẫu (203 lỗi). | **ĐỀ XUẤT ĐÁNH GIÁ** |
| **+** | **Điểm thưởng Sản phẩm trực quan (Product Bonus)** | **+0.5 đ** | • Xây dựng ứng dụng hoàn chỉnh có giao diện người dùng tương tác.<br>• Trực quan hóa suy luận thời gian thực trên nét vẽ tự do.<br>• Pipeline xử lý quang học đồng nhất với dữ liệu huấn luyện. | • `app/server.py`<br>• `app/static/index.html`<br>• `app/static/style.css`<br>• `app/static/app.js`<br>• `run_app.py` | Ứng dụng Web FastAPI + HTML5 Canvas tương tác thời gian thực, có căn tâm quang học Center of Mass, thanh xác suất 10 lớp, 10 mẫu test nhanh từ MNIST. | **ĐỀ XUẤT ĐÁNH GIÁ** |

---

## 2. DANH MỤC HỒ SƠ BÀN GIAO THEO QUY ĐỊNH CỦA GIẢNG VIÊN

| Tài liệu bàn giao | Định dạng | Tệp thực tế trong dự án | Tình trạng kiểm tra |
|:---|:---|:---|:---:|
| **Báo cáo kỹ thuật chi tiết (20–30 trang)** | Word & PDF | • `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx`<br>• `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf` | **ĐÃ XÁC MINH: ĐẠT ĐÚNG 30 TRANG** |
| **Slide thuyết trình bảo vệ** | PowerPoint | • `reports/Slide_Thuyet_Trinh_Nhom_03.pptx` | **ĐÃ HOÀN TẤT (10 SLIDES ĐỒNG BỘ)** |
| **Mã nguồn thực nghiệm và ứng dụng** | Python | • `src/`, `app/`, `tests/`, `run_app.py` | **100% HOẠT ĐỘNG, 24/24 TESTS PASS** |
| **Dữ liệu huấn luyện và kiểm thử** | NumPy compressed | • `data/mnist.npz` (Tải tự động qua `src/data_loader.py`) | **SẴN SÀNG TÁI LẬP** |
| **Bảng phân công nhiệm vụ nhóm** | Word & Markdown | • Bảng 7.1 trong Báo cáo Word<br>• `reports/BANG_PHAN_CONG_CONG_VIEC.md` | **ĐÃ CẬP NHẬT 100% ĐÓNG GÓP** |

---

## 3. VIỆC CÒN CẦN LÀM DÀNH CHO SINH VIÊN (ACTION ITEMS TRƯỚC KHI NỘP)

1. Điền thông tin cá nhân: Thay thế các phần giữ chỗ `[Họ và tên Sinh viên]`, `[Mã sinh viên]`, `[Lớp]` và `[Tên Giảng viên hướng dẫn]` trên trang bìa Báo cáo Word và Slide PowerPoint.
2. Kiểm tra xác nhận duyệt đề tài với Giảng viên bộ môn (nếu giảng viên có yêu cầu ký duyệt đề cương).
3. Nén tệp dự án hoặc đẩy mã nguồn lên kho lưu trữ GitHub cá nhân theo hướng dẫn trong `README.md`.
