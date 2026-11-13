"""
Integration & Unit Test Suite - PhishGuard AI
Menguji 18 skenario integrasi sistem, validasi input, model inference,
keamanan data leakage, dan penanganan edge cases.
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np
import joblib

from src.dashboard_utils import (
    load_model_and_metadata,
    validate_and_preprocess_input,
    run_prediction_pipeline,
    REQUIRED_FEATURES
)
from src.url_feature_extractor import extract_features_from_url

class TestPhishGuardAIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models_dir = "models"
        cls.test_csv_path = "dataset/processed/test_set.csv"
        cls.model, cls.metadata = load_model_and_metadata(cls.models_dir)
        cls.test_df = pd.read_csv(cls.test_csv_path)

    def test_01_model_loading(self):
        """Skenario 1 & 2: Model dan metadata berhasil dimuat"""
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.metadata)
        self.assertEqual(self.metadata.get("best_model_algorithm"), "Random Forest")

    def test_02_metadata_features(self):
        """Skenario 3 & 4: Fitur metadata terverifikasi 16 dimensi"""
        features = self.metadata.get("features")
        self.assertEqual(len(features), 16)
        self.assertEqual(features, REQUIRED_FEATURES)

    def test_03_valid_csv_upload_inference(self):
        """Skenario 5, 11, 12, 13: Upload CSV valid berhasil diprediksi (legitimate & phishing)"""
        sample_df = self.test_df.head(100)
        X_input, url_meta, gt, warnings = validate_and_preprocess_input(sample_df)
        self.assertEqual(len(X_input), 100)
        self.assertEqual(list(X_input.columns), REQUIRED_FEATURES)
        
        results = run_prediction_pipeline(self.model, X_input, url_meta)
        self.assertEqual(len(results), 100)
        self.assertIn("LEGITIMATE", results["Prediction"].values)
        self.assertIn("PHISHING", results["Prediction"].values)
        self.assertTrue((results["Phishing_Probability"] >= 0).all() and (results["Phishing_Probability"] <= 100).all())

    def test_04_missing_required_features_rejection(self):
        """Skenario 6: Upload CSV tanpa fitur wajib harus ditolak dengan ValueError"""
        invalid_df = pd.DataFrame({"URL": ["http://test.com"], "url_length": [15]})
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_input(invalid_df)
        self.assertIn("tidak memenuhi spesifikasi", str(ctx.exception))

    def test_05_empty_dataframe_handling(self):
        """Skenario 8: DataFrame kosong ditangani tanpa crash"""
        empty_df = pd.DataFrame(columns=REQUIRED_FEATURES + ["URL"])
        X_input, url_meta, gt, warnings = validate_and_preprocess_input(empty_df)
        self.assertEqual(len(X_input), 0)
        results = run_prediction_pipeline(self.model, X_input, url_meta)
        self.assertEqual(len(results), 0)

    def test_06_missing_values_imputation(self):
        """Skenario 9: Data dengan missing values ditangani dengan imputasi median"""
        dirty_df = self.test_df.head(20).copy()
        dirty_df.loc[0, 'url_entropy'] = np.nan
        dirty_df.loc[1, 'path_length'] = np.nan
        
        X_input, url_meta, gt, warnings = validate_and_preprocess_input(dirty_df)
        self.assertEqual(X_input.isnull().sum().sum(), 0, "Missing values harus bersih setelah imputasi")
        self.assertTrue(any("missing values" in w.lower() for w in warnings))

    def test_07_infinity_values_handling(self):
        """Skenario 10: Data dengan infinity (+inf / -inf) dinormalisasi"""
        inf_df = self.test_df.head(20).copy()
        inf_df['url_entropy'] = inf_df['url_entropy'].astype(float)
        inf_df['percentage_numeric_chars'] = inf_df['percentage_numeric_chars'].astype(float)
        inf_df.loc[0, 'url_entropy'] = np.inf
        inf_df.loc[1, 'percentage_numeric_chars'] = -np.inf
        
        X_input, url_meta, gt, warnings = validate_and_preprocess_input(inf_df)
        self.assertEqual(np.isinf(X_input.values).sum(), 0, "Infinity values harus dinormalisasi")
        self.assertTrue(any("infinity" in w.lower() for w in warnings))

    def test_08_class_label_leakage_protection(self):
        """Skenario 16: Kolom ClassLabel tidak boleh masuk ke matriks X_input"""
        leak_df = self.test_df.head(50).copy()
        self.assertIn('ClassLabel', leak_df.columns)
        
        X_input, url_meta, ground_truth, warnings = validate_and_preprocess_input(leak_df)
        self.assertNotIn('ClassLabel', X_input.columns, "ClassLabel TIDAK BOLEH berada di X_input")
        self.assertIsNotNone(ground_truth)
        self.assertTrue(any("classlabel" in w.lower() for w in warnings))

    def test_09_url_metadata_preservation(self):
        """Skenario 17: Kolom URL dipertahankan sebagai metadata identitas"""
        sample_df = self.test_df.head(10).copy()
        X_input, url_meta, ground_truth, warnings = validate_and_preprocess_input(sample_df)
        self.assertNotIn('URL', X_input.columns)
        self.assertEqual(len(url_meta), 10)
        self.assertEqual(url_meta.iloc[0], sample_df['URL'].iloc[0])

    def test_10_heuristic_url_feature_extractor(self):
        """Skenario 18: Modul ekstraksi URL mentah menghasilkan 16 fitur kompatibel"""
        test_url = "https://www.google.com/search?q=cybersecurity"
        feat_dict = extract_features_from_url(test_url)
        self.assertEqual(len(feat_dict), 16)
        for rf in REQUIRED_FEATURES:
            self.assertIn(rf, feat_dict)
            
        # Uji prediksi langsung
        X_single = pd.DataFrame([feat_dict])[REQUIRED_FEATURES]
        pred = self.model.predict(X_single)
        self.assertIn(pred[0], [0, 1])

if __name__ == "__main__":
    unittest.main()

