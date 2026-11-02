"""
Script đồng bộ hóa Hyperparameter thắng Validation với Artifacts trong saved_models/.
Tập con 10,000 mẫu train:
- Linear SVM: C=0.01 (thắng validation với Val Acc 90.36%) -> saved_models/svm_linear_sub10k.joblib
- Random Forest: n_estimators=150 (thắng validation với Val Acc 95.07%) -> saved_models/rf_sub10k.joblib
"""
import sys
import time
import json
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import joblib
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import RANDOM_STATE, MODELS_DIR
from src.data_loader import create_train_val_test, get_stratified_subset

def align_checkpoints():
    print("=" * 70)
    print("ĐỒNG BỘ CHECKPOINTS LINEAR SVM VÀ RANDOM FOREST THEO SIÊU THAM SỐ THẮNG")
    print("=" * 70)

    (x_train_50k, y_train_50k, x_val_10k, y_val_10k, x_test_10k, y_test_10k) = create_train_val_test(
        val_samples=10000, random_state=RANDOM_STATE, normalize=True, flatten=False
    )
    x_sub_2d, y_sub = get_stratified_subset(x_train_50k, y_train_50k, samples_per_class=1000, random_state=RANDOM_STATE)
    x_sub_flat = x_sub_2d.reshape(10000, -1)
    x_test_flat = x_test_10k.reshape(10000, -1)

    # 1. Linear SVM C=0.01
    print("\n1. Huấn luyện Linear SVM với C=0.01 (thắng validation)...")
    t0 = time.perf_counter()
    lsvc = LinearSVC(C=0.01, max_iter=2000, random_state=RANDOM_STATE)
    lsvc.fit(x_sub_flat, y_sub)
    train_time_lsvc = time.perf_counter() - t0

    t_infer0 = time.perf_counter()
    pred_lsvc = lsvc.predict(x_test_flat)
    infer_time_lsvc = time.perf_counter() - t_infer0
    latency_lsvc = (infer_time_lsvc / len(y_test_10k)) * 1000.0

    acc_lsvc = float(accuracy_score(y_test_10k, pred_lsvc))
    f1_lsvc = float(f1_score(y_test_10k, pred_lsvc, average="macro"))
    err_lsvc = int((pred_lsvc != y_test_10k).sum())

    save_path_lsvc = MODELS_DIR / "svm_linear_sub10k.joblib"
    joblib.dump(lsvc, save_path_lsvc)
    size_lsvc = save_path_lsvc.stat().st_size / (1024 * 1024)

    print(f"   [OK] Đã lưu: {save_path_lsvc}")
    print(f"   Params: {lsvc.get_params()['C']}")
    print(f"   Test Acc: {acc_lsvc*100:.2f}%, Macro F1: {f1_lsvc*100:.2f}%, Lỗi: {err_lsvc}/10000")
    print(f"   Train time: {train_time_lsvc:.2f}s, Latency: {latency_lsvc:.4f}ms, Size: {size_lsvc:.2f}MB")

    # 2. Random Forest n_estimators=150
    print("\n2. Huấn luyện Random Forest với n_estimators=150 (thắng validation)...")
    t0 = time.perf_counter()
    rf = RandomForestClassifier(n_estimators=150, max_features="sqrt", random_state=RANDOM_STATE, n_jobs=-1)
    rf.fit(x_sub_flat, y_sub)
    train_time_rf = time.perf_counter() - t0

    t_infer0 = time.perf_counter()
    pred_rf = rf.predict(x_test_flat)
    infer_time_rf = time.perf_counter() - t_infer0
    latency_rf = (infer_time_rf / len(y_test_10k)) * 1000.0

    acc_rf = float(accuracy_score(y_test_10k, pred_rf))
    f1_rf = float(f1_score(y_test_10k, pred_rf, average="macro"))
    err_rf = int((pred_rf != y_test_10k).sum())

    save_path_rf = MODELS_DIR / "rf_sub10k.joblib"
    joblib.dump(rf, save_path_rf)
    size_rf = save_path_rf.stat().st_size / (1024 * 1024)

    print(f"   [OK] Đã lưu: {save_path_rf}")
    print(f"   Params: n_estimators={rf.get_params()['n_estimators']}")
    print(f"   Test Acc: {acc_rf*100:.2f}%, Macro F1: {f1_rf*100:.2f}%, Lỗi: {err_rf}/10000")
    print(f"   Train time: {train_time_rf:.2f}s, Latency: {latency_rf:.4f}ms, Size: {size_rf:.2f}MB")

    # 3. Cập nhật verified_experiments.json
    results_path = RESULTS_DIR / "verified_experiments.json"
    with open(results_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    for rec in records:
        if rec.get("id") == "EXP-B04":
            rec["model_name"] = "Linear SVM (C=0.01)"
            rec["hyperparameters"] = {"C": 0.01}
            rec["test_accuracy"] = round(acc_lsvc * 100, 2)
            rec["test_macro_f1"] = round(f1_lsvc * 100, 2)
            rec["test_errors"] = err_lsvc
            rec["train_time_sec"] = round(train_time_lsvc, 2)
            rec["inference_latency_ms"] = round(latency_lsvc, 3)
            rec["model_size_mb"] = round(size_lsvc, 2)
        elif rec.get("id") == "EXP-B02":
            rec["model_name"] = "Random Forest (150 cây)"
            rec["hyperparameters"] = {"n_estimators": 150}
            rec["test_accuracy"] = round(acc_rf * 100, 2)
            rec["test_macro_f1"] = round(f1_rf * 100, 2)
            rec["test_errors"] = err_rf
            rec["train_time_sec"] = round(train_time_rf, 2)
            rec["inference_latency_ms"] = round(latency_rf, 3)
            rec["model_size_mb"] = round(size_rf, 2)

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Đã cập nhật verified_experiments.json cho EXP-B04 và EXP-B02.")

if __name__ == "__main__":
    align_checkpoints()
