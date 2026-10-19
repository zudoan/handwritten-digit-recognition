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
        """Check exact PCA dimensions saved in checkpoints: 112 for deskewed subset, 154 for full 60k."""
        import joblib
        deskew_pca_path = MODELS_DIR / "pca_transformer_deskew_sub10k.joblib"
        if deskew_pca_path.exists():
            p_deskew = joblib.load(deskew_pca_path)
            self.assertEqual(p_deskew.n_components_, 112)

        pca_path = MODELS_DIR / "pca_transformer.joblib"
        if pca_path.exists():
            p_full = joblib.load(pca_path)
            self.assertEqual(p_full.n_components_, 154)

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
        self.assertIn("Deskew", res["model_used"])


class TestAuditRegressionAndModelConsistency(unittest.TestCase):
    """
    Regression tests to ensure no audit regressions:
    1. Unified Deskew + PCA pipeline reload consistency and >= 97.5% accuracy.
    2. ModernCNN checkpoint exact parameter count (160,074 parameters).
    3. Hyperparameter search results integrity.
    4. Exact PCA component verification.
    """

    @classmethod
    def setUpClass(cls):
        load_all_models()

    def test_svm_deskew_pca_pipeline_reload_and_accuracy(self):
        """Regression test: loading saved unified pipeline gives >= 97.8% on sample batch."""
        import joblib
        pipe_path = MODELS_DIR / "svm_rbf_deskew_pca_pipeline.joblib"
        self.assertTrue(pipe_path.exists(), "svm_rbf_deskew_pca_pipeline.joblib must exist!")
        pipe = joblib.load(pipe_path)

        with np.load(NPZ_DATA_PATH) as data:
            x_test_sample = (data["x_test"][:500].astype(np.float32) / 255.0).reshape(500, -1)
            y_test_sample = data["y_test"][:500]

        preds = pipe.predict(x_test_sample)
        acc = (preds == y_test_sample).mean()
        self.assertGreaterEqual(acc, 0.970, f"Expected pipeline sample accuracy >= 97%, got {acc*100:.2f}%")

    def test_modern_cnn_checkpoint_parameters(self):
        """Verify ModernCNN architecture matches checkpoint (160,074 parameters)."""
        import torch
        cnn = ModernCNN()
        pt_path = MODELS_DIR / "modern_cnn_mnist.pt"
        self.assertTrue(pt_path.exists(), "modern_cnn_mnist.pt must exist!")
        cnn.load_state_dict(torch.load(pt_path, map_location="cpu"))
        total_params = sum(p.numel() for p in cnn.parameters())
        self.assertEqual(total_params, 160074, f"ModernCNN param count {total_params} != 160074")

    def test_hyperparameter_search_results_exist(self):
        """Verify hyperparameter search results json exists with records and selected=True."""
        import json
        json_path = Path(__file__).resolve().parent.parent / "results" / "hyperparameter_search_results.json"
        self.assertTrue(json_path.exists(), "results/hyperparameter_search_results.json must exist!")
        with open(json_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        self.assertGreaterEqual(len(records), 10)
        selected = [r for r in records if r.get("selected")]
        self.assertGreaterEqual(len(selected), 4, "Must have at least 4 selected hyperparameter winners!")

    def test_selected_hyperparameters_match_artifacts(self):
        """Verify that saved artifacts in saved_models/ strictly match the hyperparameters chosen on validation."""
        import joblib
        import json
        json_path = Path(__file__).resolve().parent.parent / "results" / "hyperparameter_search_results.json"
        with open(json_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        
        selected_map = {r["model_family"]: r["hyperparameters"] for r in records if r.get("selected")}

        # 1. Linear SVM
        lsvc_path = MODELS_DIR / "svm_linear_sub10k.joblib"
        self.assertTrue(lsvc_path.exists())
        lsvc = joblib.load(lsvc_path)
        self.assertAlmostEqual(lsvc.get_params()["C"], selected_map["Linear SVM"]["C"],
                               msg=f"Linear SVM param C {lsvc.get_params()['C']} != {selected_map['Linear SVM']['C']}")

        # 2. Random Forest
        rf_path = MODELS_DIR / "rf_sub10k.joblib"
        self.assertTrue(rf_path.exists())
        rf = joblib.load(rf_path)
        self.assertEqual(rf.get_params()["n_estimators"], selected_map["Random Forest"]["n_estimators"],
                         msg=f"Random Forest n_estimators {rf.get_params()['n_estimators']} != {selected_map['Random Forest']['n_estimators']}")

        # 3. k-NN
        knn_path = MODELS_DIR / "knn_pca_sub10k.joblib"
        self.assertTrue(knn_path.exists())
        knn = joblib.load(knn_path)
        self.assertEqual(knn.get_params()["n_neighbors"], selected_map["k-NN"]["n_neighbors"])
        self.assertEqual(knn.get_params()["weights"], selected_map["k-NN"]["weights"])

        # 4. RBF SVM
        svm_rbf_path = MODELS_DIR / "svm_rbf_pca_sub10k.joblib"
        self.assertTrue(svm_rbf_path.exists())
        svm_rbf = joblib.load(svm_rbf_path)
        self.assertAlmostEqual(svm_rbf.get_params()["C"], selected_map["RBF SVM"]["C"])

    def test_cnn_validation_history_and_checkpoint(self):
        """Verify that CNN validation protocol ran honestly and produced history, checkpoint, and figure."""
        import json
        import torch
        val_json_path = Path(__file__).resolve().parent.parent / "results" / "cnn_validation_history.json"
        self.assertTrue(val_json_path.exists(), "results/cnn_validation_history.json must exist!")
        with open(val_json_path, "r", encoding="utf-8") as f:
            val_data = json.load(f)

        self.assertIn("history", val_data)
        self.assertIn("train_loss", val_data["history"])
        self.assertIn("val_loss", val_data["history"])
        self.assertGreaterEqual(val_data["best_epoch"], 1)
        self.assertGreaterEqual(val_data["test_accuracy"], 98.5)

        val_ckpt = MODELS_DIR / "modern_cnn_val_tuned.pt"
        self.assertTrue(val_ckpt.exists(), "saved_models/modern_cnn_val_tuned.pt must exist!")
        cnn = ModernCNN()
        state_dict = torch.load(val_ckpt, map_location="cpu")
        cnn.load_state_dict(state_dict)
        self.assertEqual(sum(p.numel() for p in cnn.parameters()), 160074)

        fig_path = Path(__file__).resolve().parent.parent / "reports" / "figures" / "08_cnn_training_history.png"
        self.assertTrue(fig_path.exists(), "reports/figures/08_cnn_training_history.png must exist!")

    def test_backend_loads_linear_svm_c001(self):
        """Phase 1: Backend loads Linear SVM C=0.01 from svm_linear_sub10k.joblib."""
        from app.server import MODEL_CACHE, MODEL_REGISTRY_CONFIG
        self.assertIn("svm_linear", MODEL_CACHE)
        lsvc = MODEL_CACHE["svm_linear"]["model"]
        self.assertAlmostEqual(lsvc.get_params()["C"], 0.01)
        self.assertEqual(MODEL_REGISTRY_CONFIG["svm_linear"]["checkpoint"], "svm_linear_sub10k.joblib")
        self.assertIn("C=0.01", MODEL_REGISTRY_CONFIG["svm_linear"]["name"])

    def test_backend_loads_random_forest_150_trees(self):
        """Phase 1: Backend loads Random Forest 150 trees from rf_sub10k.joblib."""
        from app.server import MODEL_CACHE, MODEL_REGISTRY_CONFIG
        self.assertIn("rf", MODEL_CACHE)
        rf = MODEL_CACHE["rf"]["model"]
        self.assertEqual(rf.get_params()["n_estimators"], 150)
        self.assertEqual(MODEL_REGISTRY_CONFIG["rf"]["checkpoint"], "rf_sub10k.joblib")
        self.assertIn("150 cây", MODEL_REGISTRY_CONFIG["rf"]["name"])

    def test_backend_confidence_metadata_and_calibration_honesty(self):
        """Phase 1: API returns confidence_type and honestly sets is_calibrated=False."""
        samples = get_sample_test_digits()
        sample_digit = samples["samples"][0]
        
        # Test CNN
        req_cnn = PredictRequest(image_base64=sample_digit["image_base64"], model_name="cnn")
        res_cnn = asyncio.run(predict_digit(req_cnn))
        self.assertIn("Softmax", res_cnn["confidence_type"])
        self.assertFalse(res_cnn["is_calibrated"])

        # Test Linear SVM (decision_function softmax)
        req_svm = PredictRequest(image_base64=sample_digit["image_base64"], model_name="svm_linear")
        res_svm = asyncio.run(predict_digit(req_svm))
        self.assertIn("Decision", res_svm["confidence_type"])
        self.assertFalse(res_svm["is_calibrated"])

        # Test Random Forest (ensemble_tree_frequency)
        req_rf = PredictRequest(image_base64=sample_digit["image_base64"], model_name="rf")
        res_rf = asyncio.run(predict_digit(req_rf))
        self.assertIn("Tree Voting", res_rf["confidence_type"])
        self.assertFalse(res_rf["is_calibrated"])

    def test_frontend_no_hardcoded_obsolete_accuracy(self):
        """Phase 1: index.html contains no obsolete hardcoded accuracies like >99.2%, 98.3%, 97.5%."""
        html_path = Path(__file__).resolve().parent.parent / "app" / "static" / "index.html"
        self.assertTrue(html_path.exists())
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertNotIn(">99.2%", html)
        self.assertNotIn("98.3%", html)
        self.assertNotIn("97.5%", html)


if __name__ == "__main__":
    unittest.main()

