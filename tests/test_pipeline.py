"""
Automated Test Suite for MNIST Handwritten Digit Recognition Project.
Nhóm 03 - Môn Nhận dạng mẫu (Đại học Thủy Lợi)

Covers:
- Unit tests: Data loading, splits, shapes, bounds, transformers (Deskew, PCA, HOG), model forward pass.
- Integration tests: Preprocessing pipeline, model save/load, prediction range, backend API behavior.
Run via: python -m unittest tests/test_pipeline.py
"""
import unittest
import sys
import io
import base64
import asyncio
from pathlib import Path
import numpy as np
from PIL import Image

# Reconfigure stdout for Windows cp1252 compatibility
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.config import NPZ_DATA_PATH, MODELS_DIR
from src.data_loader import load_mnist_data, get_stratified_subset, create_train_val_test
from src.features import deskew_image, deskew_dataset, extract_hog_features, PCATransformer, HOGTransformer
from src.models import create_model, ModernCNN
from app.server import (
    get_center_of_mass_28x28,
    load_all_models,
    get_available_models,
    get_sample_test_digits,
    predict_digit,
    PredictRequest,
)


class TestDataLoadingAndSplits(unittest.TestCase):
    """Test data ingestion, normalization, and leakage-free dataset splitting."""

    @classmethod
    def setUpClass(cls):
        (cls.x_tr_norm, cls.y_tr), (cls.x_te_norm, cls.y_te) = load_mnist_data(normalize=True, flatten=False)

    def test_load_mnist_data_shapes(self):
        self.assertEqual(self.x_tr_norm.shape, (60000, 28, 28))
        self.assertEqual(self.y_tr.shape, (60000,))
        self.assertEqual(self.x_te_norm.shape, (10000, 28, 28))
        self.assertEqual(self.y_te.shape, (10000,))

    def test_pixel_normalization_bounds(self):
        self.assertGreaterEqual(float(self.x_tr_norm.min()), 0.0)
        self.assertLessEqual(float(self.x_tr_norm.max()), 1.0)
        self.assertEqual(self.x_tr_norm.dtype, np.float32)

    def test_stratified_subset_balance(self):
        sub_x, sub_y = get_stratified_subset(self.x_tr_norm, self.y_tr, samples_per_class=100, random_state=42)
        self.assertEqual(len(sub_y), 1000)
        bincounts = np.bincount(sub_y)
        self.assertTrue(all(c == 100 for c in bincounts))

    def test_create_train_val_test_no_overlap(self):
        x_tr, y_tr, x_val, y_val, x_te, y_te = create_train_val_test(
            val_samples=10000, random_state=42, normalize=True, flatten=True
        )
        self.assertEqual(len(y_tr), 50000)
        self.assertEqual(len(y_val), 10000)
        self.assertEqual(len(y_te), 10000)
        # Check label distribution across splits
        tr_dist = np.bincount(y_tr) / len(y_tr)
        val_dist = np.bincount(y_val) / len(y_val)
        np.testing.assert_allclose(tr_dist, val_dist, atol=0.01)

    def test_strict_zero_leakage_index_intersection(self):
        """Verify strict mathematical isolation: train indices intersect val indices is empty set."""
        from sklearn.model_selection import train_test_split
        total_train_indices = np.arange(60000)
        idx_train, idx_val = train_test_split(
            total_train_indices,
            test_size=10000,
            stratify=self.y_tr,
            random_state=42
        )
        intersection = set(idx_train).intersection(set(idx_val))
        self.assertEqual(len(intersection), 0, "Data Leakage Detected: Train and Validation sets share indices!")
        self.assertEqual(len(idx_train) + len(idx_val), 60000)


class TestFeatureEngineering(unittest.TestCase):
    """Test geometrical Deskewing, PCA compression, and HOG descriptor extraction."""

    def setUp(self):
        self.dummy_img = np.zeros((28, 28), dtype=np.float32)
        self.dummy_img[8:22, 12:16] = 1.0  # vertical stroke (digit 1)

    def test_deskew_image_shape_and_range(self):
        deskewed = deskew_image(self.dummy_img)
        self.assertEqual(deskewed.shape, (28, 28))
        self.assertGreaterEqual(float(deskewed.min()), 0.0)
        self.assertLessEqual(float(deskewed.max()), 1.0)

    def test_pca_exact_components_ground_truth(self):
        import joblib
        pca = joblib.load(MODELS_DIR / 'pca.joblib')
        self.assertEqual(pca.n_components_, 113)
        self.assertEqual(pca.n_samples_, 50000)

    def test_pca_transformer_dimensionality(self):
        rng = np.random.RandomState(42)
        toy_data = rng.randn(200, 784).astype(np.float32)
        pca = PCATransformer(n_components=0.95, random_state=42)
        transformed = pca.fit_transform(toy_data)
        self.assertLess(transformed.shape[1], 784)
        self.assertGreater(transformed.shape[1], 50)
        self.assertEqual(transformed.shape[0], 200)

    def test_hog_feature_length(self):
        toy_images = np.zeros((2, 28, 28), dtype=np.float32)
        hog_features = extract_hog_features(toy_images)
        self.assertEqual(hog_features.shape, (2, 324))


