# BÁO CÁO AUDIT KỸ THUẬT VÀ PHÂN TÍCH LỖI DỰ ÁN (PROJECT_AUDIT_REPORT.md)
**Dự án: Nhận dạng chữ số viết tay (MNIST) — Môn Nhận dạng mẫu**  
**Nhóm 03 — Trường Đại học Thủy Lợi**

---

## 1. TỔNG QUAN KẾT QUẢ AUDIT

Báo cáo audit này được thực hiện theo tiêu chuẩn kiểm định phần mềm khoa học dữ liệu và đối chiếu trực tiếp với thang điểm chính thức trong tệp `BÀI TẬP LOỚN CUỐI KỲ.pdf`.

Mục tiêu cốt lõi của nghiên cứu là trả lời câu hỏi:
> **"Đặc trưng và thuật toán nào giúp phân biệt các chữ số hiệu quả nhất?"**

---

## 2. BẢNG TỔNG HỢP CÁC VẤN ĐỀ VÀ LỖI KỸ THUẬT PHÁT HIỆN

| ID | Vấn đề / Lỗi phát hiện | Mức độ | Vị trí tệp / Code | Nguyên nhân kỹ thuật | Hướng xử lý | Trạng thái |
|:---:|:---|:---:|:---|:---|:---|:---:|
| **ERR-01** | **So sánh đặc trưng & thuật toán không công bằng (*Unfair Benchmark*)** | **CRITICAL** | `src/train_and_benchmark.py` (L256-L368), `BAO_CAO_CHI_TIET_PROJECT.md` | k-NN Raw dùng 10,000 mẫu còn k-NN PCA dùng 60,000 mẫu; SVM HOG dùng 10,000 mẫu còn SVM PCA dùng 60,000 mẫu. Mọi kết luận cho rằng PCA hay HOG vượt trội hơn là thiếu cơ sở khoa học vì cỡ mẫu huấn luyện thay đổi $6\times$. | Tách benchmark thành 2 nhóm rõ ràng: **Nhóm A (Khảo sát đặc trưng)** trên cùng tập con cố định (cùng 10k mẫu train, 10k test); **Nhóm B (Khảo sát thuật toán)** trên cùng tập con hoặc cùng tập toàn phần; tách biệt kết quả trên tập full 60k. | Đã xác định |
| **ERR-02** | **Áp dụng sai không gian PCA cho dữ liệu nắn thẳng (*PCA Domain Mismatch*)** | **HIGH** | `src/train_and_benchmark.py` (L279) | Mô hình `svm_rbf_deskew_pca` áp dụng `pca.transform(x_sub_deskewed)` trong khi `pca` được fit trên dữ liệu ảnh thô chưa nắn thẳng. Dữ liệu nắn thẳng có các trục phương sai khác với ảnh gốc. | Fit riêng một `PCATransformer` trên tập dữ liệu đã nắn thẳng (*deskewed train set*) hoặc đóng gói thành Pipeline nhất quán. | Đã xác định |
| **ERR-03** | **Thiếu tập Validation độc lập trong quá trình thực nghiệm** | **HIGH** | `src/train_and_benchmark.py` | Toàn bộ script huấn luyện trên train và đánh giá trực tiếp trên test set 10,000 ảnh mà không qua validation set để chọn siêu tham số (như C, gamma, k, n_estimators). | Thiết lập phân chia chuẩn: Train (50,000), Validation (10,000), Test (10,000) từ 60k train gốc theo phân tầng cố định `random_state=42`. | Đã xác định |
| **ERR-04** | **Xác suất giả lập không có cơ sở (*Uncalibrated Pseudo-probabilities*)** | **HIGH** | `app/server.py` (L270-L273) | Web API áp dụng hàm Softmax tùy tiện lên giá trị `decision_function` của Linear/RBF SVM để hiển thị xác suất phần trăm: `exp_d = np.exp(decision - np.max(decision)); probs = exp_d / np.sum(exp_d)`. Đây không phải là phân phối xác suất thực tế. | Sử dụng mô hình có `probability=True` (Platt Scaling) hoặc hiển thị điểm quyết định (decision score) đúng bản chất toán học, không ngụy tạo xác suất. | Đã xác định |
| **ERR-05** | **Số liệu thống kê Entropy bị lệch trong tài liệu báo cáo** | **MEDIUM** | `BAO_CAO_CHI_TIET_PROJECT.md`, `src/generate_tables.py` | Báo cáo cũ ghi Train Shannon Entropy đạt $3.3210$ bits (cân bằng 99.97%), trong khi tính toán chính xác trên 60,000 mẫu là **$3.3199$ bits (cân bằng $99.94\%$)**. Khác biệt tuy nhỏ nhưng ảnh hưởng đến tính trung thực khoa học. | Tính toán lại chính xác và cập nhật đồng bộ toàn bộ bảng biểu, văn bản báo cáo. | Đã xác định |
| **ERR-06** | **Web Demo thiếu hỗ trợ các mô hình đã huấn luyện** | **MEDIUM** | `app/server.py` (L103-L170) | Chỉ nạp 4 mô hình: CNN, SVM RBF PCA, k-NN PCA, Gaussian NB. Thiếu Bernoulli NB, Random Forest, SVM Linear, SVM HOG; đồng thời pipeline web thiếu bước trích xuất đặc trưng HOG nếu người dùng chọn model HOG. | Bổ sung nạp đủ các mô hình đã đối chuẩn, tích hợp transformer tương ứng (HOG, Deskew, PCA) theo pipeline tự động. | Đã xác định |
| **ERR-07** | **Thiếu hệ thống kiểm thử tự động (*Automated Testing Suite*)** | **MEDIUM** | Toàn bộ repository | Chưa có bất kỳ tệp `tests/` hay kịch bản `pytest` nào để kiểm tra tính toàn vẹn dữ liệu, kích thước tensor, tiền xử lý, tính tương thích của API và checkpoint mô hình. | Xây dựng bộ test toàn diện: unit tests (data, shapes, transformers, models) và integration tests (API, Canvas preprocessing). | Đã xác định |
| **ERR-08** | **Đường dẫn tuyệt đối trong tài liệu báo cáo** | **LOW** | `BAO_CAO_CHI_TIET_PROJECT.md` | Một số đường dẫn có tiền tố tuyệt đối `d:/Thuy_Loi/...` làm giảm tính di động khi chạy trên máy khác. | Chuẩn hóa toàn bộ đường dẫn relative hoặc sử dụng `pathlib.Path` xuyên suốt. | Đã xác định |

