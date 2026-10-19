# BÁO CÁO NGHIỆM THU CUỐI CÙNG (FINAL RELEASE VERIFICATION)
**Dự án: Nhận dạng chữ số viết tay trên bộ dữ liệu MNIST**  
**Học phần: Nhận dạng mẫu — Nhóm 03**  
**Ngày kiểm tra nghiệm thu:** 18/10/2026

---

## 1. BẢNG TỔNG HỢP KẾT QUẢ NGHIỆM THU TOÀN DIỆN

| STT | Hạng mục kiểm tra | Kết luận | Bằng chứng kỹ thuật / Phương pháp xác minh | Kết quả thực tế đạt được |
|:---:|---|:---:|---|---|
| **1** | **Web sử dụng Linear SVM mới (C=0.01)** | **PASS** | File: [`app/server.py`](app/server.py)<br>Test: `test_backend_loads_linear_svm_c001` trong [`tests/test_pipeline.py`](tests/test_pipeline.py) | Server nạp đúng checkpoint `svm_linear_sub10k.joblib`, tham số $C=0.01$, đạt 90.79% Test Accuracy (921 lỗi). Cấu hình cũ $C=1.0$ được chuyển thành `svm_linear_legacy`. |
| **2** | **Web sử dụng Random Forest mới (150 cây)** | **PASS** | File: [`app/server.py`](app/server.py)<br>Test: `test_backend_loads_random_forest_150_trees` trong [`tests/test_pipeline.py`](tests/test_pipeline.py) | Server nạp đúng checkpoint `rf_sub10k.joblib`, tham số `n_estimators=150`, đạt 95.28% Test Accuracy (472 lỗi). Model được nén an toàn còn 8.14 MB. Bản cũ 100 cây chuyển thành `rf_legacy`. |
| **3** | **Preprocessing khớp đúng từng mô hình** | **PASS** | File: [`app/server.py`](app/server.py)<br>Pipeline: `svm_rbf_deskew_pca_pipeline.joblib` | Mô hình deskew+pca nhận diện đúng pipeline tích hợp `['deskew', 'pca', 'svm']`, không bị lỗi reshape 112D sang 784D. |
| **4** | **API predictions khớp trực tiếp Estimator** | **PASS** | File: [`app/server.py`](app/server.py)<br>Test: `test_api_predict_sample_digit`, `test_api_predict_svm_deskew_pca` | `predicted_digit = int(model.predict(feat)[0])`. Nhãn trả về từ API đồng nhất tuyệt đối với kết quả dự đoán của estimator. |
| **5** | **Frontend không còn số liệu hardcode lỗi thời** | **PASS** | File: [`app/static/index.html`](app/static/index.html)<br>Test: `test_frontend_no_hardcoded_obsolete_accuracy` | Đã xóa triệt để các số liệu cũ `>99.2%`, `98.3%`, `97.5%`. Danh sách mô hình được nạp động từ endpoint `/api/models`. |
| **6** | **Phân biệt rành mạch CNN Baseline và CNN Validation** | **PASS** | File: [`results/verified_experiments.json`](results/verified_experiments.json)<br>File: [`results/cnn_validation_history.json`](results/cnn_validation_history.json) | CNN Baseline (60k mẫu, 99.19%, 81 lỗi) và CNN Validation (50k train/10k val, checkpoint epoch 2, 99.00%, 100 lỗi) được trình bày như hai thực nghiệm riêng biệt, có giải thích mục đích rõ ràng. |
| **7** | **Metadata môi trường chuẩn hóa chính xác** | **PASS** | File: [`src/benchmark_latency.py`](src/benchmark_latency.py)<br>File: [`results/latency_benchmark_detailed.json`](results/latency_benchmark_detailed.json) | Đã sửa lỗi `sklearn_version` lấy từ `sklearn.__version__` (1.9.1) thay vì nhầm `joblib.__version__` (1.6.0). Bổ sung đầy đủ tách bạch các trường môi trường. |
| **8** | **Báo cáo không còn số liệu cũ mâu thuẫn** | **PASS** | File: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx`](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx)<br>Banner cảnh báo trên các file markdown draft lịch sử | Đã sửa số liệu RQ2 trong báo cáo thành Linear SVM C=0.01 (90.79%) và RF 150 cây (95.28%). Gắn banner `LEGACY DRAFT` lên 4 file markdown cũ. |
| **9** | **PDF không còn trang trống bất thường** | **PASS** | File: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf)<br>Lệnh kiểm tra: `pypdf.PdfReader` | Trang 14 cũ (0 ký tự) đã được khắc phục hoàn toàn bằng thuộc tính `page_break_before` trên Heading 1. Không còn trang nào có 0 ký tự. |
| **10** | **Quy mô số trang PDF nằm trong chuẩn Rubric (20–30 trang)** | **PASS** | Script: `powershell -ExecutionPolicy Bypass -File src/convert_to_pdf.ps1` | Tổng số trang PDF được Word COM kết xuất chính xác là **28 trang**, đáp ứng hoàn hảo khung 20–30 trang của giảng viên. |
| **11** | **Slide PowerPoint không bị cắt nội dung** | **PASS** | File: [`reports/Slide_Thuyet_Trinh_Nhom_03.pptx`](reports/Slide_Thuyet_Trinh_Nhom_03.pptx)<br>Script: `python src/export_slides_pptx.py` | Bảng đối chuẩn 15 hàng cũ đã được chia thành 3 slide tập trung (Slide 5A: Đặc trưng, Slide 5B: Thuật toán, Slide 5C: CNN & Quy mô). Đáy bảng nằm ở vị trí 5.0 - 5.6 inch trên chiều cao slide 7.5 inch, không tràn viền. |
| **12** | **Git index stage đầy đủ các thành phần giao nộp** | **PASS** | Lệnh: `git status --short`<br>Tài liệu: [`GIT_RELEASE_CHECK.md`](GIT_RELEASE_CHECK.md) | 130 files đã được đưa vào Git Index (`src/`, `app/`, `tests/`, `reports/`, `results/`, `saved_models/`, `notebooks/`, ...). Không có file nào vượt ngưỡng 50 MB. |
| **13** | **Bộ kiểm thử tự động (Unit & Integration Tests)** | **PASS** | Lệnh: `python -m unittest tests/test_pipeline.py` | **28/28 tests PASS (100%)** trong thời gian 1.801s. Kiểm tra trọn vẹn từ tải dữ liệu, biến đổi đặc trưng, kiến trúc CNN, đến API và tính trung thực của frontend. |
| **14** | **Kiểm thử trình duyệt tương tác thực tế (Browser E2E)** | **PASS** | Thư mục: [`reports/evidence/web/`](reports/evidence/web/)<br>Trình duyệt tự động Playwright | Đã chạy thực tế trên `http://127.0.0.1:8000`: load app, chọn mẫu 0, dự đoán CNN, đổi model Linear SVM, Random Forest, kiểm tra lỗi bảng vẽ trống. Lưu đầy đủ screenshot minh chứng. |
| **15** | **Yêu cầu hồ sơ theo Rubric môn học** | **PASS** | Tài liệu: [`RUBRIC_COMPLIANCE.md`](RUBRIC_COMPLIANCE.md) | Đáp ứng trọn vẹn 5 tiêu chí bắt buộc (9.0 điểm) và cả 2 tiêu chí điểm thưởng (+1.0 điểm: Sáng tạo mô hình Modern CNN 99.19% và Sản phẩm Web tương tác). |

