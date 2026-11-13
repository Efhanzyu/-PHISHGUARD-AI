"""
Comprehensive Security Verification Test Suite - PhishGuard AI
Memverifikasi:
 1. Path Traversal Protection (safe_resolve_path & os.path.commonpath)
 2. Insecure Deserialization & Trusted Model Isolation
 3. CSV Formula Injection Variations (=, +, -, @, leading whitespace, tab, cr)
 4. File Upload Limits (20 MB config audit)
 5. Maximum Rows Protection (50,000 rows DoS limit)
 6. Unknown / Malicious Extra Columns Handling
 7. Robust Data Validation (NaN, Inf, Invalid non-numeric strings)
 8. Offline Processing & Zero SSRF Verification
 9. Git Repository Secrets & Credential Leakage Audit
"""

import os
import sys
import socket
import unittest
import pandas as pd
import numpy as np

from src.dashboard_utils import (
    load_model_and_metadata,
    safe_resolve_path,
    validate_and_preprocess_input,
    sanitize_csv_formula_injection,
    MAX_ALLOWED_ROWS,
    REQUIRED_FEATURES
)
from src.url_feature_extractor import extract_features_from_url

class TestPhishGuardFinalSecurity(unittest.TestCase):
    def test_01_path_traversal_commonpath_protection(self):
        """Memverifikasi bahwa safe_resolve_path menolak path traversal sequence (../, etc.)"""
        base_models_dir = "models"
        
        # 1. Path valid dalam direktori harus berhasil
        valid_path = safe_resolve_path(base_models_dir, "best_model.joblib")
        self.assertTrue(os.path.exists(valid_path))
        
        # 2. Percobaan path traversal keluar dari base dir harus memicu PermissionError
        traversal_attempts = [
            "../app.py",
            "../../Windows/System32/cmd.exe",
            "..\\..\\boot.ini",
            "/etc/passwd",
            "subdir/../../app.py"
        ]
        for attempt in traversal_attempts:
            with self.assertRaises(PermissionError, msg=f"Gagal memblokir path traversal: {attempt}"):
                safe_resolve_path(base_models_dir, attempt)

    def test_02_joblib_trusted_model_isolation(self):
        """Memverifikasi bahwa model yang dimuat adalah model resmi terisolasi dan valid"""
        model, metadata = load_model_and_metadata("models")
        self.assertIsNotNone(model)
        self.assertEqual(metadata.get("best_model_algorithm"), "Random Forest")
        self.assertEqual(metadata.get("project_name"), "PhishGuard AI")
        
        # Pastikan model dapat melakukan prediksi pada 16 fitur
        dummy_input = pd.DataFrame([[0]*16], columns=REQUIRED_FEATURES)
        pred = model.predict(dummy_input)
        self.assertIn(pred[0], [0, 1])

    def test_03_csv_formula_injection_variations(self):
        """Memverifikasi seluruh variasi formula injection (=, +, -, @, leading whitespace, tab, cr)"""
        variations = [
            "=1+1",
            "+1+1",
            "-1+1",
            "@SUM(A1:A2)",
            " =1+1",             # Leading space
            "   +1+1",           # Multiple spaces
            "\t-1+1",            # Tab
            "\r@SUM(A1:A2)",     # Carriage return
            "  \t =cmd|' /C calc'!A0"
        ]
        for payload in variations:
            sanitized = sanitize_csv_formula_injection(payload)
            self.assertTrue(sanitized.startswith("'"), f"Payload variasi {repr(payload)} gagal disanitasi: {repr(sanitized)}")
            
        # Pastikan URL normal yang valid tidak dirusak
        safe_url = "https://legitimate-bank.com/account"
        self.assertEqual(sanitize_csv_formula_injection(safe_url), safe_url)

    def test_04_streamlit_upload_size_limit_config(self):
        """Memverifikasi batas 20 MB pada konfigurasi .streamlit/config.toml"""
        config_path = os.path.join(".streamlit", "config.toml")
        self.assertTrue(os.path.exists(config_path), "File .streamlit/config.toml tidak ditemukan!")
        
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("maxUploadSize = 20", content, "Batas upload 20 MB tidak dikonfigurasi di config.toml!")
        self.assertIn("enableXsrfProtection = true", content, "XSRF protection belum aktif!")

    def test_05_csv_over_50k_rows_dos_protection(self):
        """Memverifikasi bahwa masukan > 50.000 baris ditolak seketika (Anti-Resource Exhaustion)"""
        mock_df = pd.DataFrame(index=range(MAX_ALLOWED_ROWS + 1), columns=REQUIRED_FEATURES)
        with self.assertRaises(ValueError) as ctx:
            validate_and_preprocess_input(mock_df)
        self.assertIn("melampaui batas keamanan", str(ctx.exception))

    def test_06_unknown_columns_handling(self):
        """Memverifikasi bahwa kolom asing / tak dikenal diabaikan dan tidak merusak matriks model"""
        df_with_extra = pd.DataFrame({
            col: [1] for col in REQUIRED_FEATURES
        })
        df_with_extra["unknown_malicious_col"] = ["DROP TABLE"]
        df_with_extra["another_junk_col"] = [9999]
        df_with_extra["URL"] = ["http://safe.com"]
        
        X_input, url_meta, gt, warnings = validate_and_preprocess_input(df_with_extra)
        # Matriks X_input HANYA boleh berisi 16 fitur wajib
        self.assertEqual(list(X_input.columns), REQUIRED_FEATURES)
        self.assertNotIn("unknown_malicious_col", X_input.columns)
        self.assertTrue(any("tidak dikenal" in w.lower() for w in warnings))

    def test_07_nan_inf_and_invalid_data_types(self):
        """Memverifikasi penanganan nilai NaN, Infinity, dan tipe data string pada fitur numerik"""
        dirty_df = pd.DataFrame({
            col: [10.0] for col in REQUIRED_FEATURES
        })
        # Ubah ke object agar dapat memuat string tak valid seperti membaca CSV kotor
        dirty_df['dot_count'] = dirty_df['dot_count'].astype(object)
        dirty_df.loc[0, 'url_length'] = np.nan
        dirty_df.loc[0, 'url_entropy'] = np.inf
        dirty_df.loc[0, 'percentage_numeric_chars'] = -np.inf
        dirty_df.loc[0, 'dot_count'] = "not_a_number_string" # String tidak valid
        
        X_input, url_meta, gt, warnings = validate_and_preprocess_input(dirty_df)
        # Seluruh nilai di X_input harus finite numerik
        self.assertEqual(X_input.isnull().sum().sum(), 0, "Missing values atau string gagal dinormalisasi!")
        self.assertEqual(np.isinf(X_input.values).sum(), 0, "Infinity values gagal dinormalisasi!")
        self.assertTrue(np.issubdtype(X_input['dot_count'].dtype, np.number))

    def test_08_offline_processing_zero_ssrf(self):
        """Memverifikasi bahwa proses ekstraksi URL 100% offline tanpa koneksi HTTP (Zero SSRF)"""
        original_socket = socket.socket
        socket_called = []
        
        def mock_socket(*args, **kwargs):
            socket_called.append(True)
            raise RuntimeError("SSRF ALERT: Inisialisasi socket jaringan terdeteksi!")
            
        try:
            socket.socket = mock_socket
            test_urls = [
                "http://169.254.169.254/metadata",
                "http://localhost:8505/admin",
                "http://127.0.0.1:22",
                "https://phishing-site.xyz/login.php"
            ]
            for u in test_urls:
                res = extract_features_from_url(u)
                self.assertEqual(len(res), 16)
                
            self.assertEqual(len(socket_called), 0, "Socket jaringan dipanggil saat ekstraksi URL!")
        finally:
            socket.socket = original_socket

    def test_09_github_repo_credential_leak_scan(self):
        """Memindai seluruh file yang berpotensi masuk ke git terhadap kebocoran kunci / kredensial"""
        disallowed_filenames = [".env", "secrets.toml", "id_rsa", "credentials.json"]
        found_leaks = []
        
        for root, dirs, files in os.walk("."):
            if any(skip in root for skip in [".venv", "venv", ".git"]):
                continue
            for f in files:
                if f in disallowed_filenames:
                    found_leaks.append(os.path.join(root, f))
                    
        self.assertEqual(len(found_leaks), 0, f"Ditemukan file kredensial sensitif: {found_leaks}")

if __name__ == "__main__":
    unittest.main()
