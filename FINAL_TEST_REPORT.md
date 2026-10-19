# BÁO CÁO KẾT QUẢ KIỂM THỬ HỆ THỐNG (FINAL_TEST_REPORT.md)
**Dự án: Nhận dạng chữ số viết tay (MNIST) — Nhóm 03 — Trường Đại học Thủy Lợi**  
**Môi trường thực thi: Windows 11 Pro 64-bit, Python 3.14.5, PowerShell 5.1/7.x**  
**Thời điểm chạy kiểm thử: 18/10/2026**

---

## 1. TỔNG HỢP KẾT QUẢ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Lệnh thực thi chính thức:
```powershell
python -m unittest -v tests/test_pipeline.py
```

Kết quả thực tế ghi nhận từ terminal:
```text
test_api_available_models (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_api_available_models) ... ok
test_api_predict_blank_image (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_api_predict_blank_image) ... ok
test_api_predict_invalid_model_raises_404 (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_api_predict_invalid_model_raises_404)
Verify that requesting a nonexistent model raises HTTP 404 (no silent fallback). ... ok
test_api_predict_sample_digit (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_api_predict_sample_digit) ... ok
test_api_predict_svm_deskew_pca (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_api_predict_svm_deskew_pca)
Verify that svm_deskew_pca endpoint works end-to-end. ... ok
test_center_of_mass_blank_canvas (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_center_of_mass_blank_canvas) ... ok
test_center_of_mass_stroke (tests.test_pipeline.TestBackendAPIAndPreprocessing.test_center_of_mass_stroke) ... ok
test_create_train_val_test_no_overlap (tests.test_pipeline.TestDataLoadingAndSplits.test_create_train_val_test_no_overlap) ... ok
test_load_mnist_data_shapes (tests.test_pipeline.TestDataLoadingAndSplits.test_load_mnist_data_shapes) ... ok
test_pixel_normalization_bounds (tests.test_pipeline.TestDataLoadingAndSplits.test_pixel_normalization_bounds) ... ok
test_stratified_subset_balance (tests.test_pipeline.TestDataLoadingAndSplits.test_stratified_subset_balance) ... ok
test_strict_zero_leakage_index_intersection (tests.test_pipeline.TestDataLoadingAndSplits.test_strict_zero_leakage_index_intersection)
Verify strict mathematical isolation: train indices intersect val indices is empty set. ... ok
test_deskew_image_shape_and_range (tests.test_pipeline.TestFeatureEngineering.test_deskew_image_shape_and_range) ... ok
test_hog_feature_length (tests.test_pipeline.TestFeatureEngineering.test_hog_feature_length) ... ok
test_pca_exact_components_ground_truth (tests.test_pipeline.TestFeatureEngineering.test_pca_exact_components_ground_truth)
Check exact PCA dimensions saved in checkpoints: 112 for deskewed subset, 154 for full 60k. ... ok
test_pca_transformer_dimensionality (tests.test_pipeline.TestFeatureEngineering.test_pca_transformer_dimensionality) ... ok
test_cnn_forward_dimensions (tests.test_pipeline.TestModelsAndCNN.test_cnn_forward_dimensions) ... ok
test_cnn_predict_proba_simplex (tests.test_pipeline.TestModelsAndCNN.test_cnn_predict_proba_simplex) ... ok
test_model_factory (tests.test_pipeline.TestModelsAndCNN.test_model_factory) ... ok

----------------------------------------------------------------------
Ran 19 tests in 1.000s

OK
[SERVER] Đang nạp các mô hình vào bộ nhớ...
  -> Đã nạp PCA Transformer (154 chiều)
  -> Đã nạp PCA Deskew Transformer (112 chiều)
  -> Đã nạp Modern CNN (99.19%)
  -> Đã nạp Modern CNN sub10k (97.60%)
  -> Đã nạp SVM RBF Deskew + PCA (98.03%)
  -> Đã nạp SVM RBF PCA
  -> Đã nạp k-NN PCA
  -> Đã nạp Random Forest
  -> Đã nạp Linear SVM
  -> Đã nạp Bernoulli Naive Bayes
  -> Đã nạp Gaussian Naive Bayes
  -> Đã nạp SVM HOG
[SERVER] Đã hoàn tất nạp 10 mô hình!
```

- **Tổng số test cases**: **19**
- **Số lượng PASS**: **19 / 19 (100%)**
- **Số lượng FAIL**: **0**
- **Số lượng ERROR**: **0**
- **Thời gian thực thi**: **1.000 giây**

---

## 2. KẾT QUẢ KIỂM THỬ TỪNG PHÂN TẦNG CHỨC NĂNG

