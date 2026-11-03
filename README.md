# Nhận dạng chữ số viết tay trên MNIST

Bài tập lớn học phần Nhận dạng mẫu, Nhóm 03, lớp S26-65TTNT.

- Đoàn Anh Vũ — 2351267280
- Nguyễn Hồng Nguyên — 2351267273

## Chạy web

Mở terminal tại thư mục gốc của repo:

```bash
python -m venv .venv
```

Kích hoạt môi trường:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Cài thư viện và khởi động:

```bash
python -m pip install -r requirements.txt
python run_app.py
```

Mở http://127.0.0.1:8000. Web có năm mô hình: CNN, SVM, k-NN, Random Forest và Bernoulli Naive Bayes.

Ảnh tải lên có thể dùng nét đen nền trắng, nét trắng nền đen hoặc PNG nền trong suốt. Ứng dụng chuẩn hóa nền ảnh trước khi đặt ảnh vào khung nhận dạng.

Khi nhận dạng ảnh tải lên, web gửi ảnh gốc tới backend để giữ màu và độ phân giải. Với ảnh chụp giấy, backend tách nét mực theo tương phản cục bộ, loại vùng nhiễu và điều chỉnh độ dày nét trước khi thu nhỏ. Mỗi ảnh chứa một chữ số chính. Bộ xử lý đã được điều chỉnh và kiểm tra trên bốn ảnh thực tế (5, 3, 5, 9); kết quả này không thay thế đánh giá trên một tập ảnh chụp độc lập.

`requirements-verified.txt` ghi phiên bản của môi trường CPU dùng để kiểm tra bộ mô hình này. Có thể cài tệp đó để chạy cùng phiên bản thư viện.

## Các tệp chính

| Tệp hoặc thư mục | Nội dung |
|---|---|
| `notebooks/01_EDA_Truc_Quan_MNIST.ipynb` | Kiểm tra dữ liệu, phân bố lớp/pixel, PCA, t-SNE, tương quan ảnh trung bình và cách chia tập |
| `notebooks/02_Tien_Xu_Ly_Train_MNIST.ipynb` | Tiền xử lý, huấn luyện năm mô hình, chỉ số sau từng mô hình, CM, ảnh CNN nhận sai và bảng so sánh cuối |
| `saved_models/` | Năm checkpoint, PCA, lịch sử CNN, dự đoán, bảng kết quả và cấu hình |
| `app/` | API FastAPI và giao diện web |
| `src/` | Nạp dữ liệu, xử lý đặc trưng và định nghĩa mô hình |
| `data/mnist.npz` | MNIST gồm 60.000 ảnh train gốc và 10.000 ảnh test chính thức |
| `run_app.py` | Khởi động web |
| `train_notebook_models.py` | Chạy các cell của notebook 02 bằng Python |
| `download_mnist.py` | Tải lại dữ liệu MNIST |
| `tests/` | Kiểm tra dữ liệu, mô hình, kết quả đã lưu và API |
| `reports/` | Báo cáo Word/PDF, slide 11 trang, bảng phân công riêng và hình kết quả |
| `docs/De_Bai_Cuoi_Ky.pdf` | Đề bài |

## Giao thức và kết quả

Mọi mô hình dùng **50.000 train / 10.000 validation / 10.000 test**, chia có phân tầng với seed 42. Tập test chính thức giữ riêng. Naive Bayes và Random Forest dùng pixel [0, 1]. k-NN/SVM dùng Deskew rồi PCA giữ 95% phương sai, fit trên train 50.000 ảnh và còn **113 chiều**. CNN nhận tensor 1 × 28 × 28.

PCA trong EDA mô tả 60.000 ảnh train gốc, chưa Deskew, nên còn **154 chiều**. PCA này phục vụ khám phá dữ liệu và không dùng cho k-NN/SVM.

| Mô hình | Accuracy (%) | Precision (%) | Recall (%) | F1 (%) | Số ảnh sai |
|---|---:|---:|---:|---:|---:|
| Naive Bayes | 84,46 | 84,58 | 84,20 | 84,27 | 1.554 |
| k-NN | 98,06 | 98,06 | 98,04 | 98,05 | 194 |
| SVM | 98,79 | 98,78 | 98,79 | 98,78 | 121 |
| Random Forest | 96,99 | 96,98 | 96,97 | 96,97 | 301 |
| CNN | 99,44 | 99,43 | 99,43 | 99,43 | 56 |

Precision, Recall và F1 là trung bình macro trên 10 lớp. Các chỉ số lấy trên cùng 10.000 ảnh test.

CNN có **160.074 tham số**, Adam LR đầu 0,001, weight decay 0,0001, batch train/validation 64/256. ReduceLROnPlateau giảm LR theo validation loss với factor 0,5, patience 1, min LR 0,00001. Early stopping có patience 3 và min_delta 0,0001.

Giới hạn đầu là **70 epoch**, tăng thêm 20 nếu chưa dừng sớm. Lần chạy trong bộ kết quả này **dừng tại epoch 23**, khôi phục **checkpoint epoch 20**, validation loss **0,0218**, validation accuracy **99,41%**. Checkpoint tốt nhất được chọn theo validation loss.

Web đọc chỉ số từ `saved_models/results.csv` và thông tin checkpoint từ `saved_models/selected_config.json`, đồng thời nạp trọng số và PCA trong cùng thư mục. SVM trả điểm từ decision_function khi không có predict_proba. Các điểm tin cậy chưa qua hiệu chuẩn xác suất.

## Huấn luyện

Mở notebook 02 rồi chọn **Run All**, hoặc chạy:

```bash
python train_notebook_models.py
```

Trong repo này, notebook và script đều lưu mô hình vào `saved_models/`. Khi chạy notebook riêng trên Colab/Kaggle, đầu ra nằm trong `mnist_best_models/`. Mỗi mô hình có một cell huấn luyện. CNN in log từng epoch. Naive Bayes, k-NN, SVM và Random Forest dùng lệnh fit theo thuật toán riêng, không có epoch theo cách huấn luyện CNN.

Huấn luyện mới có thể cho kết quả khác khi thay đổi thiết bị hoặc thư viện. Bảng trên mô tả lần chạy đã lưu. Sau khi thay checkpoint, khởi động lại web để nạp mô hình và chỉ số mới.

## Kiểm thử

```bash
python -m unittest tests.test_pipeline -v
```

Kiểm tra xử lý pixel ảnh upload ở frontend, nếu có Node.js:

```bash
node tests/test_upload_pixels.js
```

Bộ kiểm thử dùng năm mô hình hiện tại, đối chiếu dự đoán với CSV, kiểm tra lịch sử và checkpoint CNN, metadata web và đường dự đoán SVM khi predict_proba không khả dụng.

Bảng phân công nằm riêng trong `reports/Bang_Phan_Cong_Cong_Viec_Nhom_03.docx`. Báo cáo và slide dùng TP. Hồ Chí Minh. Gói chỉ giữ một bộ mô hình chính, hai notebook và các tệp phục vụ chạy, trình bày, kiểm tra bài làm.
