"""Đánh giá lại checkpoint và xuất bảng, hình từ cùng một bộ dự đoán.

Chạy tại thư mục gốc: python -m src.verify_saved_results
Không huấn luyện lại hoặc ghi đè checkpoint.
"""
import csv
import hashlib
import json
import platform
import time
from pathlib import Path

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import torch

from src.config import BASE_DIR, FIGURES_DIR, MODELS_DIR, NPZ_DATA_PATH, TABLES_DIR
from src.evaluate import evaluate_predictions, plot_confusion_matrix_heatmap, plot_misclassified_gallery
from src.features import deskew_dataset, extract_hog_features
from src.models import ModernCNN

RESULTS_DIR = BASE_DIR / 'results'


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')



def plot_saved_pca_variance():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for name, label in [("pca_transformer.joblib", "Ảnh thô 60k"),
                        ("pca_transformer_sub10k.joblib", "Ảnh thô 10k"),
                        ("pca_transformer_deskew_sub10k.joblib", "Deskew 10k")]:
        transformer = joblib.load(MODELS_DIR / name)
        ratio = np.cumsum(transformer.explained_variance_ratio_) * 100
        dims = transformer.n_components_
        ax.plot(np.arange(1, dims + 1), ratio, label=f"{label}: {dims} chiều")
        ax.scatter([dims], [ratio[-1]], s=22)
    ax.axhline(95, color="gray", linestyle="--", linewidth=1, label="95% phương sai")
    ax.set(xlabel="Số thành phần chính", ylabel="Phương sai tích lũy (%)", ylim=(35, 100),
           title="PCA từ các bộ biến đổi đã huấn luyện")
    ax.grid(alpha=0.2); ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout(); fig.savefig(FIGURES_DIR / "05_pca_variance_curve.png", dpi=220); plt.close(fig)

