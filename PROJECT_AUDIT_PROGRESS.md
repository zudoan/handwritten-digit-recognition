# NHẬT KÝ TIẾN TRÌNH AUDIT VÀ HOÀN THIỆN DỰ ÁN MNIST (PROJECT_AUDIT_PROGRESS.md)
**Học phần: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay (MNIST)**  
**Đơn vị: Trường Đại học Thủy Lợi — Khoa CNTT — Nhóm 03**

---

## 1. BẢNG THEO DÕI TIẾN ĐỘ 6 GIAI ĐOẠN

| Giai đoạn (Phase) | Tên giai đoạn | Trạng thái | Bắt đầu | Hoàn thành | Ghi chú chính |
|:---|:---|:---:|:---:|:---:|:---|
| **Phase 1** | **Audit toàn diện mã nguồn, mô hình & tài liệu** | 🟢 ĐÃ HOÀN THÀNH | 2026-10-18 | 2026-10-18 | Lập danh sách 8 lỗi (ERR-01 đến ERR-08) tại `PROJECT_AUDIT_REPORT.md`. |
| **Phase 2** | **Sửa lỗi tính đúng đắn (Correctness & Pipeline)** | 🟢 ĐÃ HOÀN THÀNH | 2026-10-18 | 2026-10-18 | Sửa chia tập Train 50k, Val 10k, Test 10k trong `src/data_loader.py`; thêm `HOGTransformer` trong `src/features.py`; xử lý lỗi mã hóa UTF-8 trên Windows. |
| **Phase 3** | **Thực nghiệm đối chứng có kiểm soát (Controlled Experiments)** | 🟢 ĐÃ HOÀN THÀNH | 2026-10-18 | 2026-10-18 | Tái thiết kế benchmark: Nhóm A (Đặc trưng), Nhóm B (Thuật toán), Nhóm C (CNN) trên cùng 10,000 mẫu train; tách bạch với benchmark 60,000 mẫu toàn phần. |
| **Phase 4** | **Kiểm tra và hoàn thiện ứng dụng Web Demo** | 🟢 ĐÃ HOÀN THÀNH | 2026-10-18 | 2026-10-18 | Nạp đủ 8 mô hình; nạp động danh sách model từ `/api/models`; tiền xử lý chuẩn NIST; phát hiện bảng vẽ trống; không ngụy tạo xác suất giả. |
| **Phase 5** | **Đồng bộ hóa tài liệu & Báo cáo khoa học** | 🟢 ĐÃ HOÀN THÀNH | 2026-10-18 | 2026-10-18 | Cập nhật số liệu thực nghiệm chính xác vào `EXPERIMENT_RESULTS.md`, `BAO_CAO_CHI_TIET_PROJECT.md`, `reports/tables/`, xuất thành công Word (.docx) và PPTX (.pptx). |
| **Phase 6** | **Tạo bộ kiểm thử tự động & Nghiệm thu Rubric** | 🟢 ĐÃ HOÀN THÀNH | 2026-10-18 | 2026-10-18 | Viết bộ kiểm thử `tests/test_pipeline.py` (15/15 tests PASS); lập bảng đối chiếu chi tiết tại `RUBRIC_COMPLIANCE.md`. |

---

## 2. CHI TIẾT KẾT QUẢ THỰC HIỆN TỪNG GIAI ĐOẠN

### Phase 1: Audit (Hoàn thành)
- Đọc chi tiết `BÀI TẬP LOỚN CUỐI KỲ.pdf`:
  - 5 phần bắt buộc: 9.0 điểm.
  - 2 tiêu chí thưởng: Sáng tạo (CNN +0.5đ), Sản phẩm (Web Demo +0.5đ).
  - Trả lời câu hỏi nghiên cứu: *"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"*.
- Phát hiện 8 lỗi quan trọng, lập báo cáo chi tiết trong `PROJECT_AUDIT_REPORT.md`.

