"""
Huấn luyện và Đánh giá Mô hình Modern CNN với Quy trình Validation Chuẩn mực.
- Dữ liệu: 50,000 train / 10,000 validation / 10,000 test (Stratified).
- Giao thức: Đo Validation Loss và Validation Accuracy sau mỗi epoch.
- Lựa chọn checkpoint dựa trên Validation Loss thấp nhất (Early Stopping / Best Checkpoint).
- Tuyệt đối KHÔNG sử dụng Test Set để chọn checkpoint.
- Vẽ và lưu biểu đồ: reports/figures/08_cnn_training_history.png.
"""
import sys
import time
import copy
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, f1_score

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import RANDOM_STATE, MODELS_DIR, FIGURES_DIR
from src.data_loader import create_train_val_test
from src.models import ModernCNN
from src.evaluate import evaluate_predictions


def train_cnn_validation_protocol(epochs=5, batch_size=64, patience=3):
    print("=" * 75)
    print("QUY TRÌNH HUẤN LUYỆN & VALIDATION CHUẨN MỰC CHO MODERN CNN")
    print(f"Epochs: {epochs} | Batch size: {batch_size} | Early stopping patience: {patience}")
    print("=" * 75)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Thiết bị: {device}")

    torch.manual_seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)

    # 1. Tải dữ liệu chuẩn 50k train / 10k val / 10k test
    (x_train_50k, y_train_50k, x_val_10k, y_val_10k, x_test_10k, y_test_10k) = create_train_val_test(
        val_samples=10000, random_state=RANDOM_STATE, normalize=True, flatten=False
    )
    print(f"Dữ liệu: Train={x_train_50k.shape}, Val={x_val_10k.shape}, Test={x_test_10k.shape}")

    # Đưa về dạng tensor (N, 1, 28, 28)
    t_x_train = torch.from_numpy(x_train_50k).unsqueeze(1).float()
    t_y_train = torch.from_numpy(y_train_50k).long()
    t_x_val = torch.from_numpy(x_val_10k).unsqueeze(1).float()
    t_y_val = torch.from_numpy(y_val_10k).long()
    t_x_test = torch.from_numpy(x_test_10k).unsqueeze(1).float()
    t_y_test = torch.from_numpy(y_test_10k).long()

    train_loader = DataLoader(TensorDataset(t_x_train, t_y_train), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(t_x_val, t_y_val), batch_size=batch_size, shuffle=False)

    model = ModernCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

    history = {
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": [],
        "val_macro_f1": [],
    }

    best_val_loss = float("inf")
    best_val_acc = 0.0
    best_epoch = 0
    best_weights = None
    no_improve_count = 0

    start_train_total = time.perf_counter()

    for epoch in range(1, epochs + 1):
        # --- TRAIN ---
        model.train()
        total_loss, correct, total = 0.0, 0, 0
        for b_x, b_y in train_loader:
            b_x, b_y = b_x.to(device), b_y.to(device)
            optimizer.zero_grad()
            logits = model(b_x)
            loss = criterion(logits, b_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * b_x.size(0)
            preds = torch.argmax(logits, dim=1)
            correct += (preds == b_y).sum().item()
            total += b_x.size(0)

        train_loss = total_loss / total
        train_acc = (correct / total) * 100.0

        # --- VALIDATION ---
        model.eval()
        val_loss_sum, val_preds_all, val_targets_all = 0.0, [], []
        with torch.no_grad():
            for b_x, b_y in val_loader:
                b_x, b_y = b_x.to(device), b_y.to(device)
                logits = model(b_x)
                loss = criterion(logits, b_y)
                val_loss_sum += loss.item() * b_x.size(0)
                preds = torch.argmax(logits, dim=1)
                val_preds_all.extend(preds.cpu().numpy())
                val_targets_all.extend(b_y.cpu().numpy())

        val_loss = val_loss_sum / len(y_val_10k)
        val_acc = accuracy_score(val_targets_all, val_preds_all) * 100.0
        val_f1 = f1_score(val_targets_all, val_preds_all, average="macro") * 100.0

        history["train_loss"].append(round(train_loss, 4))
        history["train_acc"].append(round(train_acc, 2))
        history["val_loss"].append(round(val_loss, 4))
        history["val_acc"].append(round(val_acc, 2))
        history["val_macro_f1"].append(round(val_f1, 2))

        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%, Val F1: {val_f1:.2f}%")

        # Lưu checkpoint tốt nhất dựa trên Validation Loss
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_val_acc = val_acc
            best_epoch = epoch
            best_weights = copy.deepcopy(model.state_dict())
            no_improve_count = 0
            print(f"   -> [BEST] Checkpoint được cập nhật tại Epoch {epoch} (Val Loss: {val_loss:.4f})")
        else:
            no_improve_count += 1
            if no_improve_count >= patience:
                print(f"   -> [EARLY STOPPING] Kích hoạt tại Epoch {epoch} do Val Loss không giảm sau {patience} epochs.")
                break

    train_duration = time.perf_counter() - start_train_total
    print(f"\nTổng thời gian huấn luyện: {train_duration:.2f}s | Best Epoch: {best_epoch} (Val Acc: {best_val_acc:.2f}%)")

    # Lưu checkpoint được lựa chọn bởi Validation
    tuned_checkpoint_path = MODELS_DIR / "modern_cnn_val_tuned.pt"
    torch.save(best_weights, tuned_checkpoint_path)
    print(f"Đã lưu checkpoint được chọn bởi validation vào: {tuned_checkpoint_path}")

    # Đánh giá cuối cùng trên 10,000 Test Set (Chỉ đánh giá 1 lần duy nhất)
    model.load_state_dict(best_weights)
    model.eval()
    test_preds_all = []
    with torch.no_grad():
        t_infer0 = time.perf_counter()
        test_logits = model(t_x_test.to(device))
        total_test_infer = time.perf_counter() - t_infer0
        test_preds = torch.argmax(test_logits, dim=1).cpu().numpy()

    test_acc = accuracy_score(y_test_10k, test_preds) * 100.0
    test_f1 = f1_score(y_test_10k, test_preds, average="macro") * 100.0
    test_errors = int((test_preds != y_test_10k).sum())
    test_latency_ms = (total_test_infer / len(y_test_10k)) * 1000.0

    print("\n" + "=" * 50)
    print("KẾT QUẢ ĐÁNH GIÁ CUỐI TRÊN 10,000 MNIST TEST SET:")
    print(f"Test Accuracy: {test_acc:.2f}% | Macro F1: {test_f1:.2f}% | Số lỗi: {test_errors}/10000 | Độ trễ: {test_latency_ms:.4f} ms")
    print("=" * 50)

    # Lưu lịch sử huấn luyện JSON
    history_path = RESULTS_DIR / "cnn_validation_history.json"
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump({
            "model": "ModernCNN",
            "epochs_run": len(history["train_loss"]),
            "best_epoch": best_epoch,
            "best_val_loss": best_val_loss,
            "best_val_acc": best_val_acc,
            "test_accuracy": round(test_acc, 2),
            "test_macro_f1": round(test_f1, 2),
            "test_errors": test_errors,
            "history": history
        }, f, indent=2)
    print(f"Đã lưu lịch sử huấn luyện: {history_path}")

    # 4. Vẽ biểu đồ Training & Validation Curves
    plt.figure(figsize=(12, 5))
    
    # Loss curve
    plt.subplot(1, 2, 1)
    epochs_range = range(1, len(history["train_loss"]) + 1)
    plt.plot(epochs_range, history["train_loss"], "o-", color="#102C57", label="Training Loss", linewidth=2)
    plt.plot(epochs_range, history["val_loss"], "s--", color="#FF6B6B", label="Validation Loss", linewidth=2)
    plt.axvline(x=best_epoch, color="green", linestyle=":", label=f"Best Checkpoint (Epoch {best_epoch})")
    plt.title("Đường cong Mất mát (Training & Validation Loss)", fontsize=12, fontweight="bold", pad=10)
    plt.xlabel("Epoch", fontsize=10)
    plt.ylabel("Cross-Entropy Loss", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)

    # Accuracy curve
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, history["train_acc"], "o-", color="#102C57", label="Training Accuracy", linewidth=2)
    plt.plot(epochs_range, history["val_acc"], "s--", color="#28A745", label="Validation Accuracy", linewidth=2)
    plt.axvline(x=best_epoch, color="green", linestyle=":", label=f"Best Checkpoint (Epoch {best_epoch})")
    plt.title("Đường cong Độ chính xác (Training & Validation Accuracy)", fontsize=12, fontweight="bold", pad=10)
    plt.xlabel("Epoch", fontsize=10)
    plt.ylabel("Accuracy (%)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)

    plt.tight_layout()
    fig_path = FIGURES_DIR / "08_cnn_training_history.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Đã lưu biểu đồ lịch sử validation: {fig_path}")

    return history

if __name__ == "__main__":
    train_cnn_validation_protocol(epochs=5, batch_size=64, patience=2)
