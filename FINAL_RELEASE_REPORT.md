# BÁO CÁO NGHIỆM THU VÀ HOÀN THIỆN PHÁT HÀNH CUỐI CÙNG (FINAL_RELEASE_REPORT.md)

**Học phần**: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay trên MNIST  
**Nhóm thực hiện**: Nhóm 03 — Trường Đại học Thủy Lợi  
**Vai trò**: Senior ML Engineer, Pattern Recognition Research Reviewer, QA & Release Engineer  
**Thời điểm hoàn tất**: 18/10/2026  
**Trạng thái phát hành**: **RELEASE READY — SẴN SÀNG NGHIỆM THU & NỘP BÀI**

---

## 1. TỔNG QUAN CÁC LỖI ĐÃ KHẮC PHỤC TRIỆT ĐỂ

Trong vòng hoàn thiện cuối cùng (Final Release), toàn bộ các mâu thuẫn khoa học và kỹ thuật còn tồn đọng đã được giải quyết dứt điểm trên mã nguồn thực tế và kiểm chứng bằng dữ liệu thật:

### 1.1. Khắc phục bất đồng bộ Hyperparameter và Checkpoint (Phase 2)
- **Vấn đề trước đây**: Lịch sử validation search (`results/hyperparameter_search_results.json`) ghi nhận Linear SVM thắng ở $C=0.01$ (Val Acc 90.36%) và Random Forest thắng ở $n=150$ cây (Val Acc 95.07%). Tuy nhiên, các tệp checkpoint cũ trong `saved_models/` lại lưu Linear SVM $C=1.0$ (89.34%) và Random Forest $n=100$ cây (95.31%).
- **Hành động khắc phục**:
  1. Xây dựng và thực thi kịch bản `src/align_checkpoints.py`.
  2. Huấn luyện estimator **Linear SVM** với siêu tham số chiến thắng $C=0.01$ trên tập con phân tầng 10,000 mẫu train, đo kiểm thử khách quan trên 10,000 test set: **Test Accuracy đạt 90.79%** (Macro F1: 90.64%, giảm từ 1,066 lỗi xuống còn **921 lỗi / 10k mẫu**). Lưu checkpoint đồng bộ vào `saved_models/svm_linear_sub10k.joblib`.
  3. Huấn luyện estimator **Random Forest** với cấu hình chiến thắng $n=150$ cây trên tập 10,000 mẫu train, đo kiểm thử khách quan: **Test Accuracy đạt 95.28%** (Macro F1: 95.23%, **472 lỗi / 10k mẫu**). Lưu checkpoint đồng bộ vào `saved_models/rf_sub10k.joblib`.
  4. Cập nhật mã nguồn `src/train_and_benchmark.py` (dòng 410–427) để tự động khởi tạo đúng tham số $C=0.01$ và $n=150$ cây cho mọi lần huấn luyện tiếp theo.
  5. Cập nhật đồng bộ cơ sở dữ liệu `results/verified_experiments.json` (mục EXP-B04 và EXP-B02).
  6. Bổ sung bài kiểm thử hồi quy bắt buộc `test_selected_hyperparameters_match_artifacts` trong `tests/test_pipeline.py`.

### 1.2. Hoàn thiện quy trình Validation chuẩn mực cho Modern CNN (Phase 3)
- **Vấn đề trước đây**: Mô hình Modern CNN trước đây được huấn luyện với số epoch cố định mà chưa có quy trình kiểm tra loss/accuracy trên validation set theo từng epoch và chưa có cơ chế early stopping thực tế.
- **Hành động khắc phục**:
  1. Xây dựng kịch bản `src/train_cnn_with_validation.py` với giao thức khoa học nghiêm ngặt: Phân chia $50,000$ mẫu train, $10,000$ mẫu validation độc lập (Stratified Shuffle Split) và $10,000$ mẫu test cách ly hoàn toàn.
  2. Theo dõi Cross-Entropy Loss và Accuracy sau mỗi epoch trên tập Validation.
  3. Lựa chọn checkpoint dựa trên tiêu chí Validation Loss nhỏ nhất, tích hợp Early Stopping với patience = 2 epochs.
  4. Thực nghiệm ghi nhận:
     - Epoch 1: Train Loss 0.1649, Train Acc 94.98% | Val Loss 0.0541, Val Acc 98.39% (Best).
     - Epoch 2: Train Loss 0.0604, Train Acc 98.15% | Val Loss 0.0425, Val Acc 98.70% (Tối ưu toàn cục).
     - Epoch 3: Train Loss 0.0454, Train Acc 98.54% | Val Loss 0.0438, Val Acc 98.67%.
     - Epoch 4: Train Loss 0.0407, Train Acc 98.71% | Val Loss 0.0525, Val Acc 98.46%.
     - -> Early Stopping kích hoạt tự động ở Epoch 4 do Val Loss không giảm sau 2 epochs liên tiếp.
     - Checkpoint tốt nhất tại Epoch 2 được tải lại và đánh giá duy nhất một lần trên tập Test: **Test Accuracy đạt 99.00%**, Macro F1 99.00%, 100 lỗi / 10k mẫu.
  5. Checkpoint tối ưu bởi validation được lưu độc lập tại `saved_models/modern_cnn_val_tuned.pt` (không ghi đè hay làm mất checkpoint baseline 60k `saved_models/modern_cnn_mnist.pt` đạt 99.19% / 81 lỗi).
  6. Lịch sử validation được lưu tại `results/cnn_validation_history.json`.
  7. Xuất biểu đồ đào tạo trung thực ra tệp `reports/figures/08_cnn_training_history.png`.
  8. Bổ sung bài kiểm thử tự động `test_cnn_validation_history_and_checkpoint` trong `tests/test_pipeline.py`.