class TestModelsAndCNN(unittest.TestCase):
    """Test model factory, PyTorch CNN forward pass, and checkpoint compatibility."""

    def test_model_factory(self):
        for m_name in ["gaussian_nb", "bernoulli_nb", "knn", "linear_svm", "rbf_svm", "rf", "cnn"]:
            m = create_model(m_name)
            self.assertIsNotNone(m)

    def test_cnn_forward_dimensions(self):
        import torch
        cnn = ModernCNN()
        cnn.eval()
        dummy_input = torch.randn(4, 1, 28, 28)
        output = cnn(dummy_input)
        self.assertEqual(output.shape, (4, 10))

    def test_cnn_predict_proba_simplex(self):
        cnn = ModernCNN()
        dummy_np = np.random.rand(5, 28, 28).astype(np.float32)
        probs = cnn.predict_proba(dummy_np)
        self.assertEqual(probs.shape, (5, 10))
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(5), atol=1e-5)


class TestBackendAPIAndPreprocessing(unittest.TestCase):
    """Test FastAPI image centering pipeline, error handling, and real-time prediction endpoints."""

    @classmethod
    def setUpClass(cls):
        load_all_models()

    def test_center_of_mass_blank_canvas(self):
        blank = np.zeros((280, 280), dtype=np.uint8)
        prep = get_center_of_mass_28x28(blank)
        self.assertEqual(prep.shape, (28, 28))
        self.assertTrue(np.all(prep == 0.0))

    def test_center_of_mass_stroke(self):
        canvas = np.zeros((280, 280), dtype=np.uint8)
        canvas[50:200, 130:150] = 255  # bright vertical stroke
        prep = get_center_of_mass_28x28(canvas)
        self.assertEqual(prep.shape, (28, 28))
        self.assertGreater(prep.sum(), 0.0)

    def _check_transparent_digit(self, foreground):
        alpha = np.zeros((280, 280), dtype=np.uint8)
        alpha[50:200, 130:150] = 255
        rgba = np.full((280, 280, 4), foreground, dtype=np.uint8)
        rgba[..., 3] = alpha
        background = 255 - foreground
        opaque = np.where(alpha > 0, foreground, background).astype(np.uint8)
        outputs = []
        for pixels in [rgba, opaque]:
            buffer = io.BytesIO()
            Image.fromarray(pixels).save(buffer, format='PNG')
            request = PredictRequest(image_base64=base64.b64encode(buffer.getvalue()).decode(), model_name='cnn', is_upload=True)
            outputs.append(asyncio.run(predict_digit(request)))
        self.assertEqual(outputs[0]['predicted_digit'], 1)
        self.assertEqual(outputs[0]['processed_image'], outputs[1]['processed_image'])

    def test_black_digit_transparent_png(self):
        self._check_transparent_digit(0)

    def test_white_digit_transparent_png(self):
        self._check_transparent_digit(255)

    def test_api_available_models(self):
        models = get_available_models()
        self.assertIn("models", models)
        self.assertGreater(len(models["models"]), 3)

    def test_api_predict_blank_image(self):
        blank = np.zeros((280, 280), dtype=np.uint8)
        pil_b = Image.fromarray(blank)
        buf = io.BytesIO()
        pil_b.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()

        req = PredictRequest(image_base64=b64, model_name="cnn")
        res = asyncio.run(predict_digit(req))
        self.assertEqual(res["predicted_digit"], -1)
        self.assertIn("trống", res["message"])

    def test_api_predict_sample_digit(self):
        samples = get_sample_test_digits()
        sample_digit = samples["samples"][0]  # Digit 0
        req = PredictRequest(image_base64=sample_digit["image_base64"], model_name="cnn")
        res = asyncio.run(predict_digit(req))
        self.assertIn(res["predicted_digit"], range(10))
        self.assertGreaterEqual(res["confidence"], 0.0)
        self.assertLessEqual(res["confidence"], 1.0)
        self.assertEqual(len(res["probabilities"]), 10)

    def test_api_predict_invalid_model_raises_404(self):
        """Verify that requesting a nonexistent model raises HTTP 404 (no silent fallback)."""
        from fastapi import HTTPException
        samples = get_sample_test_digits()
        sample_digit = samples["samples"][0]
        req = PredictRequest(image_base64=sample_digit["image_base64"], model_name="nonexistent_model_xyz")
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(predict_digit(req))
        self.assertEqual(ctx.exception.status_code, 404)

    def test_api_predict_svm_deskew_pca(self):
        """Verify that svm_deskew_pca endpoint works end-to-end."""
        samples = get_sample_test_digits()
        sample_digit = samples["samples"][0]
        req = PredictRequest(image_base64=sample_digit["image_base64"], model_name="svm_deskew_pca")
        res = asyncio.run(predict_digit(req))
        self.assertIn(res["predicted_digit"], range(10))
        self.assertEqual(len(res["probabilities"]), 10)
        self.assertIn(res["model_used"], ["SVM", "SVM RBF (Mới - Deskew + PCA 95%)"])


class TestSavedResultsConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import csv, json
        load_all_models()
        with (MODELS_DIR / 'results.csv').open(encoding='utf-8', newline='') as handle:
            cls.results = {r['Mô hình']: r for r in csv.DictReader(handle)}
        cls.config = json.loads((MODELS_DIR / 'selected_config.json').read_text(encoding='utf-8'))

    def test_all_five_result_rows_match_predictions(self):
        from sklearn.metrics import precision_recall_fscore_support
        with np.load(MODELS_DIR / 'predictions.npz') as saved, np.load(NPZ_DATA_PATH) as data:
            np.testing.assert_array_equal(saved['y_true'], data['y_test'])
            for name, row in self.results.items():
                pred = saved[name]
                self.assertEqual(len(pred), 10000)
                errors = int((pred != saved['y_true']).sum())
                self.assertEqual(errors, int(row['Số ảnh sai']))
                self.assertAlmostEqual(100 - errors / 100, float(row['Test Acc (%)']))
                scores = precision_recall_fscore_support(saved['y_true'], pred, average='macro', zero_division=0)[:3]
                for col, value in zip(['Precision (%)', 'Recall (%)', 'F1 (%)'], scores):
                    self.assertAlmostEqual(float(row[col]), value * 100)

    def test_cnn_checkpoint_matches_saved_predictions(self):
        import torch
        cnn = ModernCNN()
        cnn.load_state_dict(torch.load(MODELS_DIR / 'CNN.pt', map_location='cpu', weights_only=True))
        cnn.eval()
        self.assertEqual(sum(p.numel() for p in cnn.parameters()), 160074)
        with np.load(NPZ_DATA_PATH) as data, np.load(MODELS_DIR / 'predictions.npz') as saved:
            x = data['x_test'][:256].astype(np.float32) / 255
            with torch.inference_mode():
                pred = cnn(torch.from_numpy(x).unsqueeze(1)).argmax(1).numpy()
            np.testing.assert_array_equal(pred, saved['CNN'][:256])

    def test_history_matches_checkpoint_and_early_stopping(self):
        import pandas as pd
        history = pd.read_csv(MODELS_DIR / 'cnn_history.csv')
        best = history.loc[history.val_loss.idxmin()]
        self.assertEqual(int(best.epoch), self.config['cnn_best_epoch'])
        self.assertAlmostEqual(best.val_loss, self.config['cnn_best_val_loss'])
        self.assertEqual(int(history.epoch.max()), self.config['cnn_epochs_run'])
        self.assertAlmostEqual(best.val_acc * 100, float(self.results['CNN']['Val Acc (%)']))
        stop_loss, wait = float('inf'), 0
        for loss in history.val_loss:
            if loss < stop_loss - self.config['cnn_min_delta']:
                stop_loss, wait = loss, 0
            else:
                wait += 1
        self.assertEqual(wait, self.config['cnn_early_stopping_patience'])
        self.assertEqual(self.config['cnn_stop_reason'], 'early_stopping')
        self.assertEqual([self.config[k] for k in ['train', 'validation', 'test']], [50000, 10000, 10000])

    def test_backend_metadata_matches_saved_results(self):
        names = {'cnn': 'CNN', 'svm': 'SVM', 'knn': 'k-NN', 'rf': 'Random Forest', 'nb': 'Naive Bayes'}
        models = get_available_models()['models']
        self.assertEqual({m['id'] for m in models}, set(names))
        for model in models:
            row = self.results[names[model['id']]]
            self.assertEqual(model['accuracy'], f"{float(row['Test Acc (%)']):.2f}%")
            self.assertEqual(model['test_errors'], f"{int(row['Số ảnh sai']):,} / 10,000")
        cnn = next(m for m in models if m['id'] == 'cnn')
        self.assertIn(f"checkpoint epoch {self.config['cnn_best_epoch']}", cnn['hyperparameters'])
        self.assertIn(f"Early Stopping Epoch {self.config['cnn_epochs_run']}", cnn['hyperparameters'])

    def test_official_model_parameters_and_input_shapes(self):
        from app.server import MODEL_CACHE
        nb, knn, svm, rf = [MODEL_CACHE[k]['model'] for k in ['nb', 'knn', 'svm', 'rf']]
        self.assertEqual((nb.alpha, nb.binarize, nb.n_features_in_), (1.0, 0.2, 784))
        self.assertEqual((knn.n_neighbors, knn.weights, knn.n_features_in_, len(knn._fit_X)), (3, 'distance', 113, 50000))
        self.assertEqual((svm.C, svm.kernel, svm.gamma, svm.n_features_in_), (5, 'rbf', 'scale', 113))
        self.assertEqual((rf.n_estimators, rf.max_features, rf.n_features_in_, rf.random_state), (150, 'sqrt', 784, 42))

    def test_svm_confidence_handles_unavailable_predict_proba(self):
        from unittest.mock import patch
        from sklearn.exceptions import NotFittedError
        from app.server import MODEL_CACHE, prediction_scores, PCA_TRANSFORMER_DESKEW
        svm = MODEL_CACHE['svm']['model']
        with np.load(NPZ_DATA_PATH) as data:
            image = data['x_test'][:1].astype(np.float32) / 255
        features = PCA_TRANSFORMER_DESKEW.transform(deskew_dataset(image.reshape(1, 784)))
        predicted = int(svm.predict(features)[0])
        with patch.object(svm, 'predict_proba', create=True, side_effect=NotFittedError('no probability calibration')):
            scores = prediction_scores(svm, features, predicted)
        self.assertEqual(scores.shape, (10,))
        self.assertTrue(np.isfinite(scores).all())
        self.assertAlmostEqual(float(scores.sum()), 1.0)

    def test_all_official_api_predictions_and_confidence(self):
        sample = get_sample_test_digits()['samples'][0]
        for model_id in ['cnn', 'svm', 'knn', 'rf', 'nb']:
            res = asyncio.run(predict_digit(PredictRequest(image_base64=sample['image_base64'], model_name=model_id)))
            self.assertEqual(res['predicted_digit'], sample['digit'])
            self.assertEqual(len(res['probabilities']), 10)
            self.assertFalse(res['is_calibrated'])


