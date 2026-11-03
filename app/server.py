"""
FastAPI Backend Server for Handwritten Digit Recognition Web App.
Nhóm 03 - Môn Nhận dạng mẫu (Trường Đại học Thủy Lợi)

Provides REST APIs for:
- Model listings (Full suite of classical ML & Deep Learning models)
- Real-time digit prediction on canvas drawings or uploaded images
- Image preprocessing (Centering of mass, 28x28 resize, normalization)
- Exact feature extraction pipelines matching training (Raw, PCA, HOG, Deskew)
- Returning class probabilities, decision scores, and latency
"""
import sys
import io
import base64
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import cv2
from PIL import Image, ImageOps

# UTF-8 stdout configuration for Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import joblib
from sklearn.exceptions import NotFittedError
import torch

from src.config import MODELS_DIR, NPZ_DATA_PATH
from src.features import PCATransformer, extract_hog_features, deskew_dataset
from src.models import ModernCNN
from src.image_preprocessing import extract_uploaded_digit

app = FastAPI(title="MNIST Handwritten Digit Recognition Demo")

# Global cache for loaded models and transformers
LOADED_MODELS: Dict[str, Any] = {}
MODEL_CACHE = LOADED_MODELS  # Alias for backward compatibility and test access
PCA_TRANSFORMER: Any = None
PCA_TRANSFORMER_DESKEW: Any = None
CNN_MODEL: Any = None
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class PredictRequest(BaseModel):
    image_base64: str
    model_name: str = "cnn"
    is_upload: bool = False


