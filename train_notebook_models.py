"""
Training script replicating the exact pipeline from:
'02_Tien_Xu_Ly_Train_MNIST (3).ipynb'

Saves new models to:
1. mnist_best_models/
2. saved_models/
"""
from pathlib import Path
import urllib.request
import copy
import json
import time
import sys

import cv2
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
CPU_THREADS = 4
thread_limit = threadpool_limits(limits=CPU_THREADS)
torch.set_num_threads(CPU_THREADS)
torch.manual_seed(SEED)
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

OUT = Path('mnist_best_models')
OUT.mkdir(exist_ok=True)
SAVED_MODELS_DIR = Path('saved_models')
SAVED_MODELS_DIR.mkdir(exist_ok=True)

# 1. Nạp dữ liệu
print("=" * 65)
print("1. NẠP DỮ LIỆU MNIST...")
paths = [Path('mnist.npz'), Path('data/mnist.npz'), Path('../data/mnist.npz')]
data_path = next((p for p in paths if p.is_file()), Path('data/mnist.npz'))

if not data_path.exists():
    print(f"Tải MNIST về {data_path}...")
    urllib.request.urlretrieve(
        'https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
        data_path
    )

with np.load(data_path, allow_pickle=False) as data:
    images, labels = (data['x_train'], data['y_train'])
    test_images, test_labels = (data['x_test'], data['y_test'])

assert images.shape == (60000, 28, 28) and test_images.shape == (10000, 28, 28)
assert not np.isnan(images).any() and set(np.unique(labels)) == set(range(10))

x_train, x_val, y_train, y_val = train_test_split(
    images.astype(np.float32) / 255,
    labels,
    test_size=10000,
    stratify=labels,
    random_state=SEED
)
x_test = test_images.astype(np.float32) / 255
a_train, a_val, a_test = [x.reshape(-1, 784) for x in (x_train, x_val, x_test)]

print(f"Train {len(y_train):,} | Validation {len(y_val):,} | Test {len(test_labels):,} | Thiết bị: {DEVICE}")

results, predictions, chosen_params, val_scores = {}, {}, {}, {}

def report_model(name, val_pred, test_pred, params):
    precision, recall, f1, _ = precision_recall_fscore_support(
        test_labels, test_pred, average='macro', zero_division=0
    )
    val_acc = accuracy_score(y_val, val_pred)
    test_acc = accuracy_score(test_labels, test_pred)
    val_scores[name] = val_acc
    wrong = int((test_pred != test_labels).sum())
    
    scores = {
        'Val Acc (%)': val_acc * 100,
        'Test Acc (%)': test_acc * 100,
        'Precision (%)': precision * 100,
        'Recall (%)': recall * 100,
        'F1 (%)': f1 * 100,
        'Số ảnh sai': wrong,
    }
    results[name] = scores
    predictions[name] = test_pred
    chosen_params[name] = params
    
    print(f"[{name}] Val Acc: {val_acc:.2%} | Test Acc: {test_acc:.2%} | F1: {f1:.2%} | Sai: {wrong}/10,000")
    pd.DataFrame.from_dict(results, orient='index').rename_axis('Mô hình').to_csv(OUT / 'results.csv')
    pd.DataFrame.from_dict(results, orient='index').rename_axis('Mô hình').to_csv(SAVED_MODELS_DIR / 'results.csv')

# 2. Tiền xử lý Deskew + PCA
print("\n" + "=" * 65)
print("2. TIỀN XỬ LÝ (DESKEW + PCA 95%)...")

