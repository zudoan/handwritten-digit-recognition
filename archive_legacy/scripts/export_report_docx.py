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
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
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
    if bold_prefix and bold_prefix.startswith("Câu hỏi nghiên cứu") and text.startswith("RQ"):
        text = text.split(": ", 1)[1]
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
    if bold_prefix == "• ":
        bold_prefix = None
    if bold_prefix:
        label = bold_prefix.strip().rstrip(":")
        if text.startswith(label + " "):
            text = text[len(label) + 1:]
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



def export_markdown_report(doc):
    from docx.text.paragraph import Paragraph
    from docx.table import Table
    import hashlib
    images = {}
    for path in REPORTS_DIR.rglob("*.png"):
        images[hashlib.sha256(path.read_bytes()).hexdigest()] = path.relative_to(REPORTS_DIR).as_posix()
    lines = []
    for element in doc.element.body:
        if element.tag == qn("w:p"):
            paragraph = Paragraph(element, doc)
            text = paragraph.text.strip()
            style = paragraph.style.name
            if text:
                if style.startswith("Heading"):
                    level = int(style.rsplit(" ", 1)[-1])
                    lines.extend(["#" * level + " " + text, ""])
                else:
                    lines.extend([text, ""])
            for blip in element.xpath(".//a:blip"):
                rel_id = blip.get(qn("r:embed"))
                if rel_id:
                    part = doc.part.related_parts[rel_id]
                    path = images.get(hashlib.sha256(part.blob).hexdigest())
                    if path:
                        lines.extend([f"![Hình minh họa]({path})", ""])
        elif element.tag == qn("w:tbl"):
            table = Table(element, doc)
            for i, row in enumerate(table.rows):
                values = [cell.text.replace("\n", " ").replace("|", "/") for cell in row.cells]
                lines.append("| " + " | ".join(values) + " |")
                if i == 0:
                    lines.append("| " + " | ".join(["---"] * len(values)) + " |")
            lines.append("")
    (REPORTS_DIR / "BAO_CAO_KHOA_HOC_NHAN_DANG_CHU_SO_MNIST.md").write_text("\n".join(lines), encoding="utf-8")

