"""
Tạo bộ Slide thuyết trình PowerPoint (.pptx) chuẩn khoa học phiên bản mới nhất.
Môn: Nhận dạng mẫu - Phân hiệu Trường Đại học Thủy Lợi - Nhóm 03.
Đồng bộ 100% số liệu thực nghiệm với Notebook 02: CNN (99.42%), SVM (98.79%), k-NN (98.06%), RF (96.99%), NB (84.46%).
"""
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
PPTX_PATH = REPORTS_DIR / "Slide_Thuyet_Trinh_Nhom_03.pptx"

COLOR_PRIMARY = RGBColor(16, 44, 87)       # Deep Navy
COLOR_SECONDARY = RGBColor(41, 128, 185)   # Ocean Blue
COLOR_ACCENT = RGBColor(46, 117, 89)       # Sage / Forest Green
COLOR_DARK = RGBColor(33, 37, 41)
COLOR_MUTED = RGBColor(108, 117, 125)
COLOR_CARD_BG = RGBColor(248, 249, 250)


def add_slide_header(slide, title_text, category="MÔN NHẬN DẠNG MẪU — NHÓM 03"):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_SECONDARY
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY


def build_pptx():
    print("-> Bắt đầu tạo bộ Slide PowerPoint (.pptx) chuẩn 16:9 đồng bộ số liệu mới...")
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ========== SLIDE 1: TRANG BÌA ==========
    s1 = prs.slides.add_slide(blank_layout)
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.33), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PHÂN HIỆU TRƯỜNG ĐẠI HỌC THỦY LỢI — KHOA CÔNG NGHỆ THÔNG TIN"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SECONDARY

    p1 = tf.add_paragraph()
    p1.text = "BÁO CÁO BÀI TẬP LỚN CUỐI KỲ — HỌC PHẦN: NHẬN DẠNG MẪU"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_MUTED

    p2 = tf.add_paragraph()
    p2.text = "ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY TRÊN BỘ DỮ LIỆU MNIST"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY

    p3 = tf.add_paragraph()
    p3.text = "\nNhóm thực hiện: Nhóm 03 | Lớp: S26-65TTNT | GVHD: Bộ môn Khoa học Máy tính\nSinh viên: Đoàn Anh Vũ (MSV: 2351267280) — Nguyễn Hồng Nguyên (MSV: 2351267273)"
    p3.font.size = Pt(14.5)
    p3.font.color.rgb = COLOR_DARK

    # ========== SLIDE 2: BỐI CẢNH & CÂU HỎI NGHIÊN CỨU ==========
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "BỐI CẢNH ỨNG DỤNG & CÂU HỎI NGHIÊN CỨU")
    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = (
        "• Bối cảnh thực tiễn:\n"
        "   - Nhận diện mã bưu chính (Zip Codes) tự động phân luồng bưu kiện tốc độ cao.\n"
        "   - Tự động hóa xử lý chứng từ tài chính, séc ngân hàng và biểu mẫu thi trắc nghiệm.\n\n"
        "• Thách thức kỹ thuật cốt lõi:\n"
        "   - Sự biến thiên nội lớp lớn: Nét nghiêng, độ đậm nhạt, đứt nét do thói quen cá nhân.\n"
        "   - Sự tương đồng hình thái học cao giữa các cặp số: (4 ↔ 9), (3 ↔ 5), (7 ↔ 1).\n\n"
        "• Ba câu hỏi nghiên cứu trọng tâm (RQs):\n"
        "   - RQ1: Kỹ thuật nắn thẳng Deskewing kết hợp PCA cải thiện độ chính xác ra sao cho mô hình cổ điển?\n"
        "   - RQ2: So sánh hiệu năng toàn diện giữa 5 thuật toán học máy đại diện trên cùng dữ liệu chuẩn?\n"
        "   - RQ3: Mạng nơ-ron tích chập Modern CNN với Early Stopping mang lại ưu thế tuyệt đối thế nào?"
    )

    # ========== SLIDE 3: BỘ DỮ LIỆU THỰC NGHIỆM MNIST ==========
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "BỘ DỮ LIỆU CHUẨN HỌC THUẬT MNIST (70.000 ẢNH)")
    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.text = (
        "• Quy mô dữ liệu: 70.000 ảnh xám kích thước 28 × 28 điểm ảnh (784 chiều).\n\n"
        "• Phân chia thực nghiệm chuẩn khoa học:\n"
        "   - Tập Train: 50.000 mẫu (71.4%) huấn luyện mô hình.\n"
        "   - Tập Validation: 10.000 mẫu (14.3%) tinh chỉnh và Early Stopping.\n"
        "   - Tập Test: 10.000 mẫu (14.3%) đối chuẩn độc lập, khách quan 100%.\n\n"
        "• Phân bố nhãn: Cân bằng hoàn hảo giữa 10 lớp chữ số (0 → 9), Shannon Entropy đạt 3.32 bits (cực đại log2 10)."
    )
    if (FIGURES_DIR / "01_class_distribution.png").exists():
        s3.shapes.add_picture(str(FIGURES_DIR / "01_class_distribution.png"), Inches(6.9), Inches(1.7), width=Inches(5.6))

    # ========== SLIDE 4: KHÁM PHÁ DỮ LIỆU CHUYÊN SÂU (EDA) ==========
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "PHÂN TÍCH KHÁM PHÁ DỮ LIỆU CHUYÊN SÂU (EDA)")
    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    tf4.text = (
        "• Ảnh trung bình (Mean Digit Images):\n"
        "   - Thể hiện hình thái trọng tâm của từng chữ số: số 1 tập trung nét thẳng giữa; số 0 có vòng oval rỗng.\n\n"
        "• Bản đồ nhiệt phương sai (Variance Heatmaps):\n"
        "   - Điểm ảnh vùng biên nét có độ lệch chuẩn cao nhất.\n"
        "   - Số 4 và 7 biến thiên mạnh ở nét ngang; số 2 biến thiên mạnh ở vòng xoắn chân đáy.\n\n"
        "• Chiếu không gian t-SNE 2D:\n"
        "   - Các chữ số 0, 1, 6 tách cụm rất xa nhau. Cặp 4, 7, 9 nằm gần nhau do có chung đặc trưng nét thẳng và nghiêng."
    )
    if (FIGURES_DIR / "02_mean_variance_digits.png").exists():
        s4.shapes.add_picture(str(FIGURES_DIR / "02_mean_variance_digits.png"), Inches(6.9), Inches(1.7), width=Inches(5.7))

    # ========== SLIDE 5: TRÍCH XUẤT ĐẶC TRƯNG (DESKEW & PCA) ==========
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "TIỀN XỬ LÝ & TRÍCH XUẤT ĐẶC TRƯNG HÌNH THÁI HỌC")
    tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    tf5.text = (
        "• Kỹ thuật nắn thẳng góc nghiêng (Deskewing):\n"
        "   - Tính mô-men quán tính bậc 2 để xác định hệ số xiên alpha = mu_11 / mu_02.\n"
        "   - Áp dụng biến đổi Affine đưa chữ số nghiêng về phương thẳng đứng.\n\n"
        "• Giảm chiều PCA 95% phương sai:\n"
        "   - Áp dụng trên 50.000 ảnh đã nắn thẳng Deskewing.\n"
        "   - Xác định chính xác 113 thành phần chính bảo toàn >= 95% tổng phương sai.\n"
        "   - Giảm 6.9 lần số chiều (từ 784 xuống 113), triệt tiêu nhiễu và tăng tốc độ suy luận gấp nhiều lần."
    )
    if (FIGURES_DIR / "04_deskew_comparison.png").exists():
        s5.shapes.add_picture(str(FIGURES_DIR / "04_deskew_comparison.png"), Inches(6.9), Inches(1.7), width=Inches(5.7))

    # ========== SLIDE 6: CÁC THUẬT TOÁN HỌC MÁY KINH ĐIỂN ==========
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "CÁC THUẬT TOÁN HỌC MÁY KINH ĐIỂN ĐƯỢC KHẢO SÁT")
    tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    tf6.text = (
        "1. Bernoulli Naive Bayes (Baseline phân loại nhanh):\n"
        "   - Nhị phân hóa điểm ảnh với ngưỡng 0.2. Tốc độ suy luận siêu tốc (1.66 ms), đạt Test Accuracy 84.46%.\n\n"
        "2. Random Forest (150 cây quyết định):\n"
        "   - Học tập hợp Bagging với 150 Decision Trees trên 784 điểm ảnh thô, biểu quyết số đông, đạt Test Accuracy 96.99%.\n\n"
        "3. k-Nearest Neighbors (k-NN, k=3, Distance Weights):\n"
        "   - Phân loại phi tham số trên không gian 113 chiều Deskew+PCA. Trọng số nghịch đảo khoảng cách giúp nâng độ chính xác lên 98.06%.\n\n"
        "4. Support Vector Machine (SVM RBF Kernel):\n"
        "   - Cực đại hóa khoảng cách lề với hàm nhân RBF (C=5.0, gamma='scale') trên 113 chiều Deskew+PCA, đạt xuất sắc 98.79% (chỉ 121 lỗi)."
    )

    # ========== SLIDE 7: MODERN CNN & EARLY STOPPING ==========
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "MẠNG TÍCH CHẬP MODERN CNN VÀ CƠ CHẾ DỪNG SỚM")
    tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    tf7.text = (
        "• Kiến trúc mạng Modern CNN (3 khối tích chập):\n"
        "   - 3 Blocks: Conv2D(32/64/128) + BatchNorm + ReLU + MaxPool + Dropout.\n"
        "   - Phân loại: Flatten -> Linear(128) -> ReLU -> Dropout(0.3) -> Linear(10).\n"
        "   - Tổng tham số học được: 160.074 tham số.\n\n"
        "• Huấn luyện và Dừng sớm (Early Stopping):\n"
        "   - Tối ưu bằng Adam, kiểm tra loss sau mỗi epoch trên 10.000 mẫu validation.\n"
        "   - Đạt điểm cực tiểu Validation Loss 0.0249 tại Epoch 17, Validation Accuracy 99.32%.\n"
        "   - Đạt đỉnh cao hiệu năng: 99.42% Test Accuracy (chỉ sai 58 ảnh / 10.000 ảnh test)."
    )
    if (FIGURES_DIR / "08_cnn_training_history.png").exists():
        s7.shapes.add_picture(str(FIGURES_DIR / "08_cnn_training_history.png"), Inches(6.8), Inches(1.8), width=Inches(5.8))

    # ========== SLIDE 8: BẢNG SO SÁNH ĐỐI CHUẨN (BENCHMARK) ==========
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "BẢNG ĐỐI CHUẨN HIỆU NĂNG TOÀN DIỆN (10.000 ẢNH TEST)")
    
    rows, cols = 6, 8
    tbl_shape = s8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    tbl = tbl_shape.table
    
    b_headers = ["Hạng", "Mô hình", "Không gian đặc trưng", "Tập train", "Test Acc", "Macro F1", "Lỗi / 10k", "Độ trễ"]
    for j, h in enumerate(b_headers):
        tbl.cell(0, j).text = h
    
    b_data = [
        ["#1", "Modern CNN", "Learned Conv (28×28)", "50k tr / 10k val", "99.42%", "99.42%", "58", "8.85 ms"],
        ["#2", "SVM", "Deskewed + PCA 95% (113D)", "50.000 mẫu", "98.79%", "98.78%", "121", "20.03 ms"],
        ["#3", "k-NN", "Deskewed + PCA 95% (113D)", "50.000 mẫu", "98.06%", "98.05%", "194", "63.38 ms"],
        ["#4", "Random Forest", "Raw Pixels (784D)", "50.000 mẫu", "96.99%", "96.97%", "301", "56.72 ms"],
        ["#5", "Bernoulli Naive Bayes", "Binarized Pixels (784D)", "50.000 mẫu", "84.46%", "84.27%", "1.554", "1.66 ms"]
    ]
    for i, r_row in enumerate(b_data):
        for j, val in enumerate(r_row):
            tbl.cell(i+1, j).text = val

    # ========== SLIDE 9: MA TRẬN NHẦM LẪN (CONFUSION MATRIX) ==========
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "MA TRẬN NHẦM LẪN CỦA MODERN CNN VÀ SVM")
    if (FIGURES_DIR / "cm_modern_cnn.png").exists():
        s9.shapes.add_picture(str(FIGURES_DIR / "cm_modern_cnn.png"), Inches(0.8), Inches(1.7), width=Inches(5.6))
    if (FIGURES_DIR / "cm_svm.png").exists():
        s9.shapes.add_picture(str(FIGURES_DIR / "cm_svm.png"), Inches(6.8), Inches(1.7), width=Inches(5.6))

    # ========== SLIDE 10: TRỰC QUAN HÓA 58 MẪU LỖI CỦA CNN ==========
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "PHÂN TÍCH CHUYÊN SÂU 58 MẪU DỰ ĐOÁN SAI CỦA MODERN CNN")
    if (FIGURES_DIR / "08_cnn_error_samples.png").exists():
        s10.shapes.add_picture(str(FIGURES_DIR / "08_cnn_error_samples.png"), Inches(0.8), Inches(1.7), width=Inches(11.7))

    # ========== SLIDE 11: ỨNG DỤNG WEB DEMO VÀ BỘ TEST TỰ ĐỘNG ==========
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_header(s11, "ỨNG DỤNG WEB DEMO TƯƠNG TÁC & KIỂM THỬ TỰ ĐỘNG")
    tb11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    tf11.text = (
        "• Kiến trúc hệ thống Web tương tác thời gian thực (FastAPI + HTML5 Canvas):\n"
        "   - Nạp sẵn toàn bộ 5 mô hình vào RAM, suy luận mili-giây, phân bố xác suất trực quan 10 lớp chữ số.\n"
        "   - Chân trang (Footer) chuẩn mực hiển thị thông tin: Phân hiệu Đại học Thủy Lợi.\n\n"
        "• Pipeline tiền xử lý Center of Mass quang học:\n"
        "   - Bóc tách nét chữ cv2.boundingRect() -> Thu phóng bảo toàn tỷ lệ vào khung 20x20 -> Tịnh tiến trọng tâm quang học về chính giữa tâm (14, 14) của khung chuẩn 28x28 NIST.\n\n"
        "• Bộ kiểm thử tự động 28 test cases (tests/test_pipeline.py):\n"
        "   - Khẳng định 100% không rò rỉ dữ liệu giữa Train và Test.\n"
        "   - Kiểm tra kiến trúc CNN 160.074 tham số, pipeline PCA 113D và API endpoints: 28/28 Tests Passed (100%)."
    )

    # ========== SLIDE 12: KẾT LUẬN & HƯỚNG PHÁT TRIỂN ==========
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_header(s12, "KẾT LUẬN KHOA HỌC & HƯỚNG PHÁT TRIỂN")
    tb12 = s12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    tf12.text = (
        "• Kết luận khoa học trọng tâm:\n"
        "   1. Nắn thẳng Deskewing + PCA 95% (113 chiều) là chìa khóa tăng cường sức mạnh cho SVM (98.79%) và k-NN (98.06%).\n"
        "   2. Modern CNN với khả năng trích xuất đặc trưng tích chập đa tầng và cơ chế Early Stopping mang lại ưu thế tuyệt đối: 99.42% Test Accuracy (chỉ sai 58/10.000 ảnh).\n"
        "   3. Xây dựng thành công hệ sinh thái trọn vẹn từ nghiên cứu, huấn luyện mô hình, kiểm thử tự động đến Web Demo thực tế.\n\n"
        "• Hướng phát triển trong tương lai:\n"
        "   - Mở rộng nhận dạng chuỗi chữ số và văn bản viết tay liên tục bằng mô hình CRNN + CTC Loss.\n"
        "   - Tối ưu hóa mô hình bằng lượng tử hóa INT8 / ONNX để nhúng lên thiết bị camera thông minh và thiết bị AI biên (Edge AI)."
    )

    prs.save(PPTX_PATH)
    print(f"-> Xuất thành công file Slide PowerPoint: {PPTX_PATH}")


if __name__ == "__main__":
    build_pptx()
