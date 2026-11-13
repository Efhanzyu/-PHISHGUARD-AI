"""
Modul Utilitas Dashboard PhishGuard AI (Security-Hardened Version 2.0)
Menyediakan fungsi validasi CSV, pencegahan DoS/Resource Exhaustion,
sanitasi ketat CSV Formula Injection (CWE-1236), proteksi Path Traversal (CWE-22),
dan mitigasi Data Leakage.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List

REQUIRED_FEATURES = [
    'url_length', 'has_ip_address', 'dot_count', 'https_flag',
    'url_entropy', 'token_count', 'subdomain_count', 'query_param_count',
    'tld_length', 'path_length', 'has_hyphen_in_domain', 'number_of_digits',
    'tld_popularity', 'suspicious_file_extension', 'domain_name_length',
    'percentage_numeric_chars'
]

# Batas Keamanan Sistem (DoS & Resource Exhaustion Mitigation)
MAX_ALLOWED_ROWS = 50_000
MAX_URL_STRING_LENGTH = 2048

def safe_resolve_path(base_dir: str, target_filename: str) -> str:
    """
    Mitigasi Path Traversal (CWE-22) menggunakan canonical path dan os.path.commonpath.
    Memastikan file target benar-benar berada di dalam base_dir dan bukan direktori lain.
    """
    base_canonical = os.path.realpath(os.path.abspath(base_dir))
    target_canonical = os.path.realpath(os.path.abspath(os.path.join(base_canonical, target_filename)))
    
    # Verifikasi bahwa base_canonical adalah common ancestor path
    if os.path.commonpath([base_canonical, target_canonical]) != base_canonical:
        raise PermissionError(
            f"Path Traversal Attack Terdeteksi: Akses ke luar direktori '{base_dir}' ditolak."
        )
    return target_canonical

def load_model_and_metadata(models_dir: str = "models") -> Tuple[Any, Dict[str, Any]]:
    """
    Memuat model terbaik dan file metadata secara aman dari path lokal terverifikasi.
    Menggunakan safe_resolve_path dengan os.path.commonpath.
    """
    model_path = safe_resolve_path(models_dir, "best_model.joblib")
    meta_path = safe_resolve_path(models_dir, "model_metadata.json")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Artefak model internal tidak ditemukan di: {model_path}")
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"Metadata model internal tidak ditemukan di: {meta_path}")
        
    model = joblib.load(model_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        
    return model, metadata

def sanitize_csv_formula_injection(val: Any) -> Any:
    """
    Mitigasi Komprehensif CSV Formula Injection (CWE-1236).
    Menangani:
      1. Formula langsung: =1+1, +1+1, -1+1, @SUM(A1:A2)
      2. Karakter pemicu kontrol: \t (tab), \r (carriage return)
      3. Whitespace tersembunyi sebelum formula: '  =1+1', '   @SUM'
    """
    if isinstance(val, str):
        # Periksa string setelah lstrip untuk mendeteksi formula dengan leading whitespace
        stripped = val.lstrip()
        if len(stripped) > 0 and stripped[0] in ('=', '+', '-', '@', '\t', '\r'):
            # Prepend tanda kutip tunggal jika belum ada
            if not val.startswith("'"):
                return "'" + val
    return val

def validate_and_preprocess_input(df_uploaded: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.Series, List[str]]:
    """
    Memvalidasi DataFrame input dari upload CSV secara ketat.
    1. Membatasi ukuran baris (Anti-DoS maks 50.000 baris).
    2. Membersihkan nama kolom & memvalidasi 16 fitur wajib.
    3. Mengabaikan kolom asing/tidak dikenal secara aman tanpa merusak input model.
    4. Proteksi Data Leakage (drop ClassLabel dari matriks prediktor X).
    5. Imputasi median untuk missing values & normalisasi infinity/tipe data invalid.
    6. Sanitasi Formula Injection untuk kolom teks.
    """
    warnings = []
    
    # 1. Validasi Batas Jumlah Baris (Mitigasi Resource Exhaustion)
    total_rows = len(df_uploaded)
    if total_rows > MAX_ALLOWED_ROWS:
        raise ValueError(
            f"Jumlah baris ({total_rows:,}) melampaui batas keamanan maksimum ({MAX_ALLOWED_ROWS:,} baris). "
            "Silakan kurangi ukuran batch data untuk mencegah kegagalan alokasi memori (Resource Exhaustion)."
        )
    
    # 2. Bersihkan spasi pada nama kolom
    df = df_uploaded.copy()
    df.columns = [str(c).strip() for c in df.columns]
    
    # 3. Deteksi kolom asing / tak dikenal
    known_cols = set(REQUIRED_FEATURES + ['URL', 'ClassLabel'])
    unknown_cols = [c for c in df.columns if c not in known_cols]
    if unknown_cols:
        warnings.append(f"Ditemukan {len(unknown_cols)} kolom tidak dikenal yang diabaikan secara aman: {', '.join(unknown_cols[:5])}...")
        
    # 4. Cek metadata URL dan sanitasi formula injection
    if 'URL' in df.columns:
        sanitized_urls = df['URL'].astype(str).str.slice(0, MAX_URL_STRING_LENGTH)
        sanitized_urls = sanitized_urls.apply(sanitize_csv_formula_injection)
        url_meta = sanitized_urls
    else:
        url_meta = pd.Series([f"Row_{i+1}" for i in range(len(df))], name="URL_ID")
        warnings.append("Kolom 'URL' tidak ditemukan. Sistem menggunakan ID Baris sebagai penanda identitas.")
        
    # 5. Cek Ground Truth (ClassLabel) dan proteksi data leakage
    ground_truth = None
    if 'ClassLabel' in df.columns:
        try:
            ground_truth = df['ClassLabel'].copy()
            warnings.append("Kolom 'ClassLabel' terdeteksi: Digunakan semata sebagai Ground Truth verifikasi. Kolom ini DIKELUARKAN dari fitur input untuk mencegah Data Leakage.")
        except Exception:
            ground_truth = None
            
    # 6. Validasi keberadaan 16 fitur wajib
    missing_cols = [col for col in REQUIRED_FEATURES if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"File CSV tidak memenuhi spesifikasi model. Fitur berikut tidak ditemukan: {', '.join(missing_cols)}"
        )
        
    # 7. Ambil HANYA 16 fitur wajib sesuai urutan model (Kolom asing di-exclude)
    X_input = df[REQUIRED_FEATURES].copy()
    
    # 8. Validasi tipe data dan penanganan Missing, Infinity, dan Tipe Data Tak Valid
    for col in REQUIRED_FEATURES:
        X_input[col] = pd.to_numeric(X_input[col], errors='coerce')
        
    # Periksa missing values & imputasi median
    null_counts = X_input.isnull().sum()
    if null_counts.sum() > 0:
        imputed_cols = []
        for col in REQUIRED_FEATURES:
            if null_counts[col] > 0:
                median_val = X_input[col].median()
                X_input[col] = X_input[col].fillna(median_val if not np.isnan(median_val) else 0)
                imputed_cols.append(f"{col} ({null_counts[col]} baris diimputasi median)")
        warnings.append(f"Missing values / data non-numerik dinormalisasi via median imputation: {', '.join(imputed_cols)}")
        
    # Periksa infinite values
    inf_mask = np.isinf(X_input.values)
    if inf_mask.sum() > 0:
        X_input = X_input.replace([np.inf, -np.inf], np.nan)
        X_input = X_input.fillna(0)
        warnings.append("Nilai Infinity (+inf / -inf) dinormalisasi ke batas skalar numerik riil.")
        
    return X_input, url_meta, ground_truth, warnings

def run_prediction_pipeline(model: Any, X_input: pd.DataFrame, url_meta: pd.Series) -> pd.DataFrame:
    """
    Menjalankan inferensi model dan mengembalikan DataFrame hasil lengkap.
    Menangani DataFrame kosong dengan aman.
    """
    if len(X_input) == 0:
        return pd.DataFrame({
            "URL": [],
            "Prediction": [],
            "Predicted_Class": [],
            "Phishing_Probability": [],
            "Confidence_Score": []
        })

    # Prediksi kelas
    y_pred = model.predict(X_input)
    
    # Prediksi probabilitas
    if hasattr(model, "predict_proba"):
        prob_matrix = model.predict_proba(X_input)
        phishing_prob = prob_matrix[:, 1]
    else:
        phishing_prob = np.where(y_pred == 1, 1.0, 0.0)
        
    # Susun DataFrame hasil dengan proteksi sanitasi
    results_df = pd.DataFrame({
        "URL": url_meta.values,
        "Prediction": ["PHISHING" if p == 1 else "LEGITIMATE" for p in y_pred],
        "Predicted_Class": y_pred,
        "Phishing_Probability": np.round(phishing_prob * 100, 2),
        "Confidence_Score": np.round(np.max(prob_matrix, axis=1) * 100, 2) if hasattr(model, "predict_proba") else 100.0
    })
    
    return results_df
