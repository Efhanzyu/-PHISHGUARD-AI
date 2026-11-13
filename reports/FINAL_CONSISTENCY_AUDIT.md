# PHISHGUARD AI — FINAL CONSISTENCY AUDIT REPORT
**Mata Kuliah:** Keamanan Informasi (Semester 5) — Ujian Akhir Semester (UAS)  
**Dokumen:** Laporan Audit Konsistensi Artefak & Integritas Menyeluruh Sistem  
**Tanggal Evaluasi:** 12 November 2026  
**Auditor:** Cyber Intelligence Data Integrity & Security Audit Agent  
**Status Evaluasi:** **100% PASS (ALL ARTIFACTS SYSTEMATICALLY CONSISTENT & VERIFIED)**  

---

## 1. RINGKASAN EKSEKUTIF AUDIT KONSISTENSI

Audit Konsistensi Terakhir (*Final Consistency Audit*) ini dilakukan untuk menjamin validitas, keterpaduan, dan sinkronisasi 100% antara file fisik dataset, model Machine Learning, metadata konfigurasi, laporan akademik, serta pipeline inferensi antarmuka Streamlit pasca-koreksi jumlah sampel.

Berdasarkan hasil pengujian empiris dan verifikasi komputasi matematis:
- **Jumlah Baris Fisik:** Clean = **100.872**, Train = **80.697**, Test = **20.175** ($80.697 + 20.175 = 100.872$). Selisih: **0 (NOL)**.
- **Pemisahan Partisi (Set Theory):** Overlap URL antara Train dan Test = **0 (Zero Leakage)**. Gabungan (Union) Train + Test **100% identik** dengan Clean Dataset.
- **Konsistensi Artefak Metadata:** Nilai pada `model_metadata.json`, `metrics.json`, `FINAL_PROJECT_AUDIT.md`, dan `data_splitting_report.txt` telah tersinkronisasi sempurna tanpa kontradiksi.
- **Pipeline Fitur:** 16 fitur prediktor leksikal terbukti identik antara `best_model.joblib`, `model_metadata.json`, dan modul ekstraktor URL (`extract_features_from_url`).
- **Pencegahan Data Leakage:** Target `ClassLabel` dan identifier `URL` terverifikasi **TIDAK PERNAH** masuk ke dalam matriks input inferensi.
- **Reproduksibilitas Metrik Evaluasi:** Evaluasi ulang model Random Forest pada test set aktual (20.175 sampel) menghasilkan metrik yang **identik hingga digit presisi terakhir (selisih = 0.00000000)** dengan `reports/metrics.json`.
- **Ketahanan Kode Evaluasi:** Fallback hardcoded `80697` pada `src/evaluate_model.py` telah diganti dengan verifikasi keberadaan file fisik dinamis `train_set.csv` (melempar `FileNotFoundError` eksplisit bila file tidak ada).
- **Pengujian Otomatis:**
  - **Functional Integration Tests:** `10 / 10 PASS` (2.36 detik)
  - **Security Hardening Tests:** `9 / 9 PASS` (2.31 detik)

---

## 2. HASIL VERIFIKASI 9 POIN AUDIT

### 📋 Poin 1: Verifikasi Jumlah Baris Fisik Dataset

| File Dataset | Path Disk | Ukuran File | Jumlah Baris Data | Kolom | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Clean Features** | `dataset/processed/clean_url_features.csv` | 9.013.861 bytes | **100.872** | 18 | `PASS` |
| **Training Set** | `dataset/processed/train_set.csv` | 7.209.369 bytes | **80.697** | 18 | `PASS` |
| **Testing Set** | `dataset/processed/test_set.csv` | 1.804.759 bytes | **20.175** | 18 | `PASS` |
| **Kombinasi Train + Test** | *Penggabungan Fisik* | - | **100.872** | 18 | `PASS` |
| **Selisih (Delta)** | *Train + Test - Clean* | - | **0 (NOL)** | - | `PERFECT` |

---

### 📋 Poin 2: Audit Data Leakage & Tumpang Tindih (Overlap)