def get_center_of_mass_28x28(gray_img: np.ndarray) -> np.ndarray:
    """
    Standard MNIST centering pipeline:
    1. Threshold & crop bounding box of the digit.
    2. Resize to 20x20 preserving aspect ratio.
    3. Pad into 28x28 canvas centered at center of mass.
    """
    # Thresholding
    _, thresh = cv2.threshold(gray_img, 20, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(thresh)

    if coords is None or len(coords) < 15:
        # Blank canvas or faint accidental dot
        return np.zeros((28, 28), dtype=np.float32)

    x, y, w, h = cv2.boundingRect(coords)
    digit_roi = gray_img[y:y+h, x:x+w]

    # Resize preserving aspect ratio into 20x20 box
    if w > h:
        new_w = 20
        new_h = max(1, int(h * (20 / w)))
    else:
        new_h = 20
        new_w = max(1, int(w * (20 / h)))

    resized = cv2.resize(digit_roi, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Place in center of 28x28 blank canvas
    padded = np.zeros((28, 28), dtype=np.float32)
    start_y = (28 - new_h) // 2
    start_x = (28 - new_w) // 2
    padded[start_y:start_y+new_h, start_x:start_x+new_w] = resized

    # Calculate center of mass and shift to exactly (14, 14)
    moments = cv2.moments(padded)
    if moments["m00"] > 0:
        cx = moments["m10"] / moments["m00"]
        cy = moments["m01"] / moments["m00"]
        dx = 14.0 - cx
        dy = 14.0 - cy
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        padded = cv2.warpAffine(padded, M, (28, 28), borderValue=0)

    # Normalize to [0.0, 1.0]
    return padded / 255.0


# Model Registry configuration mapping with validated metadata
# Primary official models are trained according to Notebook 02 (02_Tien_Xu_Ly_Train_MNIST)
MODEL_REGISTRY_CONFIG = {
    # --- 1. CÁC MÔ HÌNH CHÍNH THỨC (HUẤN LUYỆN MỚI THEO NOTEBOOK 02) ---
    "cnn": {
        "name": "Modern CNN",
        "checkpoint": "CNN.pt",
        "type": "cnn",
        "accuracy": "99.44%",
        "test_errors": "56 / 10,000",
        "feature": "Learned Conv (28×28)",
        "train_samples": "50,000 train + 10,000 val",
        "hyperparameters": "3 Conv Blocks, Adam, checkpoint epoch 20, Early Stopping Epoch 23 (Val Loss 0.0218)",
        "confidence_type": "Softmax",
        "experiment_id": "EXP-NB2-CNN",
        "is_official": True,
    },
    "svm": {
        "name": "SVM",
        "checkpoint": "SVM.joblib",
        "type": "sklearn_deskew_pca",
        "accuracy": "98.79%",
        "test_errors": "121 / 10,000",
        "feature": "Deskewing + PCA (113D)",
        "train_samples": "50,000",
        "hyperparameters": "C=5.0, kernel=rbf, gamma=scale, Deskew+PCA",
        "confidence_type": "Khoảng cách lề SVM chuyển đổi (Softmax Margin)",
        "experiment_id": "EXP-NB2-SVM",
        "is_official": True,
    },
    "knn": {
        "name": "k-NN",
        "checkpoint": "k-NN.joblib",
        "type": "sklearn_deskew_pca",
        "accuracy": "98.06%",
        "test_errors": "194 / 10,000",
        "feature": "Deskewing + PCA (113D)",
        "train_samples": "50,000",
        "hyperparameters": "k=3, weights=distance, metric=euclidean, Deskew+PCA",
        "confidence_type": "Trọng số khoảng cách nghịch đảo (Distance weights)",
        "experiment_id": "EXP-NB2-KNN",
        "is_official": True,
    },
    "rf": {
        "name": "Random Forest",
        "checkpoint": "Random_Forest.joblib",
        "type": "sklearn_raw",
        "accuracy": "96.99%",
        "test_errors": "301 / 10,000",
        "feature": "Raw Pixels (784D)",
        "train_samples": "50,000",
        "hyperparameters": "n_estimators=150, max_features=sqrt",
        "confidence_type": "Tỷ lệ phiếu bầu từ 150 cây quyết định (Tree Voting)",
        "experiment_id": "EXP-NB2-RF",
        "is_official": True,
    },
    "nb": {
        "name": "Bernoulli Naive Bayes",
        "checkpoint": "Naive_Bayes.joblib",
        "type": "sklearn_bin",
        "accuracy": "84.46%",
        "test_errors": "1,554 / 10,000",
        "feature": "Binarized Pixels (784D, bin=0.2)",
        "train_samples": "50,000",
        "hyperparameters": "BernoulliNB, alpha=1.0, binarize=0.2",
        "confidence_type": "Xác suất hậu nghiệm Bayes (Log posterior)",
        "experiment_id": "EXP-NB2-NB",
        "is_official": True,
    },

 }
MODEL_REGISTRY_CONFIG['svm_deskew_pca'] = MODEL_REGISTRY_CONFIG['svm'].copy()
MODEL_REGISTRY_CONFIG['bnb'] = MODEL_REGISTRY_CONFIG['nb'].copy()


def refresh_result_metadata():
    """Read evaluation results from the same directory as the checkpoints."""
    import csv
    import json
    names = {'Naive Bayes': 'nb', 'k-NN': 'knn', 'SVM': 'svm', 'Random Forest': 'rf', 'CNN': 'cnn'}
    with (MODELS_DIR / 'results.csv').open(encoding='utf-8', newline='') as handle:
        for row in csv.DictReader(handle):
            cfg = MODEL_REGISTRY_CONFIG[names[row['Mô hình']]]
            cfg['accuracy'] = f"{float(row['Test Acc (%)']):.2f}%"
            cfg['test_errors'] = f"{int(row['Số ảnh sai']):,} / 10,000"
    config = json.loads((MODELS_DIR / 'selected_config.json').read_text(encoding='utf-8'))
    MODEL_REGISTRY_CONFIG['cnn']['hyperparameters'] = (
        f"3 Conv Blocks, Adam, checkpoint epoch {config['cnn_best_epoch']}, "
        f"Early Stopping Epoch {config['cnn_epochs_run']} (Val Loss {config['cnn_best_val_loss']:.4f})"
    )
    for alias, original in [('svm_deskew_pca', 'svm'), ('bnb', 'nb')]:
        MODEL_REGISTRY_CONFIG[alias].update(MODEL_REGISTRY_CONFIG[original])



def load_all_models():
    """Load pre-trained models and transformers into memory using official Model Registry."""
    global LOADED_MODELS, PCA_TRANSFORMER, PCA_TRANSFORMER_DESKEW, CNN_MODEL

    refresh_result_metadata()
    LOADED_MODELS.clear()
    print("[SERVER] Đang nạp các mô hình vào Model Registry...")

    # 1. Load PCA Transformer (new 113D Deskew PCA from Notebook 02)
    PCA_TRANSFORMER = joblib.load(MODELS_DIR / 'pca.joblib')
    PCA_TRANSFORMER_DESKEW = PCA_TRANSFORMER

    # 2. Iterate through Model Registry and load models
    for m_id, cfg in MODEL_REGISTRY_CONFIG.items():
        ckpt_path = MODELS_DIR / cfg["checkpoint"]
        if not ckpt_path.exists():
            print(f"  [BỎ QUA] Không tìm thấy checkpoint cho {m_id} tại {ckpt_path}")
            continue

        try:
            if cfg["type"] in ["cnn", "legacy_cnn"]:
                cnn = ModernCNN().to(DEVICE)
                state_dict = torch.load(ckpt_path, map_location=DEVICE)
                cnn.load_state_dict(state_dict)
                cnn.eval()
                if m_id == "cnn":
                    CNN_MODEL = cnn
                loaded_obj = cnn
            else:
                loaded_obj = joblib.load(ckpt_path)

            LOADED_MODELS[m_id] = {
                "id": m_id,
                "name": cfg["name"],
                "type": cfg["type"],
                "accuracy": cfg["accuracy"],
                "test_errors": cfg.get("test_errors", "N/A"),
                "feature": cfg.get("feature", "N/A"),
                "train_samples": cfg.get("train_samples", "N/A"),
                "hyperparameters": cfg.get("hyperparameters", "N/A"),
                "confidence_type": cfg.get("confidence_type", "Độ tin cậy"),
                "experiment_id": cfg.get("experiment_id", "N/A"),
                "is_official": cfg.get("is_official", True),
                "model": loaded_obj,
                "checkpoint_path": str(ckpt_path.name)
            }
            status_tag = "CHÍNH THỨC" if cfg["is_official"] else "LƯU TRỮ/TẠM KHÓA"
            print(f"  -> [OK] [{status_tag}] Nạp thành công: {m_id} ({cfg['name']})")
        except Exception as e:
            print(f"  -> [LỖI] Không thể nạp {m_id} từ {ckpt_path.name}: {e}")

    print(f"[SERVER] Đã hoàn tất nạp {len(LOADED_MODELS)} mô hình vào Model Registry!")


@app.on_event("startup")
def startup_event():
    load_all_models()


@app.get("/api/models")
def get_available_models():
    """Return only active official models metadata for the web UI (5 models from Notebook 02)."""
    models_info = []
    active_ids = ["cnn", "svm", "knn", "rf", "nb"]
    for m_id in active_ids:
        if m_id in LOADED_MODELS:
            m_data = LOADED_MODELS[m_id]
            models_info.append({
                "id": m_id,
                "name": m_data["name"],
                "accuracy": m_data["accuracy"],
                "test_errors": m_data.get("test_errors", "N/A"),
                "feature": m_data.get("feature", "N/A"),
                "train_samples": m_data.get("train_samples", "N/A"),
                "hyperparameters": m_data.get("hyperparameters", "N/A"),
                "confidence_type": m_data.get("confidence_type", "Độ tin cậy"),
                "is_official": True,
                "type": m_data["type"]
            })
    return {"models": models_info}


@app.get("/api/samples")
def get_sample_test_digits():
    """Provide 10 representative test digits from MNIST (classes 0 to 9)."""
    if not NPZ_DATA_PATH.exists():
        return {"samples": []}

    with np.load(NPZ_DATA_PATH) as data:
        x_test, y_test = data["x_test"], data["y_test"]

    samples = []
    for digit in range(10):
        matches = np.where(y_test == digit)[0]
        if len(matches) > 0:
            idx = int(matches[0])
            img = x_test[idx]
            pil_img = Image.fromarray(img)
            buff = io.BytesIO()
            pil_img.save(buff, format="PNG")
            b64 = base64.b64encode(buff.getvalue()).decode("utf-8")
            samples.append({
                "digit": digit,
                "image_base64": f"data:image/png;base64,{b64}"
            })
    return {"samples": samples}


def prediction_scores(model, features, predicted_digit):
    """Return class scores, using margins when probability estimates are unavailable."""
    try:
        return model.predict_proba(features)[0]
    except (AttributeError, NotFittedError):
        if hasattr(model, "decision_function"):
            decision = np.asarray(model.decision_function(features)[0])
            shifted = decision - np.max(decision)
            return np.exp(shifted) / np.sum(np.exp(shifted))
        scores = np.zeros(10)
        scores[predicted_digit] = 1.0
        return scores


@app.post("/api/predict")
async def predict_digit(req: PredictRequest):
    """
    Predict handwritten digit from base64 image string with exact preprocessing.
    """
    t0 = time.perf_counter()

    # 1. Parse base64
    try:
        raw_b64 = req.image_base64
        if "base64," in raw_b64:
            raw_b64 = raw_b64.split("base64,")[1]
        img_bytes = base64.b64decode(raw_b64)
        pil_img = ImageOps.exif_transpose(Image.open(io.BytesIO(img_bytes)))
        if "A" in pil_img.getbands() or "transparency" in pil_img.info:
            rgba = pil_img.convert("RGBA")
            pixels = np.asarray(rgba, dtype=np.float32)
            alpha = pixels[..., 3] / 255.0
            gray = np.asarray(rgba.convert("L"), dtype=np.float32)
            mass = float(alpha.sum())
            visible_mean = float((gray * alpha).sum()) / mass if mass else 255.0
            background = 255 if visible_mean < 127 else 0
            opaque = Image.new("RGBA", rgba.size, (background, background, background, 255))
            pil_img = Image.alpha_composite(opaque, rgba)
        if req.is_upload:
            img_arr = extract_uploaded_digit(np.array(pil_img.convert("RGB")))
        else:
            img_arr = np.array(pil_img.convert("L"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Không thể giải mã dữ liệu ảnh: {str(e)}")

    # 2. Check if image is inverted (MNIST is white digit on black background)
    if np.mean(img_arr) > 127:
        img_arr = 255 - img_arr

    # 3. Center and normalize to 28x28
    processed_28 = get_center_of_mass_28x28(img_arr)

    # Blank image check
    if np.all(processed_28 == 0):
        prep_uint8 = np.zeros((28, 28), dtype=np.uint8)
        prep_pil = Image.fromarray(prep_uint8)
        prep_buff = io.BytesIO()
        prep_pil.save(prep_buff, format="PNG")
        prep_b64 = base64.b64encode(prep_buff.getvalue()).decode("utf-8")
        return {
            "predicted_digit": -1,
            "confidence": 0.0,
            "probabilities": [0.0] * 10,
            "latency_ms": round((time.perf_counter() - t0) * 1000.0, 2),
            "model_used": "N/A",
            "is_calibrated": False,
            "message": "Bảng vẽ trống. Vui lòng vẽ một chữ số rõ ràng lên khung vẽ.",
            "processed_image": f"data:image/png;base64,{prep_b64}"
        }

    # 4. Model Selection (Strict: raise 404 on invalid model, no silent fallback)
    m_id = req.model_name
    if m_id not in LOADED_MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Mô hình '{m_id}' không tồn tại hoặc chưa được nạp. Danh sách khả dụng: {list(LOADED_MODELS.keys())}"
        )

    model_entry = LOADED_MODELS[m_id]
    m_type = model_entry["type"]
    model = model_entry["model"]

    # 5. Extract features matching model requirements
    flat = processed_28.reshape(1, -1)
    is_calibrated = False

    if m_type in ["cnn", "legacy_cnn"]:
        probs = model.predict_proba(processed_28.reshape(1, 1, 28, 28))[0]
        predicted_digit = int(np.argmax(probs))
        is_calibrated = False  # Softmax output is uncalibrated confidence

    elif m_type == "sklearn_deskew_pca":
        if hasattr(model, "steps"):
            feat = flat
        else:
            deskewed = deskew_dataset(flat)
            pca_trans = PCA_TRANSFORMER_DESKEW if PCA_TRANSFORMER_DESKEW is not None else PCA_TRANSFORMER
            if pca_trans is not None:
                feat = pca_trans.transform(deskewed)
            else:
                feat = deskewed

        official_pred = int(model.predict(feat)[0])
        probs = prediction_scores(model, feat, official_pred)
        predicted_digit = official_pred
        is_calibrated = False

    elif m_type == "sklearn_pca":
        if PCA_TRANSFORMER is not None:
            feat = PCA_TRANSFORMER.transform(flat)
        else:
            feat = flat

        official_pred = int(model.predict(feat)[0])
        probs = prediction_scores(model, feat, official_pred)
        predicted_digit = official_pred
        is_calibrated = False

    elif m_type == "sklearn_hog":
        feat = extract_hog_features(flat)
        official_pred = int(model.predict(feat)[0])
        probs = prediction_scores(model, feat, official_pred)
        predicted_digit = official_pred
        is_calibrated = False

    elif m_type == "sklearn_bin":
        feat = (flat > 0.2).astype(np.float32)
        official_pred = int(model.predict(feat)[0])
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(feat)[0]
        else:
            probs = np.zeros(10)
            probs[official_pred] = 1.0
        predicted_digit = official_pred
        is_calibrated = False

    else:  # sklearn_raw
        feat = flat
        official_pred = int(model.predict(feat)[0])
        probs = prediction_scores(model, feat, official_pred)
        predicted_digit = official_pred
        is_calibrated = False

    confidence = float(probs[predicted_digit])
    latency_ms = (time.perf_counter() - t0) * 1000.0

    # 6. Encode preprocessed 28x28 image for visual confirmation
    prep_uint8 = (processed_28 * 255).astype(np.uint8)
    prep_pil = Image.fromarray(prep_uint8)
    prep_buff = io.BytesIO()
    prep_pil.save(prep_buff, format="PNG")
    prep_b64 = base64.b64encode(prep_buff.getvalue()).decode("utf-8")

    return {
        "predicted_digit": predicted_digit,
        "confidence": confidence,
        "confidence_type": model_entry.get("confidence_type", "Độ tin cậy"),
        "probabilities": [float(p) for p in probs],
        "latency_ms": round(latency_ms, 2),
        "model_used": model_entry["name"],
        "model_id": m_id,
        "is_calibrated": is_calibrated,
        "processed_image": f"data:image/png;base64,{prep_b64}"
    }


# Mount static frontend
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
def index_page():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>MNIST Demo Server is running!</h1>"