### 2.1. Phân tầng Dữ liệu & Chống rò rỉ (Data Loading & Zero Leakage)
1. `test_load_mnist_data_shapes`: Xác nhận dữ liệu nạp từ tệp `.npz` có đúng kích thước `(60000, 28, 28)` cho train và `(10000, 28, 28)` cho test.
2. `test_pixel_normalization_bounds`: Giá trị pixel chuẩn hóa nằm chính xác trong $[0.0, 1.0]$, kiểu dữ liệu `np.float32`.
3. `test_stratified_subset_balance`: Trích xuất 1,000 mẫu subset đảm bảo chính xác 100 mẫu cho mỗi lớp chữ số.
4. `test_create_train_val_test_no_overlap`: Phân chia 50k train, 10k val, 10k test bảo toàn phân bố nhãn với độ lệch tuyệt đối $< 0.01$.
5. `test_strict_zero_leakage_index_intersection`: **Chốt chặn quan trọng**: Giao tập chỉ số giữa tập Train và Validation được chứng minh toán học là tập rỗng (`intersection = 0`).

### 2.2. Phân tầng Trích xuất Đặc trưng (Feature Engineering)
1. `test_deskew_image_shape_and_range`: Nắn thẳng bằng mô-men trung tâm bảo toàn kích thước 28x28 và miền giá trị không gian xám.
2. `test_pca_exact_components_ground_truth`: Xác nhận chính xác số chiều PCA trong các checkpoint: **112 chiều** đối với tập con nắn thẳng Deskew và **154 chiều** đối với tập toàn phần 60k.
3. `test_pca_transformer_dimensionality`: Khẳng định bộ biến đổi PCA giữ lại $\ge 95\%$ phương sai thông tin.
4. `test_hog_feature_length`: Bộ mô tả HOG trích xuất đúng véc-tơ 324 chiều.

### 2.3. Phân tầng Mô hình Học máy & Deep Learning (Models)
1. `test_model_factory`: Khởi tạo thành công 7 họ mô hình phân lớp (`gaussian_nb`, `bernoulli_nb`, `knn`, `linear_svm`, `rbf_svm`, `rf`, `cnn`).
2. `test_cnn_forward_dimensions`: Mạng Modern CNN lan truyền tiến qua các tầng Conv2D, MaxPool, BatchNorm và Dropout cho đầu ra kích thước chuẩn `(batch_size, 10)`.
3. `test_cnn_predict_proba_simplex`: Xác suất đầu ra thỏa mãn tính chất đơn giản xác suất (Simplex): $\sum_{c=0}^9 p_c = 1.0 \pm 10^{-5}$.

### 2.4. Phân tầng Backend API & Tiền xử lý Quang học (Backend & E2E)
1. `test_center_of_mass_blank_canvas`: Khi đưa vào ảnh trống, hàm căn tâm quang học phát hiện và trả về ma trận toàn số 0.
2. `test_center_of_mass_stroke`: Căn tâm quang học đưa nét viết bất đối xứng về chính xác tọa độ $(14, 14)$ của khung hình chuẩn NIST.
3. `test_api_available_models`: Endpoint `/api/models` trả về đầy đủ 10 mô hình kèm thông tin đặc trưng và độ chính xác đã xác minh.
4. `test_api_predict_blank_image`: Gửi ảnh canvas trống lên API nhận được phản hồi nhãn `-1` cùng thông báo hướng dẫn vẽ chữ số rõ ràng.
5. `test_api_predict_sample_digit`: Dự đoán ảnh mẫu chữ số 0 từ tập test trả về đúng nhãn phân lớp, độ tin cậy trong $[0, 1]$ và 10 phần tử xác suất.
6. `test_api_predict_invalid_model_raises_404`: **Sửa lỗi audit quan trọng**: Khi gửi tên mô hình không tồn tại, backend trả về mã lỗi HTTP 404 (không âm thầm fallback sang CNN).
7. `test_api_predict_svm_deskew_pca`: Kiểm thử end-to-end mô hình quán quân Nhóm A (`svm_deskew_pca`), xác nhận pipeline nắn thẳng + PCA 112D + SVM suy luận trả về kết quả chính xác.

---

## 3. KIỂM THỬ XUẤT TÀI LIỆU VÀ ĐO SỐ TRANG THỰC TẾ

### 3.1. Báo cáo Kỹ thuật Word (.docx) & PDF
- Lệnh chạy: `python src/export_report_docx.py`
- Lệnh kiểm tra và xuất PDF qua Microsoft Word COM:
```powershell
powershell -Command "
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$doc = $w.Documents.Open('D:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay\reports\Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx')
$pages = $doc.ComputeStatistics(2)
Write-Output ('Page count: ' + $pages)
$pdfPath = 'D:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay\reports\Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf'
$doc.SaveAs([ref]$pdfPath, [ref]17); $doc.Close([ref]0); $w.Quit()
"
```
- **Kết quả đo đạc chính thức**:
  - **Số trang thực tế**: **27 trang** (Đáp ứng chính xác yêu cầu 20–30 trang của Giảng viên).
  - Tệp PDF đã render hoàn chỉnh: `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`.

### 3.2. Slide thuyết trình PowerPoint (.pptx)
- Lệnh chạy: `python src/export_slides_pptx.py`
- Tệp xuất: `reports/Slide_Thuyet_Trinh_Nhom_03.pptx` (606.2 KB, 10 slides chuẩn 16:9 widescreen, đồng bộ 100% số liệu thực nghiệm).