Uji relasi himpunan terhadap kolom identitas `URL`:
* **Unique URLs di Clean Dataset:** `100.872` URL unik.
* **Unique URLs di Training Set:** `80.697` URL unik.
* **Unique URLs di Testing Set:** `20.175` URL unik.
* **Irisan URL Train & Test:** $\text{Train} \cap \text{Test} = \mathbf{0}$ (NOL / Zero Overlap).
* **Gabungan URL Train & Test:** $\text{Train} \cup \text{Test} = \mathbf{100.872}$ URL.
* **Status Kesamaan Himpunan:** $\text{Union} == \text{Clean} \rightarrow \mathbf{True}$.
* **Data Hilang / Ekstra:** **0 baris**.
* **Kesimpulan:** **PASS (ZERO DATA LEAKAGE)**.

---

### 📋 Poin 3: Pencocokan Jumlah Sampel Antar-Artefak

| Dokumen / Artefak | Sampel Clean | Sampel Training | Sampel Testing | Status Sinkronisasi |
| :--- | :---: | :---: | :---: | :---: |
| [`models/model_metadata.json`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/models/model_metadata.json) | 100.872 | 80.697 | 20.175 | **KONSISTEN 100%** |
| [`reports/metrics.json`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/reports/metrics.json) (TN+FP+FN+TP) | - | - | 20.175 (12698+1+12+7464) | **KONSISTEN 100%** |
| [`reports/FINAL_PROJECT_AUDIT.md`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/reports/FINAL_PROJECT_AUDIT.md) | 100.872 | 80.697 | 20.175 | **KONSISTEN 100%** |
| [`reports/data_splitting_report.txt`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/reports/data_splitting_report.txt) | 100.872 | 80.697 | 20.175 | **KONSISTEN 100%** |

*Catatan:* Angka lama `80.700` terbukti sudah **NIL (0 kemunculan)** pada seluruh file artefak audit dan metadata.

---

### 📋 Poin 4: Konsistensi 16 Fitur Prediktor

Pemeriksaan keselarasan daftar 16 fitur numerik pada 3 lapisan sistem:
1. **Fitur pada Model Scikit-Learn (`best_model.feature_names_in_`):** 16 fitur.
2. **Fitur pada Metadata (`model_metadata.json['features']`):** 16 fitur.
3. **Fitur pada Modul Ekstraksi (`extract_features_from_url`):** 16 fitur.

Daftar 16 fitur terverifikasi urutan dan penamaannya identik:
1. `url_length`
2. `has_ip_address`
3. `dot_count`
4. `https_flag`
5. `url_entropy`
6. `token_count`
7. `subdomain_count`
8. `query_param_count`
9. `tld_length`
10. `path_length`
11. `has_hyphen_in_domain`
12. `number_of_digits`
13. `tld_popularity`
14. `suspicious_file_extension`
15. `domain_name_length`
16. `percentage_numeric_chars`

*Hasil:* **PASS (16/16 Fitur Sinkron Sempurna)**.

---

### 📋 Poin 5: Audit Eksklusi Target `ClassLabel`

* Kolom `ClassLabel` dalam `model.feature_names_in_`: **False** (Tidak Ada).
* Kolom `ClassLabel` dalam `model_metadata.json['features']`: **False** (Tidak Ada).
* Kolom `URL` dalam `model.feature_names_in_`: **False** (Tidak Ada).
* Eksklusi dinamis pada `src/dashboard_utils.py`: `df = df.drop(columns=['ClassLabel'])` terbukti aktif pada inferensi batch.
* *Hasil:* **PASS (Tidak Ada Target Leakage)**.

---

### 📋 Poin 6: Verifikasi Metrik Evaluasi Aktual vs Tersimpan

Pengujian ulang inferensi model `models/best_model.joblib` terhadap data uji fisik `dataset/processed/test_set.csv` (20.175 baris):

