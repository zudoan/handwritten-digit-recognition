# 🔒 THƯ MỤC LƯU TRỮ & KHÓA PHIÊN BẢN CŨ (ARCHIVE LEGACY)

Thư mục này được tạo nhằm gom toàn bộ các tệp tin, mô hình và kịch bản **không còn tham gia vào phiên bản hiện tại** của dự án để khóa lại và lưu trữ an toàn, đảm bảo thư mục gốc và các thư mục chính (`saved_models/`, `src/`, `notebooks/`) hoàn toàn tinh gọn và chỉ chứa các thành phần của phiên bản chuẩn mới nhất.

---

## Cấu trúc lưu trữ:

### 1. `models/` (27 mô hình cũ)
Chứa toàn bộ các checkpoint cũ từ các lần thử nghiệm trước (baseline 10k mẫu, mô hình cũ chưa nắn thẳng Deskewing hoặc chưa chuẩn hóa theo Notebook 02):
- `modern_cnn_mnist.pt`, `modern_cnn_mnist_sub10k.pt`, `modern_cnn_val_tuned.pt`
- `svm_linear_raw.joblib`, `svm_linear_sub10k.joblib`, `svm_rbf_pca.joblib`, `svm_rbf_deskew_pca.joblib`, v.v.
- `knn_pca_k3.joblib`, `knn_raw_k3.joblib`, `knn_pca_sub10k.joblib`, v.v.
- `rf_sub10k.joblib`, `random_forest_raw.joblib`
- `bnb_sub10k.joblib`, `bernoulli_nb_bin.joblib`, `gnb_sub10k.joblib`, `gaussian_nb_raw.joblib`
- Các bộ biến đổi PCA cũ (`pca_transformer.joblib`, `pca_transformer_sub10k.joblib`, v.v.)

### 2. `notebooks/` (2 notebook cũ)
- `01_eda_and_data_analysis.ipynb` (Phiên bản EDA ban đầu)
- `02_models_and_benchmark.ipynb` (Phiên bản huấn luyện cũ trên subset 10k)

### 3. `scripts/` (Các script huấn luyện/phân tích cũ)
- Các file script huấn luyện, điều chỉnh siêu tham số và trích xuất số liệu cũ từ các phiên bản phát triển trước đó (`train_and_benchmark.py`, `train_cnn_with_validation.py`, `tune_hyperparameters.py`, v.v.).

---

> **Lưu ý:** Toàn bộ hệ thống Web demo và ứng dụng suy luận hiện tại chỉ sử dụng các mô hình chuẩn được lưu tại `saved_models/` và mã nguồn chuẩn tại `src/`.

