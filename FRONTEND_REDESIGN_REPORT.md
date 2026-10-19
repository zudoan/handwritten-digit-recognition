# BÁO CÁO NÂNG CẤP VÀ THIẾT KẾ LẠI GIAO DIỆN FRONTEND (CHUSOVIETTAY)

**Dự án:** Nhận dạng chữ số viết tay trên bộ dữ liệu MNIST  
**Môn học:** Nhận dạng mẫu — Đề tài 1  
**Nhóm thực hiện:** Nhóm 03 — Đại học Thủy Lợi  
**Thời gian thực hiện:** Tháng 10/2026  
**Art Direction:** *Premium Soft Glass + Editorial Minimalism + Interactive Creative Workspace*  

---

## 1. DANH SÁCH CÁC FILE FRONTEND ĐÃ CHỈNH SỬA

| STT | Tệp tin | Vai trò kỹ thuật & Thay đổi chính |
|:---:|:---|:---|
| 1 | [app/static/index.html](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/app/static/index.html) | Tái cấu trúc toàn diện bố cục theo hướng Humanist Editorial & Studio Workspace: Floating Glass Bar, Precision Canvas Frame với vạch căn góc cơ học (`corner-mark`), Stroke Preset Pills (14px, 20px, 28px), Model Metadata Specs Bar, Prediction Digit Showcase với hiệu ứng xung lực vi mô, Palette mẫu MNIST Test Set dạng phím bấm cảm ứng, Bảng đối chuẩn 10 mô hình học máy và giải trình quang học NIST Center of Mass. Bảo toàn 100% các ID phần tử kiểm thử tự động. |
| 2 | [app/static/style.css](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/app/static/style.css) | Xây dựng hệ thống Design Tokens CSS Variables hoàn chỉnh: Bảng màu ngà ấm (`#F7F6F1`), kính mờ khuếch tán bán trong suốt (`rgba(255, 255, 255, 0.76)`), chữ than chì sâu (`#1A201D`), điểm nhấn xanh xô thơm hữu cơ (`#335041` / `#567866`), hệ thống bóng đổ đa tầng khuếch tán mềm (`box-shadow`), hiệu ứng khúc xạ kính `backdrop-filter: blur(24px)`, hỗ trợ media queries responsive 4 cấp độ và `prefers-reduced-motion`. |
| 3 | [app/static/app.js](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/app/static/app.js) | Cải tiến logic tương tác mượt mà: Đồng bộ 2 chiều giữa Stroke Presets và thanh trượt độ đậm nét vẽ, tự động trích xuất và hiển thị siêu dữ liệu mô hình thực tế (`modelMetaBar`) từ Model Registry, xử lý tọa độ vẽ chính xác theo tỉ lệ thực của canvas (`getCanvasCoordinates`), animation xung lực mượt mà cho kết quả dự đoán, cuộn mượt đến bảng đối chuẩn benchmark, loại bỏ hoàn toàn hiện tượng layout shift và giật khung hình. |

---

## 2. ART DIRECTION & DESIGN SYSTEM LỰA CHỌN

Khác biệt hoàn toàn với các giao diện dark-mode neon AI sáo mòn, giao diện mới được xây dựng theo phong cách:

### **"Premium Soft Glass + Editorial Minimalism + Interactive Creative Workspace"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 03  CHỮ SỐ VIẾT TAY (Nhóm 03 · TLU)            ● Sẵn sàng   Đối chuẩn [▼]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ PATTERN RECOGNITION STUDIO / MNIST DATASET                                  │
│ Viết một con số. Khám phá cách máy tính nhận dạng.                          │
│                                                                             │
│ ┌───────────────────────────────┐     ┌───────────────────────────────────┐ │
│ │ 1  Bảng vẽ kỹ thuật số   [Xóa]│     │ 2  Kết quả phân lớp               │ │
│ │  ┌─────────────────────────┐  │     │ Mô hình: [ Modern CNN (99.19%)  ] │ │
│ │  │ ┌                     ┐ │  │     │ [Đặc trưng: Conv] [Acc: 99.19%]   │ │
│ │  │          (Canvas)       │  │     │ ┌───────────────┐ ┌─────────────┐ │ │
│ │  │ └                     ┘ │  │     │ │ Dự đoán:  0   │ │ 28×28 NIST  │ │ │
│ │  └─────────────────────────┘  │     │ └───────────────┘ └─────────────┘ │ │
│ │ Nét: (Mảnh) (Chuẩn) (Đậm) ──●─│     │ Phân bố xác suất 10 lớp:          │ │
│ │ [ Nhận dạng ngay ] [Tải ảnh]  │     │ 0: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%    │ │
│ │ Mẫu chuẩn: [0][1][2][3][4]... │     │ 1..9: ░░░░░░░░░░░░░░░░░░░   0%    │ │
│ └───────────────────────────────┘     └───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Hệ thống Design Tokens (CSS Variables)

