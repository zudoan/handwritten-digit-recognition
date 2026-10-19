# DANH MỤC KIỂM TRA TRƯỚC KHI NỘP BÀI (SUBMISSION_CHECKLIST.md)

**Học phần**: Nhận dạng mẫu — Đề tài 1: Nhận dạng chữ số viết tay trên bộ dữ liệu MNIST  
**Nhóm thực hiện**: Nhóm 03 — Trường Đại học Thủy Lợi  
**Kỳ học**: Học kỳ 1 — Năm học 2026–2027  

---

## 1. NHỮNG VIỆC CẦN LÀM THỦ CÔNG TRƯỚC KHI NỘP

Trước khi nộp bài hoặc in ấn, bạn (chủ project) chỉ cần hoàn thiện các mục thủ công sau:

1. **Điền thông tin thành viên và Giảng viên hướng dẫn**:
   - Mở file Word: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx`](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx)
   - Thay thế các placeholder:
     - `TS. [Họ và tên Giảng viên]` $\to$ Họ tên thầy/cô phụ trách.
     - `[Họ và tên Sinh viên 1] - MSSV: [Mã sinh viên 1]` $\to$ Thông tin Nhóm trưởng.
     - `[Họ và tên Sinh viên 2] - MSSV: [Mã sinh viên 2]` $\to$ Thành viên 2.
     - `[Họ và tên Sinh viên 3] - MSSV: [Mã sinh viên 3]` $\to$ Thành viên 3.
     - Kiểm tra Bảng 7.1 (Bảng phân công nhiệm vụ và tỷ lệ đóng góp).
   - Mở file PowerPoint: [`reports/Slide_Thuyet_Trinh_Nhom_03.pptx`](reports/Slide_Thuyet_Trinh_Nhom_03.pptx)
     - Slide 1: Cập nhật tên thành viên và GVHD tương ứng.

2. **Xuất lại PDF sau khi điền thông tin (nếu chỉnh sửa Word trực tiếp)**:
   - Chạy lệnh PowerShell:
     ```powershell
     powershell -ExecutionPolicy Bypass -File src/convert_to_pdf.ps1
     ```

3. **In ấn báo cáo (nếu giảng viên yêu cầu nộp bản cứng)**:
   - File in ấn: [`reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`](reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf) (Chuẩn 28 trang A4, căn lề đúng chuẩn ĐH Thủy Lợi).

4. **Đẩy mã nguồn lên GitHub**:
   - 130 files đã được stage sẵn vào Git Index. Chạy 2 lệnh:
     ```powershell
     git commit -m "feat(release): final submission release - sync checkpoints, web registry, docx/pdf 28p, pptx slides, and 28 tests"
     git push origin main
     ```

5. **Nộp liên kết GitHub và file lên Classroom/LMS**:
   - Link repository: `https://github.com/zudoan/handwritten-digit-recognition`
   - Đính kèm file PDF 28 trang và file PPTX 12 slides.

---

## 2. TRẠNG THÁI HỒ SƠ ĐÃ SẴN SÀNG 100%

- [x] **Báo cáo kỹ thuật Word (`.docx`)**: `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx` (2.45 MB, đầy đủ hình ảnh, bảng biểu).
- [x] **Báo cáo kỹ thuật PDF (`.pdf`)**: `reports/Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf` (**Đúng 28 trang**, 0 trang trống, 0 dòng mồ côi).
- [x] **Slide thuyết trình bảo vệ (`.pptx`)**: `reports/Slide_Thuyet_Trinh_Nhom_03.pptx` (**12 slides**, chia tách Nhóm A, B, C không bị tràn viền hay cắt bảng).
- [x] **Bộ kiểm thử tự động (Unit / Integration / Regression Tests)**: `tests/test_pipeline.py` (**28/28 tests PASS - 100%**).
- [x] **Ứng dụng Web tương tác thời gian thực**: `run_app.py` (FastAPI backend, nạp đúng Linear SVM C=0.01 và RF 150 cây, minh chứng lưu tại `reports/evidence/web/`).
- [x] **Bộ dữ liệu chuẩn MNIST**: Có sẵn tệp `data/mnist.npz` và script tự động tải `download_mnist.py`.
- [x] **Model Checkpoints**: Đầy đủ 27 checkpoints và transformers trong `saved_models/`.
