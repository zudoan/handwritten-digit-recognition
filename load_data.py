"""
Module hỗ trợ tải và xử lý dữ liệu MNIST
Bộ môn: Nhận dạng mẫu
"""

import os
import sys
import gzip
import struct
import numpy as np
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")


def load_mnist_npz(path=None):
    """
    Tải dữ liệu MNIST từ tệp mnist.npz (nhanh, chuẩn TensorFlow / Keras).
    
    Returns:
        (x_train, y_train), (x_test, y_test)
        - x_train: ndarray shape (60000, 28, 28), uint8 (0-255)
        - y_train: ndarray shape (60000,), uint8 (0-9)
        - x_test:  ndarray shape (10000, 28, 28), uint8 (0-255)
        - y_test:  ndarray shape (10000,), uint8 (0-9)
    """
    if path is None:
        path = os.path.join(DATA_DIR, "mnist.npz")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy tệp {path}. Hãy chạy `python download_mnist.py` trước.")

    with np.load(path) as data:
        x_train, y_train = data["x_train"], data["y_train"]
        x_test, y_test = data["x_test"], data["y_test"]

    return (x_train, y_train), (x_test, y_test)


def load_mnist_raw(raw_dir=None):
    """
    Đọc trực tiếp từ các tệp nhị phân IDX raw (chuẩn gốc của Yann LeCun / TFDS).
    
    Returns:
        (x_train, y_train), (x_test, y_test)
    """
    if raw_dir is None:
        raw_dir = RAW_DIR

    def read_idx_images(filename):
        path = os.path.join(raw_dir, filename)
        open_fn = gzip.open if filename.endswith(".gz") else open
        with open_fn(path, "rb") as f:
            magic, num_images, rows, cols = struct.unpack(">IIII", f.read(16))
            if magic != 2051:
                raise ValueError(f"Magic number không hợp lệ ({magic}) trong {filename}")
            images = np.frombuffer(f.read(), dtype=np.uint8)
            return images.reshape(num_images, rows, cols)

    def read_idx_labels(filename):
        path = os.path.join(raw_dir, filename)
        open_fn = gzip.open if filename.endswith(".gz") else open
        with open_fn(path, "rb") as f:
            magic, num_labels = struct.unpack(">II", f.read(8))
            if magic != 2049:
                raise ValueError(f"Magic number không hợp lệ ({magic}) trong {filename}")
            labels = np.frombuffer(f.read(), dtype=np.uint8)
            return labels

    # Đọc từ file đã giải nén nếu có, nếu không thì đọc trực tiếp từ .gz
    train_img_file = "train-images-idx3-ubyte" if os.path.exists(os.path.join(raw_dir, "train-images-idx3-ubyte")) else "train-images-idx3-ubyte.gz"
    train_lbl_file = "train-labels-idx1-ubyte" if os.path.exists(os.path.join(raw_dir, "train-labels-idx1-ubyte")) else "train-labels-idx1-ubyte.gz"
    test_img_file = "t10k-images-idx3-ubyte" if os.path.exists(os.path.join(raw_dir, "t10k-images-idx3-ubyte")) else "t10k-images-idx3-ubyte.gz"
    test_lbl_file = "t10k-labels-idx1-ubyte" if os.path.exists(os.path.join(raw_dir, "t10k-labels-idx1-ubyte")) else "t10k-labels-idx1-ubyte.gz"

    x_train = read_idx_images(train_img_file)
    y_train = read_idx_labels(train_lbl_file)
    x_test = read_idx_images(test_img_file)
    y_test = read_idx_labels(test_lbl_file)

    return (x_train, y_train), (x_test, y_test)


def show_samples(x, y, num_samples=10, title="MNIST Samples"):
    """
    Hiển thị trực quan một số ảnh mẫu.
    """
    fig, axes = plt.subplots(1, num_samples, figsize=(1.5 * num_samples, 2))
    for i in range(num_samples):
        axes[i].imshow(x[i], cmap="gray")
        axes[i].set_title(f"{y[i]}")
        axes[i].axis("off")
    fig.suptitle(title)
    plt.show()


if __name__ == "__main__":
    print("Đang kiểm tra hàm đọc dữ liệu load_mnist_npz()...")
    (x_train, y_train), (x_test, y_test) = load_mnist_npz()
    print(f"NPZ: x_train: {x_train.shape}, y_train: {y_train.shape}")
    print(f"NPZ: x_test : {x_test.shape}, y_test : {y_test.shape}")

    print("\nĐang kiểm tra hàm đọc trực tiếp từ file thô load_mnist_raw()...")
    (rx_train, ry_train), (rx_test, ry_test) = load_mnist_raw()
    print(f"RAW: x_train: {rx_train.shape}, y_train: {ry_train.shape}")
    print(f"RAW: x_test : {rx_test.shape}, y_test : {ry_test.shape}")

    # So sánh tính chính xác giữa 2 nguồn
    assert np.array_equal(x_train, rx_train), "Dữ liệu ảnh không khớp!"
    assert np.array_equal(y_train, ry_train), "Dữ liệu nhãn không khớp!"
    print("\nKiểm tra đối chiếu 100% khớp dữ liệu hoàn hảo!")