---

## 3. KẾ HOẠCH HÀNH ĐỘNG SỬA LỖI (REMEDIATION PLAN)

1. **Giai đoạn 2 (Correctness & Pipeline)**:
   - Sửa `src/data_loader.py` đảm bảo phân chia phân tầng chuẩn: Train (50,000), Validation (10,000) và giữ nguyên Test (10,000) của MNIST.
   - Sửa `src/features.py`: Đảm bảo `PCATransformer`, `DeskewTransformer` hoạt động hoàn toàn theo chuẩn Scikit-learn Pipeline (không rò rỉ dữ liệu).
   - Thiết kế quy trình huấn luyện SVM có xác suất được hiệu chuẩn (hoặc xuất score thực tế).
2. **Giai đoạn 3 (Controlled Experiments)**:
   - Viết lại quy trình benchmark trong `src/train_and_benchmark.py`:
     - **Nhóm A (Khảo sát đặc trưng)**: Cố định mô hình SVM RBF ($C=5.0$) trên cùng tập huấn luyện phân tầng 10,000 mẫu, so sánh 4 không gian: (1) Raw Pixels 784D, (2) Deskewed 784D, (3) PCA 154D (fit trên train), (4) HOG 324D, (5) Deskewed + PCA 154D (fit trên deskewed train).
     - **Nhóm B (Khảo sát thuật toán)**: Cố định tập dữ liệu, so sánh Gaussian NB, Bernoulli NB, k-NN ($k=3$), Linear SVM, RBF SVM, Random Forest.
     - **Nhóm C (Mô hình Deep Learning nâng cao)**: Modern CNN trên tập dữ liệu ảnh 2D, đối chiếu với mô hình ML tốt nhất và giải thích sự khác biệt cơ bản về việc tự động học đặc trưng.
3. **Giai đoạn 4 (Application & Web Demo)**:
   - Sửa `app/server.py` để hỗ trợ đầy đủ các mô hình có trong benchmark.
   - Chuẩn hóa tiền xử lý và trả về xác suất hoặc score chính xác.
4. **Giai đoạn 5 (Documentation & Reports)**:
   - Cập nhật số liệu chuẩn xác vào `EXPERIMENT_RESULTS.md`, `BAO_CAO_CHI_TIET_PROJECT.md`, báo cáo Word và Slide PowerPoint.
5. **Giai đoạn 6 (Testing & Rubric Compliance)**:
   - Viết bộ test `tests/test_pipeline.py` và chạy xác minh tự động.
   - Lập tài liệu `RUBRIC_COMPLIANCE.md`.