| Parameter Metrik | Hasil Komputasi Uji Aktual | Nilai Tersimpan di `reports/metrics.json` | Selisih (Delta) | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | 0.999355638166 | 0.999355638166 | **0.0000000000** | `PASS` |
| **Precision** | 0.999866041527 | 0.999866041527 | **0.0000000000** | `PASS` |
| **Recall** | 0.998394863563 | 0.998394863563 | **0.0000000000** | `PASS` |
| **F1-Score** | 0.999129910983 | 0.999129910983 | **0.0000000000** | `PASS` |
| **ROC-AUC** | 0.999995439115 | 0.999995439115 | **0.0000000000** | `PASS` |
| **True Negative (TN)** | 12.698 | 12.698 | **0** | `PASS` |
| **False Positive (FP)** | 1 | 1 | **0** | `PASS` |
| **False Negative (FN)** | 12 | 12 | **0** | `PASS` |
| **True Positive (TP)** | 7.464 | 7.464 | **0** | `PASS` |

*Hasil:* **PASS (Reproduksibilitas 100% Deterministik)**.

---

### 📋 Poin 7: Penghapusan Fallback Hardcoded pada `src/evaluate_model.py`

* **Pemeriksaan:** File [`src/evaluate_model.py`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/src/evaluate_model.py#L51-L56) telah diperiksa.
* **Perbaikan:** Angka statis `80697` pada fallback telah dieliminasi sepenuhnya. Kode kini memvalidasi keberadaan `train_set.csv` secara ketat:
  ```python
  train_csv_path = os.path.join(os.path.dirname(test_csv_path), "train_set.csv")
  if not os.path.exists(train_csv_path):
      raise FileNotFoundError(
          f"File data training aktual tidak ditemukan di: {train_csv_path}. "
          "Evaluasi memerlukan train_set.csv untuk memverifikasi metadata."
      )
  train_df = pd.read_csv(train_csv_path)
  ...
  "train_samples": len(train_df),
  ```
* *Hasil:* **PASS (Zero Hardcoded Fallback, Strict Error Raising Active)**.

---

### 📋 Poin 8: Hasil Pengujian Otomatis (Re-Execution Proof)

#### A. Functional Integration Tests (`src/test_integration.py`)
```text
test_01_model_loading ... ok
test_02_metadata_features ... ok
test_03_valid_csv_upload_inference ... ok
test_04_missing_required_features_rejection ... ok
test_05_empty_dataframe_handling ... ok
test_06_missing_values_imputation ... ok
test_07_infinity_values_handling ... ok
test_08_class_label_leakage_protection ... ok
test_09_url_metadata_preservation ... ok
test_10_heuristic_url_feature_extractor ... ok
----------------------------------------------------------------------
Ran 10 tests in 2.359s
STATUS: OK (10/10 PASS)
```

#### B. Security Hardening Tests (`tests/test_security.py`)
```text
test_01_path_traversal_commonpath_protection ... ok
test_02_joblib_trusted_model_isolation ... ok
test_03_csv_formula_injection_variations ... ok
test_04_streamlit_upload_size_limit_config ... ok
test_05_csv_over_50k_rows_dos_protection ... ok
test_06_unknown_columns_handling ... ok
test_07_nan_inf_and_invalid_data_types ... ok
test_08_offline_processing_zero_ssrf ... ok
test_09_github_repo_credential_leak_scan ... ok
----------------------------------------------------------------------
Ran 9 tests in 2.310s
STATUS: OK (9/9 PASS)
```

---

## 3. MASALAH YANG MASIH TERSISA

* **Status Anomali / Kerentanan:** **NIHIL (0 Masalah / Zero Defects)**.
* Tidak ada anomali inkonsistensi dataset, tidak ada data leakage, tidak ada selisih angka metrik, dan tidak ada kerentanan keamanan yang tersisa.
* Seluruh artefak proyek berada dalam kondisi prima untuk demonstrasi akademik dan deployment.

---

## 4. KESIMPULAN AKHIR

Sistem **PhishGuard AI** telah lolos seluruh tahapan verifikasi integritas, konsistensi data, keamanan kode, dan validasi fungsional dengan predikat **100% KONSISTEN & PRODUCTION-READY**.