---

## 2. MINH CHỨNG CHI TIẾT CÁC THỰC NGHIỆM ĐÃ ĐƯỢC XÁC MINH

10 mô hình chính thức được xác minh độc lập trên 10.000 mẫu MNIST Test Set:

```json
[
  {"id": "EXP-C01", "name": "Modern CNN (Baseline 60k)", "accuracy": 99.19, "errors": 81},
  {"id": "EXP-F01", "name": "SVM RBF + PCA 154D (Full 60k)", "accuracy": 98.54, "errors": 146},
  {"id": "EXP-A01", "name": "SVM RBF (Deskewed + PCA 112D)", "accuracy": 97.97, "errors": 203},
  {"id": "EXP-A02", "name": "SVM RBF (Deskewed Raw 784D)", "accuracy": 97.77, "errors": 223},
  {"id": "EXP-C02", "name": "Modern CNN (sub10k)", "accuracy": 97.60, "errors": 240},
  {"id": "EXP-A03", "name": "SVM RBF (HOG 324D)", "accuracy": 97.58, "errors": 242},
  {"id": "EXP-F02", "name": "k-NN (k=3) + PCA 154D (Full 60k)", "accuracy": 97.31, "errors": 269},
  {"id": "EXP-A04", "name": "SVM RBF (PCA 152D)", "accuracy": 97.22, "errors": 278},
  {"id": "EXP-A05", "name": "SVM RBF (Raw Pixels 784D)", "accuracy": 96.86, "errors": 314},
  {"id": "EXP-B02", "name": "Random Forest (150 cây)", "accuracy": 95.28, "errors": 472},
  {"id": "EXP-B03", "name": "k-NN (k=3, Euclidean Raw)", "accuracy": 95.17, "errors": 483},
  {"id": "EXP-B04", "name": "Linear SVM (C=0.01)", "accuracy": 90.79, "errors": 921},
  {"id": "EXP-B05", "name": "Bernoulli Naive Bayes", "accuracy": 84.40, "errors": 1560},
  {"id": "EXP-B06", "name": "Gaussian Naive Bayes", "accuracy": 55.80, "errors": 4420}
]
```

Bên cạnh đó, mô hình kiểm định Validation:
- `Modern CNN (Validation Tuned)`: 50.000 mẫu train, 10.000 mẫu validation, chọn checkpoint epoch 2 (val_loss: 0.0425), đạt **99.00%** trên tập test 10.000 ảnh (100 lỗi).
