# BÁO CÁO KIỂM TRA GIT REPOSITORY (GIT RELEASE CHECK)
**Dự án: Nhận dạng chữ số viết tay trên bộ dữ liệu MNIST**  
**Học phần: Nhận dạng mẫu — Nhóm 03**  
**Ngày kiểm tra:** 18/10/2026

---

## 1. TỔNG QUAN TRẠNG THÁI GIT

- **Branch hiện tại:** `main`
- **Remote URL:** `https://github.com/zudoan/handwritten-digit-recognition.git`
- **Tổng số tệp tin đã Stage (Sẵn sàng commit):** 130 files
- **Trạng thái tuân thủ chính sách GitHub:**
  - Không có file nào vượt quá 100 MB (Hard limit).
  - Không có file nào vượt quá 50 MB (Warning limit). Model lớn nhất `rf_sub10k.joblib` đã được nén an toàn còn 8.14 MB (`compress=3`).
  - Không chứa secret, API key, file tạm (`.DS_Store`, `Thumbs.db`) hay bytecode Python (`__pycache__`).

---

## 2. DANH MỤC THÀNH PHẦN ĐÃ ĐƯỢC STAGE VÀO GIT INDEX

| Nhóm thành phần | Số lượng tệp | Mô tả chi tiết |
|---|:---:|---|
| **Mã nguồn lõi (`src/`)** | 18 | `models.py`, `features.py`, `data_loader.py`, `eda.py`, `evaluate.py`, `train_and_benchmark.py`, `train_cnn_with_validation.py`, `tune_hyperparameters.py`, `benchmark_latency.py`, `export_report_docx.py`, `export_slides_pptx.py`, ... |
| **Ứng dụng Web (`app/`)** | 4 | `server.py` (FastAPI backend + Model Registry), `index.html`, `app.js`, `style.css` (Glassmorphism Canvas UI). |
| **Khởi chạy ứng dụng** | 1 | `run_app.py` (Script một lệnh chạy demo web). |
| **Bộ kiểm thử tự động (`tests/`)** | 2 | `test_pipeline.py` (28 unit, integration, và regression tests - 100% PASS), `__init__.py`. |
| **Sổ tay thực nghiệm (`notebooks/`)** | 2 | `01_eda_and_data_analysis.ipynb`, `02_models_and_benchmark.ipynb`. |
| **Checkpoints mô hình (`saved_models/`)** | 27 | Trọng số PyTorch (`modern_cnn_mnist.pt`, `modern_cnn_val_tuned.pt`, ...) và scikit-learn joblib (`rf_sub10k.joblib`, `svm_linear_sub10k.joblib`, `svm_rbf_deskew_pca_pipeline.joblib`, ...). |
| **Kết quả thực nghiệm (`results/`)** | 5 | `verified_experiments.json`, `latency_benchmark_detailed.json`, `cnn_validation_history.json`, `hyperparameter_search_results.json`, `hyperparameter_search_results.csv`. |
| **Báo cáo & Minh chứng (`reports/`)** | 68 | Báo cáo chính thức 28 trang Word & PDF, Slide trình chiếu 12 slides PPTX, 10 ma trận nhầm lẫn, 10 phòng tranh phân tích lỗi, minh chứng web testing. |
| **Tài liệu hướng dẫn & Rubric** | 5 | `README.md`, `requirements.txt`, `EXPERIMENT_RESULTS.md`, `EXPERIMENT_PROTOCOL.md`, `RUBRIC_COMPLIANCE.md`. |

---

## 3. CÁC TỆP TIN ĐƯỢC CỐ Ý KHÔNG STAGE (INTENTIONALLY UNTRACKED)

Các file nhật ký tiến trình làm việc nội bộ giữa các vòng audit (`FINAL_*_PROGRESS.md`, `PROJECT_AUDIT_REPORT.md`, `SUBMISSION_CHECKLIST.md`) được giữ lại trên máy trạm của bạn làm tài liệu tham khảo và không cần thiết phải đưa vào bản nộp mã nguồn chính trên GitHub.

---

## 4. HƯỚNG DẪN THAO TÁC CHO NGƯỜI DÙNG (USER ACTION GUIDE)

Theo đúng quy tắc release an toàn, hệ thống **không tự ý commit hoặc push** mã nguồn lên GitHub của bạn.

Sau khi bạn đã kiểm tra và hài lòng với toàn bộ các thay đổi, vui lòng mở terminal PowerShell tại thư mục dự án và thực hiện 2 lệnh sau:

```powershell
# 1. Thực hiện commit toàn bộ 130 files đã được chuẩn bị
git commit -m "feat(release): final submission release - sync checkpoints, web registry, docx/pdf 28p, pptx slides, and 28 tests"

# 2. Đẩy mã nguồn lên repository GitHub của Nhóm 03
git push origin main
```
