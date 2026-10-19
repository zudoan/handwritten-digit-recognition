"""
Configuration and constants for Handwritten Digit Recognition project (MNIST).
Nhóm 03 - Môn Nhận dạng mẫu
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
NPZ_DATA_PATH = DATA_DIR / "mnist.npz"

MODELS_DIR = BASE_DIR / "saved_models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

# Ensure directories exist
for directory in [DATA_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR, TABLES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset specifications
IMAGE_HEIGHT = 28
IMAGE_WIDTH = 28
IMAGE_CHANNELS = 1
IMAGE_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH)
NUM_PIXELS = IMAGE_HEIGHT * IMAGE_WIDTH  # 784
NUM_CLASSES = 10
CLASS_NAMES = [str(i) for i in range(10)]

# Experiment configuration
RANDOM_STATE = 42
N_JOBS = -1  # Utilize all available CPU cores
