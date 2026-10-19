"""
Model implementations and wrappers for Handwritten Digit Recognition.
Covers:
1. Classical Machine Learning:
   - Gaussian & Bernoulli Naive Bayes
   - k-Nearest Neighbors (k-NN)
   - Support Vector Machines (Linear & RBF SVM)
   - Random Forest Classifier
2. Deep Learning (Bonus / Sáng tạo):
   - Modern LeNet-5 / CNN architecture with Batch Normalization and Dropout.
"""
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import time
import joblib
import numpy as np

from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier

from src.config import RANDOM_STATE, MODELS_DIR

# Optional PyTorch import
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import TensorDataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def create_model(model_type: str, **kwargs) -> Any:
    """
    Factory function to instantiate models with optimal default hyperparameters.
    """
    m_type = model_type.lower()

    if m_type in ["gaussian_nb", "gnb"]:
        return GaussianNB(**kwargs)

    elif m_type in ["bernoulli_nb", "bnb"]:
        return BernoulliNB(binarize=kwargs.get("binarize", 0.1))

    elif m_type in ["knn", "k_nearest_neighbors"]:
        n_neighbors = kwargs.get("n_neighbors", 3)
        metric = kwargs.get("metric", "minkowski")
        p = kwargs.get("p", 2)  # p=2 is Euclidean, p=1 is Manhattan
        weights = kwargs.get("weights", "distance")
        return KNeighborsClassifier(
            n_neighbors=n_neighbors,
            metric=metric,
            p=p,
            weights=weights,
            n_jobs=-1,
        )

    elif m_type in ["linear_svm", "svm_linear"]:
        C = kwargs.get("C", 1.0)
        return LinearSVC(C=C, random_state=RANDOM_STATE, max_iter=2000)

    elif m_type in ["rbf_svm", "svm_rbf", "svm"]:
        C = kwargs.get("C", 5.0)
        gamma = kwargs.get("gamma", "scale")
        probability = kwargs.get("probability", True)
        return SVC(
            C=C,
            gamma=gamma,
            kernel="rbf",
            probability=probability,
            random_state=RANDOM_STATE,
        )

    elif m_type in ["rf", "random_forest"]:
        n_estimators = kwargs.get("n_estimators", 150)
        max_depth = kwargs.get("max_depth", None)
        return RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    elif m_type in ["cnn", "lenet"]:
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch chưa được cài đặt để chạy mô hình CNN.")
        return ModernCNN()

    else:
        raise ValueError(f"Không hỗ trợ mô hình: {model_type}")


if TORCH_AVAILABLE:
    class ModernCNN(nn.Module):
        """
        Modern Convolutional Neural Network for MNIST digit classification.
        Architecture:
            Input: (N, 1, 28, 28)
            Conv Block 1: Conv2D(1 -> 32, 3x3) -> BatchNorm -> ReLU -> MaxPool(2x2)
            Conv Block 2: Conv2D(32 -> 64, 3x3) -> BatchNorm -> ReLU -> MaxPool(2x2)
            Conv Block 3: Conv2D(64 -> 128, 3x3) -> BatchNorm -> ReLU
            Flatten -> Dropout(0.4) -> Linear(128*3*3 -> 128) -> ReLU -> Dropout(0.2) -> Linear(128 -> 10)
        """

        def __init__(self, num_classes: int = 10):
            super().__init__()
            self.features = nn.Sequential(
                # Block 1: 28x28 -> 26x26 -> 13x13
                nn.Conv2d(1, 32, kernel_size=3, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2, 2),  # 14x14

                # Block 2: 14x14 -> 7x7
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.BatchNorm2d(64),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2, 2),  # 7x7

                # Block 3: 7x7 -> 3x3
                nn.Conv2d(64, 128, kernel_size=3, padding=0),  # 5x5
                nn.BatchNorm2d(128),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2, 2),  # 2x2
            )

            self.classifier = nn.Sequential(
                nn.Dropout(0.4),
                nn.Linear(128 * 2 * 2, 128),
                nn.ReLU(inplace=True),
                nn.Dropout(0.2),
                nn.Linear(128, num_classes),
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            if x.ndim == 3:
                x = x.unsqueeze(1)
            elif x.ndim == 2:
                x = x.view(-1, 1, 28, 28)
            feat = self.features(x)
            flat = feat.view(feat.size(0), -1)
            out = self.classifier(flat)
            return out

        def predict_proba(self, x_np: np.ndarray, batch_size: int = 256) -> np.ndarray:
            """Predict probability distribution for numpy array."""
            self.eval()
            device = next(self.parameters()).device
            x_tensor = torch.from_numpy(x_np).float()
            if x_tensor.ndim == 2:
                x_tensor = x_tensor.view(-1, 1, 28, 28)
            elif x_tensor.ndim == 3:
                x_tensor = x_tensor.unsqueeze(1)

            dataset = TensorDataset(x_tensor)
            loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
            probs = []

            with torch.no_grad():
                for (batch_x,) in loader:
                    batch_x = batch_x.to(device)
                    logits = self(batch_x)
                    p = F.softmax(logits, dim=1).cpu().numpy()
                    probs.append(p)

            return np.vstack(probs)

        def predict(self, x_np: np.ndarray, batch_size: int = 256) -> np.ndarray:
            """Predict class labels for numpy array."""
            probs = self.predict_proba(x_np, batch_size=batch_size)
            return np.argmax(probs, axis=1)


def save_sklearn_model(model: Any, filename: str, save_dir: Path = MODELS_DIR) -> Path:
    """Save trained scikit-learn model using joblib."""
    out_path = save_dir / filename
    joblib.dump(model, out_path, compress=3)
    print(f"[OK] Đã lưu mô hình: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")
    return out_path


def load_sklearn_model(filename: str, save_dir: Path = MODELS_DIR) -> Any:
    """Load model from joblib file."""
    path = save_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy mô hình tại: {path}")
    return joblib.load(path)