def main():
    torch.set_num_threads(2)
    plot_saved_pca_variance()
    records = json.loads((RESULTS_DIR / 'verified_experiments.json').read_text(encoding='utf-8'))
    if not any(r['id'] == 'EXP-C03-VAL' for r in records):
        hist = json.loads((RESULTS_DIR / 'cnn_validation_history.json').read_text())
        records.append({
            'id': 'EXP-C03-VAL', 'tier': 'Validation protocol (50,000 train + 10,000 val)',
            'group': 'Nhóm C: Deep Learning', 'model_name': 'Modern CNN (Validation)',
            'feature_config': 'Learned Conv Features (28x28)', 'feature_dims': 784,
            'train_samples': 50000, 'val_samples': 10000, 'test_samples': 10000,
            'random_seed': 42, 'hyperparameters': {'optimizer': 'Adam', 'lr': 0.001,
            'weight_decay': 0.0001, 'batch_size': 64, 'best_epoch': hist['best_epoch'],
            'epochs_run': hist['epochs_run'], 'checkpoint_selection': 'min validation loss'},
            'checkpoint_path': 'saved_models/modern_cnn_val_tuned.pt',
            'train_time_sec': None, 'inference_latency_ms': None,
        })
    data = np.load(NPZ_DATA_PATH)
    images = data['x_test'].astype(np.float32) / 255.0
    labels = data['y_test']
    flat = images.reshape(len(images), -1)
    cache = {'raw': flat}
    predictions = {'y_true': labels}
    details, benchmark = {}, []
    for record in records:
        exp_id = record['id']
        path = BASE_DIR / record['checkpoint_path']
        if path.suffix == '.pt':
            model = ModernCNN()
            model.load_state_dict(torch.load(path, map_location='cpu', weights_only=True))
            features = images
            record['val_samples'] = 10000 if exp_id == 'EXP-C03-VAL' else 0
            record['checkpoint_selection'] = 'min validation loss' if exp_id == 'EXP-C03-VAL' else 'fixed epochs'
        else:
            model = joblib.load(path)
            if 'pipeline' in path.name:
                features = flat
            elif 'deskew' in path.name:
                if 'deskew' not in cache:
                    cache['deskew'] = deskew_dataset(flat)
                features = cache['deskew']
                if 'pca' in path.name:
                    features = joblib.load(MODELS_DIR / 'pca_transformer_deskew_sub10k.joblib').transform(features)
            elif 'hog' in path.name:
                if 'hog' not in cache:
                    cache['hog'] = extract_hog_features(images)
                features = cache['hog']
            elif 'pca' in path.name:
                key = 'pca_full' if record['train_samples'] == 60000 else 'pca_sub'
                if key not in cache:
                    name = 'pca_transformer.joblib' if key == 'pca_full' else 'pca_transformer_sub10k.joblib'
                    cache[key] = joblib.load(MODELS_DIR / name).transform(flat)
                features = cache[key]
            else:
                features = flat
            if record['train_samples'] == 60000:
                record['val_samples'] = 0
        start = time.perf_counter()
        pred = model.predict(features)
        elapsed = time.perf_counter() - start
        metrics = evaluate_predictions(labels, pred, record['model_name'])
        errors = int((labels != pred).sum())
        record.update(test_accuracy=round(metrics['accuracy'] * 100, 2),
                      test_macro_f1=round(metrics['macro_f1'] * 100, 2),
                      test_errors=errors, model_size_mb=round(path.stat().st_size / (1024 ** 2), 2),
                      status='VERIFIED', validation_evidence='results/checkpoint_evaluation.json')
        metrics['errors_per_class'] = (np.asarray(metrics['support']) - np.diag(metrics['confusion_matrix'])).tolist()
        metrics['checkpoint_path'] = record['checkpoint_path']
        metrics['checkpoint_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        metrics['test_errors'] = errors
        metrics['evaluation_batch_total_sec'] = round(elapsed, 4)
        details[exp_id] = metrics
        predictions[exp_id] = np.asarray(pred, dtype=np.uint8)
        benchmark.append({
            'id': exp_id, 'group': record['group'], 'model_name': record['model_name'],
            'feature_type': record['feature_config'], 'feature_dims': record['feature_dims'],
            'train_samples': record['train_samples'], 'val_samples': record['val_samples'],
            'accuracy': record['test_accuracy'], 'macro_precision': round(metrics['macro_precision'] * 100, 2),
            'macro_recall': round(metrics['macro_recall'] * 100, 2), 'macro_f1': record['test_macro_f1'],
            'test_errors': errors, 'train_time_sec': record.get('train_time_sec'),
            'inference_latency_ms': record.get('inference_latency_ms'),
            'latency_definition': 'historical batched prediction time divided by sample count',
            'model_size_mb': record['model_size_mb'], 'checkpoint_path': record['checkpoint_path'],
        })
        if exp_id in {'EXP-C01', 'EXP-A01', 'EXP-B02', 'EXP-B04'}:
            stem = {'EXP-C01': 'modern_cnn_full_60k', 'EXP-A01': 'svm_rbf_deskew_pca_sub10k',
                    'EXP-B02': 'rf_sub10k', 'EXP-B04': 'svm_linear_sub10k'}[exp_id]
            title = f"{record['model_name']} | {record['feature_config']}"
            plot_confusion_matrix_heatmap(labels, pred, title, FIGURES_DIR / f'cm_{stem}.png')
            plot_misclassified_gallery(images, labels, pred, model_name=title,
                                       save_path=FIGURES_DIR / f'errors_{stem}.png', num_samples=12)
        print(f"{exp_id}: {record['test_accuracy']:.2f}% | errors={errors}", flush=True)
        write_json(RESULTS_DIR / 'checkpoint_evaluation.json', details)
    write_json(RESULTS_DIR / 'verified_experiments.json', records)
    write_json(TABLES_DIR / 'benchmark_results.json', benchmark)
    np.savez_compressed(RESULTS_DIR / 'test_predictions.npz', **predictions)
    with (TABLES_DIR / 'per_class_cnn.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['class', 'support', 'precision', 'recall', 'f1', 'errors'])
        m = details['EXP-C01']
        for i in range(10):
            writer.writerow([i, m['support'][i], m['precision_per_class'][i], m['recall_per_class'][i], m['f1_per_class'][i], m['errors_per_class'][i]])
    cnn_pred = predictions['EXP-C01']
    right = [int(np.flatnonzero((labels == i) & (cnn_pred == i))[0]) for i in range(10)]
    wrong = np.flatnonzero(labels != cnn_pred).tolist()
    with (TABLES_DIR / 'cnn_error_samples.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream); writer.writerow(['test_index_zero_based', 'true_label', 'predicted_label'])
        writer.writerows((i, int(labels[i]), int(cnn_pred[i])) for i in wrong)
    fig, axes = plt.subplots(2, 5, figsize=(9, 4.1))
    for ax, idx in zip(axes.flat, right):
        ax.imshow(images[idx], cmap='gray'); ax.axis('off')
        ax.set_title(f'#{idx}: {labels[idx]} → {cnn_pred[idx]}', fontsize=11)
    fig.tight_layout(); fig.savefig(FIGURES_DIR / 'correct_modern_cnn.png', dpi=180); plt.close(fig)
    write_json(RESULTS_DIR / 'evaluation_environment.json', {
        'python': platform.python_version(), 'platform': platform.platform(),
        'sklearn': sklearn.__version__, 'torch': torch.__version__, 'numpy': np.__version__,
        'test_samples': len(labels), 'checkpoint_count': len(records),
        'test_prediction_path': 'results/test_predictions.npz', 'sample_index_base': 0,
    })
    write_json(RESULTS_DIR / 'cnn_report_examples.json', {'correct_indices': right, 'error_indices': wrong[:12]})
    lines = ['# Kết quả đánh giá checkpoint', '',
             'Tập kiểm thử gồm 10.000 ảnh MNIST. Độ trễ lịch sử theo lô được lưu riêng với phép đo từng ảnh trong results/latency_benchmark_detailed.json.', '']
    for size in (10000, 50000, 60000):
        lines += [f'## Tập huấn luyện {size:,} mẫu', '', '| Mô hình | Đặc trưng | Accuracy | Macro F1 | Số ảnh sai |', '|---|---|---:|---:|---:|']
        for r in sorted((r for r in records if r['train_samples'] == size), key=lambda r: -r['test_accuracy']):
            lines.append(f"| {r['model_name']} | {r['feature_config']} | {r['test_accuracy']:.2f}% | {r['test_macro_f1']:.2f}% | {r['test_errors']} |")
        lines.append('')
    (TABLES_DIR / 'benchmark_results.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
