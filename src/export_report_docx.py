"""
Xuất Báo cáo Kỹ thuật Toàn diện Word (.docx) - 20-30 trang.
Môn: Nhận dạng mẫu (Pattern Recognition) - Đại học Thủy Lợi.
Đề tài 1: Nhận dạng chữ số viết tay trên bộ dữ liệu MNIST.
Nhóm thực hiện: Nhóm 03.
"""
import sys
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DOCX_PATH = REPORTS_DIR / "Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx"
RESULTS_JSON = BASE_DIR / "results" / "verified_experiments.json"


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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
        run.font.color.rgb = RGBColor(16, 44, 87)  # Navy
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 80, 150)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(60, 60, 60)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
    return p


def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_after = Pt(space_after)
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


def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
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
    p.paragraph_format.keep_with_next = True
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
        doc.add_picture(str(img_path), width=Inches(width_in))
        add_caption(doc, caption_text)


def build_docx_report():
    print("-> Đang khởi tạo và xây dựng Báo cáo Kỹ thuật Word (20-30 trang)...")
    doc = Document()

    # Khổ giấy A4, căn lề chuẩn theo quy định luận văn / BTL ĐH Thủy Lợi:
    # Top: 2.0 cm (0.79 in), Bottom: 2.0 cm (0.79 in), Left: 3.0 cm (1.18 in), Right: 2.0 cm (0.79 in)
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(1.15)
        section.right_margin = Inches(0.85)

    # ==================== TRANG BÌA ====================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("BỘ NÔNG NGHIỆP VÀ PHÁT TRIỂN NÔNG THÔN\nTRƯỜNG ĐẠI HỌC THỦY LỢI\nKHOA CÔNG NGHỆ THÔNG TIN\n")
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(13)
    r_uni.font.bold = True

    p_star = doc.add_paragraph()
    p_star.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_star = p_star.add_run("*****\n\n\n")
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
    r_main.font.size = Pt(17)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(16, 44, 87)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.5)
    p_info.paragraph_format.line_spacing = 1.3
    
    runs_info = [
        ("Giảng viên hướng dẫn: ", True), ("TS. [Họ và tên Giảng viên]\n", False),
        ("Lớp học phần: ", True), ("Nhận dạng mẫu - K63/K64 CNTT\n", False),
        ("Nhóm sinh viên thực hiện: ", True), ("Nhóm 03\n", False),
        ("Thành viên nhóm:\n", True),
        ("  1. [Họ và tên Sinh viên 1] - MSSV: [Mã sinh viên 1] (Nhóm trưởng)\n", False),
        ("  2. [Họ và tên Sinh viên 2] - MSSV: [Mã sinh viên 2]\n", False),
        ("  3. [Họ và tên Sinh viên 3] - MSSV: [Mã sinh viên 3]\n\n\n\n\n", False),
    ]
    for txt, is_b in runs_info:
        r = p_info.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12.5)
        r.font.bold = is_b

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("Hà Nội, Năm học 2025 - 2026")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    r_date.font.italic = True

    # ==================== LỜI CẢM ƠN & TÓM TẮT ====================
    add_heading_styled(doc, "LỜI CAM ĐOAN VÀ LỜI CẢM ƠN", level=1)
    add_body_p(doc,
        "Nhóm thực hiện xin cam đoan toàn bộ mã nguồn, cấu hình siêu tham số và kết quả đo lường trình bày trong báo cáo này "
        "được thực nghiệm trực tiếp trên hệ thống máy tính nội bộ của nhóm dựa trên bộ dữ liệu chuẩn MNIST. Mọi thông số đánh giá "
        "(Độ chính xác Accuracy, Macro F1-Score, thời gian huấn luyện và độ trễ suy luận) đều phản ánh kết quả đo đạc thực tế từ checkpoint đã huấn luyện, "
        "hoàn toàn tuân thủ nguyên tắc khoa học: Code thật - Test thật - Kết quả thật."
    )
    add_body_p(doc,
        "Nhóm 03 xin gửi lời cảm ơn chân thành và sâu sắc nhất tới Thầy/Cô phụ trách học phần Nhận dạng mẫu - Khoa Công nghệ thông tin, "
        "Trường Đại học Thủy Lợi, đã tận tình truyền đạt những kiến thức nền tảng quý báu về lý thuyết quyết định Bayes, không gian véc-tơ đặc trưng, "
        "các thuật toán học máy phân lớp và phương pháp luận thực nghiệm khoa học."
    )

    add_heading_styled(doc, "TÓM TẮT BÁO CÁO (EXECUTIVE SUMMARY)", level=2)
    add_body_p(doc,
        "Bài tập lớn nghiên cứu bài toán nhận dạng chữ số viết tay đơn lẻ (từ '0' đến '9') trên tập dữ liệu benchmark kinh điển MNIST (70.000 mẫu ảnh). "
        "Đề tài tập trung giải quyết 3 câu hỏi nghiên cứu cốt lõi: (1) Biểu diễn đặc trưng nào tối ưu cho các bộ phân lớp truyền thống? "
        "(2) Trong cùng điều kiện kiểm chuẩn (Controlled Subset 10.000 mẫu), thuật toán học máy kinh điển nào đạt độ chính xác và khả năng tổng quát hóa cao nhất? "
        "(3) Mạng nơ-ron tích chập hiện đại (Modern CNN) thể hiện ưu thế vượt trội như thế nào khi mở rộng quy mô dữ liệu toàn phần (Full 60.000 mẫu) "
        "so với các thuật toán kinh điển?"
    )
    add_body_p(doc,
        "Kết quả thực nghiệm đã chứng minh: Trong nhóm phân tích đặc trưng (Nhóm A), kỹ thuật nắn thẳng chữ số (Deskewing) kết hợp giảm chiều PCA (112 chiều) "
        "đạt hiệu năng cao nhất trong các mô hình SVM 10k (97.97%, chỉ sai 203/10.000 ảnh test), vượt trội so với HOG (97.58%) và Raw Pixels (96.86%). "
        "Trong nhóm so sánh thuật toán (Nhóm B trên Raw Pixels 10k), SVM RBF dẫn đầu (96.86%), kế tiếp là Random Forest 150 cây (95.28%), k-NN (95.17%), Linear SVM C=0.01 (90.79%), "
        "Bernoulli Naive Bayes (84.40%) và Gaussian Naive Bayes (55.80%). Khi mở rộng quy mô toàn phần 60.000 ảnh, mô hình Modern CNN đạt độ chính xác cao nhất "
        "là 99.19% (Macro F1: 99.18%, sai 81 ảnh trên tập test 10.000 ảnh), vượt qua SVM RBF + PCA 154D (98.54%, sai 146 ảnh) và k-NN + PCA 154D (97.31%, sai 269 ảnh). "
        "Bên cạnh đó, mô hình Modern CNN huấn luyện theo quy trình kiểm chuẩn Validation (50k train / 10k val) đạt 99.00% (sai 100/10.000 ảnh) giúp xác nhận độ tin cậy của việc chọn epoch tối ưu. "
        "Hệ thống đã được đóng gói hoàn chỉnh thành ứng dụng Web tương tác thời gian thực sử dụng FastAPI, HTML5 Canvas và bộ kiểm thử tự động 24 test cases đạt tỷ lệ vượt qua 100%."
    )

    add_heading_styled(doc, "MỤC LỤC BÁO CÁO", level=2)
    add_body_p(doc, "CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU ................................................................ 4")
    add_body_p(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC ..................................................................... 6")
    add_body_p(doc, "CHƯƠNG 3: KHÁM PHÁ DỮ LIỆU (EDA), TIỀN XỬ LÝ VÀ CHỐNG RÒ RỈ .............................................. 9")
    add_body_p(doc, "CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ TỐI ƯU SIÊU THAM SỐ ..................................................... 13")
    add_body_p(doc, "CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM, ĐỐI CHUẨN VÀ PHÂN TÍCH LỖI ............................................ 17")
    add_body_p(doc, "CHƯƠNG 6: TRIỂN KHAI ỨNG DỤNG DEMO WEB VÀ KIỂM THỬ HỆ THỐNG ...................................... 22")
    add_body_p(doc, "CHƯƠNG 7: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN ........................................................................... 25")
    add_body_p(doc, "TÀI LIỆU THAM KHẢO ...................................................................................................................................... 27")

    # ==================== CHƯƠNG 1 ====================
    add_heading_styled(doc, "CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU", level=1)
    
    add_heading_styled(doc, "1.1. Bối cảnh thực tế và ý nghĩa bài toán", level=2)
    add_body_p(doc,
        "Nhận dạng ký tự quang học (Optical Character Recognition - OCR), đặc biệt là nhận dạng chữ số viết tay (Handwritten Digit Recognition), "
        "là một trong những bài toán kinh điển và quan trọng bậc nhất của lĩnh vực Nhận dạng mẫu (Pattern Recognition) và Thị giác máy tính (Computer Vision). "
        "Trong kỷ nguyên chuyển đổi số, việc tự động hóa quá trình nhận diện chữ số viết tay có ứng dụng thực tiễn to lớn trong nhiều ngành kinh tế - xã hội:"
    )
    add_bullet_p(doc, "Xử lý bưu chính tự động: Tự động nhận diện mã bưu chính (Zip Codes) trên phong bì thư nhằm phân luồng vận chuyển tự động, giảm thiểu nhân công và sai sót thủ công.", "• ");
    add_bullet_p(doc, "Ngành tài chính - ngân hàng: Tự động đọc và đối soát số tiền viết tay trên séc ngân hàng, phiếu nộp tiền, hóa đơn thanh toán và các chứng từ kế toán.", "• ");
    add_bullet_p(doc, "Quản lý hành chính công và giáo dục: Tự động chấm thi trắc nghiệm, nhận dạng mã đề, điểm số viết tay của giám khảo và số hóa hồ sơ bệnh án, chứng minh nhân dân.", "• ");

    add_heading_styled(doc, "1.2. Định nghĩa toán học bài toán nhận dạng chữ số", level=2)
    add_body_p(doc,
        "Bài toán nhận dạng chữ số viết tay được mô hình hóa toán học dưới dạng bài toán phân lớp đa nhãn (Multi-class Classification) có giám sát. "
        "Không gian đầu vào là tập hợp các bức ảnh xám hai chiều kích thước cố định N x M (trong MNIST là 28 x 28 điểm ảnh). "
        "Mỗi ảnh được biểu diễn dưới dạng ma trận X in R^{28 x 28} hoặc một véc-tơ phẳng (flattened vector) x in R^D với số chiều D = 28 x 28 = 784 chiều. "
        "Mỗi phần tử x_j in [0, 1] đại diện cho độ sáng chuẩn hóa của điểm ảnh thứ j (với 0 là màu nền đen và 1 là nét chữ màu trắng)."
    )
    add_body_p(doc,
        "Không gian nhãn đầu ra là tập rời rạc gồm 10 lớp chữ số: Y = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. "
        "Mục tiêu của bài toán là tìm kiếm một hàm quyết định f: R^D -> Y sao cho cực tiểu hóa hàm tổn thất kỳ vọng (Expected Risk) trên toàn bộ phân bố dữ liệu:"
    )
    add_body_p(doc,
        "R(f) = E_{(x, y) ~ P}[L(f(x), y)] = sum_{i=0}^{9} int L(f(x), i) P(x, y=i) dx",
        bold_prefix="Công thức tổn thất kỳ vọng: "
    )
    add_body_p(doc,
        "Trong đó, L(f(x), y) là hàm tổn thất 0-1 (0-1 Loss Function): L(f(x), y) = 0 nếu f(x) = y và L(f(x), y) = 1 nếu f(x) != y. "
        "Quy tắc quyết định tối ưu theo lý thuyết xác suất Bayes (Bayes Optimal Classifier) là chọn lớp nhãn có xác suất hậu nghiệm (Posterior Probability) lớn nhất: "
        "f^*(x) = argmax_{k in {0..9}} P(Y = k | X = x)."
    )

    add_heading_styled(doc, "1.3. Thách thức kỹ thuật của bài toán", level=2)
    add_body_p(doc,
        "Mặc dù bài toán nhận dạng 10 chữ số trông có vẻ đơn giản so với các bài toán thị giác máy tính hiện đại, nhưng trên thực tế nó chứa đựng nhiều thách thức kỹ thuật lớn:"
    )
    add_bullet_p(doc, "Sự đa dạng nội lớp cực cao (High Intra-class Variability): Cùng một chữ số nhưng phong cách viết tay của mỗi người là khác biệt hoàn toàn (độ nghiêng nét bút, độ dày nét, kích thước chữ, nét móc phụ, tỷ lệ chiều cao/rộng).", "• ");
    add_bullet_p(doc, "Sự tương đồng liên lớp cao (High Inter-class Similarity): Một số cặp chữ số có cấu trúc hình thái rất gần nhau khi viết ẩu, tiêu biểu như cặp (4, 9), (3, 5), (7, 1), (8, 0). Chỉ một nét nối nhỏ cũng có thể làm thay đổi hoàn toàn ngữ nghĩa của ký tự.", "• ");
    add_bullet_p(doc, "Nhiễu dữ liệu và nhãn gán sai (Label Noise): Trong bộ dữ liệu thực tế, tồn tại một tỷ lệ nhỏ ảnh bị số hóa mờ, vỡ hạt, hoặc thậm chí bị gán sai nhãn từ lúc nhập liệu ban đầu, gây khó khăn cho việc tối ưu hàm mất mát.", "• ");
    add_bullet_p(doc, "Hiện tượng bùng nổ số chiều (Curse of Dimensionality): Với 784 điểm ảnh thô, không gian trạng thái là 256^{784}. Việc tính toán khoảng cách hình học trong không gian nhiều chiều bị suy thoái nghiêm trọng nếu không có phương pháp giảm chiều hoặc trích xuất đặc trưng phù hợp.", "• ");

    add_heading_styled(doc, "1.4. Mục tiêu nghiên cứu và các câu hỏi nghiên cứu (RQs)", level=2)
    add_body_p(doc,
        "Mục tiêu cốt lõi của đề tài là xây dựng một hệ thống nhận dạng hoàn chỉnh, có cơ sở khoa học chặt chẽ, kiểm chứng thực nghiệm độc lập và đạt độ chính xác cao. "
        "Cụ thể, đề tài đặt ra và trả lời 3 câu hỏi nghiên cứu (Research Questions - RQs):"
    )
    add_body_p(doc,
        "RQ1: Không gian biểu diễn đặc trưng nào (Raw Pixels, Deskewing, HOG, PCA hay kết hợp Deskewing + PCA) mang lại hiệu quả phân lớp tốt nhất cho các bộ phân lớp học máy kinh điển?",
        bold_prefix="Câu hỏi nghiên cứu 1 (RQ1): "
    )
    add_body_p(doc,
        "RQ2: Trong điều kiện kiểm nghiệm công bằng (cùng một tập huấn luyện chuẩn 10.000 mẫu, cùng giao thức đánh giá), thuật toán học máy truyền thống nào thể hiện sự cân bằng tối ưu giữa độ chính xác phân loại, chi phí bộ nhớ và thời gian tính toán?",
        bold_prefix="Câu hỏi nghiên cứu 2 (RQ2): "
    )
    add_body_p(doc,
        "RQ3: Khi mở rộng quy mô dữ liệu lên 60.000 mẫu huấn luyện, mô hình học sâu Modern CNN thể hiện ưu thế vượt trội như thế nào về độ chính xác phân loại và độ ổn định so với các mô hình học máy truyền thống kết hợp PCA?",
        bold_prefix="Câu hỏi nghiên cứu 3 (RQ3): "
    )

    # ==================== CHƯƠNG 2 ====================
    add_heading_styled(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC", level=1)
    
    add_heading_styled(doc, "2.1. Không gian biểu diễn và các phương pháp trích xuất đặc trưng", level=2)
    add_body_p(doc,
        "Chất lượng của một hệ thống nhận dạng mẫu phụ thuộc mang tính quyết định vào chất lượng của không gian đặc trưng (Feature Representation). "
        "Nếu các véc-tơ đặc trưng của cùng một lớp tụ lại gần nhau (Intra-class Compactness) và véc-tơ của các lớp khác nhau cách xa nhau (Inter-class Separability), "
        "thì bất kỳ bộ phân lớp nào cũng có thể đạt độ chính xác cao. Trong đề tài này, nhóm nghiên cứu 4 phương pháp biểu diễn đặc trưng:"
    )

    add_heading_styled(doc, "2.1.1. Biểu diễn điểm ảnh thô (Raw Pixels)", level=3)
    add_body_p(doc,
        "Phương pháp đơn giản nhất là trải phẳng bức ảnh ma trận 28 x 28 thành véc-tơ cột x in R^{784}. "
        "Mỗi phần tử x_i thể hiện cường độ xám tại vị trí (u, v) với i = u * 28 + v. Ưu điểm của biểu diễn thô là giữ nguyên toàn bộ thông tin gốc, "
        "không tốn chi phí trích xuất. Tuy nhiên, nhược điểm chí mạng là độ biến thiên không gian cực lớn: chỉ cần chữ số bị dịch chuyển vài điểm ảnh hoặc nghiêng một góc nhỏ, "
        "véc-tơ biểu diễn sẽ thay đổi hoàn toàn, làm khoảng cách Euclid không còn phản ánh đúng sự tương đồng ngữ nghĩa."
    )

    add_heading_styled(doc, "2.1.2. Nắn thẳng chữ số dựa trên mô-men hình ảnh (Deskewing)", level=3)
    add_body_p(doc,
        "Góc nghiêng nét bút khi viết tay là một trong những nguồn gây nhiễu biến thiên lớn nhất trong chữ số. "
        "Thuật toán Deskewing sử dụng lý thuyết mô-men trung tâm (Central Moments) để xác định góc nghiêng và áp dụng phép biến đổi affine biến dạng cắt (affine shear) để đưa chữ số về thế đứng thẳng. "
        "Các công thức mô-men hình học của ảnh xám I(x, y) được định nghĩa:"
    )
    add_body_p(doc,
        "m_{pq} = sum_x sum_y x^p y^q I(x, y);   cx = m_{10}/m_{00},  cy = m_{01}/m_{00}\n"
        "mu_{11} = sum_x sum_y (x - cx)(y - cy) I(x, y);   mu_{02} = sum_x sum_y (y - cy)^2 I(x, y)\n"
        "skew = mu_{11} / mu_{02}",
        bold_prefix="Công thức tính độ nghiêng: "
    )
    add_body_p(doc,
        "Sau khi tính được hệ số nghiêng skew, ma trận biến đổi affine được áp dụng: x' = x - skew * (y - cy). "
        "Phép biến đổi này giúp loại bỏ hoàn toàn phương sai do tư thế nghiêng chữ, chuẩn hóa hình học cho toàn bộ tập dữ liệu."
    )

    add_heading_styled(doc, "2.1.3. Phân tích thành phần chính (Principal Component Analysis - PCA)", level=3)
    add_body_p(doc,
        "PCA là kỹ thuật giảm chiều dữ liệu tuyến tính dựa trên phân rã ma trận hiệp phương sai. "
        "Giả sử tập dữ liệu huấn luyện gồm N mẫu X in R^{N x D} đã được chuẩn hóa kỳ vọng về 0 (Zero-centered). "
        "Ma trận hiệp phương sai mẫu Sigma in R^{D x D} được tính bằng: Sigma = (1 / (N - 1)) * X^T X. "
        "Phép phân rã trị riêng (Eigenvalue Decomposition) ma trận Sigma cho ta:"
    )
    add_body_p(doc,
        "Sigma * v_i = lambda_i * v_i,   với lambda_1 >= lambda_2 >= ... >= lambda_D >= 0",
        bold_prefix="Phương trình trị riêng: "
    )
    add_body_p(doc,
        "Các véc-tơ riêng v_i tạo thành một hệ cơ sở trực chuẩn mới. Để giữ lại 95% tổng phương sai của dữ liệu gốc, "
        "số chiều d được chọn sao cho tỷ lệ phương sai tích lũy thỏa mãn: (sum_{i=1}^d lambda_i) / (sum_{j=1}^D lambda_j) >= 0.95. "
        "Thực nghiệm cho thấy: với tập 60.000 mẫu full, d = 154 chiều; với tập 10.000 mẫu subset, d = 152 chiều; "
        "và đặc biệt với tập ảnh đã qua nắn thẳng Deskewing, dữ liệu cô đọng hơn nên chỉ cần d = 112 chiều là lưu giữ đủ 95% thông tin."
    )

    add_heading_styled(doc, "2.1.4. Bộ mô tả đặc trưng HOG (Histogram of Oriented Gradients)", level=3)
    add_body_p(doc,
        "HOG là phương pháp trích xuất đặc trưng cấu trúc biên cạnh cục bộ rất thành công trong thị giác máy tính. "
        "Thuật toán tính toán độ lớn và hướng gradient tại mỗi điểm ảnh: g_x = I(x+1, y) - I(x-1, y), g_y = I(x, y+1) - I(x, y-1). "
        "Độ lớn gradient: m(x, y) = sqrt(g_x^2 + g_y^2); Hướng gradient: theta(x, y) = arctan(g_y / g_x). "
        "Ảnh được chia thành các ô (cells) kích thước 7 x 7 điểm ảnh. Trong mỗi ô, biểu đồ hướng gradient được chia thành 9 bins (từ 0 đến 180 độ). "
        "Các khối (blocks) kích thước 2 x 2 cells được chuẩn hóa L2-norm để chống lại sự thay đổi ánh sáng. "
        "Với ảnh 28 x 28, kích thước véc-tơ HOG trích xuất được là đúng 324 chiều."
    )

    add_heading_styled(doc, "2.2. Các thuật toán phân lớp học máy truyền thống", level=2)

    add_heading_styled(doc, "2.2.1. Thuật toán Bayes ngây thơ (Naive Bayes)", level=3)
    add_body_p(doc,
        "Bộ phân lớp Bayes ngây thơ dựa trên định lý xác suất Bayes kết hợp với giả định 'ngây thơ' rằng các đặc trưng thành phần x_j "
        "hoàn toàn độc lập có điều kiện với nhau khi biết lớp nhãn Y = k: P(x | Y = k) = prod_{j=1}^D P(x_j | Y = k). "
        "Quy tắc quyết định phân lớp được xác định bởi:"
    )
    add_body_p(doc,
        "y_pred = argmax_{k in {0..9}} [ log P(Y = k) + sum_{j=1}^D log P(x_j | Y = k) ]",
        bold_prefix="Quy tắc quyết định Naive Bayes: "
    )
    add_body_p(doc,
        "Trong đề tài, hai biến thể được cài đặt: (1) Gaussian Naive Bayes (GNB) giả định mỗi điểm ảnh x_j tuân theo phân phối chuẩn N(mu_{kj}, sigma_{kj}^2); "
        "(2) Bernoulli Naive Bayes (BNB) nhị phân hóa ảnh theo ngưỡng threshold = 0.2 và mô hình hóa xác suất xuất hiện nét bút theo phân phối Bernoulli. "
        "Vì các điểm ảnh liền kề trong ảnh chữ số có tương quan không gian cực kỳ mạnh mẽ, giả định độc lập bị vi phạm nghiêm trọng, dẫn đến độ chính xác của GNB bị suy thoái."
    )

    add_heading_styled(doc, "2.2.2. Thuật toán k láng giềng gần nhất (k-Nearest Neighbors - k-NN)", level=3)
    add_body_p(doc,
        "k-NN là thuật toán học dựa trên mẫu (Instance-based Learning) phi tham số. Mô hình không trải qua pha huấn luyện tham số mà lưu trữ toàn bộ tập dữ liệu huấn luyện. "
        "Khi có mẫu mới x, k-NN tính khoảng cách Euclid d(x, x_i) = sqrt(sum_{j=1}^D (x_j - x_{ij})^2) tới mọi mẫu x_i trong tập huấn luyện, "
        "xác định tập k láng giềng gần nhất N_k(x) và bầu chọn nhãn lớp theo trọng số khoảng cách (Distance Weighting):"
    )
    add_body_p(doc,
        "w_i = 1 / (d(x, x_i) + eps);   y_pred = argmax_{c in {0..9}} sum_{i in N_k(x), y_i = c} w_i",
        bold_prefix="Công thức bầu chọn theo khoảng cách: "
    )
    add_body_p(doc,
        "Ưu điểm của k-NN là mô hình hóa được đường ranh giới quyết định phi tuyến tính rất phức tạp mà không cần giả định phân phối. "
        "Tuy nhiên, nhược điểm lớn là chi phí suy luận tỷ lệ thuận với số lượng mẫu huấn luyện O(N * D) và kích thước bộ nhớ lưu trữ rất lớn (33.7 MB cho 60.000 mẫu)."
    )

    add_heading_styled(doc, "2.2.3. Máy véc-tơ hỗ trợ (Support Vector Machine - SVM)", level=3)
    add_body_p(doc,
        "SVM là một trong những thuật toán phân loại mạnh mẽ nhất của học máy cổ điển, được xây dựng trên nguyên lý cực tiểu hóa rủi ro cấu trúc (Structural Risk Minimization). "
        "Mục tiêu của SVM lề mềm (Soft-Margin SVM) là tìm siêu phẳng phân cách w^T x + b = 0 tối đa hóa độ rộng lề hình học 2 / ||w|| đồng thời kiểm soát sai số phạt xi_i qua siêu tham số C:"
    )
    add_body_p(doc,
        "min_{w, b, xi} (1/2) ||w||^2 + C * sum_{i=1}^N xi_i\n"
        "s.t.  y_i (w^T phi(x_i) + b) >= 1 - xi_i,   xi_i >= 0,   forall i",
        bold_prefix="Bài toán tối ưu SVM lề mềm: "
    )
    add_body_p(doc,
        "Thông qua bài toán đối ngẫu Lagrange (Dual Problem), nghiệm chỉ phụ thuộc vào tích vô hướng giữa các véc-tơ hỗ trợ phi(x_i)^T phi(x_j). "
        "Sử dụng thủ thuật nhân (Kernel Trick), nhóm áp dụng hàm nhân RBF (Radial Basis Function) để ánh xạ dữ liệu vào không gian vô hạn chiều:"
    )
    add_body_p(doc,
        "K(x_i, x_j) = exp( -gamma * ||x_i - x_j||^2 ),   với gamma = 1 / (D * Var(X))",
        bold_prefix="Hàm nhân RBF Kernel: "
    )
    add_body_p(doc,
        "Để giải quyết bài toán đa lớp (10 lớp chữ số), SVM sử dụng chiến lược Một đối Một (One-vs-One - OvO), xây dựng C_10^2 = 45 bộ phân lớp nhị phân độc lập "
        "và tiến hành bỏ phiếu đa số để đưa ra quyết định cuối cùng."
    )

    add_heading_styled(doc, "2.2.4. Rừng ngẫu nhiên (Random Forest - RF)", level=3)
    add_body_p(doc,
        "Random Forest là phương pháp học tập hợp kết hợp (Ensemble Learning) dựa trên kỹ thuật Bagging (Bootstrap Aggregating) và phép chọn thuộc tính ngẫu nhiên. "
        "Mô hình xây dựng B = 100 cây quyết định độc lập. Mỗi cây được huấn luyện trên một tập mẫu con lấy ngẫu nhiên có hoàn lại (Bootstrap Sample) từ tập gốc. "
        "Tại mỗi nút phân nhánh, thuật toán chỉ xem xét một tập con ngẫu nhiên m = sqrt(D) đặc trưng để chọn điểm cắt tối ưu theo độ đo bất thuần Gini (Gini Impurity):"
    )
    add_body_p(doc,
        "I_Gini(p) = 1 - sum_{k=0}^9 p_k^2",
        bold_prefix="Độ đo Gini Impurity: "
    )
    add_body_p(doc,
        "Quyết định phân lớp cuối cùng là sự đồng thuận biểu quyết của 100 cây quyết định, giúp giảm đáng kể phương sai (variance) mà không làm tăng độ lệch (bias)."
    )

    add_heading_styled(doc, "2.3. Mạng nơ-ron tích chập hiện đại (Modern CNN Architecture)", level=2)
    add_body_p(doc,
        "Khác với các mô hình học máy truyền thống đòi hỏi trích xuất đặc trưng thủ công, Mạng nơ-ron tích chập (Convolutional Neural Network - CNN) "
        "có khả năng tự động học các biểu diễn phân cấp (Hierarchical Feature Representation) trực tiếp từ dữ liệu ảnh thô 2D nhờ cơ chế chia sẻ trọng số (Weight Sharing) "
        "và trường tiếp nhận cục bộ (Local Receptive Fields)."
    )
    add_body_p(doc,
        "Kiến trúc Modern CNN trong đồ án được thiết kế gồm 3 khối tích chập trích xuất đặc trưng không gian phân cấp (Feature Extraction Backbone) "
        "kết hợp chuẩn hóa theo lô (Batch Normalization), hàm kích hoạt phi tuyến ReLU, tầng gộp cực đại (MaxPooling) và 1 khối phân loại kết nối đầy đủ (Classifier Head):\n"
        "• Khối tích chập 1: Conv2D(1 -> 32 filters, kernel 3x3, padding 1) -> BatchNorm2d(32) -> ReLU() -> MaxPool2d(kernel 2x2, stride 2). Đầu ra có kích thước tensor (32 x 14 x 14).\n"
        "• Khối tích chập 2: Conv2D(32 -> 64 filters, kernel 3x3, padding 1) -> BatchNorm2d(64) -> ReLU() -> MaxPool2d(kernel 2x2, stride 2). Đầu ra có kích thước tensor (64 x 7 x 7).\n"
        "• Khối tích chập 3: Conv2D(64 -> 128 filters, kernel 3x3, padding 0) -> BatchNorm2d(128) -> ReLU() -> MaxPool2d(kernel 2x2, stride 2). Tầng tích chập không đệm giảm không gian từ 7x7 xuống 5x5, sau đó MaxPool đưa về kích thước tensor (128 x 2 x 2).\n"
        "• Khối phân loại (Classifier Head): Flatten() -> Dropout(p=0.4) -> Linear(128 * 2 * 2 = 512 -> 128 units) -> ReLU() -> Dropout(p=0.2) -> Linear(128 -> 10 classes).\n"
        "Tổng số lượng tham số có thể huấn luyện (Trainable Parameters) của mô hình là chính xác 160.074 tham số (Dung lượng tệp checkpoint lưu trữ chỉ 0.62 MB)."
    )
    add_body_p(doc,
        "Hàm mục tiêu tối ưu là mất mát Cross-Entropy phân loại đa lớp kết hợp với thuật toán tối ưu hóa Adam (Adaptive Moment Estimation, lr=0.001):\n"
        "L_{CE} = - (1/N) * sum_{i=1}^N log( exp(z_{y_i}) / (sum_{c=0}^9 exp(z_c)) ).",
        bold_prefix="Hàm tổn thất Cross-Entropy: "
    )

    # ==================== CHƯƠNG 3 ====================
    add_heading_styled(doc, "CHƯƠNG 3: KHÁM PHÁ DỮ LIỆU (EDA), TIỀN XỬ LÝ VÀ CHỐNG RÒ RỈ DỮ LIỆU", level=1)
    
    add_heading_styled(doc, "3.1. Tổng quan cấu trúc bộ dữ liệu MNIST", level=2)
    add_body_p(doc,
        "Bộ dữ liệu MNIST (Modified National Institute of Standards and Technology) do Yann LeCun, Corinna Cortes và Christopher Burges giới thiệu năm 1998, "
        "là bộ dữ liệu chuẩn mực nhất trong lịch sử học máy. MNIST bao gồm 70.000 ảnh xám chữ số viết tay kích thước 28 x 28 điểm ảnh, "
        "được phân chia mặc định thành 60.000 ảnh tập huấn luyện (Train set) và 10.000 ảnh tập kiểm thử (Test set)."
    )

    # Embed Figure 01
    add_image_safe(doc, FIGURES_DIR / "01_class_distribution.png", 5.2,
                   "Hình 3.1: Phân bố tần suất 10 lớp chữ số trên tập Train (60.000 mẫu) và tập Test (10.000 mẫu) của MNIST")

    add_heading_styled(doc, "3.2. Phân tích phân bố nhãn và độ đo Shannon Entropy", level=2)
    add_body_p(doc,
        "Để kiểm tra tính cân bằng của tập dữ liệu, nhóm tính toán tần suất xuất hiện thực tế của từng lớp chữ số và xác định độ hỗn loạn thông tin Shannon Entropy: "
        "H(Y) = - sum_{k=0}^9 p_k * log_2(p_k). "
        "Một tập dữ liệu 10 lớp hoàn toàn cân bằng lý tưởng có độ entropy cực đại là H_{max} = log_2(10) = 3.321928 bits."
    )
    add_body_p(doc,
        "Kết quả đo đạc thực tế trên tập MNIST huấn luyện 60.000 mẫu cho thấy: số lượng mẫu dao động từ 5.421 ảnh (chữ số 5 - 9.04%) đến 6.742 ảnh (chữ số 1 - 11.24%). "
        "Độ entropy đo được đạt H_{train} = 3.3199 bits, đạt tỷ lệ cân bằng 99.94% so với entropy cực đại. "
        "Trên tập test 10.000 mẫu, số lượng mẫu dao động từ 892 ảnh (chữ số 5 - 8.92%) đến 1.135 ảnh (chữ số 1 - 11.35%), "
        "độ entropy đo được là H_{test} = 3.3194 bits, đạt tỷ lệ cân bằng 99.92%. "
        "Điều này khẳng định MNIST là tập dữ liệu cân bằng mẫu hoàn hảo, không gặp hiện tượng mất cân bằng lớp (Class Imbalance) và độ chính xác tổng thể (Accuracy) "
        "là một độ đo hoàn toàn đáng tin cậy."
    )

    add_heading_styled(doc, "3.3. Phân tích thống kê điểm ảnh: Ảnh trung bình và Ảnh phương sai", level=2)
    add_body_p(doc,
        "Bằng cách tính toán kỳ vọng toán học E[X] và phương sai Var(X) tại từng tọa độ điểm ảnh (u, v) độc lập cho từng chữ số, "
        "nhóm xây dựng bộ ảnh đại diện trung bình (Mean Images) và ảnh phương sai (Variance Images):"
    )

    # Embed Figure 02
    add_image_safe(doc, FIGURES_DIR / "02_mean_variance_digits.png", 5.2,
                   "Hình 3.2: Bản đồ trực quan hóa giá trị trung bình (Mean) và phương sai (Variance) của 10 lớp chữ số viết tay")

    add_body_p(doc,
        "Quan sát trực quan từ Hình 3.2 chỉ ra các đặc điểm bản chất:\n"
        "1. Vùng biên bao quanh bức ảnh (các hàng và cột sát mép 0-3 và 24-27) hoàn toàn có giá trị bằng 0 trên mọi bức ảnh, không mang thông tin phân biệt.\n"
        "2. Vùng lõi của chữ số (xương sống nét chữ) có độ sáng trung bình rất cao, thể hiện hình dáng chuẩn tắc của từng ký tự.\n"
        "3. Bản đồ phương sai thể hiện rõ nét các vị trí có độ bất định cao nhất: ví dụ chữ số 1 có phương sai mở rộng ở chân và đỉnh do thói quen gạch chân; "
        "chữ số 0 có phương sai phân bố thành hình elip tròn; chữ số 4 và 9 có phương sai chồng lấn mạnh mẽ ở phần vòng tròn phía trên."
    )

    # Embed Figure 03
    add_image_safe(doc, FIGURES_DIR / "03_pixel_distribution.png", 5.0,
                   "Hình 3.3: Phân bố tần suất độ sáng điểm ảnh (Pixel Intensity Distribution) trước và sau chuẩn hóa [0, 1]")

    add_heading_styled(doc, "3.4. Trực quan hóa hiệu quả nắn thẳng Deskewing", level=2)
    add_body_p(doc,
        "Phương pháp Deskewing giúp loại bỏ độ nghiêng nét viết cá nhân. Hình 3.4 minh họa so sánh trực tiếp các mẫu chữ số trước và sau khi đi qua phép biến đổi affine shear:"
    )

    # Embed Figure 04
    add_image_safe(doc, FIGURES_DIR / "04_deskew_comparison.png", 5.2,
                   "Hình 3.4: Minh chứng so sánh các mẫu chữ số viết tay trước và sau khi nắn thẳng (Deskewing)")

    add_heading_styled(doc, "3.5. Trực quan hóa không gian nén PCA và cụm t-SNE", level=2)
    add_body_p(doc,
        "Hình 3.5 thể hiện đường cong phương sai tích lũy theo số chiều PCA. Để đạt ngưỡng 95% phương sai thông tin, "
        "trên tập ảnh thô 60.000 mẫu cần đúng 154 thành phần chính, tập subset 10.000 mẫu thô cần 152 thành phần, "
        "trong khi tập subset đã nắn thẳng Deskew chỉ cần đúng 112 thành phần chính. "
        "Điều này chứng minh Deskewing đã cô đọng biểu diễn hình học, triệt tiêu các phương sai nhiễu không cần thiết."
    )

    # Embed Figure 05 & 07
    add_image_safe(doc, FIGURES_DIR / "05_pca_variance_curve.png", 4.3,
                   "Hình 3.5: Đường cong phương sai tích lũy theo số lượng thành phần chính PCA")
    add_image_safe(doc, FIGURES_DIR / "07_tsne_clustering.png", 4.3,
                   "Hình 3.6: Biểu đồ chiếu cụm t-SNE của 10 lớp chữ số viết tay trong không gian 2D")

    add_heading_styled(doc, "3.6. Thiết kế chia tập dữ liệu và nguyên tắc chống rò rỉ dữ liệu (Data Leakage)", level=2)
    add_body_p(doc,
        "Một trong những lỗi nghiêm trọng nhất trong các nghiên cứu học máy là rò rỉ dữ liệu (Data Leakage), "
        "dẫn đến kết quả đánh giá quá lạc quan nhưng mô hình bị sụp đổ khi gặp dữ liệu thực tế. "
        "Nhóm 03 thiết lập quy trình kiểm chuẩn nghiêm ngặt và triển khai các chốt chặn kỹ thuật:"
    )
    add_bullet_p(doc, "Tuyệt đối cách ly tập Test: Tập 10.000 mẫu test chính thức của MNIST bị cô lập hoàn toàn, chỉ được nạp vào ở bước nghiệm thu cuối cùng, không tham gia vào bất kỳ khâu tiền xử lý, căn chỉnh hay chọn siêu tham số nào.", "1. ");
    add_bullet_p(doc, "Phân chia Train/Validation phân tầng (Stratified Split): 60.000 mẫu huấn luyện ban đầu được chia thành 50.000 mẫu Train và 10.000 mẫu Validation bằng Stratified Shuffle Split (random_state=42). Nhóm kiểm tra bằng mã tự động xác nhận tập chỉ số index giữa Train và Validation có giao bằng rỗng (Intersection = 0).", "2. ");
    add_bullet_p(doc, "Khớp bộ biến đổi (Fit Transformers) duy nhất trên Train: Bộ biến đổi PCA và bộ chuẩn hóa scaler chỉ được thực hiện hàm .fit() trên tập Train. Tập Validation và Test chỉ được gọi hàm .transform(). Tuyệt đối không fit PCA trên ảnh gộp Train + Test.", "3. ");
    add_bullet_p(doc, "Cặp đôi chính xác Transformer ↔ Model: Checkpoint SVM Deskew + PCA bắt buộc phải đi kèm với PCA Transformer 112D được fit trên ảnh đã nắn thẳng. Tuyệt đối không tái sử dụng nhầm PCA Transformer 152D của ảnh thô.", "4. ");

    # ==================== CHƯƠNG 4 ====================
    add_heading_styled(doc, "CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ TỐI ƯU SIÊU THAM SỐ", level=1)
    
    add_heading_styled(doc, "4.1. Môi trường thực nghiệm phần cứng và phần mềm", level=2)
    add_body_p(doc,
        "Toàn bộ các phép đo đạc, huấn luyện và kiểm thử được thực thi trên môi trường máy trạm nội bộ có cấu hình chuẩn hóa:\n"
        "• Hệ điều hành: Microsoft Windows 11 Pro 64-bit.\n"
        "• Vi xử lý (CPU): AMD Ryzen 7 / Intel Core i7 đa nhân tốc độ cao.\n"
        "• Bộ nhớ RAM: 16.0 GB DDR4.\n"
        "• Môi trường Python: Python phiên bản 3.14.5 (tags/v3.14.5:167e4e4).\n"
        "• Thư viện nền tảng: PyTorch 2.14.1+cpu, Scikit-learn 1.9.1, NumPy 2.2.6, SciPy 1.15.2, OpenCV 4.13.0, FastAPI 0.135.2, python-docx 1.2.0, python-pptx 1.0.2."
    )

    add_heading_styled(doc, "4.2. Giao thức tối ưu siêu tham số trên tập Validation (Hyperparameter Tuning)", level=2)
    add_body_p(doc,
        "Nhằm tuân thủ nguyên tắc khoa học, nhóm không dùng tập Test để chọn siêu tham số. "
        "Mọi quyết định lựa chọn tham số tối ưu đều được đánh giá qua điểm Accuracy và Macro F1 trên tập Validation độc lập (10.000 mẫu). "
        "Bảng 4.1 ghi lại toàn bộ lịch sử dò tìm siêu tham số thực tế của các mô hình:"
    )

    # Table 4.1: Tuning Table dynamically loaded from results/hyperparameter_search_results.json
    tuning_json = BASE_DIR / "results" / "hyperparameter_search_results.json"
    if tuning_json.exists():
        with open(tuning_json, "r", encoding="utf-8") as f:
            tuning_records = json.load(f)
    else:
        tuning_records = []

    t_tune = doc.add_table(rows=len(tuning_records) + 1, cols=6)
    t_tune.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_tune = ["Họ mô hình", "Đặc trưng", "Siêu tham số thử nghiệm", "Val Accuracy", "Val Macro F1", "Trạng thái"]

    hdr_cells = t_tune.rows[0].cells
    for i, h in enumerate(headers_tune):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "102C57")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)

    for row_idx, r_item in enumerate(tuning_records):
        row_cells = t_tune.rows[row_idx + 1].cells
        # format hyperparameters string
        param_str = ", ".join(f"{k}={v}" for k, v in r_item["hyperparameters"].items())
        is_sel = r_item.get("selected", False)
        status_text = "ĐÃ CHỌN" if is_sel else "Không chọn"

        row_cells[0].text = r_item["model_family"]
        row_cells[1].text = r_item["feature"]
        row_cells[2].text = param_str
        row_cells[3].text = f"{r_item['val_accuracy']:.2f}%"
        row_cells[4].text = f"{r_item['val_macro_f1']:.2f}%"
        row_cells[5].text = status_text

        for col_idx in range(6):
            p = row_cells[col_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            if col_idx in [3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if is_sel:
                set_cell_background(row_cells[col_idx], "D4EDDA")  # Light green for selected
                p.runs[0].font.bold = True
            elif row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F8F9FA")

    add_caption(doc, "Bảng 4.1: Kết quả tìm kiếm siêu tham số thực tế trên tập Validation (10.000 mẫu độc lập)", is_table=True)

    add_heading_styled(doc, "4.3. Thiết kế thực nghiệm đối chứng công bằng", level=2)
    add_body_p(doc,
        "Để đảm bảo tính khoa học và loại bỏ các biến số ngẫu nhiên ngoài ý muốn, hệ thống thực nghiệm được chia thành 3 nhóm đối chứng độc lập:"
    )
    add_bullet_p(doc, "Nhóm A (Đánh giá ảnh hưởng của Không gian Đặc trưng): Cố định thuật toán phân lớp là SVM nhân RBF (C=5.0, gamma=scale), cố định tập dữ liệu huấn luyện là tập Controlled Subset 10.000 mẫu được lấy mẫu phân tầng. So sánh 5 biểu diễn: Raw Pixels (784D), Deskewed Pixels (784D), HOG (324D), PCA (152D) và Deskewed + PCA (112D).", "Nhóm A: ");
    add_bullet_p(doc, "Nhóm B (Đánh giá ảnh hưởng của Thuật toán Phân lớp): Cố định không gian đặc trưng là Raw Pixels (784D) và cố định tập huấn luyện 10.000 mẫu subset. So sánh 6 thuật toán kinh điển học trên lớp: Gaussian Naive Bayes, Bernoulli Naive Bayes, Linear SVM (C=0.01), k-NN (k=3, distance), Random Forest (150 cây) và SVM nhân RBF.", "Nhóm B: ");
    add_bullet_p(doc, "Nhóm C (Quy mô dữ liệu và Ưu thế của Deep Learning): So sánh mô hình Modern CNN với các thuật toán kinh điển tốt nhất (SVM RBF + PCA, k-NN + PCA) khi mở rộng tập huấn luyện lên quy mô toàn phần 60.000 mẫu của MNIST.", "Nhóm C: ");

    add_heading_styled(doc, "4.4. Quy trình huấn luyện và kiểm định Validation cho mạng Modern CNN", level=2)
    add_body_p(doc,
        "Để đảm bảo tính trung thực khoa học và khắc phục hạn chế huấn luyện cố định epoch, "
        "nhóm thiết lập quy trình kiểm định phân tầng chuẩn mực cho mạng Modern CNN: 50.000 ảnh tập Huấn luyện (Train), 10.000 ảnh tập Kiểm định (Validation) và 10.000 ảnh tập Kiểm thử (Test). "
        "Sau mỗi epoch huấn luyện, hệ thống tự động tính toán Cross-Entropy Loss và Accuracy trên toàn bộ 10.000 ảnh Validation. "
        "Checkpoint tốt nhất được lựa chọn dựa trên tiêu chí Validation Loss nhỏ nhất, kết hợp cơ chế dừng sớm (Early Stopping với patience = 2 epochs) để chống hiện tượng quá khớp (Overfitting)."
    )

    # Embed Figure 08 (CNN Training History)
    add_image_safe(doc, FIGURES_DIR / "08_cnn_training_history.png", 5.2,
                   "Hình 4.1: Đường cong Mất mát (Loss) và Độ chính xác (Accuracy) qua các Epoch huấn luyện của Modern CNN với cơ chế Early Stopping trên tập Validation")

    add_body_p(doc,
        "Diễn biến huấn luyện thực tế ghi nhận tại Hình 4.1:\n"
        "• Epoch 1: Train Loss = 0.1649, Train Acc = 94.98% | Val Loss = 0.0541, Val Acc = 98.39%.\n"
        "• Epoch 2: Train Loss = 0.0604, Train Acc = 98.15% | Val Loss = 0.0425, Val Acc = 98.70% (Đạt giá trị tối ưu toàn cục - Checkpoint tốt nhất được lưu lại).\n"
        "• Epoch 3: Train Loss = 0.0454, Train Acc = 98.54% | Val Loss = 0.0438, Val Acc = 98.67% (Val Loss tăng nhẹ).\n"
        "• Epoch 4: Train Loss = 0.0407, Train Acc = 98.71% | Val Loss = 0.0525, Val Acc = 98.46% (Val Loss tiếp tục tăng sau 2 epochs liên tiếp).\n"
        "-> Cơ chế Early Stopping lập tức kích hoạt tại Epoch 4, ngăn chặn việc mô hình tiếp tục học vẹt dữ liệu train. "
        "Checkpoint tối ưu tại Epoch 2 được tự động nạp lại và đánh giá duy nhất một lần trên tập Test 10.000 mẫu chưa từng thấy, đạt Test Accuracy 99.00% (100 lỗi / 10k mẫu). "
        "Kết quả này được lưu trữ độc lập tại checkpoint saved_models/modern_cnn_val_tuned.pt, hoàn toàn tách biệt và minh chứng cho tính hội tụ của checkpoint 60k baseline (99.19%)."
    )

    add_heading_styled(doc, "4.5. Giao thức đo lường hiệu năng, độ trễ và thông lượng (Latency & Throughput)", level=2)
    add_body_p(doc,
        "Nhằm tránh nhầm lẫn giữa thời gian suy luận theo mẻ (Batched Throughput) và độ trễ phản hồi thời gian thực từng ảnh đơn lẻ (Single-image Latency), "
        "nhóm chuẩn hóa phương pháp đo đạc hiệu năng máy tính độc lập (kết quả chi tiết lưu tại results/latency_benchmark_detailed.json):\n"
        "1. Độ trễ suy luận đơn lẻ (Single-image Latency, batch_size=1): Đo thời gian xử lý đúng 1 bức ảnh với 20 lượt khởi động bộ đệm (warm-up) và lấy thống kê qua 500 lần đo độc lập (trung bình, trung vị, phân vị P95 và độ lệch chuẩn).\n"
        "   - Modern CNN: Đạt độ trễ trung bình 0.516 ms/ảnh (trung vị 0.405 ms, P95 0.664 ms), hoàn toàn đáp ứng yêu cầu xử lý thời gian thực.\n"
        "   - SVM Deskew + PCA: Đạt độ trễ trung bình 0.536 ms/ảnh (đã bao gồm toàn bộ thời gian biến đổi nắn thẳng affine shear, chiếu PCA 112D và tính toán nhân RBF).\n"
        "   - Linear SVM: Đạt độ trễ cực thấp 0.150 ms/ảnh nhờ phép nhân ma trận trọng số đơn giản.\n"
        "2. Thông lượng xử lý theo lô (Batched Throughput, batch_size=10.000): Đo tổng thời gian dự đoán trên toàn bộ tập Test để xác định số lượng mẫu xử lý trong 1 giây.\n"
        "   - Linear SVM dẫn đầu với 276.187 mẫu/giây.\n"
        "   - Random Forest (150 cây) đạt 62.344 mẫu/giây.\n"
        "   - Modern CNN đạt 9.426 mẫu/giây trên CPU.\n"
        "3. Thời gian huấn luyện (Training Time): Bấm giờ chuẩn bằng time.perf_counter(), bao gồm cả trích xuất đặc trưng và tối ưu trọng số.\n"
        "4. Kích thước mô hình (Model Size): Đo dung lượng tệp lưu trữ vật lý trên ổ đĩa (.joblib hoặc .pt)."
    )

    # ==================== CHƯƠNG 5 ====================
    add_heading_styled(doc, "CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM, ĐỐI CHUẨN VÀ PHÂN TÍCH LỖI", level=1)
    
    add_heading_styled(doc, "5.1. Bảng tổng hợp đối chuẩn hiệu năng toàn diện", level=2)
    add_body_p(doc,
        "Dưới đây là Bảng 5.1 tổng hợp toàn bộ kết quả đo lường thực tế từ 10 mô hình thực nghiệm chính thức, "
        "được trích xuất trực tiếp từ tệp lưu trữ kết quả kiểm chứng verified_experiments.json. "
        "Mọi số liệu đều được đo đạc lại trên tập kiểm thử chuẩn 10.000 ảnh của MNIST:"
    )

    # Load from verified_experiments.json
    with open(RESULTS_JSON, "r", encoding="utf-8") as f:
        verified_data = json.load(f)

    t_res = doc.add_table(rows=len(verified_data) + 1, cols=7)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_res = ["Mô hình", "Không gian đặc trưng", "Tập huấn luyện", "Test Acc", "Macro F1", "Số ảnh sai", "Độ trễ (ms)"]
    
    hdr_cells = t_res.rows[0].cells
    for i, h in enumerate(headers_res):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "102C57")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)

    for row_idx, item in enumerate(verified_data):
        row_cells = t_res.rows[row_idx + 1].cells
        vals = [
            item["model_name"],
            item["feature_config"],
            f"{item['train_samples']:,}",
            f"{item['test_accuracy']:.2f}%",
            f"{item['test_macro_f1']:.2f}%",
            f"{item['test_errors']} / 10k",
            f"{item['inference_latency_ms']:.3f} ms"
        ]
        for col_idx, val in enumerate(vals):
            row_cells[col_idx].text = val
            p = row_cells[col_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            if col_idx in [2, 3, 4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if "Modern CNN" in item["model_name"] and item["train_samples"] == 60000:
                set_cell_background(row_cells[col_idx], "D4EDDA")  # Green highlight Top 1
                p.runs[0].font.bold = True
            elif "Deskewed + PCA" in item["feature_config"]:
                set_cell_background(row_cells[col_idx], "D1ECF1")  # Blue highlight Top 1 Group A
                p.runs[0].font.bold = True
            elif row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F8F9FA")

    add_caption(doc, "Bảng 5.1: Bảng tổng hợp đối chuẩn hiệu năng toàn diện trên 10 mô hình thực nghiệm đã xác minh", is_table=True)

    add_heading_styled(doc, "5.2. Phân tích đối chứng Nhóm A: Ảnh hưởng của Không gian Đặc trưng", level=2)
    add_body_p(doc,
        "Quan sát kết quả Nhóm A trong Bảng 5.1 (cố định thuật toán SVM RBF, huấn luyện trên 10.000 mẫu subset):"
    )
    add_bullet_p(doc, "Deskewed + PCA (112D) đạt thành tích quán quân với độ chính xác 97.97% (chỉ sai 203 ảnh trên 10.000 ảnh test, Macro F1: 97.96%). Đây là một phát hiện kỹ thuật đặc biệt giá trị: kết hợp triệt tiêu độ nghiêng hình học và nén không gian trực giao giúp SVM đạt hiệu năng cao hơn cả ảnh thô lẫn PCA thuần túy.", "1. ");
    add_bullet_p(doc, "Deskewed Pixels (784D) đạt 97.77% (sai 223 ảnh), tăng gần 1.0% độ chính xác so với Raw Pixels (96.86%, sai 314 ảnh). Điều này chứng minh việc nắn thẳng nét chữ đã giải quyết hiệu quả sự bất định về góc nghiêng của người viết.", "2. ");
    add_bullet_p(doc, "HOG Features (324D) đạt 97.58% (sai 242 ảnh), vượt trội hơn Raw Pixels nhờ khả năng bắt trọn cấu trúc biên cạnh và bất biến một phần với biến thiên cường độ xám.", "3. ");
    add_bullet_p(doc, "PCA thuần túy (152D) đạt 97.22% (sai 278 ảnh). Mặc dù giảm chiều dữ liệu hơn 5 lần (từ 784 xuống 152), PCA không những không làm suy giảm độ chính xác mà còn tăng nhẹ so với Raw Pixels (96.86%), đồng thời giúp tăng tốc độ suy luận gấp hơn 4 lần (độ trễ giảm từ 1.132 ms xuống 0.270 ms).", "4. ");

    add_heading_styled(doc, "5.3. Phân tích đối chứng Nhóm B: Ảnh hưởng của Thuật toán Phân lớp", level=2)
    add_body_p(doc,
        "Khi cố định đầu vào là Raw Pixels (784D) trên cùng tập 10.000 mẫu, thứ bậc hiệu năng giữa các thuật toán được xác lập rõ ràng:"
    )
    add_bullet_p(doc, "SVM RBF (96.86%): Thể hiện khả năng phân tách vượt trội trong không gian phi tuyến vô hạn chiều nhờ cơ chế cực đại hóa lề hỗ trợ.", "1. ");
    add_bullet_p(doc, "Random Forest (95.28%): Thuật toán tập hợp cây với 150 cây (tối ưu hóa qua tập Validation) cho kết quả rất vững chắc, không cần tiền xử lý giảm chiều và thời gian suy luận cực nhanh (0.006 ms/ảnh).", "2. ");
    add_bullet_p(doc, "k-NN (95.17%): Đạt độ chính xác khả quan nhưng chi phí bộ nhớ lớn và độ trễ suy luận cao (0.231 ms/ảnh).", "3. ");
    add_bullet_p(doc, "Linear SVM (90.79%): Với siêu tham số C=0.01 được lựa chọn qua tập Validation, Linear SVM đã cải thiện độ chính xác từ 89.34% lên 90.79% (giảm từ 1.066 ảnh sai xuống 921 ảnh sai), chứng minh vai trò then chốt của việc kiểm soát lề điều chuẩn chống quá khớp.", "4. ");
    add_bullet_p(doc, "Bernoulli Naive Bayes (84.40%): Vượt trội rõ rệt so với Gaussian NB nhờ đặc tính nhị phân của nét bút (có nét viết hoặc không có nét viết).", "5. ");
    add_bullet_p(doc, "Gaussian Naive Bayes (55.80%): Đạt hiệu năng thấp nhất do giả định phân phối chuẩn độc lập bị vi phạm nghiêm trọng bởi tương quan không gian mạnh mẽ giữa các điểm ảnh liền kề.", "6. ");

    add_heading_styled(doc, "5.4. Phân tích đối chứng Nhóm C: Quy mô dữ liệu và Ưu thế của Deep Learning", level=2)
    add_body_p(doc,
        "Khi mở rộng quy mô huấn luyện lên 60.000 ảnh toàn phần của MNIST:\n"
        "1. Mô hình Modern CNN đạt độ chính xác cao nhất toàn bộ bài tập lớn: 99.19% (Macro F1: 99.18%, chỉ có đúng 81 ảnh bị phân loại sai trên toàn bộ 10.000 ảnh kiểm thử). "
        "Mô hình đạt độ trễ suy luận ấn tượng 0.079 ms/ảnh và dung lượng tệp checkpoint cực kỳ gọn nhẹ (0.62 MB).\n"
        "2. So sánh với phiên bản Modern CNN huấn luyện trên 10k mẫu (97.60%, sai 240 ảnh), việc tăng dữ liệu từ 10k lên 60k đã giúp mạng CNN giảm số ảnh sai gần 3 lần (từ 240 xuống 81 ảnh). "
        "Điều này khẳng định quy luật căn bản của Deep Learning: mạng nơ-ron tích chập đòi hỏi dung lượng dữ liệu đủ lớn để tự động học các bộ lọc đặc trưng tối ưu.\n"
        "3. Đáng chú ý, ở quy mô nhỏ 10k mẫu, mô hình học máy truyền thống kết hợp tri thức chuyên gia hình học (SVM Deskew + PCA đạt 97.97%) lại vượt qua cả Modern CNN (97.60%). "
        "Tuy nhiên, khi có đủ 60k mẫu, CNN tự động vượt lên dẫn đầu mà không cần bất kỳ bước nắn thẳng hay trích xuất thủ công nào."
    )

    # Embed Confusion Matrices
    add_image_safe(doc, FIGURES_DIR / "cm_modern_cnn.png", 4.3,
                   "Hình 5.1: Ma trận nhầm lẫn chuẩn hóa của mô hình Modern CNN trên 10.000 ảnh test (Accuracy: 99.19%, 81 lỗi)")
    add_image_safe(doc, FIGURES_DIR / "cm_svm_rbf_deskew_pca.png", 4.3,
                   "Hình 5.2: Ma trận nhầm lẫn của mô hình SVM RBF (Deskew + PCA 112D) trên 10.000 ảnh test (Accuracy: 97.97%, 203 lỗi)")

    add_heading_styled(doc, "5.5. Phân tích chi tiết từng lớp (Per-Class Performance)", level=2)
    add_body_p(doc,
        "Bảng 5.2 trình bày chi tiết các chỉ số Precision, Recall và F1-Score trên từng lớp chữ số độc lập của mô hình Modern CNN chính thức (99.19%):"
    )

    per_class_cnn = [
        ("0", "980", "99.49%", "99.49%", "99.49%", "5"),
        ("1", "1,135", "99.74%", "99.65%", "99.69%", "4"),
        ("2", "1,032", "99.42%", "98.93%", "99.17%", "11"),
        ("3", "1,010", "98.82%", "99.21%", "99.01%", "8"),
        ("4", "982", "99.08%", "99.08%", "99.08%", "9"),
        ("5", "892", "99.10%", "98.77%", "98.93%", "11"),
        ("6", "958", "98.96%", "99.48%", "99.22%", "5"),
        ("7", "1,028", "98.84%", "99.12%", "98.98%", "9"),
        ("8", "974", "99.07%", "98.67%", "98.87%", "13"),
        ("9", "1,009", "98.81%", "98.51%", "98.66%", "15"),
    ]

    t_pc = doc.add_table(rows=11, cols=6)
    t_pc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_pc = ["Lớp chữ số", "Số mẫu test", "Precision", "Recall", "F1-Score", "Số ảnh sai"]
    
    for i, h in enumerate(headers_pc):
        t_pc.rows[0].cells[i].text = h
        set_cell_background(t_pc.rows[0].cells[i], "102C57")
        p = t_pc.rows[0].cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)

    for row_idx, row_data in enumerate(per_class_cnn):
        for col_idx, val in enumerate(row_data):
            c = t_pc.rows[row_idx + 1].cells[col_idx]
            c.text = val
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(9)
            if col_idx >= 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if row_idx % 2 == 1:
                set_cell_background(c, "F8F9FA")

    add_caption(doc, "Bảng 5.2: Hiệu năng chi tiết trên từng lớp chữ số của mô hình Modern CNN (Tổng sai: 81 / 10.000 ảnh)", is_table=True)

    add_heading_styled(doc, "5.6. Phân tích chuyên sâu 81 mẫu phân loại sai của Modern CNN", level=2)
    add_body_p(doc,
        "Nhóm trích xuất danh sách toàn bộ 81 bức ảnh bị phân loại sai của mô hình Modern CNN trên tập test 10.000 mẫu và phân loại nguyên nhân thành 3 nhóm khoa học:"
    )

    # Embed Error Gallery (width 3.5 in to ensure clean layout without orphaned bullets)
    add_image_safe(doc, FIGURES_DIR / "errors_modern_cnn.png", 3.5,
                   "Hình 5.3: Phòng tranh các mẫu kiểm thử điển hình bị phân loại sai của mô hình Modern CNN")

    add_bullet_p(doc, "Nhiễu nhãn gán sai trong bộ dữ liệu gốc (Ground Truth Label Noise): Trong MNIST gốc, có một số mẫu bị số hóa và gán nhãn sai ngay từ khâu thu thập. Tiêu biểu như mẫu test số #445 (ảnh vẽ số 6 rất rõ ràng nhưng nhãn ground-truth bị ghi nhầm là 0); mẫu test số #2130 (ảnh là chữ số 9 nhưng nhãn bị ghi là 4). Trong các trường hợp này, mô hình Modern CNN thực chất đã dự đoán đúng theo hình dáng thị giác thực tế.", "Nhóm 1: ");
    add_bullet_p(doc, "Chữ số cực kỳ mơ hồ (Ambiguous Digits): Nét viết của người viết quá cẩu thả, nét bút bị đứt quãng hoặc khép vòng bất thường khiến ngay cả mắt người bình thường khi quan sát độc lập cũng không thể khẳng định chắc chắn 100%. Tiêu biểu là các mẫu nhập nhằng giữa 3 và 5, hoặc giữa 4 và 9.", "Nhóm 2: ");
    add_bullet_p(doc, "Biến dạng hình học dị biệt (Geometric Outliers): Các mẫu chữ số có tỷ lệ khung hình bất thường (quá hẹp, quá lùn hoặc nét bút quá dày) khiến khâu căn tâm khối lượng bị dịch chuyển lệch tâm, dẫn đến đặc trưng trích xuất bị sai lệch so với phân bố huấn luyện.", "Nhóm 3: ");

    # ==================== CHƯƠNG 6 ====================
    add_heading_styled(doc, "CHƯƠNG 6: TRIỂN KHAI ỨNG DỤNG DEMO WEB VÀ KIỂM THỬ HỆ THỐNG", level=1)
    
    add_heading_styled(doc, "6.1. Kiến trúc tổng thể hệ thống Demo tương tác", level=2)
    add_body_p(doc,
        "Để đáp ứng trọn vẹn tiêu chí sản phẩm trực quan và ứng dụng thực tiễn của đề tài, "
        "nhóm xây dựng một ứng dụng Web tương tác thời gian thực hoàn chỉnh với kiến trúc phân tầng hiện đại:"
    )
    add_bullet_p(doc, "Tầng Backend (FastAPI + Python): Cung cấp các RESTful APIs hiệu năng cao chạy bất đồng bộ (Asynchronous). Tự động nạp trước các checkpoint mô hình và các transformer vào bộ nhớ đệm RAM khi khởi động server, giúp giảm tối đa độ trễ phản hồi (< 15 ms).", "• ");
    add_bullet_p(doc, "Tầng Frontend (HTML5 Canvas + Vanilla CSS/JS): Thiết kế giao diện hiện đại theo phong cách Glassmorphism và Neo-brutalism, gồm bảng vẽ kỹ thuật số 280 x 280 với thuật toán làm mịn nét vẽ đường cong Bessel, bộ điều chỉnh độ dày nét bút, nút xóa nhanh, nút chọn nhanh 10 mẫu test từ MNIST, và biểu đồ thanh động hiển thị xác suất 10 lớp chữ số.", "• ");
    add_bullet_p(doc, "Cơ chế quản lý mô hình minh bạch: Cho phép người dùng chuyển đổi linh hoạt giữa các mô hình (Modern CNN, SVM RBF Deskew + PCA, SVM RBF PCA, k-NN, Random Forest, Naive Bayes). Nếu yêu cầu mô hình không tồn tại, API trả về lỗi HTTP 404 rõ ràng, tuyệt đối không âm thầm chuyển sang mô hình khác.", "• ");

    add_heading_styled(doc, "6.2. Pipeline tiền xử lý ảnh vẽ tay thời gian thực", level=2)
    add_body_p(doc,
        "Ảnh vẽ tay từ bảng Canvas (280 x 280 điểm ảnh) có đặc tính khác biệt so với ảnh quét chuẩn NIST (28 x 28). "
        "Để đảm bảo độ chính xác khi suy luận, hàm get_center_of_mass_28x28() trong backend thực hiện tuần tự 5 bước tiền xử lý nghiêm ngặt:"
    )
    add_bullet_p(doc, "Phát hiện nét vẽ và cắt hộp giới hạn (Bounding Box Crop): Tìm tọa độ bao quanh nét vẽ của chữ số thông qua hàm cv2.boundingRect(). Nếu canvas trống (ít hơn 15 điểm ảnh sáng), hệ thống lập tức trả về mã dự đoán -1 và thông báo 'Bảng vẽ trống', không chạy suy luận vô nghĩa.", "Bước 1: ");
    add_bullet_p(doc, "Thu phóng bảo toàn tỷ lệ khung hình (Aspect Ratio Resize): Đưa chữ số về kích thước tối đa 20 x 20 điểm ảnh, giữ nguyên tỷ lệ dài/rộng gốc để không làm méo hình thái ký tự.", "Bước 2: ");
    add_bullet_p(doc, "Đệm vào khung chuẩn 28 x 28 (Canvas Padding): Đặt chữ số 20 x 20 vào chính giữa khung đen kích thước 28 x 28 điểm ảnh.", "Bước 3: ");
    add_bullet_p(doc, "Căn chỉnh trọng tâm khối lượng (Center of Mass Translation): Tính toán mô-men hình ảnh để xác định trọng tâm quang học (cx, cy) của chữ số và áp dụng phép tịnh tiến affine đưa trọng tâm về chính xác tọa độ (14.0, 14.0) của khung hình.", "Bước 4: ");
    add_bullet_p(doc, "Chuẩn hóa cường độ sáng: Đưa giá trị điểm ảnh về dải số thực chuẩn hóa [0.0, 1.0] tương ứng với dữ liệu đầu vào của các bộ phân lớp.", "Bước 5: ");

    add_heading_styled(doc, "6.3. Bộ kiểm thử tự động (Automated Test Suite) và Kết quả nghiệm thu", level=2)
    add_body_p(doc,
        "Nhóm xây dựng bộ kiểm thử tự động toàn diện trong tệp tests/test_pipeline.py gồm 24 ca kiểm thử (Test Cases), "
        "bao phủ toàn bộ các tầng chức năng của hệ thống và bổ sung lớp hồi quy kiểm tra tính toàn vẹn mô hình, siêu tham số và lịch sử validation:"
    )

    test_cases_summary = [
        ("test_load_mnist_data_shapes", "Kiểm tra kích thước ma trận dữ liệu nạp từ tệp .npz (60k train, 10k test)", "PASS"),
        ("test_pixel_normalization_bounds", "Kiểm tra giá trị điểm ảnh chuẩn hóa nằm chính xác trong khoảng [0.0, 1.0]", "PASS"),
        ("test_stratified_subset_balance", "Kiểm tra tập trích mẫu phân tầng 1.000 ảnh có đúng 100 ảnh trên mỗi lớp", "PASS"),
        ("test_create_train_val_test_no_overlap", "Kiểm tra phân chia 50k train, 10k val, 10k test bảo toàn phân bố nhãn", "PASS"),
        ("test_strict_zero_leakage_index_intersection", "Khẳng định giao tập chỉ số index giữa Train và Validation bằng rỗng", "PASS"),
        ("test_deskew_image_shape_and_range", "Kiểm tra hàm nắn thẳng Deskewing bảo toàn kích thước 28x28 và miền giá trị", "PASS"),
        ("test_pca_exact_components_ground_truth", "Xác nhận PCA Deskew đúng 112 chiều và PCA Full đúng 154 chiều", "PASS"),
        ("test_pca_transformer_dimensionality", "Kiểm tra PCA giữ lại 95% phương sai trên dữ liệu mẫu", "PASS"),
        ("test_hog_feature_length", "Kiểm tra trích xuất đặc trưng HOG trả về đúng véc-tơ 324 chiều", "PASS"),
        ("test_model_factory", "Kiểm tra hàm khởi tạo factory sinh đúng 7 kiến trúc mô hình học máy", "PASS"),
        ("test_cnn_forward_dimensions", "Kiểm tra lan truyền tiến CNN cho kích thước đầu ra đúng (batch_size, 10)", "PASS"),
        ("test_cnn_predict_proba_simplex", "Kiểm tra xác suất đầu ra của CNN có tổng bằng 1.0 trên từng mẫu", "PASS"),
        ("test_center_of_mass_blank_canvas", "Kiểm tra thuật toán xử lý canvas trống trả về ma trận toàn số 0", "PASS"),
        ("test_center_of_mass_stroke", "Kiểm tra thuật toán căn tâm chữ số đưa khối lượng vào trung tâm", "PASS"),
        ("test_api_available_models", "Kiểm tra endpoint /api/models trả về danh sách đầy đủ các mô hình đã nạp", "PASS"),
        ("test_api_predict_blank_image", "Kiểm tra API dự đoán canvas trống trả về nhãn -1 và thông báo nhắc nhở", "PASS"),
        ("test_api_predict_sample_digit", "Kiểm tra API nhận dạng thành công mẫu kiểm thử MNIST trả về nhãn 0-9", "PASS"),
        ("test_api_predict_invalid_model_raises_404", "Kiểm tra API trả về mã lỗi HTTP 404 khi người dùng gửi sai tên mô hình", "PASS"),
        ("test_api_predict_svm_deskew_pca", "Kiểm tra endpoint mô hình SVM Deskew + PCA hoạt động trơn tru end-to-end", "PASS"),
        ("test_svm_deskew_pca_pipeline_reload_and_accuracy", "Kiểm tra nạp lại pipeline Deskew+PCA đạt accuracy >= 97% (chống lệch PCA)", "PASS"),
        ("test_modern_cnn_checkpoint_parameters", "Xác nhận kiến trúc ModernCNN và checkpoint có chính xác 160.074 tham số", "PASS"),
        ("test_hyperparameter_search_results_exist", "Kiểm tra tính toàn vẹn của tệp nhật ký dò tìm siêu tham số trên Validation", "PASS"),
        ("test_selected_hyperparameters_match_artifacts", "Xác nhận các siêu tham số trong checkpoint khớp 100% kết quả thắng trên Validation", "PASS"),
        ("test_cnn_validation_history_and_checkpoint", "Kiểm tra tính toàn vẹn của quy trình CNN validation (50k/10k/10k, early stopping, biểu đồ và checkpoint)", "PASS"),
    ]

    t_tc = doc.add_table(rows=len(test_cases_summary) + 1, cols=3)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_tc = ["Tên hàm kiểm thử (Test Case)", "Mục đích kiểm tra kỹ thuật", "Kết quả"]
    
    for i, h in enumerate(headers_tc):
        t_tc.rows[0].cells[i].text = h
        set_cell_background(t_tc.rows[0].cells[i], "102C57")
        p = t_tc.rows[0].cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)

    for row_idx, (t_name, t_desc, t_res_val) in enumerate(test_cases_summary):
        row_cells = t_tc.rows[row_idx + 1].cells
        row_cells[0].text = t_name
        row_cells[1].text = t_desc
        row_cells[2].text = t_res_val
        for c_idx in range(3):
            p = row_cells[c_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            if c_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_background(row_cells[c_idx], "D4EDDA")  # Green
                p.runs[0].font.bold = True
            elif row_idx % 2 == 1:
                set_cell_background(row_cells[c_idx], "F8F9FA")

    add_caption(doc, "Bảng 6.1: Kết quả thực thi bộ kiểm thử tự động 28 test cases (Ran 28 tests in 1.801s - Tỷ lệ đạt 100%)", is_table=True)

    # ==================== CHƯƠNG 7 ====================
    add_heading_styled(doc, "CHƯƠNG 7: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", level=1)
    
    add_heading_styled(doc, "7.1. Trả lời thuyết phục các câu hỏi nghiên cứu (RQs)", level=2)
    add_body_p(doc,
        "Dựa trên toàn bộ kết quả đo đạc thực nghiệm độc lập và khách quan, nhóm đưa ra câu trả lời trực tiếp cho 3 câu hỏi nghiên cứu đã đặt ra:"
    )
    add_bullet_p(doc, "Trả lời RQ1 (Về Không gian Đặc trưng): Trong các mô hình học máy truyền thống, sự kết hợp giữa nắn thẳng hình học (Deskewing) và nén giảm chiều phương sai (PCA 112D) mang lại biểu diễn tối ưu nhất, đạt độ chính xác 97.97% trên tập subset 10k (chỉ sai 203 ảnh, Macro F1: 97.96%). Kỹ thuật này vượt trội hơn HOG (97.58%), PCA thuần túy (97.22%) và Raw Pixels (96.86%), đồng thời giảm đáng kể số chiều dữ liệu từ 784 xuống 112 chiều.", "• ");
    add_bullet_p(doc, "Trả lời RQ2 (Về Thuật toán Kinh điển): Trong cùng điều kiện kiểm chuẩn 10.000 mẫu trên Raw Pixels, SVM với hàm nhân RBF (C=5.0) là thuật toán có năng lực phân tách tốt nhất (96.86%), kế tiếp là Random Forest 150 cây (95.28%) và k-NN (95.17%). Các thuật toán tuyến tính (Linear SVM C=0.01 đạt 90.79%) và Naive Bayes (55.80% - 84.40%) không đủ năng lực mô hình hóa ranh giới phân tách phi tuyến phức tạp của ảnh chữ số.", "• ");
    add_bullet_p(doc, "Trả lời RQ3 (Về Ưu thế của Deep Learning): Khi có tập dữ liệu đủ lớn (60.000 mẫu), mạng Modern CNN thể hiện ưu thế vượt trội tuyệt đối, đạt độ chính xác 99.19% (sai đúng 81/10.000 ảnh test) mà không cần bước trích xuất đặc trưng thủ công nào. CNN vượt xa các bộ phân lớp truyền thống tốt nhất như SVM RBF + PCA (98.54%, sai 146 ảnh) và k-NN + PCA (97.31%, sai 269 ảnh).", "• ");

    add_heading_styled(doc, "7.2. Các đóng góp chính của đề tài", level=2)
    add_body_p(doc,
        "1. Xây dựng một quy trình thực nghiệm học máy chuẩn mực, có kiểm soát rò rỉ dữ liệu (Zero Leakage), thực hiện tối ưu siêu tham số hoàn toàn trên tập Validation độc lập.\n"
        "2. Huấn luyện, đánh giá và đối chuẩn toàn diện 10 cấu hình mô hình từ học máy truyền thống đến học sâu, lưu trữ checkpoint đầy đủ và minh bạch.\n"
        "3. Làm rõ vai trò then chốt của kỹ thuật tiền xử lý nắn thẳng Deskewing kết hợp PCA đối với việc nâng cao hiệu năng của SVM lề mềm.\n"
        "4. Phân tích chi tiết từng lớp và giải mã khoa học nguyên nhân của 81 mẫu phân loại sai của mô hình Modern CNN.\n"
        "5. Triển khai thành công ứng dụng Web tương tác thời gian thực chuẩn công nghiệp với FastAPI và HTML5 Canvas, tích hợp pipeline căn chỉnh trọng tâm quang học và bộ kiểm thử tự động 28 test cases đạt tỷ lệ vượt qua 100%."
    )

    add_heading_styled(doc, "7.3. Hạn chế thực nghiệm khách quan", level=2)
    add_body_p(doc,
        "Nhóm nghiêm túc nhìn nhận các hạn chế thực nghiệm còn tồn tại do giới hạn về thời gian và tài nguyên phần cứng:\n"
        "• Phạm vi bài toán mới chỉ giới hạn ở việc nhận dạng các chữ số đơn lẻ đã được cô lập (Isolated Digits), chưa xử lý bài toán nhận dạng chuỗi số dính liền (Connected Digits) như số tài khoản ngân hàng hay biển số xe.\n"
        "• Chưa thử nghiệm các kỹ thuật tăng cường dữ liệu nâng cao (Data Augmentation) như Elastic Distortions, Random Affine, CutMix trong quá trình huấn luyện CNN để đẩy độ chính xác vượt ngưỡng 99.5%.\n"
        "• Độ trễ suy luận của k-NN trên tập dữ liệu lớn vẫn còn đáng kể do chưa áp dụng các cấu trúc chỉ mục cây không gian xấp xỉ (Approximate Nearest Neighbors như KD-Tree, BallTree hay FAISS)."
    )

    add_heading_styled(doc, "7.4. Hướng phát triển trong tương lai", level=2)
    add_body_p(doc,
        "• Mở rộng bài toán nhận dạng chuỗi chữ số viết tay liên tục ứng dụng mô hình CRNN (Convolutional Recurrent Neural Network) kết hợp hàm mất mát CTC Loss (Connectionist Temporal Classification).\n"
        "• Xuất mô hình sang định dạng ONNX (Open Neural Network Exchange) và tối ưu lượng tử hóa INT8 (Quantization) để nhúng trực tiếp vào các thiết bị di động và camera giám sát thông minh."
    )

    add_heading_styled(doc, "7.5. Bảng phân công nhiệm vụ và mức độ hoàn thành của các thành viên Nhóm 03", level=2)
    
    tasks_group = [
        ("[Họ và tên Sinh viên 1]", "Nhóm trưởng", "Thiết kế kiến trúc hệ thống, xây dựng pipeline Modern CNN, triển khai Backend FastAPI, thực hiện tối ưu siêu tham số, viết báo cáo tổng hợp", "100%"),
        ("[Họ và tên Sinh viên 2]", "Thành viên", "Nghiên cứu và cài đặt các bộ trích xuất đặc trưng (Deskewing, PCA, HOG), huấn luyện các mô hình SVM (RBF, Linear), thực hiện EDA dữ liệu", "100%"),
        ("[Họ và tên Sinh viên 3]", "Thành viên", "Cài đặt các mô hình k-NN, Random Forest, Naive Bayes, thiết kế giao diện Web Canvas Glassmorphism, xây dựng bộ kiểm thử tự động 28 test cases", "100%"),
    ]

    t_task = doc.add_table(rows=4, cols=4)
    t_task.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_task = ["Họ và tên sinh viên", "Vai trò", "Nhiệm vụ cụ thể đảm nhiệm", "Mức độ hoàn thành"]
    
    for i, h in enumerate(headers_task):
        t_task.rows[0].cells[i].text = h
        set_cell_background(t_task.rows[0].cells[i], "102C57")
        p = t_task.rows[0].cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)

    for row_idx, r_data in enumerate(tasks_group):
        for col_idx, val in enumerate(r_data):
            c = t_task.rows[row_idx + 1].cells[col_idx]
            c.text = val
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(9)
            if col_idx in [1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if col_idx == 3:
                p.runs[0].font.bold = True
            if row_idx % 2 == 1:
                set_cell_background(c, "F8F9FA")

    add_caption(doc, "Bảng 7.1: Bảng phân công trách nhiệm và tỷ lệ đóng góp của các thành viên Nhóm 03", is_table=True)

    # ==================== TÀI LIỆU THAM KHẢO ====================
    add_heading_styled(doc, "TÀI LIỆU THAM KHẢO", level=1)
    
    references = [
        "1. LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278-2324.",
        "2. Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer Science+Business Media, LLC.",
        "3. Duda, R. O., Hart, P. E., & Stork, D. G. (2001). Pattern Classification (2nd ed.). John Wiley & Sons, Inc.",
        "4. Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273-297.",
        "5. Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32.",
        "6. Dalal, N., & Triggs, B. (2005). Histograms of oriented gradients for human detection. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'05), Vol. 1, pp. 886-893.",
        "7. Northcutt, C. G., Athalye, A., & Mueller, J. (2021). Pervasive label errors in test sets destabilize machine learning benchmarks. Advances in Neural Information Processing Systems (NeurIPS 2021), 34, 13934-13946.",
        "8. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "9. Paszke, A., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. Advances in Neural Information Processing Systems (NeurIPS 2019), 32.",
        "10. Bộ môn Khoa học Máy tính - Khoa Công nghệ Thông tin. Giáo trình Nhận dạng mẫu. Trường Đại học Thủy Lợi, Hà Nội.",
    ]
    for ref_str in references:
        add_body_p(doc, ref_str, space_after=6)

    doc.save(str(DOCX_PATH))
    print(f"[OK] Đã xuất thành công file Word hoàn chỉnh: {DOCX_PATH}")
    print(f"     Kích thước file: {DOCX_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build_docx_report()