- **Màu nền chủ đạo (`--color-bg-base`):** `#F7F6F1` — Sắc ngà ấm (Warm Ivory), mang lại cảm giác tinh tế, thị giác êm dịu, không gây mỏi mắt.
- **Mặt phẳng kính mờ (`--color-surface-glass`):** `rgba(255, 255, 255, 0.76)` kết hợp viền mờ `rgba(255, 255, 255, 0.95)` và `backdrop-filter: blur(24px)` tạo chiều sâu hữu cơ, sạch sẽ.
- **Màu chữ chính (`--color-text-main`):** `#1A201D` — Than chì sâu (Deep Charcoal), độ tương phản cao đạt chuẩn WCAG AAA trên nền sáng.
- **Màu chữ phụ (`--color-text-muted`):** `#5E6762` — Xám đá trung tính.
- **Màu điểm nhấn (`--color-accent`):** `#335041` — Xanh xô thơm trầm (Deep Sage Green), tượng trưng cho độ chính xác và tính học thuật cao.
- **Khung Canvas vẽ (`--color-canvas-bg`):** `#111413` — Nền đen tuyền nhung mịn, tạo độ tương phản cực đại cho nét cọ trắng `#FFFFFF` đúng quy chuẩn nhị phân MNIST.
- **Bóng đổ đa tầng:** Phối hợp 3 lớp đổ bóng khuếch tán vi mô:
  `box-shadow: 0 4px 6px -1px rgba(26, 32, 29, 0.03), 0 20px 40px -12px rgba(26, 32, 29, 0.08), 0 0 0 1px rgba(26, 32, 29, 0.04)`.

---

## 3. HỆ THỐNG MOTION DESIGN & ANIMATIONS CÓ CHỦ ĐÍCH

Tất cả các chuyển động đều tuân thủ nguyên lý tự nhiên, phục vụ trải nghiệm người dùng, thời lượng từ 150ms đến 350ms:

1. **Hiệu ứng xuất hiện trang (Entrance Stagger Reveal):**
   - Header, Hero, Workspace và Benchmark Drawer xuất hiện tuần tự với hiệu ứng `cubic-bezier(0.16, 1, 0.3, 1)` kết hợp fade-in và dịch chuyển nhẹ $12\text{px}$ theo trục Y trong $0.45\text{s}$.
2. **Micro-interactions trên Buttons & Cards:**
   - Các nút bấm có hiệu ứng nhấn nhẹ (`transform: scale(0.985)` trong $150\text{ms}$) và đổi bóng mềm khi hover (`translateY(-1px)`).
   - Nút xóa bảng vẽ tạo rung vi mô phản hồi xúc giác nhẹ (`scale(0.995)`).
3. **Hiệu ứng thay đổi chữ số phân loại (Digit Transition Pulse):**
   - Khi có kết quả dự đoán mới từ API, chữ số khổng lồ `#predictedDigit` thực hiện hiệu ứng xung lực vi mô (`digitEntrance` keyframes: scale từ $0.94$ lên $1.0$, độ mờ tăng từ $0.4$ lên $1.0$) trong $0.22\text{s}$.
4. **Biểu đồ xác suất động (Horizontal Probability Morphing):**
   - Thanh xác suất của lớp chiến thắng tự động chuyển màu sang `--color-accent` và nở rộng mượt mà với `transition: width 0.32s cubic-bezier(0.2, 0.8, 0.2, 1)`.