### Phase 2: Correctness & Pipeline (Hoàn thành)
- Sửa hàm `create_train_val_test` trong `src/data_loader.py`: chia 50,000 train, 10,000 validation (stratified) và giữ nguyên 10,000 test.
- Thêm `HOGTransformer` trong `src/features.py` tương thích Scikit-learn Pipeline.
- Khắc phục triệt để lỗi mã hóa Unicode `charmap cp1252` trên Windows PowerShell cho toàn bộ các script Python (`generate_tables.py`, `create_notebooks.py`, `train_and_benchmark.py`).

### Phase 3: Controlled Experiments (Hoàn thành)
- Thiết lập giao thức thực nghiệm đối chứng đơn biến tại `EXPERIMENT_PROTOCOL.md`.
- Đo lường thực tế trên cùng tập con phân tầng 10,000 mẫu train:
  - **Nhóm A (Khảo sát Đặc trưng)**:
    - Deskewed Pixels: **97.77%** (+0.91% so với Raw)
    - HOG (324D): **97.58%** (+0.72% so với Raw)
    - PCA (141D): **97.22%** (+0.36% so với Raw)
    - Raw Pixels (784D): **96.86%**
  - **Nhóm B (Khảo sát Thuật toán)**:
    - RBF SVM: **96.86%**
    - k-NN (PCA): **95.44%**
    - Random Forest: **95.31%**
    - k-NN (Raw): **95.17%**
    - Linear SVM: **89.34%**
    - Bernoulli NB: **84.40%**
    - Gaussian NB: **55.80%**
  - **Nhóm C (Modern CNN)**:
    - Trên cùng 10,000 mẫu: **97.60%**
    - Trên toàn bộ 60,000 mẫu: **99.32%** (chỉ 68 lỗi / 10,000 mẫu test)
- Lưu trữ kết quả chính xác tại `EXPERIMENT_RESULTS.md` và `reports/tables/benchmark_results.md`.

### Phase 4: Application & Web Demo (Hoàn thành)
- Nâng cấp `app/server.py`:
  - Hỗ trợ đầy đủ 8 mô hình: Modern CNN, SVM RBF PCA, k-NN PCA, Random Forest, Linear SVM, Bernoulli NB, Gaussian NB, SVM HOG.
  - Áp dụng đúng pipeline tiền xử lý (PCA, HOG, Deskew, Binarize, Raw) tương ứng từng mô hình.
  - Bắt lỗi bảng vẽ trống / nét quá mờ (trả về status rõ ràng, không crash).
- Nâng cấp `app/static/app.js`: Tự động nạp danh sách mô hình từ `/api/models`.

### Phase 5: Documentation & Reports (Hoàn thành)
- Cập nhật số liệu Shannon Entropy thực tế ($3.3199$ bits, cân bằng $99.94\%$) và các bảng đối chuẩn trong `BAO_CAO_CHI_TIET_PROJECT.md` và `reports/BAO_CAO_KHOA_HOC_NHAN_DANG_CHU_SO_MNIST.md`.
- Xuất thành công tệp Microsoft Word: `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx` (882.4 KB).
- Xuất thành công tệp PowerPoint: `reports/Slide_Thuyet_Trinh_Nhom_03.pptx` (605.6 KB).
- Tạo thành công 2 Notebook Jupyter: `01_eda_and_data_analysis.ipynb`, `02_models_and_benchmark.ipynb`.

### Phase 6: Automated Testing & Rubric (Hoàn thành)
- Viết bộ kiểm thử `tests/test_pipeline.py` với 15 test cases (Data loading, normalization, splits, deskew, PCA, HOG, CNN, API, blank canvas).
- Chạy kiểm thử: **15/15 tests PASSED (100% OK)** trong 1.029 giây.
- Lập bảng đối chiếu toàn diện tại `RUBRIC_COMPLIANCE.md`.
