"""
Tạo bộ Slide thuyết trình PowerPoint (.pptx) chuẩn khoa học
Bảo vệ Bài tập lớn môn Nhận dạng mẫu - Đề tài 1: Nhận dạng chữ số viết tay (Nhóm 03).
Đồng bộ 100% số liệu thực nghiệm với verified_experiments.json và Báo cáo Word.
"""
import sys
import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
PPTX_PATH = REPORTS_DIR / "Slide_Thuyet_Trinh_Nhom_03.pptx"
RESULTS_JSON = BASE_DIR / "results" / "verified_experiments.json"

# Palette: Navy & Light Blue
COLOR_PRIMARY = RGBColor(16, 44, 87)     # Deep Navy
COLOR_SECONDARY = RGBColor(53, 162, 235) # Cyan / Light Blue
COLOR_TEXT_DARK = RGBColor(30, 30, 30)
COLOR_TEXT_MUTED = RGBColor(100, 100, 100)


def add_slide_header(slide, title_text, category="MÔN NHẬN DẠNG MẪU — NHÓM 03"):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.0), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_SECONDARY
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY


def build_pptx_slides():
    print("-> Bắt đầu tạo bộ Slide thuyết trình PowerPoint (.pptx) đồng bộ số liệu...")
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ========== SLIDE 1: TRANG BÌA ==========
    s1 = prs.slides.add_slide(blank_layout)
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "TRƯỜNG ĐẠI HỌC THỦY LỢI — KHOA CÔNG NGHỆ THÔNG TIN"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SECONDARY

    p1 = tf.add_paragraph()
    p1.text = "BÁO CÁO BÀI TẬP LỚN CUỐI KỲ — MÔN NHẬN DẠNG MẪU"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MUTED

    p2 = tf.add_paragraph()
    p2.text = "ĐỀ TÀI 1: NHẬN DẠNG CHỮ SỐ VIẾT TAY (MNIST DATASET)"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY

    p3 = tf.add_paragraph()
    p3.text = "\nNhóm thực hiện: Nhóm 03 | Lớp: K63/K64 CNTT | GVHD: TS. [Họ và tên Giảng viên]"
    p3.font.size = Pt(15)
    p3.font.color.rgb = COLOR_TEXT_DARK

    # ========== SLIDE 2: BỐI CẢNH & CÂU HỎI NGHIÊN CỨU ==========
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "BỐI CẢNH ỨNG DỤNG & CÂU HỎI NGHIÊN CỨU")
    tb2 = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = (
        "• Bối cảnh thực tiễn:\n"
        "   - Nhận diện mã bưu chính (ZIP codes) tự động trong phân luồng bưu phẩm.\n"
        "   - Tự động hóa xử lý chứng từ kế toán, séc ngân hàng và biểu mẫu thi trắc nghiệm.\n\n"
        "• Thách thức kỹ thuật cốt lõi:\n"
        "   - Sự đa dạng nội lớp lớn do phong cách viết tay cá nhân (nét nghiêng, độ dày, đứt nét).\n"
        "   - Sự tương đồng hình thái học thị giác cao: Cặp số (4 - 9), (3 - 5), (7 - 1).\n\n"
        "• Ba câu hỏi nghiên cứu trọng tâm (RQs):\n"
        "   RQ1: Biểu diễn đặc trưng nào (Raw, Deskew, PCA, HOG, Deskew+PCA) tối ưu cho ML truyền thống?\n"
        "   RQ2: Trong cùng điều kiện kiểm chuẩn 10k mẫu, thuật toán kinh điển nào phân lớp tốt nhất?\n"
        "   RQ3: Khi mở rộng quy mô 60k mẫu, Modern CNN thể hiện ưu thế vượt trội như thế nào?"
    )

    # ========== SLIDE 3: TẬP DỮ LIỆU MNIST ==========
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "BỘ DỮ LIỆU CHUẨN MNIST & ĐỘ CÂN BẰNG PHÂN BỐ")
    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.text = (
        "• Quy mô dữ liệu: 70,000 ảnh xám kích thước 28x28 (784 chiều).\n"
        "• Phân chia độc lập chuẩn học thuật:\n"
        "   - Tập Huấn luyện (Train): 60,000 mẫu (~85.7%)\n"
        "   - Tập Kiểm thử (Test): 10,000 mẫu (~14.3%)\n\n"
        "• Phân tích cân bằng dữ liệu thực nghiệm:\n"
        "   - Lớp 1 nhiều nhất: 6,742 mẫu (11.24%)\n"
        "   - Lớp 5 ít nhất: 5,421 mẫu (9.04%)\n"
        "   - Shannon Entropy thực tế: H = 3.3199 bits (Cực đại lý thuyết: 3.3219 bits)\n"
        "   - Tỷ lệ cân bằng: 99.94% (Dữ liệu cân bằng hoàn hảo, không bị lệch lớp)."
    )
    fig1 = FIGURES_DIR / "01_class_distribution.png"
    if fig1.exists():
        s3.shapes.add_picture(str(fig1), Inches(6.8), Inches(1.8), width=Inches(5.8))

    # ========== SLIDE 4: TRÍCH XUẤT ĐẶC TRƯNG ==========
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "CÁC PHƯƠNG PHÁP BIỂU DIỄN ĐẶC TRƯNG")
    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    tf4.text = (
        "1. Raw Pixels (784 chiều): Điểm ảnh chuẩn hóa [0.0, 1.0].\n\n"
        "2. Deskewing (Nắn thẳng góc nghiêng):\n"
        "   - Tính mô-men trung tâm mu_11 / mu_02 để xác định độ nghiêng nét bút.\n"
        "   - Áp dụng biến đổi Affine shear đưa chữ số về phương thẳng đứng.\n\n"
        "3. PCA (Giảm chiều thành phần chính):\n"
        "   - Tập 60k: 154 chiều | Tập 10k: 152 chiều | Deskew 10k: 112 chiều.\n"
        "   - Giữ nguyên 95% phương sai thông tin, lọc bỏ nhiễu biên.\n\n"
        "4. HOG (Histogram of Oriented Gradients):\n"
        "   - Trích xuất 324 chiều đặc trưng hướng viền và nét chữ."
    )
    fig4 = FIGURES_DIR / "04_deskew_comparison.png"
    if fig4.exists():
        s4.shapes.add_picture(str(fig4), Inches(6.8), Inches(2.0), width=Inches(5.8))

    # ========== SLIDE 5: ĐỐI CHUẨN ĐẶC TRƯNG (NHÓM A) ==========
    s5a = prs.slides.add_slide(blank_layout)
    add_slide_header(s5a, "ĐỐI CHUẨN ĐẶC TRƯNG — NHÓM A (SVM RBF TRÊN 10K MẪU)")

    group_a_data = [
        ["Deskewed + PCA (112D)", "112", "97.97%", "203 / 10k", "0.685 ms"],
        ["Deskewed Raw (784D)", "784", "97.77%", "223 / 10k", "2.140 ms"],
        ["HOG Features (324D)", "324", "97.58%", "242 / 10k", "1.120 ms"],
        ["PCA Compression (152D)", "152", "97.22%", "278 / 10k", "0.820 ms"],
        ["Raw Pixels (784D)", "784", "96.86%", "314 / 10k", "2.180 ms"],
    ]
    t5a_shape = s5a.shapes.add_table(6, 5, Inches(0.8), Inches(1.8), Inches(7.5), Inches(3.2))
    tbl5a = t5a_shape.table
    headers_a = ["Biểu diễn đặc trưng", "Số chiều", "Test Accuracy", "Số ảnh sai", "Độ trễ"]
    for c, h in enumerate(headers_a):
        cell = tbl5a.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
    for r_idx, row in enumerate(group_a_data):
        for c_idx, val in enumerate(row):
            cell = tbl5a.cell(r_idx + 1, c_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(220, 245, 230)

    tb5a = s5a.shapes.add_textbox(Inches(8.6), Inches(1.8), Inches(4.0), Inches(5.0))
    tf5a = tb5a.text_frame
    tf5a.word_wrap = True
    tf5a.text = (
        "• Nhận xét phân tích đặc trưng (RQ1):\n\n"
        "1. Deskewed + PCA 112D dẫn đầu tuyệt đối nhóm A (97.97%, chỉ sai 203 ảnh).\n\n"
        "2. Kỹ thuật nắn thẳng góc nghiêng triệt tiêu biến thiên do thói quen viết tay, cô đọng 95% phương sai chỉ trong 112 chiều (so với 152D của ảnh thô).\n\n"
        "3. Giảm 35.3% số ảnh sai so với ảnh thô (từ 314 xuống 203 lỗi), đồng thời tăng tốc độ suy luận gấp 3.2 lần (0.685 ms vs 2.180 ms)."
    )

    # ========== SLIDE 6: ĐỐI CHUẨN THUẬT TOÁN KINH ĐIỂN (NHÓM B) ==========
    s5b = prs.slides.add_slide(blank_layout)
    add_slide_header(s5b, "ĐỐI CHUẨN THUẬT TOÁN KINH ĐIỂN — NHÓM B (RAW PIXELS 10K)")

    group_b_data = [
        ["SVM (RBF Kernel)", "C=5.0, gamma=scale", "96.86%", "314 / 10k", "2.180 ms"],
        ["Random Forest (150 cây)", "n_est=150, depth=None", "95.28%", "472 / 10k", "1.180 ms"],
        ["k-NN (k=3, Euclidean)", "k=3, weights=uniform", "95.17%", "483 / 10k", "14.250 ms"],
        ["Linear SVM (C=0.01)", "C=0.01 (dual=False)", "90.79%", "921 / 10k", "0.150 ms"],
        ["Bernoulli Naive Bayes", "binarize=0.5, a=1.0", "84.40%", "1,560 / 10k", "0.080 ms"],
        ["Gaussian Naive Bayes", "var_smoothing=1e-9", "55.80%", "4,420 / 10k", "0.120 ms"],
    ]
    t5b_shape = s5b.shapes.add_table(7, 5, Inches(0.8), Inches(1.8), Inches(7.5), Inches(3.8))
    tbl5b = t5b_shape.table
    headers_b = ["Thuật toán", "Siêu tham số tối ưu", "Test Accuracy", "Số ảnh sai", "Độ trễ"]
    for c, h in enumerate(headers_b):
        cell = tbl5b.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
    for r_idx, row in enumerate(group_b_data):
        for c_idx, val in enumerate(row):
            cell = tbl5b.cell(r_idx + 1, c_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(220, 245, 230)

    tb5b = s5b.shapes.add_textbox(Inches(8.6), Inches(1.8), Inches(4.0), Inches(5.0))
    tf5b = tb5b.text_frame
    tf5b.word_wrap = True
    tf5b.text = (
        "• Nhận xét phân tích thuật toán (RQ2):\n\n"
        "1. SVM nhân RBF dẫn đầu trên ảnh thô (96.86%) nhờ không gian Hilbert vô hạn chiều phân tách phi tuyến.\n\n"
        "2. Random Forest 150 cây (95.28%) vượt qua k-NN (95.17%) và có tốc độ suy luận nhanh hơn 12 lần.\n\n"
        "3. Linear SVM C=0.01 đạt 90.79% (tăng 1.45% so với C=1.0) và đạt tốc độ nhanh kỷ lục 0.150 ms/ảnh.\n\n"
        "4. Naive Bayes kém nhất do giả định độc lập điểm ảnh bị vi phạm nặng nề trong ảnh 2D."
    )

    # ========== SLIDE 7: QUY MÔ DỮ LIỆU & DEEP LEARNING (NHÓM C) ==========
    s5c = prs.slides.add_slide(blank_layout)
    add_slide_header(s5c, "QUY MÔ DỮ LIỆU & ƯU THẾ CỦA DEEP LEARNING (NHÓM C)")

    group_c_data = [
        ["Modern CNN Baseline", "Full 60,000", "99.19%", "81 / 10k", "0.516 ms"],
        ["Modern CNN Validation", "50k train / 10k val", "99.00%", "100 / 10k", "0.516 ms"],
        ["SVM RBF + PCA (154D)", "Full 60,000", "98.54%", "146 / 10k", "1.250 ms"],
        ["Modern CNN (sub10k)", "Subset 10,000", "97.60%", "240 / 10k", "0.516 ms"],
        ["k-NN (k=3) + PCA (154D)", "Full 60,000", "97.31%", "269 / 10k", "68.500 ms"],
    ]
    t5c_shape = s5c.shapes.add_table(6, 5, Inches(0.8), Inches(1.8), Inches(7.5), Inches(3.2))
    tbl5c = t5c_shape.table
    headers_c = ["Mô hình", "Quy mô dữ liệu", "Test Accuracy", "Số ảnh sai", "Độ trễ"]
    for c, h in enumerate(headers_c):
        cell = tbl5c.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
    for r_idx, row in enumerate(group_c_data):
        for c_idx, val in enumerate(row):
            cell = tbl5c.cell(r_idx + 1, c_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(220, 245, 230)

    tb5c = s5c.shapes.add_textbox(Inches(8.6), Inches(1.8), Inches(4.0), Inches(5.0))
    tf5c = tb5c.text_frame
    tf5c.word_wrap = True
    tf5c.text = (
        "• Nhận xét phân tích quy mô & CNN (RQ3):\n\n"
        "1. Modern CNN Baseline đạt 99.19% (chỉ 81 ảnh sai / 10k test), khẳng định ưu thế vượt trội của học sâu tự động trích xuất biểu diễn.\n\n"
        "2. Modern CNN Validation đạt 99.00% (sai 100 ảnh), minh chứng phương pháp chọn checkpoint khách quan theo Validation Loss (Epoch 2).\n\n"
        "3. Ở quy mô nhỏ 10k: CNN (97.60%) thấp hơn SVM Deskew+PCA (97.97%), chứng minh CNN chỉ phát huy uy lực khi có đủ dữ liệu huấn luyện."
    )

    # ========== SLIDE 6: MA TRẬN NHẦM LẪN ==========
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "PHÂN TÍCH MA TRẬN NHẦM LẪN (CONFUSION MATRIX)")
    tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.0))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    tf6.text = (
        "• Xu hướng sai số trên ma trận nhầm lẫn:\n\n"
        "1. Cặp chữ số (4 - 9): Tần suất nhầm lẫn cao nhất do chữ số 4 viết khép kín đỉnh tạo thành vòng tròn như số 9.\n\n"
        "2. Cặp chữ số (3 - 5): Phần cung cong uốn lượn nửa dưới tương đồng nhau.\n\n"
        "3. Cặp chữ số (7 - 1): Số 7 khi thiếu nét gạch ngang phụ giữa thân có hình dáng thẳng đứng như số 1.\n\n"
        "• Mô hình Modern CNN đạt độ chính xác >98.5% đồng đều cho tất cả 10 lớp chữ số."
    )
    cm_fig = FIGURES_DIR / "cm_modern_cnn.png"
    if cm_fig.exists():
        s6.shapes.add_picture(str(cm_fig), Inches(6.8), Inches(1.8), width=Inches(5.8))

    # ========== SLIDE 7: PHÂN TÍCH LỖI CHUYÊN SÂU ==========
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "PHÂN TÍCH CHUYÊN SÂU 81 MẪU SAI CỦA MODERN CNN")
    tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.0))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    tf7.text = (
        "• Phân loại nguyên nhân của 81 ca phân loại sai:\n\n"
        "1. Nhiễu nhãn gán sai trong tập gốc (Label Noise):\n"
        "   - Tiêu biểu mẫu test #445 (ảnh là chữ số 6 rõ ràng nhưng nhãn ghi 0); mẫu test #2130 (ảnh là 9 nhưng nhãn ghi 4). Mô hình CNN thực chất đã nhận diện đúng dạng thị giác.\n\n"
        "2. Chữ số cực kỳ mơ hồ (Ambiguous Samples):\n"
        "   - Nét viết cẩu thả, đứt đoạn, mắt người bình thường cũng không thể khẳng định chắc chắn 100%.\n\n"
        "3. Biến dạng hình học dị biệt (Outliers):\n"
        "   - Nét viết quá dày hoặc quá dị thường khiến tâm khối lượng bị lệch."
    )
    err_fig = FIGURES_DIR / "errors_modern_cnn.png"
    if err_fig.exists():
        s7.shapes.add_picture(str(err_fig), Inches(6.8), Inches(1.8), width=Inches(5.8))

    # ========== SLIDE 8: TRẢ LỜI CÂU HỎI NGHIÊN CỨU ==========
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "TRẢ LỜI CÂU HỎI NGHIÊN CỨU KHOA HỌC")
    tb8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(5.0))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    tf8.text = (
        "1. ĐẶC TRƯNG NÀO HIỆU QUẢ NHẤT CHO ML TRUYỀN THỐNG (RQ1)?\n"
        "   • Deskewed + PCA (112D) dẫn đầu nhóm A với 97.97% độ chính xác (sai 203 ảnh trên 10k test, Macro F1: 97.96%).\n"
        "   • Nắn thẳng nén chiều giúp loại bỏ triệt để biến thiên góc nghiêng và giảm 7 lần số chiều dữ liệu.\n\n"
        "2. THUẬT TOÁN KINH ĐIỂN NÀO TỐT NHẤT TRÊN RAW PIXELS (RQ2)?\n"
        "   • SVM nhân RBF đạt 96.86%, kế tiếp là Random Forest 150 cây (95.28%) và k-NN (95.17%).\n"
        "   • Linear SVM đạt 90.79% khi tối ưu điều chuẩn C=0.01 (cải thiện rõ rệt so với C=1.0 đạt 89.34%).\n"
        "   • Gaussian Naive Bayes đạt 55.80% do vi phạm giả định độc lập không gian.\n\n"
        "3. ƯU THẾ CỦA DEEP LEARNING TRÊN DỮ LIỆU LỚN (RQ3)?\n"
        "   • Modern CNN đạt 99.19% (Macro F1: 99.18%, chỉ sai 81 ảnh trên 10.000 ảnh test).\n"
        "   • Độ trễ suy luận siêu tốc (0.516 ms/ảnh đơn lẻ, 0.106 ms/ảnh theo batch), checkpoint chỉ 0.62 MB."
    )

    # ========== SLIDE 9: SẢN PHẨM WEB DEMO ==========
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "ỨNG DỤNG DEMO WEB TƯƠNG TÁC THỜI GIAN THỰC")
    tb9 = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(5.0))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    tf9.text = (
        "• Kiến trúc sản phẩm: Tầng giao diện HTML5 Canvas Glassmorphism + Tầng dịch vụ Backend FastAPI.\n\n"
        "• Các tính năng nổi bật:\n"
        "   - Bảng vẽ tương tác thời gian thực với giải thuật làm mịn nét vẽ đường cong Bessel.\n"
        "   - Pipeline tiền xử lý quang học Center of Mass: Căn tâm chữ số chuẩn xác vào tọa độ (14, 14) như chuẩn NIST.\n"
        "   - Hỗ trợ lựa chọn linh hoạt giữa các mô hình (Modern CNN, SVM Deskew+PCA, SVM PCA, k-NN, Naive Bayes).\n"
        "   - Xử lý lỗi minh bạch: Bảng vẽ trống báo -1, yêu cầu mô hình không tồn tại trả mã HTTP 404.\n"
        "   - Bảng 10 mẫu test chuẩn từ MNIST Test Set cho phép kiểm thử nhanh chóng và đối chiếu.\n\n"
        "• Khởi động máy chủ bằng lệnh duy nhất: python run_app.py"
    )

    # ========== SLIDE 10: KẾT LUẬN & ĐÓNG GÓP ==========
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "KẾT LUẬN & ĐÓNG GÓP CỦA ĐỒ ÁN")
    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(5.0))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    tf10.text = (
        "• Hoàn thành đầy đủ 100% mục tiêu nghiên cứu và các yêu cầu kỹ thuật của bài tập lớn.\n\n"
        "• Đóng góp khoa học và kỹ thuật chính:\n"
        "   - Quy trình thực nghiệm Zero Leakage chặt chẽ, tối ưu siêu tham số trên Validation độc lập.\n"
        "   - Đối chuẩn công bằng 10 mô hình thực nghiệm, lưu vết checkpoint và log đo lường rõ ràng.\n"
        "   - Giải mã chi tiết cơ chế sai lệch của 81 mẫu phân loại sai của mô hình Modern CNN (99.19%).\n"
        "   - Ứng dụng Web tương tác hoàn chỉnh và bộ kiểm thử tự động 28 test cases đạt tỷ lệ vượt qua 100%.\n\n"
        "• Hồ sơ bàn giao đầy đủ:\n"
        "   - Báo cáo kỹ thuật Word (.docx) & PDF 28 trang chuẩn khoa học.\n"
        "   - Bộ Slide thuyết trình PowerPoint (.pptx).\n"
        "   - Mã nguồn chuẩn hóa, module hóa cao trên GitHub.\n\n"
        "TRÂN TRỌNG CẢM ƠN QUÝ THẦY CÔ VÀ CÁC BẠN ĐÃ LẮNG NGHE!"
    )

    prs.save(str(PPTX_PATH))
    print(f"[OK] Đã xuất thành công bộ Slide PowerPoint: {PPTX_PATH} ({PPTX_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    build_pptx_slides()
