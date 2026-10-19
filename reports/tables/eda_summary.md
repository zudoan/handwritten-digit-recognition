# BẢNG THỐNG KÊ CHI TIẾT TẬP DỮ LIỆU MNIST
**Học phần: Nhận dạng mẫu — Nhóm 03**

### 1. Phân bố số lượng mẫu giữa các lớp (Class Distribution)

| Chữ số | Huấn luyện (Train) | Tỷ lệ (%) | Kiểm thử (Test) | Tỷ lệ (%) | Tổng cộng | Tỷ lệ tổng (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 5,923 | 9.87% | 980 | 9.80% | 6,903 | 9.86% |
| **1** | 6,742 | 11.24% | 1,135 | 11.35% | 7,877 | 11.25% |
| **2** | 5,958 | 9.93% | 1,032 | 10.32% | 6,990 | 9.99% |
| **3** | 6,131 | 10.22% | 1,010 | 10.10% | 7,141 | 10.20% |
| **4** | 5,842 | 9.74% | 982 | 9.82% | 6,824 | 9.75% |
| **5** | 5,421 | 9.04% | 892 | 8.92% | 6,313 | 9.02% |
| **6** | 5,918 | 9.86% | 958 | 9.58% | 6,876 | 9.82% |
| **7** | 6,265 | 10.44% | 1,028 | 10.28% | 7,293 | 10.42% |
| **8** | 5,851 | 9.75% | 974 | 9.74% | 6,825 | 9.75% |
| **9** | 5,949 | 9.92% | 1,009 | 10.09% | 6,958 | 9.94% |
| **Tổng** | **60,000** | **100.00%** | **10,000** | **100.00%** | **70,000** | **100.00%** |

### 2. Chỉ số cân bằng dữ liệu (Data Balance Metrics)
- **Độ hỗn loạn thông tin (Shannon Entropy)**: 3.3199 bits (so với cực đại lý thuyết: 3.3219 bits).
- **Hệ số cân bằng (Balance Ratio)**: 99.94% (Tập dữ liệu gần như cân bằng hoàn hảo, không xảy ra hiện tượng mất cân bằng lớp cực đoan - class imbalance).
- **Lớp có số mẫu nhiều nhất**: Lớp 1 (6,742 mẫu trong tập Train, chiếm 11.24%).
- **Lớp có số mẫu ít nhất**: Lớp 5 (5,421 mẫu trong tập Train, chiếm 9.04%).

### 3. Thông số kỹ thuật không gian đặc trưng
- **Độ phân giải ảnh**: $28 \times 28$ điểm ảnh.
- **Số kênh màu**: 1 kênh (Ảnh mức xám - Grayscale).
- **Số chiều vector sau phẳng hóa**: $784$ chiều ($28 \times 28$).
- **Miền giá trị pixel gốc**: Số nguyên $[0, 255]$ ($	ext{uint8}$).
- **Miền giá trị sau chuẩn hóa Min-Max**: Số thực $[0.0, 1.0]$ ($	ext{float32}$).
