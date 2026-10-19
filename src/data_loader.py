"""
Data loader and preprocessing utilities for MNIST dataset.
Supports raw loading, normalization, flattening, and train/val splitting.
"""
from pathlib import Path
from typing import Tuple, Optional
import numpy as np
from sklearn.model_selection import train_test_split

from src.config import NPZ_DATA_PATH, RANDOM_STATE


def load_mnist_data(
    normalize: bool = True,
    flatten: bool = False,
    data_path: Optional[Path] = None,
) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """
    Load MNIST dataset from .npz archive.

    Args:
        normalize: If True, scales pixel values from [0, 255] to [0.0, 1.0].
        flatten: If True, reshapes (N, 28, 28) into (N, 784).
        data_path: Path to mnist.npz. Defaults to config.NPZ_DATA_PATH.

    Returns:
        ((x_train, y_train), (x_test, y_test))
    """
    path = data_path or NPZ_DATA_PATH
    if not Path(path).exists():
        raise FileNotFoundError(
            f"File dữ liệu không tồn tại tại: {path}. Vui lòng chạy download_mnist.py trước."
        )

    with np.load(path) as data:
        x_train, y_train = data["x_train"], data["y_train"]
        x_test, y_test = data["x_test"], data["y_test"]

    if normalize:
        x_train = x_train.astype(np.float32) / 255.0
        x_test = x_test.astype(np.float32) / 255.0

    if flatten:
        x_train = x_train.reshape(x_train.shape[0], -1)
        x_test = x_test.reshape(x_test.shape[0], -1)

    return (x_train, y_train), (x_test, y_test)


def get_stratified_subset(
    x: np.ndarray,
    y: np.ndarray,
    samples_per_class: int = 1000,
    random_state: int = RANDOM_STATE,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract a balanced stratified subset of data (useful for algorithms with high complexity like k-NN / RBF SVM).
    """
    rng = np.random.RandomState(random_state)
    selected_indices = []
    for cls in np.unique(y):
        cls_indices = np.where(y == cls)[0]
        chosen = rng.choice(cls_indices, size=min(samples_per_class, len(cls_indices)), replace=False)
        selected_indices.extend(chosen)
    rng.shuffle(selected_indices)
    return x[selected_indices], y[selected_indices]


def create_train_val_test(
    val_samples: int = 10000,
    random_state: int = RANDOM_STATE,
    normalize: bool = True,
    flatten: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Create standard 3-way split: Train (50k), Validation (10k), Test (10k).
    Validation is carved out of the original 60k training samples using stratified sampling.
    """
    (x_train_full, y_train_full), (x_test, y_test) = load_mnist_data(
        normalize=normalize, flatten=flatten
    )

    val_ratio = val_samples / len(y_train_full)  # 10000 / 60000 = 1/6
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full,
        y_train_full,
        test_size=val_ratio,
        random_state=random_state,
        stratify=y_train_full,
    )
    return x_train, y_train, x_val, y_val, x_test, y_test