def deskew(batch):
    result = np.empty_like(batch)
    for i, image in enumerate(batch):
        moment = cv2.moments(image)
        skew = moment['mu11'] / moment['mu02'] if abs(moment['mu02']) >= 0.01 else 0
        matrix = np.float32([[1, skew, -14 * skew], [0, 1, 0]])
        result[i] = cv2.warpAffine(image, matrix, (28, 28), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return result.reshape(-1, 784)

t0 = time.time()
deskew_train = deskew(x_train)
deskew_val = deskew(x_val)
deskew_test = deskew(x_test)
print(f"Deskew hoàn tất trong {time.time() - t0:.2f}s")

pca = PCA(n_components=0.95, random_state=SEED)
t0 = time.time()
b_train = pca.fit_transform(deskew_train)
b_val = pca.transform(deskew_val)
b_test = pca.transform(deskew_test)
print(f"PCA hoàn tất trong {time.time() - t0:.2f}s: 784 -> {pca.n_components_} chiều.")

joblib.dump(pca, OUT / 'pca.joblib', compress=3)
joblib.dump(pca, SAVED_MODELS_DIR / 'pca.joblib', compress=3)

# 3. Naive Bayes
print("\n" + "=" * 65)
print("3. HUẤN LUYỆN NAIVE BAYES...")
t0 = time.time()
nb = BernoulliNB(alpha=1.0, binarize=0.2)
nb.fit(a_train, y_train)
print(f"Fit Naive Bayes trong {time.time() - t0:.2f}s")
joblib.dump(nb, OUT / 'Naive_Bayes.joblib', compress=3)
joblib.dump(nb, SAVED_MODELS_DIR / 'Naive_Bayes.joblib', compress=3)
report_model('Naive Bayes', nb.predict(a_val), nb.predict(a_test),
             'BernoulliNB, alpha=1.0, binarize=0.2')

# 4. k-NN
print("\n" + "=" * 65)
print("4. HUẤN LUYỆN k-NN (k=3, Deskew + PCA)...")
t0 = time.time()
knn = KNeighborsClassifier(n_neighbors=3, weights='distance', n_jobs=CPU_THREADS)
knn.fit(b_train, y_train)
print(f"Fit k-NN trong {time.time() - t0:.2f}s. Đang dự đoán val & test...")
joblib.dump(knn, OUT / 'k-NN.joblib', compress=3)
joblib.dump(knn, SAVED_MODELS_DIR / 'k-NN.joblib', compress=3)
report_model('k-NN', knn.predict(b_val), knn.predict(b_test),
             'k=3, weights=distance, Deskew + PCA 95%')

# 5. SVM
print("\n" + "=" * 65)
print("5. HUẤN LUYỆN SVM RBF (C=5, Deskew + PCA)...")
t0 = time.time()
svm = SVC(C=5, kernel='rbf', gamma='scale', cache_size=512)
svm.fit(b_train, y_train)
print(f"Fit SVM trong {time.time() - t0:.2f}s. Đang dự đoán val & test...")
joblib.dump(svm, OUT / 'SVM.joblib', compress=3)
joblib.dump(svm, SAVED_MODELS_DIR / 'SVM.joblib', compress=3)
report_model('SVM', svm.predict(b_val), svm.predict(b_test),
             'kernel=rbf, C=5, gamma=scale, Deskew + PCA 95%')

# 6. Random Forest
print("\n" + "=" * 65)
print("6. HUẤN LUYỆN RANDOM FOREST (150 cây, Raw pixels)...")
t0 = time.time()
rf = RandomForestClassifier(n_estimators=150, max_features='sqrt',
                            random_state=SEED, n_jobs=CPU_THREADS)
rf.fit(a_train, y_train)
print(f"Fit Random Forest trong {time.time() - t0:.2f}s")
joblib.dump(rf, OUT / 'Random_Forest.joblib', compress=3)
joblib.dump(rf, SAVED_MODELS_DIR / 'Random_Forest.joblib', compress=3)
report_model('Random Forest', rf.predict(a_val), rf.predict(a_test),
             'n_estimators=150, max_features=sqrt, max_depth=None, random_state=42')

# 7. Modern CNN
print("\n" + "=" * 65)
print("7. HUẤN LUYỆN MODERN CNN...")

def make_loader(x, y, batch_size, shuffle=False):
    dataset = TensorDataset(torch.from_numpy(x).unsqueeze(1), torch.from_numpy(y).long())
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

def run_epoch(loader, training, cnn_model, criterion, optimizer):
    cnn_model.train(training)
    total_loss, correct, total = 0.0, 0, 0
    with torch.set_grad_enabled(training):
        for x, y in loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            if training:
                optimizer.zero_grad()
            logits = cnn_model(x)
            loss = criterion(logits, y)
            if training:
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * len(y)
            correct += (logits.argmax(1) == y).sum().item()
            total += len(y)
    return total_loss / total, correct / total

INITIAL_EPOCHS, EXTEND_EPOCHS = 70, 20
PATIENCE, MIN_DELTA = 3, 1e-4
torch.manual_seed(SEED)

cnn_model = nn.Sequential(
    nn.Conv2d(1, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(64, 128, 3), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten(),
    nn.Dropout(0.4), nn.Linear(512, 128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128, 10),
).to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(cnn_model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=1, threshold=MIN_DELTA,
    threshold_mode='abs', min_lr=1e-5
)

train_loader = make_loader(x_train, y_train, 64, shuffle=True)
val_loader = make_loader(x_val, y_val, 256)
print(f"CNN: {sum(p.numel() for p in cnn_model.parameters()):,} tham số | Giới hạn ban đầu: {INITIAL_EPOCHS} epoch")

history, best_loss, stop_loss, wait = [], float('inf'), float('inf'), 0
epoch, epoch_limit = 0, INITIAL_EPOCHS

while True:
    if epoch >= epoch_limit:
        epoch_limit += EXTEND_EPOCHS
        print(f"Tăng giới hạn lên {epoch_limit} epoch.")
    epoch += 1
    lr = optimizer.param_groups[0]['lr']
    train_loss, train_acc = run_epoch(train_loader, True, cnn_model, criterion, optimizer)
    val_loss, val_acc = run_epoch(val_loader, False, cnn_model, criterion, optimizer)
    scheduler.step(val_loss)
    history.append({
        'epoch': epoch, 'lr': lr, 'train_loss': train_loss,
        'val_loss': val_loss, 'train_acc': train_acc, 'val_acc': val_acc
    })
    print(f"Epoch {epoch:02d}/{epoch_limit} | LR {lr:.6f} | train loss {train_loss:.4f}, acc {train_acc:.2%}"
          f" | val loss {val_loss:.4f}, acc {val_acc:.2%}", flush=True)
    
    if val_loss < best_loss:
        best_loss, best_epoch = val_loss, epoch
        best_weights = copy.deepcopy(cnn_model.state_dict())
    if val_loss < stop_loss - MIN_DELTA:
        stop_loss, wait = val_loss, 0
    else:
        wait += 1
        
    pd.DataFrame(history).to_csv(OUT / 'cnn_history.csv', index=False)
    pd.DataFrame(history).to_csv(SAVED_MODELS_DIR / 'cnn_history.csv', index=False)
    
    if wait >= PATIENCE:
        print(f"Early stopping kích hoạt tại epoch {epoch}.")
        break

cnn_model.load_state_dict(best_weights)
cnn_model.eval()

torch.save(best_weights, OUT / 'CNN.pt')
torch.save(best_weights, SAVED_MODELS_DIR / 'CNN.pt')
print(f"Đã khôi phục checkpoint epoch {best_epoch}, validation loss {best_loss:.4f}.")

val_pred, test_pred = [], []
with torch.no_grad():
    for loader, output in [(val_loader, val_pred), (make_loader(x_test, test_labels, 256), test_pred)]:
        for x, _ in loader:
            output.append(cnn_model(x.to(DEVICE)).argmax(1).cpu().numpy())

report_model('CNN', np.concatenate(val_pred), np.concatenate(test_pred),
             f'Adam, LR đầu=0.001, weight_decay=0.0001, batch=64, checkpoint epoch {best_epoch}')

# 8. Lưu cấu hình & dự đoán tổng hợp
np.savez_compressed(OUT / 'predictions.npz', y_true=test_labels, **predictions)
np.savez_compressed(SAVED_MODELS_DIR / 'predictions.npz', y_true=test_labels, **predictions)

config = {
    'seed': SEED, 'train': 50000, 'validation': 10000, 'test': 10000,
    'parameters': chosen_params, 'cnn_best_epoch': best_epoch, 'cnn_best_val_loss': best_loss,
    'cnn_initial_epoch_limit': INITIAL_EPOCHS, 'cnn_final_epoch_limit': epoch_limit,
    'cnn_extend_epochs': EXTEND_EPOCHS, 'cnn_epochs_run': epoch,
    'cnn_stop_reason': 'early_stopping', 'cnn_early_stopping_patience': PATIENCE,
    'cnn_min_delta': MIN_DELTA, 'cnn_initial_lr': 0.001,
    'cnn_scheduler_factor': 0.5, 'cnn_scheduler_patience': 1, 'cnn_min_lr': 1e-5,
    'selected_by_validation': max(val_scores, key=val_scores.get),
}
(OUT / 'selected_config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
(SAVED_MODELS_DIR / 'selected_config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')

print("\n" + "=" * 65)
print("TỔNG HỢP KẾT QUẢ THỰC NGHIỆM ĐÃ LƯU:")
comparison = pd.DataFrame.from_dict(results, orient='index').rename_axis('Mô hình')
columns = ['Test Acc (%)', 'Precision (%)', 'Recall (%)', 'F1 (%)', 'Số ảnh sai']
print(comparison[columns].round(2))
print("=" * 65)
print("HOÀN TẤT HUẤN LUYỆN TOÀN BỘ 5 MÔ HÌNH CHUẨN!")

