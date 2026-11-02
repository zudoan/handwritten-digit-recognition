"""
Tạo Báo cáo Kỹ thuật Toàn diện Word (.docx) phiên bản mới nhất chuẩn học thuật.
Đề tài 1: Nhận dạng chữ số viết tay trên bộ dữ liệu MNIST.
Phân hiệu Trường Đại học Thủy Lợi - Khoa Công nghệ Thông tin - Nhóm 03.
Đồng bộ 100% số liệu với Notebook 02: Modern CNN (99.42%), SVM (98.79%), k-NN (98.06%), Random Forest (96.99%), Naive Bayes (84.46%).
"""
import sys
import json
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
DOCX_PATH = REPORTS_DIR / "Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx"


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_heading_styled(doc, text, level):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    run.font.name = "Times New Roman"
    if level == 1:
        p.paragraph_format.page_break_before = True
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
    return p


def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT if "\n" in text else WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(12)
        r_b.font.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="Normal" if bold_prefix else "List Bullet")
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(12)
        r_b.font.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_caption(doc, text, is_table=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = False
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.italic = True
    r.font.color.rgb = RGBColor(80, 80, 80)
    return p


def add_image_safe(doc, img_path, width_in, caption_text):
    if Path(img_path).exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        picture_p = doc.add_paragraph()
        picture_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        picture_p.paragraph_format.keep_with_next = True
        picture_p.add_run().add_picture(str(img_path), width=Inches(width_in))
        add_caption(doc, caption_text)


def style_table(table, col_widths, col_alignments, header_bg="2C3E50", alt_bg="F8F9FA"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        is_header = (i == 0)
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for j, cell in enumerate(row.cells):
            cell.width = Inches(col_widths[j])
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            if is_header:
                set_cell_background(cell, header_bg)
            elif i % 2 == 1:
                set_cell_background(cell, alt_bg)
            else:
                set_cell_background(cell, "FFFFFF")

            for p in cell.paragraphs:
                p.alignment = col_alignments[j]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    if is_header:
                        r.font.size = Pt(11)
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        r.font.size = Pt(10.5)


def build_full_docx():
    print("-> Đang khởi tạo và xuất Báo cáo Kỹ thuật Word (.docx) phiên bản mới nhất...")
    doc = Document()
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(12)
    for style_name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        doc.styles[style_name].font.color.rgb = RGBColor(0, 0, 0)
    
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    number = OxmlElement("w:fldSimple")
    number.set(qn("w:instr"), "PAGE")
    footer._p.append(number)

    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(1.15)
        section.right_margin = Inches(0.85)

    # ==================== TRANG BÌA ====================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("BỘ NÔNG NGHIỆP VÀ PHÁT TRIỂN NÔNG THÔN\nPHÂN HIỆU TRƯỜNG ĐẠI HỌC THỦY LỢI\nKHOA CÔNG NGHỆ THÔNG TIN\n")
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(13)
    r_uni.font.bold = True

    p_star = doc.add_paragraph()
    p_star.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_star = p_star.add_run("*****\n\n")
    r_star.font.name = "Times New Roman"
    r_star.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_title.add_run("BÁO CÁO BÀI TẬP LỚN CUỐI KỲ\nHỌC PHẦN: NHẬN DẠNG MẪU (PATTERN RECOGNITION)\n\n")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True

    r_main = p_title.add_run("ĐỀ TÀI 1: NGHIÊN CỨU, THỰC NGHIỆM VÀ TRIỂN KHAI\nHỆ THỐNG NHẬN DẠNG CHỮ SỐ VIẾT TAY TRÊN BỘ DỮ LIỆU MNIST\n\n\n")
    r_main.font.name = "Times New Roman"
    r_main.font.size = Pt(16.5)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(0, 0, 0)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.2)
    p_info.paragraph_format.line_spacing = 1.3
    
    runs_info = [
        ("Giảng viên hướng dẫn: ", True), ("Bộ môn Khoa học Máy tính\n", False),
        ("Lớp học phần: ", True), ("Nhận dạng mẫu — S26-65TTNT\n", False),
        ("Nhóm sinh viên thực hiện: ", True), ("Nhóm 03\n", False),
        ("Thành viên nhóm:\n", True),
        ("  1. Đoàn Anh Vũ — MSSV: 2351267280\n", False),
        ("  2. Nguyễn Hồng Nguyên — MSSV: 2351267273\n", False),
        ("\n\n\n", False),
    ]
    for txt, is_b in runs_info:
        r = p_info.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12.5)
        r.font.bold = is_b

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("Hà Nội, Năm 2026")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    r_date.font.italic = True

    # ==================== LỜI CẢM ƠN & TÓM TẮT ====================
    add_heading_styled(doc, "GIỚI THIỆU BÁO CÁO VÀ LỜI CẢM ƠN", level=1)
    add_body_p(doc, "Báo cáo trình bày chi tiết toàn bộ cơ sở lý thuyết, quá trình thực nghiệm, đánh giá định lượng và đóng gói sản phẩm phần mềm của Đề tài 1: Nhận dạng chữ số viết tay trên bộ dữ liệu chuẩn MNIST.")
    add_body_p(doc, "Nhóm 03 xin bày tỏ lòng biết ơn sâu sắc tới các thầy cô giảng viên Bộ môn Khoa học Máy tính, Khoa Công nghệ Thông tin — Phân hiệu Trường Đại học Thủy Lợi đã tận tâm giảng dạy, trang bị hệ thống tri thức bài bản về xử lý ảnh, trích xuất đặc trưng và các mô hình phân lớp học máy hiện đại.")

    add_heading_styled(doc, "TÓM TẮT BÁO CÁO", level=2)
    add_body_p(doc, "Đề tài thực hiện khảo sát và đối chuẩn toàn diện 5 thuật toán học máy đại diện trên tập dữ liệu chuẩn MNIST (70.000 ảnh) theo quy chuẩn phân chia khoa học: 50.000 mẫu huấn luyện (Train), 10.000 mẫu kiểm chứng (Validation) và 10.000 mẫu kiểm thử độc lập (Test).")
    add_body_p(doc, "Kết quả thực nghiệm đã chứng minh sức mạnh vượt trội của kỹ thuật xử lý hình thái học nắn thẳng Deskewing kết hợp giảm chiều PCA 95% (113 chiều), giúp đưa SVM RBF đạt 98.79% và k-NN đạt 98.06% Test Accuracy. Đặc biệt, mô hình học sâu Modern CNN với 3 khối tích chập chuẩn hóa và cơ chế dừng sớm Early Stopping (Epoch 17, Val Loss 0.0249) đã xuất sắc xác lập đỉnh cao hiệu năng với Test Accuracy đạt 99.42% (chỉ mắc 58 lỗi trên 10.000 ảnh test). Hệ thống đã được tích hợp hoàn chỉnh vào ứng dụng Web tương tác thời gian thực với độ trễ phản hồi mili-giây và vượt qua 100% bộ kiểm thử tự động 28 test cases.")

    add_heading_styled(doc, "MỤC LỤC BÁO CÁO", level=2)
    toc_items = [
        ("CHƯƠNG 1  GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU", "3"),
        ("CHƯƠNG 2  CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC", "5"),
        ("CHƯƠNG 3  DỮ LIỆU MNIST VÀ QUY CHUẨN TIỀN XỬ LÝ", "9"),
        ("CHƯƠNG 4  THIẾT KẾ THỰC NGHIỆM VÀ ĐỐI CHUẨN MÔ HÌNH", "13"),
        ("CHƯƠNG 5  KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH LỖI", "16"),
        ("CHƯƠNG 6  TRIỂN KHAI WEB DEMO VÀ KIỂM THỬ HỆ THỐNG", "22"),
        ("CHƯƠNG 7  KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "25"),
        ("TÀI LIỆU THAM KHẢO", "27")
    ]
    for title, pg in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.2
        p_t.paragraph_format.space_after = Pt(3)
        r1 = p_t.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r_dots = p_t.add_run(" " + "." * max(10, 85 - len(title)) + " ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(11)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)
        r2 = p_t.add_run(pg)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        r2.font.bold = True

    # ==================== CHƯƠNG 1 ====================
    add_heading_styled(doc, "CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU", level=1)
    add_heading_styled(doc, "1.1. Bối cảnh thực tế và ý nghĩa bài toán", level=2)
    add_body_p(doc, "Nhận dạng chữ số viết tay (Handwritten Digit Recognition) là bài toán nền tảng của nhận dạng mẫu và thị giác máy tính. Trong bối cảnh cách mạng công nghiệp 4.0 và chuyển đổi số, việc tự động hóa đọc và xử lý chữ số viết tay có ý nghĩa kinh tế và ứng dụng thực tiễn to lớn:")
    add_bullet_p(doc, "Tự động hóa đọc mã bưu chính (Zip Codes) trên bì thư, bưu kiện nhằm phân luồng vận chuyển tự động, tiết kiệm hàng triệu giờ lao động thủ công.", "• Bưu chính tự động: ")
    add_bullet_p(doc, "Tự động nhận dạng số tiền viết tay, số tài khoản trên séc ngân hàng, phiếu nộp tiền và hóa đơn chứng từ kế toán.", "• Tài chính ngân hàng: ")
    add_bullet_p(doc, "Chấm thi trắc nghiệm, nhận diện số báo danh, điểm số của giám khảo và số hóa hồ sơ y tế bệnh án.", "• Hành chính công & Giáo dục: ")

    add_heading_styled(doc, "1.2. Định nghĩa toán học bài toán", level=2)
    add_body_p(doc, "Bài toán được định nghĩa dưới dạng bài toán phân lớp đa lớp có giám sát (Supervised Multi-class Classification):")
    add_body_p(doc, "Không gian đầu vào là ảnh xám 28x28 điểm ảnh x thuộc [0.0, 1.0]^784. Không gian nhãn đầu ra là tập 10 lớp rời rạc Y = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. Mục tiêu là tìm hàm quyết định f: X -> Y cực tiểu hóa rủi ro kỳ vọng với hàm tổn thất 0-1.")

    add_heading_styled(doc, "1.3. Thách thức kỹ thuật cốt lõi", level=2)
    add_bullet_p(doc, "Sự biến thiên lớn trong thói quen viết tay cá nhân về nét nghiêng, độ đậm nhạt, kích thước và độ cong uốn.", "• Biến thiên nội lớp (Intra-class Variability): ")
    add_bullet_p(doc, "Các cặp số có cấu trúc hình thái học rất gần nhau khi viết nhanh: 4 và 9, 3 và 5, 7 và 1, 8 và 0.", "• Tương đồng liên lớp (Inter-class Similarity): ")
    add_bullet_p(doc, "Không gian 784 điểm ảnh thô chứa nhiều chiều dư thừa ở vùng biên đen, gây tốn kém tài nguyên tính toán và dễ gây overfitting.", "• Lời nguyền số chiều (Curse of Dimensionality): ")

    add_heading_styled(doc, "1.4. Mục tiêu nghiên cứu và các câu hỏi nghiên cứu (RQs)", level=2)
    add_bullet_p(doc, "Kỹ thuật nắn thẳng góc nghiêng (Deskewing) kết hợp phân tích thành phần chính (PCA) cải thiện độ chính xác phân loại của các thuật toán ML kinh điển (SVM, k-NN) như thế nào so với điểm ảnh thô?", "• Câu hỏi 1 (RQ1): ")
    add_bullet_p(doc, "So sánh hiệu năng toàn diện giữa các họ thuật toán kinh điển (Naive Bayes, k-NN, Random Forest, SVM) trên cùng tập dữ liệu chuẩn?", "• Câu hỏi 2 (RQ2): ")
    add_bullet_p(doc, "Mạng nơ-ron tích chập hiện đại (Modern CNN) với cơ chế Early Stopping mang lại ưu thế vượt trội ra sao so với các mô hình học máy truyền thống về độ chính xác và độ trễ suy luận?", "• Câu hỏi 3 (RQ3): ")

    # ==================== CHƯƠNG 2 ====================
    add_heading_styled(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC", level=1)
    add_heading_styled(doc, "2.1. Không gian biểu diễn và trích xuất đặc trưng", level=2)
    add_body_p(doc, "2.1.1. Kỹ thuật nắn thẳng nét nghiêng (Deskewing bằng Image Moments):", bold_prefix="a) Deskewing: ")
    add_body_p(doc, "Để loại trừ góc nghiêng nét viết cá nhân, thuật toán tính toán mô-men trung tâm bậc 2 của ảnh: mu_pq = sum_x sum_y (x - x_bar)^p (y - y_bar)^q I(x, y). Hệ số nghiêng được tính bởi alpha = mu_11 / mu_02. Sau đó, phép biến đổi Affine được áp dụng để tịnh tiến tọa độ x' = x - alpha * y, đưa chữ số xiên về phương thẳng đứng chuẩn hóa.")
    add_image_safe(doc, FIGURES_DIR / "04_deskew_comparison.png", 6.0, "Hình 2.1: Trực quan hóa tác động của phép biến đổi Deskewing nắn thẳng chữ số MNIST")

    add_body_p(doc, "2.1.2. Phân tích thành phần chính (PCA giữ 95% phương sai):", bold_prefix="b) PCA Dimensionality Reduction: ")
    add_body_p(doc, "PCA tìm kiếm hệ cơ sở trực chuẩn mới sao cho phương sai dữ liệu chiếu lên các trục là cực đại. Trên 50.000 mẫu ảnh đã nắn thẳng, thuật toán tìm ra chính xác 113 thành phần chính để bảo toàn >= 95% tổng phương sai dữ liệu, giảm 6.9 lần số chiều từ 784 xuống 113 chiều.")
    add_image_safe(doc, FIGURES_DIR / "05_pca_variance_curve.png", 5.8, "Hình 2.2: Đường cong phương sai tích lũy theo số lượng thành phần chính PCA")

    add_heading_styled(doc, "2.2. Các thuật toán học máy kinh điển", level=2)
    add_body_p(doc, "• Support Vector Machine (SVM RBF Kernel): Tìm siêu phẳng cực đại hóa khoảng cách lề. Hàm nhân RBF K(x, z) = exp(-gamma ||x - z||^2) với C=5.0, gamma='scale' chiếu phi tuyến vào không gian đặc trưng Hilbert.")
    add_body_p(doc, "• k-Nearest Neighbors (k-NN, k=3, Distance weights): Phân loại phi tham số dựa trên khoảng cách Euclidean trong không gian 113 chiều Deskew+PCA, gán trọng số nghịch đảo khoảng cách.")
    add_body_p(doc, "• Random Forest (150 cây quyết định): Học tập hợp Bagging với 150 Decision Trees, mỗi nhánh chọn sqrt(784) = 28 đặc trưng ngẫu nhiên, biểu quyết số đông.")
    add_body_p(doc, "• Bernoulli Naive Bayes: Áp dụng định lý Bayes với giả định độc lập có điều kiện, dữ liệu được nhị phân hóa với ngưỡng 0.2.")

    add_heading_styled(doc, "2.3. Mạng nơ-ron tích chập hiện đại (Modern CNN)", level=2)
    add_body_p(doc, "Mạng Modern CNN gồm 3 khối tích chập chuẩn hóa: Conv2d(32) -> BatchNorm -> ReLU -> Conv2d(32) -> MaxPool(2x2) -> Dropout(0.25) -> Conv2d(64) -> BatchNorm -> ReLU -> Conv2d(64) -> MaxPool(2x2) -> Dropout(0.25) -> Conv2d(128) -> BatchNorm -> ReLU -> Flatten -> Dropout(0.4) -> Linear(128) -> ReLU -> Dropout(0.3) -> Linear(10). Tổng cộng 160.074 tham số học được.")

    # ==================== CHƯƠNG 3 ====================
    add_heading_styled(doc, "CHƯƠNG 3: DỮ LIỆU MNIST VÀ QUY CHUẨN TIỀN XỬ LÝ", level=1)
    add_heading_styled(doc, "3.1. Phân chia tập dữ liệu chuẩn học thuật", level=2)
    add_body_p(doc, "Bộ dữ liệu MNIST 70.000 ảnh xám 28x28 được phân chia nghiêm ngặt: 50.000 mẫu Train, 10.000 mẫu Validation để tinh chỉnh và Early Stopping, cùng 10.000 mẫu Test độc lập dùng để đối chuẩn khách quan.")
    add_image_safe(doc, FIGURES_DIR / "01_class_distribution.png", 5.8, "Hình 3.1: Phân bố số lượng mẫu cân bằng giữa 10 lớp chữ số trong tập dữ liệu MNIST")
    add_image_safe(doc, FIGURES_DIR / "02_mean_variance_digits.png", 6.0, "Hình 3.2: Bản đồ nhiệt ảnh trung bình (Mean) và độ lệch chuẩn phương sai (Std) 10 chữ số")

    add_heading_styled(doc, "3.2. Không gian tiềm ẩn t-SNE", level=2)
    add_body_p(doc, "Chiếu dữ liệu bằng thuật toán t-SNE (t-Distributed Stochastic Neighbor Embedding) trực quan hóa cụm phân bố dữ liệu trong không gian 2D.")
    add_image_safe(doc, FIGURES_DIR / "07_tsne_clustering.png", 5.8, "Hình 3.3: Phân bố cụm 10 chữ số MNIST trong không gian t-SNE 2 chiều")

    # ==================== CHƯƠNG 4 ====================
    add_heading_styled(doc, "CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ ĐỐI CHUẨN MÔ HÌNH", level=1)
    add_heading_styled(doc, "4.1. Thiết kế thực nghiệm kiểm chứng công bằng", level=2)
    add_body_p(doc, "Toàn bộ 5 mô hình đều được huấn luyện trên 50.000 mẫu và đánh giá trên 10.000 mẫu test chuẩn. Tuyệt đối không có rò rỉ dữ liệu.")

    add_heading_styled(doc, "4.2. Huấn luyện Modern CNN với Early Stopping", level=2)
    add_body_p(doc, "Mô hình CNN được tối ưu bằng Adam optimizer, tự động điều chỉnh learning rate và dừng sớm tại Epoch 17 với Validation Loss cực tiểu 0.0249, Validation Accuracy đạt 99.32%.")
    add_image_safe(doc, FIGURES_DIR / "08_cnn_training_history.png", 6.2, "Hình 4.1: Đường cong hàm mất mát (Loss) và độ chính xác (Accuracy) qua 17 epoch huấn luyện của Modern CNN")

    # ==================== CHƯƠNG 5 ====================
    add_heading_styled(doc, "CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH LỖI", level=1)
    add_heading_styled(doc, "5.1. Bảng đối chuẩn kết quả toàn diện trên 10.000 ảnh MNIST Test Set", level=2)
    add_body_p(doc, "Dưới đây là bảng tổng hợp kết quả thực nghiệm kiểm chứng chính thức của 5 mô hình trên 10.000 ảnh test độc lập:")

    # Bảng Benchmark
    tbl_bench = doc.add_table(rows=6, cols=8)
    bench_headers = ["Hạng", "Mô hình", "Không gian đặc trưng", "Tập train", "Test Acc", "Macro F1", "Lỗi / 10k", "Độ trễ"]
    for j, h in enumerate(bench_headers):
        tbl_bench.rows[0].cells[j].paragraphs[0].text = h
    
    bench_data = [
        ["#1", "Modern CNN", "Learned Conv (28×28)", "50k tr / 10k val", "99.42%", "99.42%", "58", "8.85 ms"],
        ["#2", "SVM", "Deskewed + PCA 95% (113D)", "50.000 train", "98.79%", "98.78%", "121", "20.03 ms"],
        ["#3", "k-NN", "Deskewed + PCA 95% (113D)", "50.000 train", "98.06%", "98.05%", "194", "63.38 ms"],
        ["#4", "Random Forest", "Raw Pixels (784D)", "50.000 train", "96.99%", "96.97%", "301", "56.72 ms"],
        ["#5", "Bernoulli Naive Bayes", "Binarized Pixels (784D, bin=0.2)", "50.000 train", "84.46%", "84.27%", "1.554", "1.66 ms"]
    ]
    for i, row in enumerate(bench_data):
        for j, val in enumerate(row):
            tbl_bench.rows[i+1].cells[j].paragraphs[0].text = val
    
    col_w = [0.55, 1.15, 1.55, 1.05, 0.75, 0.75, 0.65, 0.75]
    col_align = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
                 WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER,
                 WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT]
    style_table(tbl_bench, col_w, col_align)
    add_caption(doc, "Bảng 5.1: Bảng đối chuẩn kết quả thực nghiệm 5 mô hình trên 10.000 ảnh MNIST Test Set", is_table=True)

    add_heading_styled(doc, "5.2. Hiệu năng chi tiết từng lớp chữ số của Modern CNN (99.42%)", level=2)
    add_body_p(doc, "Mô hình Modern CNN đạt độ chính xác gần như tuyệt đối trên tất cả các lớp chữ số, với lớp 0 đạt 99.80% Recall (chỉ sai 2 ảnh) và lớp 1 đạt 99.56% Recall:")

    # Bảng Per-class
    df_pc = pd.read_csv(TABLES_DIR / "per_class_cnn.csv")
    tbl_pc = doc.add_table(rows=len(df_pc) + 2, cols=6)
    pc_headers = ["Lớp", "Số mẫu test", "Precision", "Recall", "F1-Score", "Số ảnh sai"]
    for j, h in enumerate(pc_headers):
        tbl_pc.rows[0].cells[j].paragraphs[0].text = h
    
    for i, r_data in df_pc.iterrows():
        tbl_pc.rows[i+1].cells[0].paragraphs[0].text = str(int(r_data["Chữ số"]))
        tbl_pc.rows[i+1].cells[1].paragraphs[0].text = f"{int(r_data['Số mẫu test']):,}"
        tbl_pc.rows[i+1].cells[2].paragraphs[0].text = f"{r_data['Precision (%)']:.2f}%"
        tbl_pc.rows[i+1].cells[3].paragraphs[0].text = f"{r_data['Recall (%)']:.2f}%"
        tbl_pc.rows[i+1].cells[4].paragraphs[0].text = f"{r_data['F1-score (%)']:.2f}%"
        tbl_pc.rows[i+1].cells[5].paragraphs[0].text = str(int(r_data["Số ảnh đoán sai"]))
    
    # Dòng tổng
    last_idx = len(df_pc) + 1
    tbl_pc.rows[last_idx].cells[0].paragraphs[0].text = "Macro"
    tbl_pc.rows[last_idx].cells[1].paragraphs[0].text = "10.000"
    tbl_pc.rows[last_idx].cells[2].paragraphs[0].text = "99.42%"
    tbl_pc.rows[last_idx].cells[3].paragraphs[0].text = "99.41%"
    tbl_pc.rows[last_idx].cells[4].paragraphs[0].text = "99.42%"
    tbl_pc.rows[last_idx].cells[5].paragraphs[0].text = "Tổng: 58"

    pc_w = [0.8, 1.2, 1.2, 1.2, 1.2, 1.2]
    pc_a = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT,
            WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    style_table(tbl_pc, pc_w, pc_a)
    add_caption(doc, "Bảng 5.2: Hiệu năng chi tiết trên từng lớp chữ số của Modern CNN (Tổng sai: 58 / 10.000 ảnh)", is_table=True)

    add_heading_styled(doc, "5.3. Phân tích 58 mẫu Modern CNN dự đoán sai", level=2)
    add_body_p(doc, "Trên 10.000 ảnh kiểm thử, Modern CNN chỉ dự đoán sai đúng 58 ảnh (tỷ lệ lỗi 0.58%). Hình 5.1 hiển thị trực quan toàn bộ 58 mẫu này cùng nhãn thật (True) và nhãn dự đoán (Pred):")
    add_image_safe(doc, FIGURES_DIR / "08_cnn_error_samples.png", 6.5, "Hình 5.1: Trực quan hóa toàn bộ 58 mẫu CNN dự đoán sai trên 10.000 ảnh MNIST Test Set")

    add_heading_styled(doc, "5.4. Ma trận nhầm lẫn của các mô hình", level=2)
    add_body_p(doc, "Dưới đây là ma trận nhầm lẫn (Confusion Matrix) của mô hình Modern CNN và SVM trên 10.000 ảnh test:")
    add_image_safe(doc, FIGURES_DIR / "cm_modern_cnn.png", 5.2, "Hình 5.2: Ma trận nhầm lẫn của Modern CNN (Độ chính xác: 99.42% · 58 lỗi)")
    add_image_safe(doc, FIGURES_DIR / "cm_svm.png", 5.2, "Hình 5.3: Ma trận nhầm lẫn của SVM RBF Deskew+PCA (Độ chính xác: 98.79% · 121 lỗi)")

    # ==================== CHƯƠNG 6 ====================
    add_heading_styled(doc, "CHƯƠNG 6: TRIỂN KHAI WEB DEMO VÀ KIỂM THỬ HỆ THỐNG", level=1)
    add_heading_styled(doc, "6.1. Kiến trúc hệ thống Web tương tác thời gian thực", level=2)
    add_body_p(doc, "Hệ thống demo tương tác được xây dựng với Backend FastAPI hiệu năng cao, nạp sẵn trọng số của 5 mô hình vào bộ nhớ RAM. Frontend sử dụng HTML5 Canvas mượt mà, hỗ trợ cả chuột và bút cảm ứng, giao diện Soft Glassmorphism tinh tế.")
    add_body_p(doc, "Chân trang (Footer) của hệ thống được tinh gọn chuẩn mực hiển thị thông tin: Phân hiệu Đại học Thủy Lợi.")

    add_heading_styled(doc, "6.2. Pipeline tiền xử lý quang học Center of Mass", level=2)
    add_body_p(doc, "Để đảm bảo nét vẽ tự do từ người dùng có tỷ lệ tương đồng cao nhất với dữ liệu chuẩn MNIST, hệ thống áp dụng thuật toán 5 bước:")
    add_bullet_p(doc, "Phát hiện vùng nét chữ bằng cv2.boundingRect(). Nếu canvas trống (< 15 pixel sáng), trả về mã -1 ngay lập tức.", "• Bước 1 (Bounding Box Crop): ")
    add_bullet_p(doc, "Thu phóng giữ nguyên tỷ lệ khung hình vào ô vuông 20x20 điểm ảnh.", "• Bước 2 (Aspect Ratio Resize): ")
    add_bullet_p(doc, "Tính toán trọng tâm khối lượng quang học: cx = sum(x*I) / sum(I), cy = sum(y*I) / sum(I).", "• Bước 3 (Center of Mass): ")
    add_bullet_p(doc, "Tịnh tiến đưa trọng tâm về chính xác tâm (14.0, 14.0) của khung chuẩn 28x28 NIST.", "• Bước 4 (Canvas Centering): ")
    add_bullet_p(doc, "Chuẩn hóa giá trị điểm ảnh về dải [0.0, 1.0] trước khi đưa vào mô hình suy luận.", "• Bước 5 (Normalization): ")

    add_heading_styled(doc, "6.3. Bộ kiểm thử tự động (Automated Test Suite)", level=2)
    add_body_p(doc, "Hệ thống tích hợp bộ kiểm thử tự động 28 test cases trong tests/test_pipeline.py. Toàn bộ 28 bài kiểm tra từ tính toàn vẹn dữ liệu, kiểm tra không rò rỉ, tham số CNN 160.074 đến các API endpoints đều đạt kết quả tuyệt đối: 28/28 Tests Passed (100%).")

    # ==================== CHƯƠNG 7 ====================
    add_heading_styled(doc, "CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", level=1)
    add_heading_styled(doc, "7.1. Kết luận khoa học", level=2)
    add_body_p(doc, "1. Kỹ thuật nắn thẳng góc nghiêng Deskewing kết hợp giảm chiều PCA (113 chiều) đã tạo bước đột phá cho các thuật toán học máy kinh điển, đưa SVM RBF đạt đến 98.79% và k-NN đạt 98.06% Accuracy.")
    add_body_p(doc, "2. Modern CNN với 3 khối tích chập chuẩn hóa và cơ chế dừng sớm Early Stopping trên tập Validation độc lập đã chứng minh sức mạnh tuyệt đối với đỉnh cao 99.42% Test Accuracy (chỉ sai 58 ảnh trên 10.000 ảnh test).")
    add_body_p(doc, "3. Toàn bộ giải pháp đã được đóng gói hoàn chỉnh thành ứng dụng Web trực quan, vận hành ổn định thời gian thực.")

    add_heading_styled(doc, "7.2. Hướng phát triển trong tương lai", level=2)
    add_bullet_p(doc, "Mở rộng bài toán nhận dạng chuỗi chữ số viết tay liên tục ứng dụng mô hình CRNN (Convolutional Recurrent Neural Network) kết hợp CTC Loss.")
    add_bullet_p(doc, "Xuất mô hình sang định dạng ONNX và tối ưu lượng tử hóa INT8 để nhúng trực tiếp vào các thiết bị AI biên (Edge AI) và camera thông minh.")

    add_heading_styled(doc, "7.3. Bảng phân công nhiệm vụ và tỷ lệ đóng góp của Nhóm 03", level=2)
    
    # Bảng phân công
    tbl_pc_m = doc.add_table(rows=3, cols=6)
    pc_m_headers = ["STT", "Họ và Tên", "Mã SV", "Vai trò", "Nhiệm vụ chính phụ trách", "Đóng góp"]
    for j, h in enumerate(pc_m_headers):
        tbl_pc_m.rows[0].cells[j].paragraphs[0].text = h
    
    m_data = [
        ["1", "Đoàn Anh Vũ", "2351267280", "Nhóm trưởng",
         "Quản lý dự án, pipeline nạp & EDA dữ liệu, mô hình Modern CNN (99.42%), Naive Bayes, viết Chương 1, 3, 5 báo cáo và slide.", "50.0%"],
        ["2", "Nguyễn Hồng Nguyên", "2351267273", "Thành viên",
         "Nghiên cứu Deskewing, PCA 113D, mô hình SVM (98.79%), k-NN (98.06%), Random Forest (96.99%), Web Demo, 28 tests, viết Chương 2, 4, 6, 7.", "50.0%"]
    ]
    for i, r_row in enumerate(m_data):
        for j, val in enumerate(r_row):
            tbl_pc_m.rows[i+1].cells[j].paragraphs[0].text = val
    
    m_w = [0.45, 1.25, 0.95, 0.95, 3.0, 0.6]
    m_a = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER,
           WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    style_table(tbl_pc_m, m_w, m_a)
    add_caption(doc, "Bảng 7.1: Bảng phân công nhiệm vụ và tỷ lệ đóng góp thành viên Nhóm 03", is_table=True)

    # ==================== TÀI LIỆU THAM KHẢO ====================
    add_heading_styled(doc, "TÀI LIỆU THAM KHẢO", level=1)
    refs = [
        "1. LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278-2324.",
        "2. Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273-297.",
        "3. Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32.",
        "4. Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer Science+Business Media, LLC.",
        "5. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "6. Paszke, A., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. NeurIPS 2019, 32.",
        "7. Bộ môn Khoa học Máy tính — Khoa Công nghệ Thông tin. Giáo trình Nhận dạng mẫu. Phân hiệu Trường Đại học Thủy Lợi, 2026."
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.line_spacing = 1.2
        p_r.paragraph_format.space_after = Pt(4)
        run_r = p_r.add_run(r)
        run_r.font.name = "Times New Roman"
        run_r.font.size = Pt(11.5)

    doc.save(DOCX_PATH)
    print(f"-> Xuất thành công file Word: {DOCX_PATH}")


if __name__ == "__main__":
    build_full_docx()
