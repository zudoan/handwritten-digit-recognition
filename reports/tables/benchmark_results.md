# Bảng đối chuẩn kết quả các mô hình học máy (10.000 ảnh MNIST Test Set)

| Xếp hạng | Mô hình | Không gian đặc trưng | Tập huấn luyện | Accuracy | Macro F1 | Số ảnh sai / 10k | Độ trễ suy luận |
|:---:|---|---|---|:---:|:---:|:---:|:---:|
| **#1** | **Modern CNN** | Learned Conv (28×28) | 50k train / 10k val | **99.42%** | **99.42%** | **58** | 8.85 ms |
| **#2** | **SVM** | Deskewed + PCA 95% (113D) | 50.000 mẫu | **98.79%** | **98.78%** | **121** | 20.03 ms |
| **#3** | **k-NN** | Deskewed + PCA 95% (113D) | 50.000 mẫu | **98.06%** | **98.05%** | **194** | 63.38 ms |
| **#4** | **Random Forest** | Raw Pixels (784D) | 50.000 mẫu | **96.99%** | **96.97%** | **301** | 56.72 ms |
| **#5** | **Bernoulli Naive Bayes** | Binarized Pixels (784D, bin=0.2) | 50.000 mẫu | **84.46%** | **84.27%** | **1.554** | 1.66 ms |