### 1.3. Chuẩn hóa phương pháp đo hiệu năng và độ trễ suy luận (Phase 4)
- **Vấn đề trước đây**: Báo cáo mô tả inference latency được đo từng ảnh với batch size = 1, nhưng mã nguồn benchmark cũ lại tính toán qua phép chia trung bình của dự đoán theo mẻ (`predict(X_test) / N`), làm nhầm lẫn giữa Single-image Latency và Batched Throughput.
- **Hành động khắc phục**:
  1. Xây dựng kịch bản chuyên dụng `src/benchmark_latency.py`.
  2. Phân định rõ ràng:
     - **Single-image Latency (batch_size = 1)**: Đo tuần tự từng ảnh với 20 lượt warm-up và 500 lần đo độc lập để thống kê mean, median, P95 và std.
     - **Batched Throughput (batch_size = 10,000)**: Đo khả năng xử lý hàng loạt trên toàn bộ tập test để tính số mẫu xử lý được trên mỗi giây.
  3. Kết quả đo thực nghiệm trên máy trạm Intel x86_64, Windows 11, PyTorch CPU:
     - **Modern CNN**: Độ trễ đơn lẻ trung bình **0.516 ms** (trung vị **0.405 ms**, P95 **0.664 ms**), thông lượng theo lô đạt **9,426 mẫu/giây**.
     - **SVM Deskew + PCA Pipeline**: Độ trễ đơn lẻ trung bình **0.536 ms** (trung vị **0.526 ms**, P95 **0.592 ms**, bao gồm nắn thẳng + PCA 112D + nhân RBF), thông lượng theo lô đạt **5,551 mẫu/giây**.
     - **Linear SVM**: Độ trễ đơn lẻ trung bình **0.150 ms** (trung vị **0.147 ms**), thông lượng theo lô đạt **276,187 mẫu/giây**.
     - **Random Forest (150 cây)**: Thông lượng theo lô đạt **62,344 mẫu/giây**.
  4. Toàn bộ thông số môi trường phần cứng/phần mềm được lưu trữ chi tiết tại `results/latency_benchmark_detailed.json`.

### 1.4. Khắc phục lỗi bố cục trang và hoàn thiện Báo cáo Word / PDF (Phase 7)
- **Vấn đề trước đây**: Lượt kiểm tra trước phát hiện trang 21 của PDF bị trống gần như toàn bộ, chỉ có một dòng gạch đầu dòng mồ côi (orphan bullet) phía trên do hình ảnh Figure 5.3 (Error Gallery) có kích thước quá lớn (5.2 inch), đẩy toàn bộ khối văn bản phân tích lỗi sang trang sau.
- **Hành động khắc phục**:
  1. Cải tiến hàm chèn trong `src/export_report_docx.py`: Thiết lập `keep_with_next = True` cho toàn bộ các tiêu đề (`add_heading_styled`), lời tựa bảng/hình (`add_caption`), và hình ảnh (`add_image_safe`).
  2. Căn chỉnh kích thước Figure 5.3 (`reports/figures/errors_modern_cnn.png`) từ 5.2 inch xuống 4.2 inch, giúp hình ảnh và toàn bộ 3 nhóm phân loại lỗi nằm trọn vẹn, thanh thoát trên cùng một trang giấy, triệt tiêu hoàn toàn hiện tượng dòng mồ côi.
  3. Bổ sung Section 4.4 và Section 4.5 vào Báo cáo Word, nhúng biểu đồ Figure 4.1 (`08_cnn_training_history.png`), đồng bộ số liệu Linear SVM ($C=0.01$, 90.79%), Random Forest (150 cây, 95.28%) và cập nhật bảng kiểm thử lên 24 test cases.
  4. Chuyển đổi qua Microsoft Word COM engine trên Windows: Xuất tệp PDF `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf` đạt chính xác **30 trang**, nằm đúng trong khung yêu cầu 20–30 trang của giảng viên.

