# PhishGuard AI — Intelligent Phishing URL Detection System
**Pengembangan Sistem Deteksi URL Phishing Berbasis Machine Learning Menggunakan Fitur Leksikal dan Struktural URL**

[![Python 3.11](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.1-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67.0-red.svg)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

---

## 1. Deskripsi Proyek
**PhishGuard AI** adalah sistem pertahanan keamanan informasi (*Defensive AI*) yang dibangun untuk mendeteksi, mengklasifikasikan, dan menganalisis tautan situs web berbahaya (*Phishing URL*) secara offline dan massal. Sistem ini memanfaatkan algoritma pembelajaran mesin *Random Forest Classifier* yang dilatih menggunakan 16 fitur representasi leksikal, struktural, protokol, dan statistik URL (Shannon Entropy) tanpa bergantung pada tokenisasi teks mentah yang berisiko mengalami *data leakage*.

Aplikasi dilengkapi antarmuka web interaktif berbasis **Streamlit** dengan tema *dark cybersecurity*, mendukung deteksi massal berbasis file CSV, pemindaian URL tunggal heuristik, visualisasi kurva evaluasi (*Confusion Matrix, ROC Curve, Feature Importance*), dan ekspor laporan deteksi.

---

## 2. Arsitektur dan Teknologi

```text
               +-------------------------------------------+
               |        Input Data: CSV (16 Fitur)         |
               +-------------------------------------------+
                                     |
                                     v
               +-------------------------------------------+
               |   Pembersihan & Validasi (Data Preprocess)|
               |  - Median Imputation (Missing Values)     |
               |  - Normalisasi Infinity (+/- inf)         |
               |  - Proteksi Data Leakage (Drop Target)    |
               +-------------------------------------------+
                                     |
                                     v
               +-------------------------------------------+
               |       Random Forest Classifier (Ensemble) |
               |     100 Decision Trees (max_depth=20)     |
               +-------------------------------------------+
                                     |
                                     v
         +---------------------------+---------------------------+
         |                                                       |
         v                                                       v
+-------------------------+                             +-------------------------+
| Legitimate URL (Aman)   |                             | Phishing URL (Bahaya)   |
| Label 0 (Badge Hijau)   |                             | Label 1 (Badge Merah)   |
+-------------------------+                             +-------------------------+
```

### Spesifikasi Teknologi:
- **Bahasa Pemrograman**: Python 3.11.9 (64-bit Windows)
- **Framework Web**: Streamlit 1.67.0
- **Machine Learning**: Scikit-Learn 1.9.1
- **Analisis & Manipulasi Data**: Pandas 3.0.2, NumPy 2.4.4
- **Visualisasi Ilmiah**: Matplotlib 3.10.9, Seaborn 0.13.2
- **Serialisasi Model**: Joblib 1.5.3

---

## 3. Struktur Direktori Proyek

```text
AI-IDS-DEFENSIVE-AI/
│
├── dataset/
│   ├── raw/
│   └── processed/
│       ├── clean_url_features.csv    # 100,872 baris data bersih
│       ├── train_set.csv             # 80,697 baris data pelatihan (80%)
│       └── test_set.csv              # 20,175 baris data pengujian (20%)
│
├── models/
│   ├── best_model.joblib             # Model Random Forest terbaik (1.95 MB)
│   ├── random_forest_model.joblib    # Model utama Random Forest
│   ├── decision_tree_model.joblib    # Model pembanding Decision Tree
│   └── model_metadata.json           # Metadata teknis, hyperparameter, metrik
│
├── reports/
│   ├── figures/
│   │   ├── class_distribution.png
│   │   ├── correlation_heatmap.png
│   │   ├── top_features_correlation.png
│   │   ├── https_flag_analysis.png
│   │   ├── important_features_histograms.png
│   │   ├── roc_curve_comparison.png
│   │   └── feature_importance_comparison.png
│   ├── screenshots/
│   │   ├── 01_overview_dashboard.png
│   │   ├── 02_batch_detection_page.png
│   │   ├── 03_single_url_scanner.png
│   │   ├── 04_model_evaluation.png
│   │   ├── 05_model_metadata.png
│   │   └── 06_user_guide.png
│   ├── integration_testing_report.md
│   ├── dashboard_final_audit.md
│   ├── metrics.json
│   ├── model_comparison.csv
│   └── feature_importance.csv
│
├── src/
│   ├── inspect_url_dataset.py        # Audit integritas dataset
│   ├── eda.py                        # Analisis eksplorasi data
│   ├── preprocessing.py              # Pipeline pembersihan data
│   ├── split_dataset.py              # Stratified data splitting
│   ├── train_model.py                # Pelatihan DT dan RF (5-fold CV)
│   ├── evaluate_model.py             # Evaluasi komparatif model
│   ├── dashboard_utils.py            # Utilitas inferensi & validasi
│   ├── url_feature_extractor.py      # Ekstraktor heuristik 16 fitur
│   ├── test_integration.py           # Unit & integration test suite
│   └── capture_screenshots.py        # Pengambil screenshot otomatis
│
├── app.py                            # Aplikasi antarmuka Streamlit
├── requirements.txt                  # Daftar dependensi pustaka
├── README.md                         # Dokumentasi utama proyek
└── .gitignore
```

---

## 4. Panduan Instalasi dan Menjalankan Sistem

### A. Persyaratan Sistem
- Sistem Operasi: Windows 10/11 (atau Linux/macOS)
- Python: Versi 3.11 atau lebih baru
- Kapasitas RAM: Minimal 4 GB (Rekomendasi 8 GB+)
- Browser: Google Chrome, Microsoft Edge, atau Mozilla Firefox

### B. Langkah Instalasi
1. Buka terminal PowerShell di direktori proyek:
   ```powershell
   cd "E:\01. Matkul\Semester 5\01. KI\UAS"
   ```
2. Aktifkan lingkungan virtual Python (`.venv`):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
3. Pasang seluruh dependensi:
   ```powershell
   pip install -r requirements.txt
   ```

### C. Menjalankan Dashboard Aplikasi
Jalankan aplikasi Streamlit melalui perintah berikut:
```powershell
python -m streamlit run app.py
```
Aplikasi akan secara otomatis membuka antarmuka browser pada alamat:
`http://localhost:8501` (atau port alternatif seperti `http://localhost:8505`).

---

## 5. Format File CSV Masukan (Batch Detection)

Aplikasi menerima file CSV yang memuat **16 fitur prediktor numerik** sesuai spesifikasi model:

| No | Nama Fitur | Tipe Data | Definisi & Karakteristik |
|:---:|:---|:---:|:---|
| 1 | `url_length` | Integer | Panjang karakter total URL |
| 2 | `has_ip_address` | Biner (0/1) | Bernilai 1 jika host berupa alamat IP |
| 3 | `dot_count` | Integer | Jumlah karakter titik (.) pada URL |
| 4 | `https_flag` | Biner (0/1) | 1 jika menggunakan protokol HTTPS, 0 jika HTTP |
| 5 | `url_entropy` | Float | Nilai Shannon Entropy mengukur keacakan karakter |
| 6 | `token_count` | Integer | Jumlah segmen kata berdasarkan delimiter URL |
| 7 | `subdomain_count` | Integer | Kedalaman subdomain pada host |
| 8 | `query_param_count` | Integer | Jumlah parameter query pada URL |
| 9 | `tld_length` | Integer | Panjang karakter TLD (misal: 'com' = 3) |
| 10 | `path_length` | Integer | Panjang karakter path direktori |
| 11 | `has_hyphen_in_domain` | Biner (0/1) | 1 jika ada tanda hubung (-) di domain |
| 12 | `number_of_digits` | Integer | Jumlah karakter numerik (0-9) |
| 13 | `tld_popularity` | Biner (0/1) | 1 jika TLD termasuk populer (.com, .org, dll.) |
| 14 | `suspicious_file_extension` | Biner (0/1) | 1 jika path berakhiran file berbahaya (.exe, .zip) |
| 15 | `domain_name_length` | Integer | Panjang nama domain utama |
| 16 | `percentage_numeric_chars` | Float | Rasio persentase digit angka terhadap panjang URL |

*Catatan Keamanan:* Kolom `URL` bersifat opsional dan hanya dijadikan metadata. Kolom `ClassLabel` (jika ada) otomatis dipisahkan sebagai *Ground Truth* dan **tidak diikutsertakan** dalam matriks fitur prediksi untuk mencegah *data leakage*.

---

## 6. Hasil Evaluasi Kinerja Model

Pengujian dilakukan pada **20.175 data testing independen** (*unseen test set*):

| Metrik Evaluasi | Decision Tree (Pembanding) | Random Forest (Model Terpilih) | Keunggulan Random Forest |
|:---|:---:|:---:|:---:|
| **Accuracy** | 0.99931 (99.93%) | **0.99936 (99.94%)** | Lebih akurat |
| **Precision (Phishing)** | 0.99906 (99.91%) | **0.99987 (99.99%)** | Nyaris bebas alarm palsu |
| **Recall (Phishing)** | **0.99906 (99.91%)** | 0.99839 (99.84%) | Menangkap 99.84% serangan |
| **F1-Score** | 0.99906 (99.91%) | **0.99913 (99.91%)** | Skor F1 seimbang tertinggi |
| **ROC-AUC** | 0.99959 | **0.999995** | Diskriminasi sempurna |
| **False Positive (FP)** | 7 kasus | **Hanya 1 kasus (0.0079%)** | **Menekan 85.7% False Alarm** |
| **False Negative (FN)** | **7 kasus** | 12 kasus (0.16%) | Selisih 5 dari 7.476 serangan |
| **Kecepatan Inferensi** | 0.0601 detik | 0.0731 detik | **~276.000 URL/detik** |

### Analisis Feature Importance (Gini Importance):
1. `path_length` (**38.79%**): Panjang direktori path merupakan pembeda terkuat antara halaman login palsu dan situs normal.
2. `token_count` (**15.06%**): URL phishing cenderung memiliki struktur token berlebihan.
3. `https_flag` (**13.40%**): Protokol transportasi URL.
4. `number_of_digits` (**10.81%**) & `percentage_numeric_chars` (**9.56%**): Phishing URL sering memuat string acak atau parameter numerik panjang.

---

## 7. Keterbatasan Sistem dan Etika Keamanan Informasi

1. **Analisis Leksikal & Struktural Murni**: PhishGuard AI menganalisis karakteristik sintaksis URL secara *offline/batch*, tidak melakukan *web crawling* aktif terhadap konten HTML atau muatan JavaScript halaman target.
2. **Karakteristik Zero-Day Domain**: Tautan phishing baru yang sengaja dibuat sangat pendek dan menyerupai format domain legitimate murni (*homograph attacks* tingkat tinggi) dapat membutuhkan lapisan verifikasi tambahan seperti reputasi DNS dan sertifikat SSL.
3. **Penyangkalan Jaminan (Disclaimer)**: Probabilitas prediksi yang dihasilkan sistem merupakan skor estimasi statistik berbasis Machine Learning, bukan kepastian mutlak hukum atas suatu situs web.

---

## 8. Lisensi & Hak Cipta
Dikembangkan untuk keperluan akademik mata kuliah **Keamanan Informasi**, Program Studi Informatika, Semester Ganjil 2026/2027.