def build_docx_report():
    print("-> Đang khởi tạo và xây dựng Báo cáo Kỹ thuật Word (20-30 trang)...")
    doc = Document()
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(12)
    for style_name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        doc.styles[style_name].font.color.rgb = RGBColor(0, 0, 0)
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    number = OxmlElement("w:fldSimple"); number.set(qn("w:instr"), "PAGE")
    footer._p.append(number)


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
    r_main.font.color.rgb = RGBColor(0, 0, 0)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.5)
    p_info.paragraph_format.line_spacing = 1.3
    
    runs_info = [
        ("Giảng viên hướng dẫn: ", True), ("........................................\n", False),
        ("Lớp học phần: ", True), ("Nhận dạng mẫu - S26-65TTNT\n", False),
        ("Nhóm sinh viên thực hiện: ", True), ("Nhóm 03\n", False),
        ("Thành viên nhóm:\n", True),
        ("  1. Đoàn Anh Vũ - MSSV: 2351267280\n", False),
        ("  2. Nguyễn Hồng Nguyên - MSSV: 2351267273\n", False),
        ("\n\n\n\n", False),
    ]
    for txt, is_b in runs_info:
        r = p_info.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12.5)
        r.font.bold = is_b

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("Hà Nội, năm 2026")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    r_date.font.italic = True

    # ==================== LỜI CẢM ƠN & TÓM TẮT ====================
    add_heading_styled(doc, "GIỚI THIỆU BÁO CÁO VÀ LỜI CẢM ƠN", level=1)
    add_body_p(doc,
        'Báo cáo trình bày mã nguồn, cấu hình mô hình và kết quả nhận dạng chữ số viết tay trên MNIST. Các bảng đánh giá sử dụng checkpoint kèm theo repo và tập test chính thức gồm 10.000 ảnh. Nguồn dữ liệu, thuật toán và thư viện được ghi trong phần tài liệu tham khảo.'
    )
    add_body_p(doc,
        'Nhóm 03 cảm ơn giảng viên học phần Nhận dạng mẫu đã hướng dẫn các kiến thức về phân lớp, biểu diễn đặc trưng và đánh giá mô hình, làm cơ sở thực hiện đề tài.'
    )

    add_heading_styled(doc, "TÓM TẮT BÁO CÁO", level=2)
    add_body_p(doc,
        'Đề tài nghiên cứu nhận dạng chữ số viết tay đơn lẻ từ 0 đến 9 trên MNIST. Nội dung thực nghiệm gồm so sánh đặc trưng với SVM RBF, so sánh các thuật toán trên tập con 10.000 mẫu và khảo sát CNN ở các quy mô dữ liệu khác nhau. Kết quả được tích hợp vào ứng dụng web có bảng vẽ, tải ảnh và chọn mẫu test.'
    )
    add_body_p(doc,
        'Trong nhóm SVM cùng huấn luyện trên 10.000 mẫu, Deskew + PCA 112 chiều đạt Accuracy 97.97%, cao hơn HOG 97.58%, PCA 97.22% và ảnh thô 96.86%. Trong nhóm thuật toán dùng điểm ảnh, SVM RBF đạt 96.86%, Random Forest 150 cây đạt 95.28%, k-NN đạt 95.17% và Linear SVM C=0.01 đạt 90.79%. CNN huấn luyện trên 60.000 mẫu đạt 99.19%, tương ứng 81 ảnh sai; CNN chọn checkpoint bằng validation đạt 99.00%, tương ứng 100 ảnh sai. Hai kết quả CNN thuộc hai quy trình huấn luyện riêng.'
    )

    add_heading_styled(doc, "MỤC LỤC BÁO CÁO", level=2)
    page_map_path = REPORTS_DIR / "tables" / "report_page_map.json"
    page_map = json.loads(page_map_path.read_text()) if page_map_path.exists() else {}
    contents = ["CHƯƠNG 1  GIỚI THIỆU BÀI TOÁN", "CHƯƠNG 2  CƠ SỞ LÝ THUYẾT",
                "CHƯƠNG 3  DỮ LIỆU VÀ TIỀN XỬ LÝ", "CHƯƠNG 4  THIẾT KẾ THỰC NGHIỆM",
                "CHƯƠNG 5  KẾT QUẢ VÀ PHÂN TÍCH", "CHƯƠNG 6  WEB DEMO VÀ KIỂM THỬ",
                "CHƯƠNG 7  KẾT LUẬN", "TÀI LIỆU THAM KHẢO"]
    for index, title in enumerate(contents, 1):
        p_toc = add_body_p(doc, title + "\t" + str(page_map.get(str(index), "")))
        p_toc.paragraph_format.tab_stops.add_tab_stop(Inches(6.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

    # ==================== CHƯƠNG 1 ====================
    add_heading_styled(doc, "CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU", level=1)
    
    add_heading_styled(doc, "1.1. Bối cảnh thực tế và ý nghĩa bài toán", level=2)
    add_body_p(doc,
        'Nhận dạng chữ số viết tay là một bài toán của nhận dạng mẫu và thị giác máy tính. Kết quả nhận dạng có thể hỗ trợ nhập liệu từ biểu mẫu, chứng từ và mã bưu chính. Đề tài khảo sát bước phân lớp một chữ số đã được tách khỏi ảnh; các ứng dụng dưới đây là bối cảnh sử dụng, chưa thuộc phạm vi triển khai đầy đủ của hệ thống.'
    )
    add_bullet_p(doc, "Xử lý bưu chính tự động: Tự động nhận diện mã bưu chính (Zip Codes) trên phong bì thư nhằm phân luồng vận chuyển tự động, giảm thiểu nhân công và sai sót thủ công.", "• ");
    add_bullet_p(doc, "Ngành tài chính - ngân hàng: Tự động đọc và đối soát số tiền viết tay trên séc ngân hàng, phiếu nộp tiền, hóa đơn thanh toán và các chứng từ kế toán.", "• ");
    add_bullet_p(doc, "Quản lý hành chính công và giáo dục: Tự động chấm thi trắc nghiệm, nhận dạng mã đề, điểm số viết tay của giám khảo và số hóa hồ sơ bệnh án, chứng minh nhân dân.", "• ");

    add_heading_styled(doc, "1.2. Định nghĩa toán học bài toán nhận dạng chữ số", level=2)
    add_body_p(doc,
        'Bài toán được mô hình hóa dưới dạng phân lớp đa lớp có giám sát. Mỗi ảnh xám 28 x 28 chứa một chữ số và được gán đúng một nhãn thuộc tập {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. Khi dùng mô hình cổ điển, ảnh được trải phẳng thành véc-tơ 784 chiều; CNN nhận ma trận ảnh có một kênh.'
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
        'Các cách viết khác nhau tạo ra biến thiên về hình dạng và vị trí của chữ số. Các khó khăn chính trong phạm vi đề tài gồm:'
    )
    add_bullet_p(doc, 'Đa dạng trong cùng lớp: mỗi chữ số có thể thay đổi về độ nghiêng, độ dày nét, kích thước, nét móc và tỷ lệ dài/rộng theo người viết.', "• ");
    add_bullet_p(doc, 'Tương đồng giữa các lớp: các cặp 4 và 9, 3 và 5, 7 và 1, 8 và 0 có thể có nét gần nhau. Một nét nối hoặc nét móc ngắn thường là thông tin phân biệt giữa hai lớp.', "• ");
    add_bullet_p(doc, 'Chất lượng ảnh: nét mờ, đứt đoạn hoặc khép vòng không rõ có thể làm mất thông tin phân biệt. Báo cáo đánh giá theo nhãn MNIST được cung cấp và không tự sửa nhãn.', "• ");
    add_bullet_p(doc, 'Số chiều biểu diễn: véc-tơ pixel có 784 chiều, trong đó nhiều vị trí ở biên có phương sai thấp. PCA được khảo sát để giảm số chiều; HOG được dùng để biểu diễn hướng nét thay cho toàn bộ cường độ pixel.', "• ");

    add_heading_styled(doc, "1.4. Mục tiêu nghiên cứu và các câu hỏi nghiên cứu (RQs)", level=2)
    add_body_p(doc,
        'Đề tài xây dựng và so sánh các bộ phân lớp chữ số viết tay, sau đó tích hợp mô hình vào ứng dụng web. Ba câu hỏi nghiên cứu được xác định như sau:'
    )
    add_body_p(doc,
        'RQ1: Trong các cấu hình SVM RBF cùng train 10.000 mẫu, biểu diễn ảnh thô, Deskew, HOG, PCA hoặc Deskew + PCA cho kết quả nào cao nhất?',
        bold_prefix="Câu hỏi nghiên cứu 1 (RQ1): "
    )
    add_body_p(doc,
        'RQ2: Khi dùng cùng tập train 10.000 mẫu, các thuật toán phân lớp khác nhau về Accuracy, Macro F1, số lỗi và yêu cầu lưu trữ như thế nào?',
        bold_prefix="Câu hỏi nghiên cứu 2 (RQ2): "
    )
    add_body_p(doc,
        'RQ3: Kết quả CNN thay đổi như thế nào giữa quy mô 10.000 và 60.000 mẫu huấn luyện, và so với SVM RBF + PCA, k-NN + PCA ở quy mô 60.000 mẫu?',
        bold_prefix="Câu hỏi nghiên cứu 3 (RQ3): "
    )

    # ==================== CHƯƠNG 2 ====================
    add_heading_styled(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC", level=1)
    
    add_heading_styled(doc, "2.1. Không gian biểu diễn và các phương pháp trích xuất đặc trưng", level=2)
    add_body_p(doc,
        'Biểu diễn đặc trưng ảnh hưởng đến cách bộ phân lớp so sánh và tách các chữ số. Đề tài khảo sát pixel thô, Deskew, PCA và HOG, đồng thời kết hợp Deskew với PCA. Mỗi bộ biến đổi được áp dụng nhất quán cho train và test.'
    )

    add_heading_styled(doc, "2.1.1. Biểu diễn điểm ảnh thô (Raw Pixels)", level=3)
    add_body_p(doc,
        'Ảnh 28 x 28 được trải phẳng thành véc-tơ 784 chiều. Giá trị x_i là cường độ pixel tại tọa độ (u, v), với i = u * 28 + v. Biểu diễn này giữ các điểm ảnh gốc và không cần bộ trích xuất riêng; khoảng cách giữa hai véc-tơ vẫn nhạy với dịch chuyển và độ nghiêng nét chữ.'
    )

    add_heading_styled(doc, "2.1.2. Nắn thẳng chữ số dựa trên mô-men hình ảnh (Deskewing)", level=3)
    add_body_p(doc,
        'Deskew ước lượng độ nghiêng từ mô-men trung tâm của ảnh và dùng phép biến đổi shear để hiệu chỉnh nét chữ. Các mô-men của ảnh xám I(x, y) được tính như sau:'
    )
    add_body_p(doc,
        "m_{pq} = sum_x sum_y x^p y^q I(x, y);   cx = m_{10}/m_{00},  cy = m_{01}/m_{00}\n"
        "mu_{11} = sum_x sum_y (x - cx)(y - cy) I(x, y);   mu_{02} = sum_x sum_y (y - cy)^2 I(x, y)\n"
        "skew = mu_{11} / mu_{02}",
        bold_prefix="Công thức tính độ nghiêng: "
    )
    add_body_p(doc,
        'Trong mã nguồn, phép nắn thẳng sử dụng skew = mu11 / mu02 và ánh xạ ngược x_nguon = x_dich + skew * (y - 14), y_nguon = y_dich. Nội suy tuyến tính được thực hiện bằng cv2.warpAffine với WARP_INVERSE_MAP. Phép biến đổi giảm độ nghiêng nét chữ; ảnh có mu02 quá nhỏ được giữ nguyên.'
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
        'Các véc-tơ riêng v_i tạo thành cơ sở trực chuẩn. Số thành phần d được chọn sao cho tổng trị riêng của d thành phần đầu đạt ít nhất 95% tổng trị riêng. Các bộ PCA đã lưu có 154 chiều cho ảnh thô 60.000 mẫu, 152 chiều cho ảnh thô 10.000 mẫu và 112 chiều cho tập con đã deskew. Tỷ lệ này phản ánh phương sai giữ lại, không đồng nghĩa giữ nguyên 95% thông tin phân lớp.'
    )

    add_heading_styled(doc, "2.1.4. Bộ mô tả đặc trưng HOG (Histogram of Oriented Gradients)", level=3)
    add_body_p(doc,
        'HOG mô tả hướng gradient trong các vùng cục bộ. Với ảnh I, g_x = I(x+1,y) - I(x-1,y), g_y = I(x,y+1) - I(x,y-1), độ lớn m = sqrt(g_x² + g_y²) và hướng theta = atan2(g_y,g_x). Cấu hình dùng ô 7 x 7, khối 2 x 2 ô, 9 khoảng hướng và chuẩn hóa L2-Hys. Ảnh 28 x 28 tạo 9 vị trí khối, mỗi khối có 36 phần tử, nên véc-tơ gồm 324 chiều.'
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
        'Hai biến thể được sử dụng gồm Gaussian NB và Bernoulli NB. Gaussian NB mô hình hóa mỗi pixel theo phân phối chuẩn có tham số riêng cho từng lớp. Bernoulli NB nhị phân hóa pixel với ngưỡng 0.2 và mô hình hóa xác suất xuất hiện nét. Các pixel lân cận có tương quan, vì vậy giả định độc lập có điều kiện chỉ là một xấp xỉ.'
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
        'k-NN tạo ranh giới quyết định theo các mẫu tham chiếu và không cần giả định phân phối dữ liệu. Với tìm kiếm trực tiếp, chi phí tính khoảng cách tỷ lệ theo N * D. Mô hình cần lưu tập tham chiếu; dung lượng checkpoint được thống kê cùng các kết quả thực nghiệm.'
    )

    add_heading_styled(doc, "2.2.3. Máy véc-tơ hỗ trợ (Support Vector Machine - SVM)", level=3)
    add_body_p(doc,
        'SVM lề mềm tìm siêu phẳng w^T x + b = 0 có lề lớn và kiểm soát các điểm vi phạm lề thông qua biến xi_i và hệ số C. Với kernel RBF, quyết định được tính trong không gian đặc trưng phi tuyến:'
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
        'SVC với kernel RBF dùng chiến lược one-vs-one cho 10 lớp, tương ứng 45 bài toán hai lớp. LinearSVC dùng one-vs-rest. Hai cấu hình SVM khác nhau cả dạng ranh giới và cách xây dựng bộ phân lớp đa lớp.'
    )

    add_heading_styled(doc, "2.2.4. Rừng ngẫu nhiên (Random Forest - RF)", level=3)
    add_body_p(doc,
        'Cấu hình được chọn sử dụng B = 150 cây quyết định. Mỗi cây học trên một mẫu bootstrap và xét một tập đặc trưng ngẫu nhiên tại mỗi nút. Các cây cùng học từ bộ dữ liệu gốc nên không được xem là độc lập hoàn toàn.'
    )
    add_body_p(doc,
        "I_Gini(p) = 1 - sum_{k=0}^9 p_k^2",
        bold_prefix="Độ đo Gini Impurity: "
    )
    add_body_p(doc,
        'Trong RandomForestClassifier, xác suất của từng lớp được lấy trung bình từ các cây và nhãn dự đoán là lớp có xác suất trung bình lớn nhất. Cách kết hợp này giúp giảm phương sai so với một cây riêng lẻ.'
    )

    add_heading_styled(doc, "2.3. Mạng nơ-ron tích chập hiện đại (Modern CNN Architecture)", level=2)
    add_body_p(doc,
        'CNN học bộ lọc tích chập trực tiếp từ ảnh hai chiều. Chia sẻ trọng số và vùng tiếp nhận cục bộ giúp biểu diễn các nét chữ ở nhiều vị trí. Kiến trúc được sử dụng giữ đầu vào một kênh và tạo đầu ra gồm 10 điểm lớp.'
    )
    add_body_p(doc,
        "CNN gồm ba khối trích xuất đặc trưng và một bộ phân lớp:\n"
        "• Khối 1: Conv2D 1→32, kernel 3 x 3, padding 1; BatchNorm, ReLU và MaxPool 2 x 2. Đầu ra 32 x 14 x 14.\n"
        "• Khối 2: Conv2D 32→64, kernel 3 x 3, padding 1; BatchNorm, ReLU và MaxPool 2 x 2. Đầu ra 64 x 7 x 7.\n"
        "• Khối 3: Conv2D 64→128, kernel 3 x 3, padding 0; BatchNorm, ReLU và MaxPool 2 x 2. Đầu ra 128 x 2 x 2.\n"
        "• Phân lớp: Flatten 512 chiều, Dropout 0.4, Linear 512→128, ReLU, Dropout 0.2 và Linear 128→10.\n"
        "Mô hình có 160.074 tham số có thể huấn luyện; checkpoint khoảng 0.62 MiB."

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
        'MNIST gồm 70.000 ảnh xám chữ số viết tay kích thước 28 x 28, được chia sẵn thành 60.000 ảnh train và 10.000 ảnh test. Repo kèm tệp data/mnist.npz; download_mnist.py ghi địa chỉ tải từ kho TensorFlow/Keras và kho IDX của CVDF. Dữ liệu đầu vào có kiểu uint8, giá trị từ 0 đến 255 và nhãn từ 0 đến 9.'
    )

    # Embed Figure 01
    add_image_safe(doc, FIGURES_DIR / "01_class_distribution.png", 5.2,
                   "Hình 3.1: Phân bố tần suất 10 lớp chữ số trên tập Train (60.000 mẫu) và tập Test (10.000 mẫu) của MNIST")

    add_body_p(doc, "Kiểm tra tệp dữ liệu xác nhận ảnh và nhãn có đúng kích thước, không có NaN, pixel thuộc [0, 255] và nhãn thuộc 0–9. Pixel được chuyển sang float32 và chia 255 trước khi huấn luyện. Các mẫu có nét viết khác thường được giữ lại trong đánh giá; repo chưa có bước tự động sửa nhãn.")
    add_heading_styled(doc, "3.2. Phân tích phân bố nhãn và độ đo Shannon Entropy", level=2)
    add_body_p(doc,
        "Để kiểm tra tính cân bằng của tập dữ liệu, nhóm tính toán tần suất xuất hiện thực tế của từng lớp chữ số và xác định độ hỗn loạn thông tin Shannon Entropy: "
        "H(Y) = - sum_{k=0}^9 p_k * log_2(p_k). "
        "Một tập dữ liệu 10 lớp hoàn toàn cân bằng lý tưởng có độ entropy cực đại là H_{max} = log_2(10) = 3.321928 bits."
    )
    add_body_p(doc,
        'Trên tập train, số mẫu mỗi lớp dao động từ 5.421 ảnh ở lớp 5 đến 6.742 ảnh ở lớp 1; entropy đạt khoảng 3.3199 bit. Tập test có từ 892 đến 1.135 ảnh mỗi lớp, entropy khoảng 3.3194 bit. Phân bố gần cân bằng nhưng số lượng giữa các lớp vẫn khác nhau. Vì vậy, báo cáo sử dụng cả Accuracy và các chỉ số macro để đánh giá.'
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
        'Ảnh trung bình cho thấy vùng có nét viết thường xuyên xuất hiện, còn ảnh phương sai phản ánh sự thay đổi giữa các cách viết cùng lớp. Pixel ở vùng biên thường tối và ít biến thiên; một số ảnh vẫn có nét chạm biên. Các lớp 4 và 9 có vùng nét phía trên tương tự nhau, trong khi lớp 1 thay đổi rõ ở phần đầu và chân nét.'
    )

    # Embed Figure 03
    add_image_safe(doc, FIGURES_DIR / "03_pixel_distribution.png", 5.0,
                   "Hình 3.3: Phân bố cường độ pixel sau chuẩn hóa về [0, 1]")

    add_heading_styled(doc, "3.4. Trực quan hóa hiệu quả nắn thẳng Deskewing", level=2)
    add_body_p(doc,
        "Phương pháp Deskewing giúp loại bỏ độ nghiêng nét viết cá nhân. Hình 3.4 minh họa so sánh trực tiếp các mẫu chữ số trước và sau khi đi qua phép biến đổi affine shear:"
    )

    # Embed Figure 04
    add_image_safe(doc, FIGURES_DIR / "04_deskew_comparison.png", 5.2,
                   "Hình 3.4: Minh chứng so sánh các mẫu chữ số viết tay trước và sau khi nắn thẳng (Deskewing)")

    add_heading_styled(doc, "3.5. Trực quan hóa không gian nén PCA và cụm t-SNE", level=2)
    add_body_p(doc,
        'Hình 3.5 biểu diễn phương sai tích lũy của các bộ PCA đã lưu. Các bộ biến đổi đã lưu giữ ít nhất 95% phương sai: 154 thành phần cho 60.000 ảnh thô, 152 thành phần cho tập con 10.000 ảnh thô và 112 thành phần cho tập con đã deskew. Số chiều được xác định riêng từ dữ liệu huấn luyện của từng cấu hình.'
    )

    # Embed Figure 05 & 07
    add_image_safe(doc, FIGURES_DIR / "05_pca_variance_curve.png", 4.3,
                   "Hình 3.5: Đường cong phương sai tích lũy theo số lượng thành phần chính PCA")
    add_image_safe(doc, FIGURES_DIR / "07_tsne_clustering.png", 4.3,
                   "Hình 3.6: Biểu đồ chiếu cụm t-SNE của 10 lớp chữ số viết tay trong không gian 2D")

    add_heading_styled(doc, "3.6. Thiết kế chia tập dữ liệu và nguyên tắc chống rò rỉ dữ liệu (Data Leakage)", level=2)
    add_body_p(doc,
        'Tập test được dùng để đánh giá checkpoint, không dùng để fit PCA hoặc chọn siêu tham số. Thiết kế dữ liệu gồm hai nhánh: các cấu hình toàn phần huấn luyện trên 60.000 ảnh; nhánh validation chia 60.000 ảnh thành 50.000 train và 10.000 validation. Tập con so sánh 10.000 ảnh được lấy từ nhánh 50.000 train, với 1.000 ảnh mỗi lớp và random_state=42.'
    )
    add_bullet_p(doc, 'Tập test gồm 10.000 ảnh chính thức, được chuẩn hóa và biến đổi bằng các tham số đã học từ train. Việc chạy lại checkpoint trên tập này phục vụ kiểm tra tính nhất quán của kết quả.', "1. ");
    add_bullet_p(doc, 'Nhánh validation sử dụng train_test_split có stratify theo nhãn và random_state=42, tạo 50.000 ảnh train và 10.000 ảnh validation có chỉ số không giao nhau.', "2. ");
    add_bullet_p(doc, 'PCA được fit trên tập train tương ứng. Validation và test dùng transform của cùng bộ PCA; thông tin từ hai tập này không tham gia xác định các thành phần chính.', "3. ");
    add_bullet_p(doc, 'SVM Deskew + PCA sử dụng bộ PCA 112 chiều học trên ảnh đã deskew. Pipeline đóng gói bước deskew, PCA và SVM để tái sử dụng đúng thứ tự khi dự đoán.', "4. ");

    # ==================== CHƯƠNG 4 ====================
    add_heading_styled(doc, "CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ TỐI ƯU SIÊU THAM SỐ", level=1)
    
    add_heading_styled(doc, "4.1. Môi trường thực nghiệm phần cứng và phần mềm", level=2)
    add_body_p(doc,
        'Nhật ký đo độ trễ gốc ghi nhận môi trường Windows AMD64, CPU Intel64 Family 6 Model 183, Python 3.14.5, scikit-learn 1.9.1, PyTorch 2.14.1+cpu, NumPy 2.4.6 và thiết bị CPU. Repo không ghi đầy đủ dung lượng RAM và tên thương mại của CPU. Môi trường chạy lại checkpoint được lưu riêng trong results/evaluation_environment.json; các thời gian lịch sử không được xem là phép đo trên máy chạy lại.'
    )

    add_heading_styled(doc, "4.2. Giao thức tối ưu siêu tham số trên tập Validation (Hyperparameter Tuning)", level=2)
    add_body_p(doc,
        'Tệp hyperparameter_search_results.json lưu các cấu hình thử trên 10.000 ảnh validation và đánh dấu cấu hình được chọn cho từng họ mô hình. Bảng 4.1 trình bày Accuracy, Macro F1 và siêu tham số tương ứng. Các cấu hình toàn phần và CNN baseline dùng quy trình riêng, không áp dụng dừng sớm cho toàn bộ thí nghiệm.'
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
        'Các thí nghiệm được chia theo câu hỏi so sánh. Trong mỗi nhóm, quy mô dữ liệu và cách biểu diễn được ghi rõ để xác định phạm vi của kết luận.'
    )
    add_bullet_p(doc, "Nhóm A (Đánh giá ảnh hưởng của Không gian Đặc trưng): Cố định thuật toán phân lớp là SVM nhân RBF (C=5.0, gamma=scale), cố định tập dữ liệu huấn luyện là tập Controlled Subset 10.000 mẫu được lấy mẫu phân tầng. So sánh 5 biểu diễn: Raw Pixels (784D), Deskewed Pixels (784D), HOG (324D), PCA (152D) và Deskewed + PCA (112D).", "Nhóm A: ");
    add_bullet_p(doc, 'Nhóm B so sánh Gaussian NB, Bernoulli NB, Linear SVM C=0.01, k-NN k=3, Random Forest 150 cây và SVM RBF trên cùng 10.000 ảnh. Phần lớn dùng 784 pixel chuẩn hóa; Bernoulli NB nhị phân hóa pixel theo ngưỡng 0.2. k-NN + PCA là cấu hình bổ sung, không được dùng để kết luận riêng tác động của thuật toán khi đặc trưng đã thay đổi.', "Nhóm B: ");
    add_bullet_p(doc, 'Nhóm C gồm CNN huấn luyện cố định 5 epoch trên 10.000 ảnh, CNN baseline cố định 4 epoch trên 60.000 ảnh và CNN chọn checkpoint trên 50.000 train / 10.000 validation. Nhánh 60.000 ảnh được so sánh với SVM RBF + PCA và k-NN + PCA cùng quy mô.', "Nhóm C: ");

    add_heading_styled(doc, "4.4. Quy trình huấn luyện và kiểm định Validation cho mạng Modern CNN", level=2)
    add_body_p(doc,
        'CNN validation dùng 50.000 ảnh train và 10.000 ảnh validation. Sau mỗi epoch, mô hình được đánh giá bằng validation loss và validation accuracy. Checkpoint có validation loss nhỏ nhất được lưu lại. Nhật ký kèm theo ghi nhận dừng ở epoch 4 sau hai epoch không cải thiện; checkpoint được chọn ở epoch 2. CNN baseline 60.000 ảnh là thí nghiệm huấn luyện cố định 4 epoch, không có tập validation độc lập.'
    )

    # Embed Figure 08 (CNN Training History)
    add_image_safe(doc, FIGURES_DIR / "08_cnn_training_history.png", 5.2,
                   "Hình 4.1: Đường cong Mất mát (Loss) và Độ chính xác (Accuracy) qua các Epoch huấn luyện của Modern CNN với cơ chế Early Stopping trên tập Validation")

    add_body_p(doc,
        'Lịch sử huấn luyện ghi nhận validation loss lần lượt là 0.0541, 0.0425, 0.0438 và 0.0525 qua bốn epoch. Epoch 2 có loss nhỏ nhất và validation accuracy 98.70%. Checkpoint này đạt test accuracy 99.00%, sai 100 ảnh, được lưu tại modern_cnn_val_tuned.pt. CNN baseline đạt 99.19% từ quy trình 60.000 train riêng. Chênh lệch này chịu ảnh hưởng của cả lượng dữ liệu huấn luyện và cách chọn checkpoint.'
    )

    add_heading_styled(doc, "4.5. Giao thức đo lường hiệu năng, độ trễ và thông lượng (Latency & Throughput)", level=2)
    add_body_p(doc,
        'Kết quả đo hiệu năng gốc được lưu trong results/latency_benchmark_detailed.json. Độ trễ từng ảnh được đo sau 50 lần khởi động và 500 lần chạy có bấm giờ. CNN có trung bình 0.516 ms, trung vị 0.405 ms và P95 0.664 ms; pipeline SVM Deskew + PCA có trung bình 0.536 ms. Khi dự đoán theo lô 10.000 ảnh, CNN đạt khoảng 9.426 mẫu/giây, SVM Deskew + PCA đạt khoảng 5.551 mẫu/giây. Thời gian trung bình mỗi ảnh trong một lô không đại diện cho độ trễ một yêu cầu web. Thời gian huấn luyện trong bảng tổng hợp là thời gian fit mô hình; việc trích xuất đặc trưng và tải dữ liệu có thể được đo bên ngoài khoảng này. Dung lượng tệp được tính theo MiB, bằng số byte chia cho 1024².'
    )

    # ==================== CHƯƠNG 5 ====================
    add_heading_styled(doc, "CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM, ĐỐI CHUẨN VÀ PHÂN TÍCH LỖI", level=1)
    
    add_heading_styled(doc, "5.1. Bảng tổng hợp đối chuẩn hiệu năng toàn diện", level=2)
    add_body_p(doc,
        'Bảng 5.1 tổng hợp 16 cấu hình từ verified_experiments.json, gồm 12 cấu hình train 10.000 mẫu, 3 cấu hình train 60.000 mẫu và 1 CNN train 50.000 mẫu có validation. Chỉ số được tính lại từ dự đoán trên đủ 10.000 ảnh test. Thời gian huấn luyện là số liệu lịch sử; dấu gạch trong bảng chỉ trường chưa có phép đo được lưu.'
    )

    add_body_p(doc, "Accuracy là tỷ lệ ảnh dự đoán đúng. Với từng lớp c: Precision_c = TP_c / (TP_c + FP_c), Recall_c = TP_c / (TP_c + FN_c), F1_c = 2 * Precision_c * Recall_c / (Precision_c + Recall_c). Macro F1 là trung bình F1 của 10 lớp. Ma trận nhầm lẫn dùng hàng là nhãn thật, cột là nhãn dự đoán. Số ảnh sai của lớp c bằng tổng hàng c trừ phần tử trên đường chéo.")
    # Load from verified_experiments.json
    with open(RESULTS_JSON, "r", encoding="utf-8") as f:
        verified_data = json.load(f)

    t_res = doc.add_table(rows=len(verified_data) + 1, cols=7)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_res = ["Mô hình", "Không gian đặc trưng", "Tập huấn luyện", "Test Acc", "Macro F1", "Số ảnh sai", "Thời gian fit (s)"]
    
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
            f"{item['train_time_sec']:.2f}" if item.get("train_time_sec") is not None else "—"
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

    add_caption(doc, "Bảng 5.1: Kết quả 16 cấu hình trên 10.000 ảnh test và thời gian fit lịch sử", is_table=True)

    add_heading_styled(doc, "5.2. Phân tích đối chứng Nhóm A: Ảnh hưởng của Không gian Đặc trưng", level=2)
    add_body_p(doc,
        "Quan sát kết quả Nhóm A trong Bảng 5.1 (cố định thuật toán SVM RBF, huấn luyện trên 10.000 mẫu subset):"
    )
    add_bullet_p(doc, 'Deskew + PCA 112 chiều đạt 97.97%, sai 203 ảnh, Macro F1 97.96%; cao nhất trong năm cấu hình SVM cùng huấn luyện trên 10.000 mẫu. So với ảnh thô đạt 96.86%, số ảnh sai giảm 111. Kết luận này áp dụng cho tập con và các siêu tham số đã thử.', "1. ");
    add_bullet_p(doc, 'Deskew trên 784 pixel đạt 97.77%, sai 223 ảnh. So với ảnh thô 96.86%, Accuracy tăng 0.91 điểm phần trăm và số ảnh sai giảm 91 trong cùng cấu hình SVM RBF.', "2. ");
    add_bullet_p(doc, 'HOG 324 chiều đạt 97.58%, sai 242 ảnh, cao hơn ảnh thô 0.72 điểm phần trăm. Đặc trưng mô tả phân bố hướng gradient trong các vùng của ảnh.', "3. ");
    add_bullet_p(doc, 'PCA trên ảnh thô giữ 152 thành phần và đạt 97.22%, cao hơn ảnh thô 0.36 điểm phần trăm. Số chiều giảm từ 784 xuống 152; mức thay đổi độ chính xác phụ thuộc dữ liệu và bộ phân lớp.', "4. ");

    add_heading_styled(doc, "5.3. Phân tích đối chứng Nhóm B: Ảnh hưởng của Thuật toán Phân lớp", level=2)
    add_body_p(doc,
        'Trong nhóm 10.000 train, các mô hình dùng pixel chuẩn hóa; Bernoulli NB bổ sung bước nhị phân hóa. Kết quả của từng thuật toán được phân tích như sau:'
    )
    add_bullet_p(doc, 'SVM RBF đạt 96.86% trên ảnh thô, cao hơn Linear SVM C=0.01 đạt 90.79% trong cùng tập train 10.000 mẫu. Kết quả cho thấy kernel RBF phù hợp hơn ở cấu hình đang khảo sát.', "1. ");
    add_bullet_p(doc, 'Random Forest 150 cây đạt 95.28%, sai 472 ảnh. Mô hình sử dụng trực tiếp pixel chuẩn hóa và số cây được chọn từ thí nghiệm validation.', "2. ");
    add_bullet_p(doc, 'k-NN trên điểm ảnh thô đạt 95.17%. Mô hình lưu tập tham chiếu và cần tính khoảng cách khi dự đoán; chi phí tăng theo số mẫu và số chiều.', "3. ");
    add_bullet_p(doc, 'Linear SVM C=0.01 đạt 90.79%, sai 921 ảnh. Đây là cấu hình được chọn trong các giá trị C đã khảo sát trên validation.', "4. ");
    add_bullet_p(doc, 'Bernoulli NB đạt 84.40%, cao hơn Gaussian NB ở nhóm 10.000 train. Mô hình dùng sự có mặt của pixel sau nhị phân hóa, phù hợp hơn giả định Gaussian trong thí nghiệm này.', "5. ");
    add_bullet_p(doc, 'Gaussian NB đạt 55.80%, thấp nhất trong nhóm khảo sát. Phân bố pixel có nhiều giá trị bằng 0 và các pixel lân cận có tương quan; hai đặc điểm này có thể hạn chế giả định phân phối chuẩn và độc lập có điều kiện của mô hình.', "6. ");

    add_heading_styled(doc, "5.4. Phân tích đối chứng Nhóm C: Quy mô dữ liệu và Ưu thế của Deep Learning", level=2)
    add_body_p(doc,
        'CNN baseline 60.000 mẫu đạt Accuracy 99.19%, Macro F1 99.18% và sai 81/10.000 ảnh test. CNN 10.000 mẫu đạt 97.60%, sai 240 ảnh. Số lỗi giảm 159 khi tăng dữ liệu, nhưng hai cấu hình chạy số epoch khác nhau nên chênh lệch không thể quy hoàn toàn cho lượng dữ liệu. Ở nhóm 10.000 mẫu, SVM Deskew + PCA đạt 97.97%, cao hơn CNN 0.37 điểm phần trăm. Ở nhóm 60.000 mẫu, CNN cao hơn SVM RBF + PCA đạt 98.54% và k-NN + PCA đạt 97.31%.'
    )

    add_body_p(doc, "CNN được chọn mặc định cho demo vì có Accuracy cao nhất trong nhóm 60.000 train và checkpoint khoảng 0.62 MiB. SVM Deskew + PCA là lựa chọn thay thế cho nhóm train 10.000 mẫu; k-NN cần lưu dữ liệu tham chiếu và có chi phí tìm láng giềng khi dự đoán. Linear SVM và Naive Bayes có cấu trúc đơn giản nhưng Accuracy thấp hơn trong thí nghiệm. Các ưu nhược điểm này được xem xét cùng quy mô train và cách biểu diễn dữ liệu.")
    # Embed Confusion Matrices
    add_image_safe(doc, FIGURES_DIR / "cm_modern_cnn_full_60k.png", 4.3,
                   "Hình 5.1: Ma trận nhầm lẫn chuẩn hóa của mô hình Modern CNN trên 10.000 ảnh test (Accuracy: 99.19%, 81 lỗi)")
    add_image_safe(doc, FIGURES_DIR / "cm_svm_rbf_deskew_pca_sub10k.png", 4.3,
                   "Hình 5.2: Ma trận nhầm lẫn của mô hình SVM RBF (Deskew + PCA 112D) trên 10.000 ảnh test (Accuracy: 97.97%, 203 lỗi)")

    add_image_safe(doc, FIGURES_DIR / "correct_modern_cnn.png", 5.1,
                   "Hình 5.3: Ví dụ CNN dự đoán đúng mỗi lớp, ghi chỉ số test và nhãn thật → dự đoán")
    add_body_p(doc, "Các ví dụ đúng được lấy từ cùng bộ dự đoán dùng để tính chỉ số; mỗi lớp chọn mẫu đúng đầu tiên theo thứ tự test. Tệp results/test_predictions.npz lưu nhãn thật và dự đoán của các checkpoint, giúp kiểm tra lại từng trường hợp.")
    add_heading_styled(doc, "5.5. Phân tích chi tiết từng lớp (Per-Class Performance)", level=2)
    add_body_p(doc,
        "Bảng 5.2 trình bày chi tiết các chỉ số Precision, Recall và F1-Score trên từng lớp chữ số độc lập của mô hình Modern CNN chính thức (99.19%):"
    )

    measured_cnn = json.loads((BASE_DIR / "results" / "checkpoint_evaluation.json").read_text(encoding="utf-8"))["EXP-C01"]
    per_class_cnn = [
        (str(i), f"{measured_cnn['support'][i]:,}",
         f"{measured_cnn['precision_per_class'][i] * 100:.2f}%",
         f"{measured_cnn['recall_per_class'][i] * 100:.2f}%",
         f"{measured_cnn['f1_per_class'][i] * 100:.2f}%",
         str(measured_cnn['errors_per_class'][i])) for i in range(10)
    ]
    assert sum(measured_cnn["errors_per_class"]) == measured_cnn["test_errors"] == 81

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

    add_heading_styled(doc, "5.6. Phân tích 81 mẫu CNN dự đoán sai", level=2)
    add_body_p(doc,
        'Danh sách 81 ảnh CNN dự đoán sai được xuất tại reports/tables/cnn_error_samples.csv với chỉ số ảnh bắt đầu từ 0, nhãn dữ liệu và nhãn dự đoán. Hình 5.4 trình bày một số lỗi. Phân tích hình dạng dưới đây là nhận xét trực quan, không thay thế quy trình kiểm tra lại nhãn gốc.'
    )

    # Embed Error Gallery (width 3.5 in to ensure clean layout without orphaned bullets)
    add_image_safe(doc, FIGURES_DIR / "errors_modern_cnn_full_60k.png", 3.5,
                   "Hình 5.4: Một số mẫu CNN dự đoán sai, gồm nhãn gốc và nhãn dự đoán")

    add_body_p(doc, "Mẫu #259 có nhãn 6 nhưng được dự đoán là 0; nét vòng chiếm phần lớn ảnh trong khi nét móc phía trên ngắn. Mẫu #447 có nhãn 4 nhưng được dự đoán là 9; vùng nét phía trên dày và gần khép kín. Đây là hai ví dụ cho sự tương đồng hình dạng giữa các lớp. Các nhãn gốc được giữ nguyên trong toàn bộ phép tính.")
    add_bullet_p(doc, 'Nét viết có hình dạng gần lớp khác: những mẫu có vòng chưa khép, nét nối mờ hoặc thiếu nét có thể tạo ra đặc trưng giống một chữ số khác. Báo cáo giữ nguyên nhãn MNIST khi tính chỉ số và không kết luận nhãn gốc sai chỉ từ hình thức nét viết.', "Nhóm 1: ");
    add_bullet_p(doc, 'Nét chữ khó phân biệt: một số kiểu viết 3 và 5, 4 và 9 hoặc 7 và 1 có cấu trúc gần nhau. Khi thông tin phân biệt nằm ở một nét ngắn, dự đoán dễ thay đổi theo vị trí và độ rõ của nét.', "Nhóm 2: ");
    add_bullet_p(doc, 'Biến thiên hình học: tỷ lệ dài/rộng, độ nghiêng, độ dày nét và vị trí trong khung ảnh khác nhau có thể làm giảm khả năng nhận dạng. Trong đánh giá MNIST, CNN nhận ảnh test đã chuẩn hóa, không đi qua bước căn tâm của ảnh vẽ trên web.', "Nhóm 3: ");

    # ==================== CHƯƠNG 6 ====================
    add_heading_styled(doc, "CHƯƠNG 6: TRIỂN KHAI ỨNG DỤNG DEMO WEB VÀ KIỂM THỬ HỆ THỐNG", level=1)
    
    add_heading_styled(doc, "6.1. Kiến trúc tổng thể hệ thống Demo tương tác", level=2)
    add_body_p(doc,
        'Ứng dụng web gồm backend FastAPI và giao diện HTML/CSS/JavaScript. Người dùng có thể vẽ chữ số, tải ảnh hoặc chọn mẫu MNIST, sau đó xem dự đoán và ảnh sau tiền xử lý.'
    )
    add_bullet_p(doc, 'Backend FastAPI cung cấp API liệt kê mô hình, lấy mẫu và dự đoán. Checkpoint được nạp vào bộ nhớ khi khởi động; mỗi mô hình dùng bước biến đổi tương ứng với cấu hình huấn luyện.', "• ");
    add_bullet_p(doc, 'Frontend sử dụng HTML5 Canvas để vẽ, chỉnh độ dày nét và xóa ảnh. Giao diện hỗ trợ chọn mô hình, chọn mẫu test và hiển thị biểu đồ điểm cho 10 lớp.', "• ");
    add_bullet_p(doc, 'Danh mục mô hình ánh xạ tên lựa chọn tới checkpoint cụ thể. API trả HTTP 404 khi tên mô hình không tồn tại. Điểm hiển thị được tính từ softmax, khoảng cách lề hoặc đầu ra của mô hình; các điểm này chưa được hiệu chuẩn thành xác suất đúng trên dữ liệu ngoài MNIST.', "• ");

    add_heading_styled(doc, "6.2. Pipeline tiền xử lý ảnh vẽ tay thời gian thực", level=2)
    add_body_p(doc,
        'Ảnh vẽ hoặc tải lên được chuyển sang mức xám, cắt vùng chữ, thu phóng, đệm và căn trọng tâm trước khi đưa về 28 x 28. Quy trình giúp chuẩn hóa kích thước và vị trí, nhưng chưa có bộ dữ liệu ngoài MNIST để đánh giá độ chính xác trên nét vẽ thực tế.'
    )
    add_bullet_p(doc, "Phát hiện nét vẽ và cắt hộp giới hạn (Bounding Box Crop): Tìm tọa độ bao quanh nét vẽ của chữ số thông qua hàm cv2.boundingRect(). Nếu canvas trống (ít hơn 15 điểm ảnh sáng), hệ thống lập tức trả về mã dự đoán -1 và thông báo 'Bảng vẽ trống', không chạy suy luận vô nghĩa.", "Bước 1: ");
    add_bullet_p(doc, "Thu phóng bảo toàn tỷ lệ khung hình (Aspect Ratio Resize): Đưa chữ số về kích thước tối đa 20 x 20 điểm ảnh, giữ nguyên tỷ lệ dài/rộng gốc để không làm méo hình thái ký tự.", "Bước 2: ");
    add_bullet_p(doc, "Đệm vào khung chuẩn 28 x 28 (Canvas Padding): Đặt chữ số 20 x 20 vào chính giữa khung đen kích thước 28 x 28 điểm ảnh.", "Bước 3: ");
    add_bullet_p(doc, "Căn chỉnh trọng tâm khối lượng (Center of Mass Translation): Tính toán mô-men hình ảnh để xác định trọng tâm quang học (cx, cy) của chữ số và áp dụng phép tịnh tiến affine đưa trọng tâm về chính xác tọa độ (14.0, 14.0) của khung hình.", "Bước 4: ");
    add_bullet_p(doc, "Chuẩn hóa cường độ sáng: Đưa giá trị điểm ảnh về dải số thực chuẩn hóa [0.0, 1.0] tương ứng với dữ liệu đầu vào của các bộ phân lớp.", "Bước 5: ");

    add_body_p(doc, "Từ thư mục gốc, cài thư viện bằng python -m pip install -r requirements.txt và chạy web bằng python run_app.py. Lệnh python -m unittest tests.test_pipeline -v chạy bộ kiểm thử; python -m src.verify_saved_results đánh giá lại checkpoint và cập nhật bảng kết quả mà không huấn luyện lại. Huấn luyện các nhóm mô hình dùng python -m src.train_and_benchmark; nhánh CNN validation dùng python -m src.train_cnn_with_validation.")
    add_heading_styled(doc, "6.3. Bộ kiểm thử tự động (Automated Test Suite) và Kết quả nghiệm thu", level=2)
    add_body_p(doc,
        'Bộ tests/test_pipeline.py gồm 28 ca kiểm thử về nạp dữ liệu, chia tập, đặc trưng, cấu trúc CNN, ánh xạ checkpoint và API dự đoán. Kết quả lần chạy kiểm tra được lưu tại results/test_suite_result.json. Bảng 6.1 liệt kê các nhóm kiểm tra và trạng thái thực thi.'
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
        ("test_api_predict_blank_image", "Kiểm tra API dự đoán canvas trống trả về nhãn -1 và thông báo ảnh trống", "PASS"),
        ("test_api_predict_sample_digit", "Kiểm tra API nhận dạng thành công mẫu kiểm thử MNIST trả về nhãn 0-9", "PASS"),
        ("test_api_predict_invalid_model_raises_404", "Kiểm tra API trả về mã lỗi HTTP 404 khi người dùng gửi sai tên mô hình", "PASS"),
        ("test_api_predict_svm_deskew_pca", "Kiểm tra endpoint mô hình SVM Deskew + PCA hoạt động trơn tru end-to-end", "PASS"),
        ("test_svm_deskew_pca_pipeline_reload_and_accuracy", "Kiểm tra nạp lại pipeline Deskew+PCA đạt accuracy >= 97% (chống lệch PCA)", "PASS"),
        ("test_modern_cnn_checkpoint_parameters", "Xác nhận kiến trúc ModernCNN và checkpoint có chính xác 160.074 tham số", "PASS"),
        ("test_hyperparameter_search_results_exist", "Kiểm tra tính toàn vẹn của tệp nhật ký dò tìm siêu tham số trên Validation", "PASS"),
        ("test_selected_hyperparameters_match_artifacts", "Xác nhận các siêu tham số trong checkpoint khớp 100% kết quả thắng trên Validation", "PASS"),
        ("test_cnn_validation_history_and_checkpoint", "Kiểm tra tính toàn vẹn của quy trình CNN validation (50k/10k/10k, early stopping, biểu đồ và checkpoint)", "PASS"),
    ]

    test_cases_summary.extend([
        ("test_backend_loads_linear_svm_c001", "API nạp Linear SVM C=0.01", "PASS"),
        ("test_backend_loads_random_forest_150_trees", "API nạp Random Forest 150 cây", "PASS"),
        ("test_backend_confidence_metadata_and_calibration_honesty", "Đầu ra ghi loại điểm và trạng thái hiệu chuẩn", "PASS"),
        ("test_frontend_no_hardcoded_obsolete_accuracy", "Giao diện không chứa số liệu cũ được kiểm tra", "PASS"),
    ])
    suite_result = json.loads((BASE_DIR / "results" / "test_suite_result.json").read_text(encoding="utf-8"))
    test_cases_summary = [(name, desc, suite_result["tests"].get(name, "Chưa chạy"))
                          for name, desc, _ in test_cases_summary]
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

    add_caption(doc, "Bảng 6.1: Kết quả chạy 28 ca kiểm thử tự động", is_table=True)

    add_body_p(doc, "Kiểm tra HTTP ghi nhận trang chính trả mã 200, API liệt kê 12 mô hình và 10 mẫu test. Các yêu cầu dự đoán mẫu số 0 qua CNN, CNN validation, SVM Deskew + PCA, Random Forest và Linear SVM đều trả nhãn 0 cùng 10 điểm lớp. Ảnh trống trả nhãn -1; tên mô hình không tồn tại trả mã 404. Kết quả lưu tại results/http_smoke_result.json.")

    # ==================== CHƯƠNG 7 ====================
    add_heading_styled(doc, "CHƯƠNG 7: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", level=1)
    
    add_heading_styled(doc, "7.1. Kết quả theo các câu hỏi nghiên cứu", level=2)
    add_body_p(doc,
        'Các kết quả thực nghiệm trả lời ba câu hỏi đặt ra ở Chương 1 trong phạm vi bộ dữ liệu và cấu hình đã khảo sát.'
    )
    add_bullet_p(doc, 'RQ1: Với SVM RBF cùng train 10.000 mẫu, Deskew + PCA 112 chiều đạt Accuracy cao nhất, 97.97%. Các cấu hình HOG, PCA ảnh thô và pixel thô lần lượt đạt 97.58%, 97.22% và 96.86%.', "• ");
    add_bullet_p(doc, 'RQ2: Trên 10.000 ảnh train với điểm ảnh chuẩn hóa, SVM RBF đạt 96.86%, Random Forest 150 cây đạt 95.28%, k-NN đạt 95.17% và Linear SVM đạt 90.79%. Bernoulli NB sử dụng pixel nhị phân và đạt 84.40%; Gaussian NB đạt 55.80%.', "• ");
    add_bullet_p(doc, 'RQ3: CNN train 60.000 mẫu đạt 99.19%, cao hơn CNN train 10.000 mẫu đạt 97.60%. Trong nhóm train 60.000 mẫu, CNN có kết quả cao nhất trong các cấu hình đã thử. CNN chọn checkpoint bằng validation là nhánh riêng, đạt 99.00%.', "• ");

    add_heading_styled(doc, "7.2. Các đóng góp chính của đề tài", level=2)
    add_body_p(doc,
        'Đề tài xây dựng các bước nạp dữ liệu, trích xuất đặc trưng, huấn luyện và đánh giá cho năm họ mô hình. Repo lưu checkpoint, lịch sử tìm siêu tham số, lịch sử CNN validation và bảng kết quả của 16 cấu hình. Phần phân tích so sánh đặc trưng, thuật toán và quy mô dữ liệu theo từng nhóm. Ứng dụng web tích hợp mô hình cùng các bước xử lý ảnh để thực hiện dự đoán tương tác.'
    )

    add_heading_styled(doc, "7.3. Hạn chế thực nghiệm khách quan", level=2)
    add_body_p(doc,
        'Phạm vi triển khai chỉ gồm chữ số đơn lẻ đã tách khỏi ảnh. Hệ thống chưa nhận dạng chuỗi số, chưa được đánh giá trên tập ảnh ngoài MNIST và chưa hiệu chuẩn điểm tin cậy. Mỗi cấu hình mới có một lần huấn luyện được lưu, nên báo cáo chưa ước lượng độ lệch chuẩn giữa nhiều seed. CNN 10.000 và 60.000 mẫu có số epoch khác nhau; kết quả so sánh chịu ảnh hưởng đồng thời của hai yếu tố này.'
    )

    add_heading_styled(doc, "7.4. Hướng phát triển trong tương lai", level=2)
    add_body_p(doc,
        "• Mở rộng bài toán nhận dạng chuỗi chữ số viết tay liên tục ứng dụng mô hình CRNN (Convolutional Recurrent Neural Network) kết hợp hàm mất mát CTC Loss (Connectionist Temporal Classification).\n"
        "• Xuất mô hình sang định dạng ONNX (Open Neural Network Exchange) và tối ưu lượng tử hóa INT8 (Quantization) để nhúng trực tiếp vào các thiết bị di động và camera giám sát thông minh."
    )

    assignment_heading = add_heading_styled(doc, "7.5. Bảng phân công nhiệm vụ và mức độ hoàn thành của các thành viên Nhóm 03", level=2)
    assignment_heading.paragraph_format.page_break_before = True
    
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
    references.append("11. Nguồn dữ liệu trong download_mnist.py: https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz và https://storage.googleapis.com/cvdf-datasets/mnist/. Mã tải và dữ liệu nén đi kèm repo.")
    for ref_str in references:
        add_body_p(doc, ref_str, space_after=6)

    for table, widths in ((t_tune, [0.85, 1.0, 1.85, 0.8, 0.85, 1.15]),
                          (t_res, [1.25, 1.45, 0.7, 0.65, 0.65, 0.75, 1.05]),
                          (t_tc, [2.7, 3.1, 0.7])):
        table.autofit = False
        for column, width in zip(table.columns, widths):
            column.width = Inches(width)
        for row in table.rows:
            for cell, width in zip(row.cells, widths):
                cell.width = Inches(width)
    for table in doc.tables:
        if table._tbl is t_task._tbl:
            continue
        for i, row in enumerate(table.rows):
            pr = row._tr.get_or_add_trPr()
            cant_split = OxmlElement("w:cantSplit"); pr.append(cant_split)
            if i == 0:
                repeat = OxmlElement("w:tblHeader"); pr.append(repeat)
            for cell in row.cells:
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                tc_pr = cell._tc.get_or_add_tcPr()
                borders = OxmlElement("w:tcBorders")
                for edge in ("top", "left", "bottom", "right"):
                    border = OxmlElement("w:" + edge)
                    border.set(qn("w:val"), "single"); border.set(qn("w:sz"), "4")
                    border.set(qn("w:color"), "D9D9D9"); borders.append(border)
                tc_pr.append(borders)
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.space_after = Pt(2)
                    paragraph.paragraph_format.line_spacing = 1.1
                    for run in paragraph.runs:
                        run.font.name = "Times New Roman"
    doc.save(str(DOCX_PATH))
    export_markdown_report(doc)
    print(f"[OK] Đã xuất thành công file Word hoàn chỉnh: {DOCX_PATH}")
    print(f"     Kích thước file: {DOCX_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build_docx_report()
