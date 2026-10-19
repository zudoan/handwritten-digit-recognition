# BÁO CÁO TOÀN DIỆN VỀ AUDIT VÀ KHẮC PHỤC LỖI KỸ THUẬT (FINAL_AUDIT_REPORT.md)
**Dự án: Nhận dạng chữ số viết tay (MNIST) — Bài tập lớn môn Nhận dạng mẫu**  
**Nhóm thực hiện: Nhóm 03 — Trường Đại học Thủy Lợi**  
**Ngày hoàn tất nghiệm thu kỹ thuật: 18/10/2026**

---

## 1. TỔNG QUAN MỤC TIÊU VÀ NGUYÊN TẮC THỰC THI

Theo yêu cầu kiểm định kỹ thuật cuối cùng (Final Technical Audit & Fix), toàn bộ các vấn đề khoa học, dữ liệu và kỹ thuật được rà soát với nguyên tắc cốt lõi:
> **"CODE THẬT → TEST THẬT → KẾT QUẢ THẬT → BÁO CÁO THẬT"**

Không tạo số liệu giả định, không phỏng đoán kết quả, mọi con số trình bày trong báo cáo đều được đối chiếu trực tiếp từ checkpoint đã nạp và đo lường độc lập trên 10,000 mẫu kiểm thử chuẩn của MNIST.

---

## 2. DANH SÁCH CÁC VẤN ĐỀ ĐÃ PHÁT HIỆN VÀ KHẮC PHỤC CHI TIẾT

### Vấn đề 1: Sai lệch số liệu độ chính xác của Modern CNN
- **Phát hiện**: Trong các tài liệu và slide cũ, mô hình Modern CNN được ghi đạt `99.32%` (sai 68 ảnh).
- **Kiểm tra thực tế**: Nạp checkpoint `saved_models/modern_cnn_mnist.pt`, chạy suy luận tuần tự trên toàn bộ 10,000 ảnh của MNIST Test Set.
- **Kết quả đo đạc thực tế**:
  - Accuracy: **99.19%** (chính xác: $9,919 / 10,000$).
  - Macro F1-Score: **99.18%**.
  - Số lượng ảnh phân loại sai: **81 ảnh**.
- **Khắc phục**: Thay thế toàn bộ số liệu 99.32% (68 ảnh sai) bằng **99.19% (81 ảnh sai)** trên toàn bộ các tệp: `results/verified_experiments.json`, `app/server.py`, `src/export_report_docx.py`, `src/export_slides_pptx.py`, `EXPERIMENT_RESULTS.md`, `README.md`.

### Vấn đề 2: Cấu hình Deskew + PCA bị bỏ sót trong báo cáo
- **Phát hiện**: Benchmark cũ từng ghi nhận cấu hình Deskew + PCA trên tập con 10k mẫu đạt độ chính xác cao nhất trong nhóm SVM, nhưng các báo cáo Word và Slide trước đây chưa đưa cấu hình này vào bảng đối chuẩn chính thức.
- **Kiểm tra thực tế**: Nạp checkpoint `saved_models/svm_rbf_deskew_pca_sub10k.joblib` và transformer `saved_models/pca_transformer_deskew_sub10k.joblib`.
- **Kết quả đo đạc thực tế sau khi đồng bộ cơ sở PCA (112D)**:
  - Accuracy: **97.97%** (203 ảnh sai trên 10k test, Macro F1: **97.96%**).
  - Checkpoint và pipeline thống nhất: `saved_models/svm_rbf_deskew_pca_pipeline.joblib`.
  - Đây chính là cấu hình quán quân của **Nhóm A (Khảo sát Không gian Đặc trưng)**.
- **Khắc phục**:
  - Đã tích hợp đầy đủ vào `results/verified_experiments.json` (ID: `EXP-A01`).
  - Thêm endpoint và pipeline xử lý trong `app/server.py` (`svm_deskew_pca`).
  - Phân tích chi tiết cơ chế khoa học trong Báo cáo Word 27 trang và Slide PowerPoint.