5. **Hỗ trợ `prefers-reduced-motion`:**
   - Khi người dùng bật chế độ giảm chuyển động trong hệ điều hành, tất cả các transition và keyframes tự động hạ thời gian về $0.01\text{ms}$ để tránh gây khó chịu thị giác.

---

## 4. CẢI TIẾN TRẢI NGHIỆM NGƯỜI DÙNG (UX ENHANCEMENTS)

1. **Precision Canvas Frame:** Canvas vẽ được bao bọc bởi khung đo kỹ thuật số với 4 vạch căn góc cơ học (`corner-mark`), giúp người dùng dễ dàng định vị vùng vẽ trung tâm.
2. **Stroke Preset Pills (Mảnh 14 / Chuẩn 20 / Đậm 28):** Cho phép người dùng chuyển nhanh độ dày nét vẽ chỉ bằng 1 cú nhấp chuột thay vì phải kéo thanh trượt thủ công.
3. **Live Model Specs Bar:** Khi chọn bất kỳ mô hình nào từ dropdown, thanh thông số (`modelMetaBar`) lập tức hiển thị rõ:
   - *Không gian đặc trưng:* (ví dụ: `Learned Conv (28×28)` hoặc `Deskewing + PCA (112D)`).
   - *Kích thước tập huấn luyện:* (ví dụ: `60,000 mẫu` hoặc `10,000 mẫu`).
   - *Độ chính xác đối chuẩn:* (ví dụ: `99.19%`).
   - *Nhãn xác thực:* Huy hiệu `VERIFIED BENCHMARK` xanh lá phân biệt rõ với các mô hình tham chiếu legacy.
4. **Palette Mẫu Test Chuẩn NIST (Digits 0–9):** Người dùng có thể nhấp trực tiếp vào 10 chữ số thực tế trích xuất từ tập MNIST Test để kiểm thử ngay lập tức mà không cần tự vẽ.
5. **Bảng Đối Chuẩn 10 Mô Hình Học Máy:** Đặt ngay trong giao diện với xếp hạng huy chương rõ ràng, độ chính xác thực nghiệm, số lượng mẫu sai trên 10.000 ảnh kiểm thử và độ trễ suy luận tính bằng mili-giây.

---

## 5. CÁC ENDPOINT VÀ CHỨC NĂNG ĐÃ KIỂM THỬ THÀNH CÔNG

| Endpoint / Luồng tương tác | Phương thức | Kết quả kiểm thử | Ghi chú kỹ thuật |
|:---|:---:|:---:|:---|
| `GET /` | HTTP | **PASS (200 OK)** | Giao diện mới tải đầy đủ HTML/CSS/JS, không có lỗi console |
| `GET /api/models` | HTTP | **PASS (200 OK)** | Trả về đủ 12 mô hình từ Model Registry với đầy đủ metadata |
| `GET /api/samples` | HTTP | **PASS (200 OK)** | Trả về 10 ảnh mẫu test chuẩn hóa từ MNIST Test Set |
| `POST /api/predict` (Canvas vẽ tự do) | HTTP | **PASS (200 OK)** | Dự đoán đúng chữ số, tính đúng độ trễ (`latency_ms`) |
| `POST /api/predict` (Mẫu test 0) | HTTP | **PASS (200 OK)** | Nhận diện chính xác chữ số `0`, xác suất 100.0% |
| `POST /api/predict` (Mẫu test 7) | HTTP | **PASS (200 OK)** | Nhận diện chính xác chữ số `7`, xác suất 100.0% |
| Chuyển mô hình sang `svm_deskew_pca` | UI / API | **PASS** | Tự động dự đoán lại ngay lập tức với estimator mới |
| Xóa bảng vẽ (`btnClear`) | DOM | **PASS** | Canvas trở về đen tuyền, kết quả reset về trạng thái chờ |
| Tải ảnh từ máy tính (`imageUpload`) | DOM / FileReader | **PASS** | Tự động căn giữa và co dãn đúng tỷ lệ khung hình |

---