class TestUploadedImageSegmentation(unittest.TestCase):
    def test_plain_digit_ignores_corner_artifact(self):
        from src.image_preprocessing import extract_uploaded_digit
        image = np.full((160, 120, 3), 255, dtype=np.uint8)
        image[0:2, :30] = 0
        image[40:125, 55:65] = 0
        result = extract_uploaded_digit(image)
        self.assertEqual(int(result[:5].sum()), 0)
        self.assertGreater(int(result[40:125, 55:65].sum()), 0)

    def test_photographed_ink_separates_from_grid_and_page_edge(self):
        import cv2
        from src.image_preprocessing import extract_uploaded_digit
        image = np.full((500, 400, 3), 190, dtype=np.uint8)
        for x in range(0, 400, 20):
            cv2.line(image, (x, 0), (x, 499), (155, 165, 180), 1)
        for y in range(0, 500, 20):
            cv2.line(image, (0, y), (399, y), (155, 165, 180), 1)
        cv2.putText(image, '3', (145, 320), cv2.FONT_HERSHEY_SIMPLEX, 5, (45, 55, 105), 5)
        image[:10] = 20
        result = extract_uploaded_digit(image)
        self.assertEqual(int(result[:20].sum()), 0)
        self.assertGreater(int(result[180:330, 140:260].sum()), 0)
        self.assertLess(np.count_nonzero(result), 15000)

    def test_empty_white_upload_stays_empty(self):
        from src.image_preprocessing import extract_uploaded_digit
        self.assertFalse(extract_uploaded_digit(np.full((300, 300, 3), 255, dtype=np.uint8)).any())


if __name__ == '__main__':
    unittest.main()