### Vấn đề 3: Sai lệch số chiều PCA giữa các tài liệu
- **Phát hiện**: Một số tài liệu cũ ghi số chiều PCA là 141 hoặc 154 cho mọi tập dữ liệu mà không phân biệt dữ liệu dùng để fit.
- **Kiểm tra thực tế**: Đọc trực tiếp thuộc tính `n_components_` từ các transformer đã fit với `n_components=0.95`:
  - `saved_models/pca_transformer.joblib` (Fit trên full 60,000 mẫu train): **154 chiều**.
  - `saved_models/pca_transformer_sub10k.joblib` (Fit trên 10,000 mẫu subset train): **152 chiều**.
  - `saved_models/pca_transformer_deskew_sub10k.joblib` (Fit trên 10,000 mẫu subset đã nắn thẳng Deskew): **112 chiều**.
- **Khắc phục**: Đồng bộ chính xác số chiều thực tế trên tất cả các tài liệu và bổ sung unit test kiểm tra tự động (`test_pca_exact_components_ground_truth`).

### Vấn đề 4: Lỗi Backend tự động Fallback sang CNN khi yêu cầu sai tên mô hình
- **Phát hiện**: Trong `app/server.py`, khi người dùng gửi `model_name` không tồn tại, mã nguồn cũ tự động gán `m_id = "cnn"`, gây hiểu nhầm về mô hình đang thực sự chạy suy luận.
- **Khắc phục**:
  - Loại bỏ hoàn toàn fallback âm thầm.
  - Trả về mã lỗi **HTTP 404 Not Found** kèm thông báo danh sách mô hình hợp lệ.
  - Bổ sung integration test `test_api_predict_invalid_model_raises_404` kiểm tra tính năng này.

### Vấn đề 5: Nguy cơ bất đồng bộ nhãn dự đoán trong API
- **Phát hiện**: Đối với SVM, việc dùng `argmax(probabilities)` từ Platt scaling có thể không đồng nhất tuyệt đối với đường phân cách `decision_function()` / `predict()`.
- **Khắc phục**: Quy định chuẩn chính thức trong `app/server.py`: Nhãn phân loại chính thức `predicted_digit` luôn được lấy từ `int(model.predict(feat)[0])`, đồng thời chỉ số tin cậy và phân bố xác suất phản ánh đúng mức độ tin cậy của mô hình mà không giả định phân phối chuẩn đã hiệu chuẩn (`is_calibrated = False`).

### Vấn đề 6: Dung lượng Báo cáo Word chưa đạt yêu cầu 20–30 trang của Giảng viên
- **Phát hiện**: Báo cáo Word cũ render ra chỉ đạt khoảng 12 trang, chưa đáp ứng quy định độ dài của đồ án cuối kỳ.
- **Khắc phục**:
  - Tái cấu trúc và nâng cấp `src/export_report_docx.py` thành công trình nghiên cứu đầy đủ 7 chương.
  - Bổ sung nội dung khoa học sâu sắc: Mô hình toán học đầy đủ (công thức Bayes, mô-men hình ảnh Deskew, phân rã trị riêng PCA, bài toán tối ưu lề mềm SVM và hàm nhân RBF, cấu trúc phân nhánh Random Forest, kiến trúc tích chập và hàm mất mát Cross-Entropy).
  - Phân tích thống kê dữ liệu: Shannon Entropy ($H = 3.3199$ bits, cân bằng 99.94%), phân tích ảnh kỳ vọng và phương sai, biểu đồ t-SNE.
  - Chi tiết hóa quá trình dò tìm siêu tham số trên Validation Set và phân tích nguồn gốc của 81 ca sai sót của Modern CNN.
  - **Kiểm định thực tế**: Chạy Word COM trên Windows xuất ra PDF chính thức đạt chính xác **27 trang** (nằm hoàn hảo trong dải 20–30 trang yêu cầu).

