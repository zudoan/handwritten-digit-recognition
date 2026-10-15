import os
import sys
import gzip
import shutil
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# 1. Official raw files from Google CVDF mirror (used by tensorflow_datasets)
RAW_FILES = {
    "train-images-idx3-ubyte.gz": "https://storage.googleapis.com/cvdf-datasets/mnist/train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz": "https://storage.googleapis.com/cvdf-datasets/mnist/train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz": "https://storage.googleapis.com/cvdf-datasets/mnist/t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz": "https://storage.googleapis.com/cvdf-datasets/mnist/t10k-labels-idx1-ubyte.gz",
}

# 2. Pre-packaged numpy format from Google storage (TensorFlow / Keras standard)
NPZ_URL = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"
NPZ_PATH = os.path.join(DATA_DIR, "mnist.npz")


def download_file(url, target_path):
    print(f"Đang tải: {url} -> {target_path}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response, open(target_path, "wb") as out_file:
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 1024 * 64
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = downloaded / total_size * 100
                print(f"\r  Tiến độ: {downloaded}/{total_size} bytes ({percent:.1f}%)", end="")
    print("\n  Hoàn thành!")


def extract_gzip(gz_path, out_path):
    print(f"Giải nén: {gz_path} -> {out_path}...")
    with gzip.open(gz_path, "rb") as f_in, open(out_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def main():
    print("=== BẮT ĐẦU TẢI DỮ LIỆU TENSORFLOW MNIST ===")
    
    # Tải mnist.npz
    if not os.path.exists(NPZ_PATH):
        download_file(NPZ_URL, NPZ_PATH)
    else:
        print(f"Tệp {NPZ_PATH} đã tồn tại.")

    # Tải các tệp raw gz và giải nén
    for filename, url in RAW_FILES.items():
        gz_path = os.path.join(RAW_DIR, filename)
        if not os.path.exists(gz_path):
            download_file(url, gz_path)
        else:
            print(f"Tệp {gz_path} đã tồn tại.")
        
        # Giải nén ra tệp ubyte
        uncompressed_filename = filename.replace(".gz", "")
        uncompressed_path = os.path.join(RAW_DIR, uncompressed_filename)
        if not os.path.exists(uncompressed_path):
            extract_gzip(gz_path, uncompressed_path)

    # Kiểm tra dữ liệu
    print("\n=== KIỂM TRA DỮ LIỆU ĐÃ TẢI ===")
    data = np.load(NPZ_PATH)
    x_train, y_train = data["x_train"], data["y_train"]
    x_test, y_test = data["x_test"], data["y_test"]
    print(f"Tập huấn luyện (x_train): {x_train.shape}, nhãn (y_train): {y_train.shape}")
    print(f"Tập kiểm thử   (x_test) : {x_test.shape}, nhãn (y_test) : {y_test.shape}")
    print(f"Giá trị pixel: min={x_train.min()}, max={x_train.max()}, kiểu={x_train.dtype}")

    # Tạo ảnh minh họa mẫu dữ liệu
    fig, axes = plt.subplots(2, 5, figsize=(10, 4))
    fig.suptitle("Mẫu dữ liệu chữ số viết tay MNIST (TensorFlow Dataset)", fontsize=14)
    for i in range(10):
        row, col = i // 5, i % 5
        axes[row, col].imshow(x_train[i], cmap="gray")
        axes[row, col].set_title(f"Nhãn: {y_train[i]}")
        axes[row, col].axis("off")
    plt.tight_layout()
    preview_path = os.path.join(DATA_DIR, "mnist_samples.png")
    plt.savefig(preview_path, dpi=150)
    print(f"Đã lưu ảnh mẫu kiểm tra tại: {preview_path}")
    print("=== TẢI VÀ KIỂM TRA DỮ LIỆU THÀNH CÔNG ===")


if __name__ == "__main__":
    main()