## 6. BẰNG CHỨNG THỰC NGHIỆM THỊ GIÁC (VISUAL EVIDENCE)

Toàn bộ quá trình kiểm thử tự động trên trình duyệt thật đã được ghi hình và lưu trữ tại thư mục [reports/evidence/web/](file:///d:/Thuy_Loi/Nam_4/nhan_dang_mau/ChuSoVietTay/reports/evidence/web/):

1. **Tổng quan giao diện mới (Warm Ivory & Soft Glass):**  
   `reports/evidence/web/redesign_overview.png`  
   *Mô tả:* Giao diện mang đậm tính học thuật, thoáng đãng, màu ngà ấm sang trọng, phân cấp thị giác rõ ràng giữa bảng vẽ và bảng phân tích kết quả.
2. **Nhận dạng mẫu chữ số 0:**  
   `reports/evidence/web/sample_0_prediction.png`  
   *Mô tả:* Chữ số 0 hiển thị khổng lồ, sắc nét; ảnh căn tâm $28\times 28$ chuẩn NIST hiển thị trực quan; thanh xác suất lớp 0 đạt 100.0%.
3. **Chuyển đổi mô hình sang SVM Deskew + PCA:**  
   `reports/evidence/web/svm_deskew_prediction.png`  
   *Mô tả:* Huy hiệu đặc trưng cập nhật thành *Deskewing + PCA (112D)*, tập huấn luyện 10.000 mẫu, độ chính xác 97.97%.
4. **Xóa bảng vẽ về trạng thái ban đầu:**  
   `reports/evidence/web/canvas_cleared.png`  
   *Mô tả:* Canvas đen nhung sạch sẽ, hiển thị gợi ý vẽ mờ, các chỉ số kết quả quay về trạng thái rỗng thanh lịch.
5. **Nhận dạng mẫu chữ số 7:**  
   `reports/evidence/web/sample_7_prediction.png`  
   *Mô tả:* Mô hình phân loại chuẩn xác chữ số 7, độ trễ $8.7\text{ms}$.
6. **Bảng đối chuẩn 10 mô hình học máy:**  
   `reports/evidence/web/benchmark_table.png`  
   *Mô tả:* Bảng dữ liệu đối chuẩn đẹp mắt, có huy hiệu xếp hạng #1 Modern CNN (99.19%), giải trình chi tiết thuật toán Center of Mass.

---

## 7. BÁO CÁO KIỂM THỬ TỰ ĐỘNG (UNIT & INTEGRATION TESTS)

Đã chạy toàn bộ bộ kiểm thử tự động của dự án:
```powershell
python -m unittest tests/test_pipeline.py
```

**Kết quả kiểm tra:**
```
Ran 28 tests in 1.879s
OK (100% PASS, 0 FAIL, 0 ERROR)
```

- Tất cả 14 bài kiểm tra suy luận của các mô hình trong Model Registry (`test_model_registry_loaded_and_predicts_all_models`) đều đạt kết quả xuất sắc.
- Quy chuẩn tiền xử lý Center of Mass bảo toàn trọng tâm $(14, 14)$ đạt chuẩn 100%.
- Toàn bộ các phần tử giao diện trên `index.html` tương thích hoàn toàn với các kịch bản kiểm thử API.

---

## 8. HƯỚNG DẪN KHỞI CHẠY ỨNG DỤNG TRÊN WINDOWS

Để khởi chạy và trải nghiệm giao diện mới trên máy tính Windows, thực hiện các bước sau trong PowerShell hoặc Command Prompt:

### Bước 1: Kích hoạt môi trường ảo (nếu có)
```powershell
.\.venv\Scripts\Activate.ps1
```

### Bước 2: Chạy máy chủ Web Demo
```powershell
python run_app.py
```

### Bước 3: Mở trình duyệt Web
Truy cập địa chỉ cục bộ:
```
http://127.0.0.1:8000
```

> **Mẹo trình duyệt:** Khi mở lần đầu, hãy nhấn **`Ctrl + F5`** (hoặc `Ctrl + Shift + R`) để trình duyệt xóa bộ nhớ đệm cũ và tải đầy đủ giao diện mới tinh tế nhất.