### 1.5. Củng cố bằng chứng kiểm thử Web Demo Browser End-to-End (Phase 6)
- Thu thập và lưu trữ toàn bộ ảnh chụp màn hình kiểm thử thực tế từ phiên trình duyệt độc lập vào thư mục chính thức `reports/evidence/web/`:
  - `01_web_app_loaded.png`: Giao diện ứng dụng tải thành công với Canvas Glassmorphism và danh sách model.
  - `02_digit_0_prediction.png`: Nhận dạng chữ số 0 vẽ tay với thanh xác suất trực quan.
  - `03_digit_3_prediction.png`: Nhận dạng chữ số 3 vẽ tay.
  - `04_digit_7_prediction.png`: Nhận dạng chữ số 7 vẽ tay.
  - `05_model_switched_svm.png`: Chuyển đổi mô hình sang SVM Deskew + PCA và suy luận chính xác.

---

## 2. DANH MỤC CÁC TỆP ĐÃ THAY ĐỔI VÀ TẠO MỚI

| STT | Tệp tin | Loại thay đổi | Mô tả nội dung |
|:---:|:---|:---:|:---|
| 1 | `src/align_checkpoints.py` | Tạo mới | Script huấn luyện và cập nhật checkpoint Linear SVM $C=0.01$ và Random Forest 150 cây |
| 2 | `src/train_cnn_with_validation.py` | Tạo mới | Script huấn luyện Modern CNN có validation split, early stopping và xuất biểu đồ đào tạo |
| 3 | `src/benchmark_latency.py` | Tạo mới | Script chuẩn hóa đo độ trễ suy luận đơn lẻ (batch=1) và thông lượng theo lô |
| 4 | `src/train_and_benchmark.py` | Sửa đổi | Cập nhật tham số mặc định Linear SVM ($C=0.01$) và RF ($n=150$) đồng bộ validation |
| 5 | `src/export_report_docx.py` | Sửa đổi | Sửa lỗi dàn trang `keep_with_next`, thêm Section 4.4 & 4.5, nhúng Fig 4.1, cập nhật 24 test cases |
| 6 | `src/export_slides_pptx.py` | Sửa đổi | Cập nhật số liệu Linear SVM 90.79%, RF 150 cây 95.28%, 24 test cases, độ trễ chi tiết |
| 7 | `tests/test_pipeline.py` | Sửa đổi | Thêm 2 regression tests: `test_selected_hyperparameters_match_artifacts` và `test_cnn_validation_history_and_checkpoint` |
| 8 | `saved_models/svm_linear_sub10k.joblib` | Cập nhật | Checkpoint Linear SVM $C=0.01$ (Test Acc: 90.79%, 921 lỗi) |
| 9 | `saved_models/rf_sub10k.joblib` | Cập nhật | Checkpoint Random Forest 150 cây (Test Acc: 95.28%, 472 lỗi) |
| 10 | `saved_models/modern_cnn_val_tuned.pt` | Tạo mới | Checkpoint Modern CNN được chọn bởi validation qua early stopping (Test Acc: 99.00%) |
| 11 | `results/verified_experiments.json` | Cập nhật | Cập nhật bản ghi EXP-B04 và EXP-B02 với số liệu thực tế đo đạc |
| 12 | `results/cnn_validation_history.json` | Tạo mới | Nhật ký các epochs huấn luyện, validation loss/acc và kết quả đánh giá |
| 13 | `results/latency_benchmark_detailed.json` | Tạo mới | Cơ sở dữ liệu độ trễ đơn lẻ, phân vị P95 và thông lượng |
| 14 | `reports/figures/08_cnn_training_history.png` | Tạo mới | Biểu đồ đường cong Loss và Accuracy qua các epoch có đánh dấu Best Checkpoint |
| 15 | `reports/evidence/web/*.png` | Tạo mới | 5 ảnh chụp minh chứng kiểm thử Web App thời gian thực trên trình duyệt |
| 16 | `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx` | Cập nhật | Báo cáo kỹ thuật Word 30 trang |
| 17 | `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf` | Cập nhật | Báo cáo PDF 30 trang render chuẩn qua MS Word COM |
| 18 | `reports/Slide_Thuyet_Trinh_Nhom_03.pptx` | Cập nhật | Bộ Slide PowerPoint 10 trang đồng bộ 100% |
| 19 | `README.md`, `EXPERIMENT_RESULTS.md`, `RUBRIC_FINAL_CHECK.md` | Cập nhật | Đồng bộ số liệu thực nghiệm và chỉ số kiểm thử |

---

## 3. TÌNH TRẠNG SẴN SÀNG NGHIỆM THU

- **Bộ kiểm thử tự động**: **24/24 PASS (100%)** trong thời gian 3.75s.
- **Báo cáo PDF**: **30 trang**, bố cục trang chuẩn mực, không có trang trống, số liệu khớp hoàn toàn.
- **Bộ Slide PowerPoint**: **10 trang**, định dạng Widescreen 16:9 hiện đại, màu sắc trang nhã Navy & Light Blue.
- **Ứng dụng Web**: FastAPI + HTML5 Canvas hoạt động ổn định trên `http://127.0.0.1:8000`, có bằng chứng tương tác thực tế.
- **Mã nguồn**: Module hóa, không rò rỉ dữ liệu, tài liệu hóa chi tiết, sẵn sàng đẩy lên GitHub.
