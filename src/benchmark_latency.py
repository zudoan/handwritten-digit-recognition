"""
Đo đạc và Đối chuẩn Độ trễ Suy luận (Latency Benchmark) Chuẩn mực Khoa học.
Phân biệt rành mạch:
1. Single-image Latency (batch_size=1) với 50 lần warm-up + 500 lần đo thực tế (Mean, Median, P95, Std).
2. Batched Inference Latency (trên toàn bộ 10,000 mẫu kiểm thử).
3. Pipeline Latency (Bao gồm tiền xử lý/trích xuất đặc trưng + suy luận mô hình).
Ghi rõ cấu hình phần cứng và phiên bản thư viện.
Lưu kết quả ra results/latency_benchmark_detailed.json.
"""
import sys
import time
import json
import platform
from pathlib import Path
import numpy as np
import joblib
import torch

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

RESULTS_DIR = BASE_DIR / "results"
MODELS_DIR = BASE_DIR / "saved_models"
DATA_PATH = BASE_DIR / "data" / "mnist.npz"

import sklearn
from src.models import ModernCNN

def run_latency_benchmark():
    print("=" * 75)
    print("CHƯƠNG TRÌNH ĐO ĐẠC ĐỘ TRỄ SUY LUẬN TOÀN DIỆN (BENCHMARK LATENCY)")
    print("=" * 75)

    env_info = {
        "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "processor": platform.processor(),
        "cpu": platform.processor(),
        "python_version": platform.python_version(),
        "sklearn_version": sklearn.__version__,
        "joblib_version": joblib.__version__,
        "torch_version": torch.__version__,
        "numpy_version": np.__version__,
        "device": "cpu",
        "batch_size": 1,
        "batched_eval_size": 10000,
        "measurement_method": "Single-image (50 warmups + 500 timed runs) & Batched throughput (10,000 samples)"
    }
    print("Môi trường:", env_info)

    with np.load(DATA_PATH) as data:
        x_test_raw = data["x_test"].astype(np.float32) / 255.0
        y_test = data["y_test"]

    x_test_flat = x_test_raw.reshape(-1, 784)
    pca_deskew = joblib.load(MODELS_DIR / "pca_transformer_deskew_sub10k.joblib")
    pca_raw = joblib.load(MODELS_DIR / "pca_transformer.joblib")

    # Danh sách các mô hình cần đo
    models_to_test = [
        {
            "name": "Modern CNN",
            "type": "torch",
            "path": MODELS_DIR / "modern_cnn_mnist.pt",
            "input_shape": "image_28x28",
        },
        {
            "name": "SVM RBF (Deskew + PCA Pipeline)",
            "type": "pipeline",
            "path": MODELS_DIR / "svm_rbf_deskew_pca_pipeline.joblib",
            "input_shape": "flat_784",
        },
        {
            "name": "SVM RBF (PCA 154D)",
            "type": "sklearn_pca",
            "path": MODELS_DIR / "svm_rbf_pca.joblib",
            "pca": pca_raw,
            "input_shape": "flat_784",
        },
        {
            "name": "k-NN (PCA 154D)",
            "type": "sklearn_pca",
            "path": MODELS_DIR / "knn_pca_k3.joblib",
            "pca": pca_raw,
            "input_shape": "flat_784",
        },
        {
            "name": "Random Forest (150 cây)",
            "type": "sklearn_raw",
            "path": MODELS_DIR / "rf_sub10k.joblib",
            "input_shape": "flat_784",
        },
        {
            "name": "Linear SVM (C=0.01)",
            "type": "sklearn_raw",
            "path": MODELS_DIR / "svm_linear_sub10k.joblib",
            "input_shape": "flat_784",
        },
    ]

    benchmark_records = []

    for item in models_to_test:
        m_name = item["name"]
        print(f"\n---> Đang đo độ trễ: {m_name} <---")
        m_type = item["type"]

        if m_type == "torch":
            model = ModernCNN()
            model.load_state_dict(torch.load(item["path"], map_location="cpu"))
            model.eval()

            def predict_single(x_img):
                with torch.no_grad():
                    t = torch.from_numpy(x_img).unsqueeze(0).unsqueeze(0).float()
                    return int(torch.argmax(model(t), dim=1).item())

            def predict_batch(x_imgs):
                with torch.no_grad():
                    t = torch.from_numpy(x_imgs).unsqueeze(1).float()
                    return torch.argmax(model(t), dim=1).numpy()

        elif m_type == "pipeline":
            pipe = joblib.load(item["path"])
            predict_single = lambda x_flat: int(pipe.predict(x_flat.reshape(1, -1))[0])
            predict_batch = lambda x_flats: pipe.predict(x_flats)

        elif m_type == "sklearn_pca":
            clf = joblib.load(item["path"])
            pca_m = item["pca"]
            def predict_single(x_flat):
                feat = pca_m.transform(x_flat.reshape(1, -1))
                return int(clf.predict(feat)[0])
            def predict_batch(x_flats):
                feats = pca_m.transform(x_flats)
                return clf.predict(feats)

        elif m_type == "sklearn_raw":
            clf = joblib.load(item["path"])
            predict_single = lambda x_flat: int(clf.predict(x_flat.reshape(1, -1))[0])
            predict_batch = lambda x_flats: clf.predict(x_flats)

        # 1. Warm-up (50 lần)
        sample = x_test_raw[0] if item["input_shape"] == "image_28x28" else x_test_flat[0]
        for _ in range(50):
            _ = predict_single(sample)

        # 2. Single-image Latency (500 lần đo độc lập)
        single_times_ms = []
        for i in range(500):
            s = x_test_raw[i % 500] if item["input_shape"] == "image_28x28" else x_test_flat[i % 500]
            t0 = time.perf_counter()
            _ = predict_single(s)
            single_times_ms.append((time.perf_counter() - t0) * 1000.0)

        single_mean = float(np.mean(single_times_ms))
        single_median = float(np.median(single_times_ms))
        single_p95 = float(np.percentile(single_times_ms, 95))
        single_std = float(np.std(single_times_ms))

        # 3. Batched Latency trên toàn bộ 10,000 mẫu
        inputs_batch = x_test_raw if item["input_shape"] == "image_28x28" else x_test_flat
        t_batch0 = time.perf_counter()
        _ = predict_batch(inputs_batch)
        batch_total_sec = time.perf_counter() - t_batch0
        batch_avg_ms = (batch_total_sec / len(y_test)) * 1000.0
        throughput = len(y_test) / batch_total_sec

        print(f"  • Single-image Latency (batch=1): Mean = {single_mean:.3f} ms | Median = {single_median:.3f} ms | P95 = {single_p95:.3f} ms (Std: {single_std:.3f})")
        print(f"  • Batched Latency (10k test): Total = {batch_total_sec:.2f} s | Avg = {batch_avg_ms:.4f} ms/ảnh | Throughput = {throughput:.1f} ảnh/s")

        benchmark_records.append({
            "model_name": m_name,
            "single_image_mean_ms": round(single_mean, 3),
            "single_image_median_ms": round(single_median, 3),
            "single_image_p95_ms": round(single_p95, 3),
            "single_image_std_ms": round(single_std, 3),
            "batch_total_sec": round(batch_total_sec, 3),
            "batch_avg_latency_ms": round(batch_avg_ms, 4),
            "throughput_samples_per_sec": round(throughput, 1),
        })

    out_file = RESULTS_DIR / "latency_benchmark_detailed.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"environment": env_info, "benchmarks": benchmark_records}, f, indent=2)
    print(f"\n[OK] Đã lưu kết quả đo đạc độ trễ chi tiết vào: {out_file}")

if __name__ == "__main__":
    run_latency_benchmark()
