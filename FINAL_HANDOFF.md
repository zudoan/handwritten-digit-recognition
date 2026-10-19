# TÀI LIỆU BÀN GIAO TOÀN DIỆN DỰ ÁN (FINAL_HANDOFF.md)
**Dành cho: Sinh viên / Chủ project — Nhóm 03**  
**Môn học: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay trên MNIST**  
**Đơn vị: Khoa Công nghệ Thông tin — Trường Đại học Thủy Lợi**

---

## 1. TỔNG KẾT TRẠNG THÁI HOÀN THÀNH DỰ ÁN

Dự án đã trải qua vòng kiểm định kỹ thuật cuối cùng (Final Technical Audit & Fix), khắc phục triệt để các tồn đọng về số liệu, phương pháp luận thực nghiệm, chất lượng kiểm thử và độ dài tài liệu bàn giao. Toàn bộ các tiêu chí đều đạt trạng thái sẵn sàng nghiệm thu:

- **Độ tin cậy số liệu**: 100% đồng bộ giữa mã nguồn, checkpoint, tệp JSON (`verified_experiments.json`), Báo cáo Word, Báo cáo PDF, Slide PowerPoint và README.
- **Mô hình chính thức Modern CNN**: Đạt **99.19% Accuracy**, **99.18% Macro F1**, chỉ sai **81/10.000** ảnh kiểm thử (Checkpoint: `saved_models/modern_cnn_mnist.pt`).
- **Mô hình quán quân Nhóm A (Đặc trưng)**: **SVM RBF Deskew + PCA** (112 chiều) đạt **97.97% Accuracy**, **97.96% Macro F1** (chỉ sai 203 ảnh / 10k test) trên tập con 10k mẫu (Checkpoint: `saved_models/svm_rbf_deskew_pca_pipeline.joblib` và `saved_models/svm_rbf_deskew_pca_sub10k.joblib`).
- **Báo cáo Kỹ thuật Word & PDF**: Đã mở rộng hoàn chỉnh 7 chương khoa học sâu sắc, đo lường thực tế qua Microsoft Word COM đạt chính xác **27 trang** (thỏa mãn yêu cầu 20–30 trang).
- **Bộ kiểm thử tự động**: 22/22 test cases PASS (100%), chứng minh Zero Data Leakage, kiểm soát toàn diện lỗi backend và kiểm tra hồi quy reload checkpoint.

---

## 2. CÁC TỆP BÀN GIAO QUAN TRỌNG NHẤT

### 2.1. Tài liệu báo cáo và Slide nộp giảng viên
1. [Báo cáo Word chính thức (.docx)](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx) — 27 trang.
2. [Báo cáo PDF chính thức (.pdf)](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf) — Đã xuất sẵn từ Microsoft Word.
3. [Slide thuyết trình bảo vệ (.pptx)](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/reports/Slide_Thuyet_Trinh_Nhom_03.pptx) — 10 slides chuẩn 16:9 widescreen.
4. [Bảng phân công nhiệm vụ nhóm](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/reports/BANG_PHAN_CONG_CONG_VIEC.md).

### 2.2. Dữ liệu thực nghiệm và tài liệu kiểm định
1. [results/verified_experiments.json](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/results/verified_experiments.json) — Cơ sở dữ liệu 12 cấu hình thực nghiệm đã xác minh.
2. [FINAL_AUDIT_REPORT.md](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/FINAL_AUDIT_REPORT.md) — Chi tiết các lỗi đã phát hiện và sửa chữa.
3. [FINAL_EXPERIMENT_RESULTS.md](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/FINAL_EXPERIMENT_RESULTS.md) — Bảng kết quả thực nghiệm và lịch sử validation.
4. [EXPERIMENT_PROTOCOL.md](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/EXPERIMENT_PROTOCOL.md) — Giao thức thực nghiệm đối chứng đơn biến.
5. [RUBRIC_FINAL_CHECK.md](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/RUBRIC_FINAL_CHECK.md) — Bảng đối chiếu tiêu chí chấm điểm 9đ + 1đ thưởng.
6. [FINAL_TEST_REPORT.md](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/FINAL_TEST_REPORT.md) — Báo cáo kết quả chạy 22 test cases.

---

## 3. HƯỚNG DẪN THỰC THI CHO CHỦ PROJECT TRÊN WINDOWS POWERSHELL

Mở **PowerShell** tại thư mục gốc của dự án (`d:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay`), thực thi các lệnh sau:

### 3.1. Chạy ứng dụng Web Demo tương tác (Phục vụ trình diễn trước Giảng viên)
```powershell
python run_app.py
```
- Mở trình duyệt web truy cập: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Trải nghiệm vẽ chữ số trên Canvas, chọn mô hình trong dropdown, hoặc bấm vào 10 mẫu test chuẩn bên dưới để xem suy luận thời gian thực và biểu đồ phân bố xác suất.

### 3.2. Chạy toàn bộ bộ kiểm thử tự động (19/19 tests)
```powershell
python -m unittest -v tests/test_pipeline.py
```

### 3.3. Xuất lại Báo cáo Word 27 trang và Slide PowerPoint (Nếu có thay đổi)
```powershell
# Tạo Báo cáo Word
python src/export_report_docx.py

# Xuất sang PDF và đo số trang qua Microsoft Word COM
powershell -Command "
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$doc = $w.Documents.Open('D:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay\reports\Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx')
Write-Output ('So trang thuc te: ' + $doc.ComputeStatistics(2))
$pdf = 'D:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay\reports\Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf'
$doc.SaveAs([ref]$pdf, [ref]17); $doc.Close([ref]0); $w.Quit()
"

# Tạo Slide PowerPoint
python src/export_slides_pptx.py
```

---

## 4. NHỮNG VIỆC CHỦ PROJECT CẦN TỰ HOÀN THIỆN TRƯỚC KHI NỘP

1. **Điền thông tin cá nhân**:
   - Mở file `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx` hoặc chỉnh sửa trong `src/export_report_docx.py` để điền họ tên, mã số sinh viên của 3 thành viên Nhóm 03 và tên Giảng viên hướng dẫn trên trang bìa và Bảng phân công nhiệm vụ.
   - Làm tương tự trên Slide 1 của `reports/Slide_Thuyet_Trinh_Nhom_03.pptx`.
2. **Xác nhận duyệt đề tài với Giảng viên**:
   - Theo đề cương học phần, sinh viên cần xác nhận nguồn dữ liệu và đề tài với giảng viên bộ môn. Hãy chủ động trao đổi với thầy/cô hướng dẫn.
3. **Nén tệp nộp bài**:
   - Tệp `.zip` nộp bài nên bao gồm mã nguồn, báo cáo `.docx`, báo cáo `.pdf`, slide `.pptx`, các checkpoints trong `saved_models/` và tệp dữ liệu `data/mnist.npz`.