### Vấn đề 7: Nâng cấp bộ kiểm thử tự động
- **Phát hiện**: Bộ test cũ (15 tests) chưa có kiểm tra toán học về giao tập index train/val để chứng minh Zero Data Leakage, chưa kiểm tra lỗi HTTP 404 và chưa kiểm tra model Deskew + PCA.
- **Khắc phục**: Nâng cấp `tests/test_pipeline.py` lên **22 test cases** toàn diện, bổ sung kiểm tra giao tập index rỗng ($\text{Train} \cap \text{Val} = \emptyset$), kiểm tra số chiều PCA 112/154, kiểm tra HTTP 404, kiểm tra suy luận Deskew + PCA và kiểm tra hồi quy reload pipeline đạt $\ge 97\%$. Toàn bộ 22/22 tests đạt trạng thái **PASS 100%**.

---

## 3. DANH SÁCH CÁC TỆP ĐÃ THAY ĐỔI VÀ ĐỒNG BỘ

| STT | Tệp thay đổi | Nội dung can thiệp kỹ thuật | Trạng thái |
|:---:|:---|:---|:---:|
| 1 | `results/verified_experiments.json` | Cập nhật đầy đủ 12 thực nghiệm đối chuẩn, CNN 99.19% (81 lỗi), SVM Deskew+PCA 97.97% (112D, 203 lỗi) | **ĐÃ ĐỒNG BỘ** |
| 2 | `app/server.py` | Bỏ fallback CNN, trả HTTP 404, nạp Deskew PCA 112D, đảm bảo `predict()` đồng nhất benchmark | **ĐÃ ĐỒNG BỘ** |
| 3 | `tests/test_pipeline.py` | Nâng cấp lên 22 unit, integration & regression tests, kiểm tra Zero Leakage, PCA dims, HTTP 404 | **22/22 PASS** |
| 4 | `src/export_report_docx.py` | Viết lại trình tạo báo cáo Word 7 chương, số liệu thực, đo thực tế 27 trang qua Word COM | **ĐÃ XÁC MINH (27 TRANG)** |
| 5 | `src/export_slides_pptx.py` | Đồng bộ 100% số liệu với benchmark, đưa Deskew+PCA vào bảng, loại bỏ nhận định chủ quan | **ĐÃ ĐỒNG BỘ** |
| 6 | `EXPERIMENT_RESULTS.md` | Đồng bộ bảng đối chuẩn Nhóm A, B, C, bổ sung Deskew+PCA (112D) và CNN (99.19%) | **ĐÃ ĐỒNG BỘ** |
| 7 | `EXPERIMENT_PROTOCOL.md` | Sửa số chiều PCA 112D (Deskew subset) và 152D (Raw subset), cập nhật protocol validation | **ĐÃ ĐỒNG BỘ** |
| 8 | `README.md` | Cập nhật bảng kết quả thực tế, lệnh chạy kiểm thử Windows PowerShell và hướng dẫn chi tiết | **ĐÃ ĐỒNG BỘ** |
| 9 | `requirements.txt` | Cập nhật đầy đủ các thư viện thực sự được dùng (torch, fastapi, uvicorn, python-docx, etc.) | **ĐÃ ĐỒNG BỘ** |

---

## 4. CÁC HẠN CHẾ CÒN TỒN TẠI (TRANSPARENCY & LIMITATIONS)

Nhóm công khai các giới hạn khách quan chưa giải quyết trong khuôn khổ đồ án:
1. **Phạm vi bài toán**: Mới chỉ tập trung vào nhận dạng chữ số đơn lẻ đã được phân đoạn (Isolated Digits), chưa tích hợp giải thuật phân đoạn chuỗi số dính liền (Connected Digits Segmentation).
2. **Kỹ thuật tăng cường dữ liệu cho CNN**: Chưa áp dụng Elastic Distortions hay CutMix trong pha huấn luyện CNN để đạt các mức độ chính xác cực hạn (> 99.6%).
3. **Chỉ mục k-NN**: k-NN hiện tại vẫn sử dụng tìm kiếm vét cạn (Brute-force Search) trong scikit-learn thay vì cấu trúc chỉ mục Approximate Nearest Neighbors (ANN) như FAISS hoặc HNSW.
