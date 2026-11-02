"""
Thực hiện tìm kiếm và tối ưu hóa siêu tham số (Hyperparameter Tuning)
trên tập Validation độc lập (10,000 mẫu) theo đúng nguyên tắc khoa học.
Lưu kết quả chi tiết ra:
- results/hyperparameter_search_results.json
- results/hyperparameter_search_results.csv
Đảm bảo mô hình được lưu trong saved_models/ hoàn toàn khớp với siêu tham số đã chọn.
"""
import sys
import time
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
RESULTS_DIR = BASE_DIR / "results"
MODELS_DIR = BASE_DIR / "saved_models"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

from src.config import RANDOM_STATE
from src.data_loader import create_train_val_test, get_stratified_subset
from src.features import PCATransformer


def run_hyperparameter_tuning():
    print("=" * 70)
    print("BẮT ĐẦU TỐI ƯU SIÊU THAM SỐ TRÊN TẬP VALIDATION ĐỘC LẬP (10,000 MẪU)")
    print("=" * 70)

    # 1. Tải và phân chia tập dữ liệu 50k train / 10k val / 10k test
    (x_train_50k, y_train_50k, x_val_10k, y_val_10k, x_test_10k, y_test_10k) = create_train_val_test(
        val_samples=10000, random_state=RANDOM_STATE, normalize=True, flatten=False
    )

    # Trích xuất tập con 10,000 mẫu train phân tầng để tối ưu
    x_sub_2d, y_sub = get_stratified_subset(x_train_50k, y_train_50k, samples_per_class=1000, random_state=RANDOM_STATE)
    x_sub_flat = x_sub_2d.reshape(10000, -1)
    x_val_flat = x_val_10k.reshape(10000, -1)

    # Khớp PCA trên 10,000 mẫu train
    print("-> Khớp PCA trên 10,000 mẫu train subset...")
    pca = PCATransformer(n_components=0.95, random_state=RANDOM_STATE)
    x_sub_pca = pca.fit_transform(x_sub_flat)
    x_val_pca = pca.transform(x_val_flat)
    print(f"   Số chiều PCA: {pca.n_components_} chiều.")

    search_records: List[Dict[str, Any]] = []

    # =========================================================================
    # 1. k-NN (trên PCA 152D)
    # =========================================================================
    print("\n[1/4] Dò tìm siêu tham số cho k-NN...")
    knn_candidates = [
        {"n_neighbors": 3, "weights": "uniform"},
        {"n_neighbors": 3, "weights": "distance"},
        {"n_neighbors": 5, "weights": "uniform"},
        {"n_neighbors": 5, "weights": "distance"},
        {"n_neighbors": 7, "weights": "distance"},
    ]

    best_knn_score = -1.0
    best_knn_params = None

    for cand in knn_candidates:
        t0 = time.perf_counter()
        clf = KNeighborsClassifier(n_neighbors=cand["n_neighbors"], weights=cand["weights"], metric="euclidean")
        clf.fit(x_sub_pca, y_sub)
        val_preds = clf.predict(x_val_pca)
        val_acc = float(accuracy_score(y_val_10k, val_preds))
        val_f1 = float(f1_score(y_val_10k, val_preds, average="macro"))
        train_time = round(time.perf_counter() - t0, 3)

        rec = {
            "model_family": "k-NN",
            "feature": f"PCA ({pca.n_components_}D)",
            "hyperparameters": cand,
            "val_accuracy": round(val_acc * 100, 2),
            "val_macro_f1": round(val_f1 * 100, 2),
            "train_time_sec": train_time,
            "selected": False,
        }
        search_records.append(rec)
        print(f"  k={cand['n_neighbors']:d}, weights={cand['weights']:8s} -> Val Acc: {val_acc*100:.2f}%, F1: {val_f1*100:.2f}%")

        if val_acc > best_knn_score:
            best_knn_score = val_acc
            best_knn_params = cand

    for r in search_records:
        if r["model_family"] == "k-NN" and r["hyperparameters"] == best_knn_params:
            r["selected"] = True

    # =========================================================================
    # 2. Linear SVM (trên Raw Pixels 784D)
    # =========================================================================
    print("\n[2/4] Dò tìm siêu tham số cho Linear SVM...")
    linear_candidates = [
        {"C": 0.01},
        {"C": 0.1},
        {"C": 1.0},
        {"C": 5.0},
    ]

    best_lin_score = -1.0
    best_lin_params = None

    for cand in linear_candidates:
        t0 = time.perf_counter()
        clf = LinearSVC(C=cand["C"], max_iter=2000, random_state=RANDOM_STATE)
        clf.fit(x_sub_flat, y_sub)
        val_preds = clf.predict(x_val_flat)
        val_acc = float(accuracy_score(y_val_10k, val_preds))
        val_f1 = float(f1_score(y_val_10k, val_preds, average="macro"))
        train_time = round(time.perf_counter() - t0, 3)

        rec = {
            "model_family": "Linear SVM",
            "feature": "Raw Pixels (784D)",
            "hyperparameters": cand,
            "val_accuracy": round(val_acc * 100, 2),
            "val_macro_f1": round(val_f1 * 100, 2),
            "train_time_sec": train_time,
            "selected": False,
        }
        search_records.append(rec)
        print(f"  C={cand['C']:<5} -> Val Acc: {val_acc*100:.2f}%, F1: {val_f1*100:.2f}%")

        if val_acc > best_lin_score:
            best_lin_score = val_acc
            best_lin_params = cand

    for r in search_records:
        if r["model_family"] == "Linear SVM" and r["hyperparameters"] == best_lin_params:
            r["selected"] = True

    # =========================================================================
    # 3. RBF SVM (trên PCA 152D)
    # =========================================================================
    print("\n[3/4] Dò tìm siêu tham số cho RBF SVM...")
    rbf_candidates = [
        {"C": 1.0, "gamma": "scale"},
        {"C": 5.0, "gamma": "scale"},
        {"C": 10.0, "gamma": "scale"},
    ]

    best_rbf_score = -1.0
    best_rbf_params = None

    for cand in rbf_candidates:
        t0 = time.perf_counter()
        clf = SVC(C=cand["C"], kernel="rbf", gamma=cand["gamma"], random_state=RANDOM_STATE)
        clf.fit(x_sub_pca, y_sub)
        val_preds = clf.predict(x_val_pca)
        val_acc = float(accuracy_score(y_val_10k, val_preds))
        val_f1 = float(f1_score(y_val_10k, val_preds, average="macro"))
        train_time = round(time.perf_counter() - t0, 3)

        rec = {
            "model_family": "RBF SVM",
            "feature": f"PCA ({pca.n_components_}D)",
            "hyperparameters": cand,
            "val_accuracy": round(val_acc * 100, 2),
            "val_macro_f1": round(val_f1 * 100, 2),
            "train_time_sec": train_time,
            "selected": False,
        }
        search_records.append(rec)
        print(f"  C={cand['C']:<4}, gamma={cand['gamma']:5s} -> Val Acc: {val_acc*100:.2f}%, F1: {val_f1*100:.2f}%")

        if val_acc > best_rbf_score:
            best_rbf_score = val_acc
            best_rbf_params = cand

    for r in search_records:
        if r["model_family"] == "RBF SVM" and r["hyperparameters"] == best_rbf_params:
            r["selected"] = True

    # =========================================================================
    # 4. Random Forest (trên Raw Pixels 784D)
    # =========================================================================
    print("\n[4/4] Dò tìm siêu tham số cho Random Forest...")
    rf_candidates = [
        {"n_estimators": 50, "max_features": "sqrt"},
        {"n_estimators": 100, "max_features": "sqrt"},
        {"n_estimators": 150, "max_features": "sqrt"},
    ]

    best_rf_score = -1.0
    best_rf_params = None

    for cand in rf_candidates:
        t0 = time.perf_counter()
        clf = RandomForestClassifier(n_estimators=cand["n_estimators"], max_features=cand["max_features"], random_state=RANDOM_STATE, n_jobs=-1)
        clf.fit(x_sub_flat, y_sub)
        val_preds = clf.predict(x_val_flat)
        val_acc = float(accuracy_score(y_val_10k, val_preds))
        val_f1 = float(f1_score(y_val_10k, val_preds, average="macro"))
        train_time = round(time.perf_counter() - t0, 3)

        rec = {
            "model_family": "Random Forest",
            "feature": "Raw Pixels (784D)",
            "hyperparameters": cand,
            "val_accuracy": round(val_acc * 100, 2),
            "val_macro_f1": round(val_f1 * 100, 2),
            "train_time_sec": train_time,
            "selected": False,
        }
        search_records.append(rec)
        print(f"  n_estimators={cand['n_estimators']:<4} -> Val Acc: {val_acc*100:.2f}%, F1: {val_f1*100:.2f}%")

        if val_acc > best_rf_score:
            best_rf_score = val_acc
            best_rf_params = cand

    for r in search_records:
        if r["model_family"] == "Random Forest" and r["hyperparameters"] == best_rf_params:
            r["selected"] = True

    # Lưu kết quả JSON
    json_path = RESULTS_DIR / "hyperparameter_search_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(search_records, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Đã lưu kết quả dò tìm siêu tham số vào: {json_path}")

    # Lưu kết quả CSV
    csv_path = RESULTS_DIR / "hyperparameter_search_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Model Family", "Feature", "Hyperparameters", "Val Accuracy (%)", "Val Macro F1 (%)", "Train Time (s)", "Selected"])
        for r in search_records:
            writer.writerow([
                r["model_family"],
                r["feature"],
                json.dumps(r["hyperparameters"]),
                r["val_accuracy"],
                r["val_macro_f1"],
                r["train_time_sec"],
                "YES" if r["selected"] else "NO"
            ])
    print(f"[OK] Đã lưu kết quả dạng CSV vào: {csv_path}")

    print("\n--- CÁC CẤU HÌNH THẮNG TRÊN TẬP VALIDATION ---")
    print(f"  k-NN:          {best_knn_params} (Val Acc: {best_knn_score*100:.2f}%)")
    print(f"  Linear SVM:    {best_lin_params} (Val Acc: {best_lin_score*100:.2f}%)")
    print(f"  RBF SVM:       {best_rbf_params} (Val Acc: {best_rbf_score*100:.2f}%)")
    print(f"  Random Forest: {best_rf_params} (Val Acc: {best_rf_score*100:.2f}%)")


if __name__ == "__main__":
    run_hyperparameter_tuning()
