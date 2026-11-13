# LAPORAN INTEGRATION TESTING & AUDIT SISTEM PHISHGUARD AI

**Sistem:** PhishGuard AI — Intelligent Phishing URL Detection System  
**Tanggal Pengujian:** 12 November 2026  
**Lingkungan Pengujian:** Windows 11 x64, Python 3.11.9, Scikit-learn 1.9.1, Streamlit 1.67.0  
**Lokasi Workspace:** `E:\01. Matkul\Semester 5\01. KI\UAS`  

---

## 1. Ringkasan Eksekutif Pengujian

Pengujian integrasi (*Integration Testing*) dan pengujian unit (*Unit Testing*) dilakukan secara komprehensif untuk memastikan sistem **PhishGuard AI** dapat memproses data, memvalidasi masukan pengguna, mengeksekusi model Machine Learning (*Random Forest Classifier*), mencegah kebocoran data (*data leakage*), dan menyajikan antarmuka visual secara andal dan presisi.

Seluruh 18 skenario pengujian fungsional dan integritas data telah dieksekusi dengan hasil akhir **100% PASS**.

---

## 2. Tabel Hasil Pengujian Integrasi (18 Skenario)

| No | Skenario Pengujian | Hasil yang Diharapkan | Hasil Aktual | Status |
|:---:|:---|:---|:---|:---:|
| 1 | **Inisialisasi Server & Aplikasi** | Aplikasi Streamlit dapat dijalankan di port lokal tanpa fatal crash | Server Uvicorn/Streamlit aktif pada port 8505 (`http://localhost:8505`) dengan kode status 200 OK | **PASS** |
| 2 | **Pemuatan Artefak Model** | Model `models/best_model.joblib` berhasil dimuat dengan `joblib` | Model Random Forest berhasil dimuat ke memori dengan kelas `<class 'sklearn.ensemble._forest.RandomForestClassifier'>` | **PASS** |
| 3 | **Pemuatan Metadata Model** | File `models/model_metadata.json` valid dan terbaca lengkap | Metadata JSON valid memuat 16 fitur, metrik evaluasi, tanggal pelatihan, dan versi dependensi | **PASS** |
| 4 | **Tampilan Overview Dashboard** | Menampilkan metrik Accuracy, Precision, Recall, F1, dan ROC-AUC sesuai metadata | Metric cards menampilkan angka akurat: Acc 99.94%, Prec 99.99%, Rec 99.84%, F1 99.91%, ROC 0.999995 | **PASS** |
| 5 | **Upload File CSV Valid** | File CSV dengan 16 fitur prediktor berhasil dibaca dan divalidasi | File CSV valid diparsing sempurna dengan jumlah baris terverifikasi | **PASS** |
| 6 | **Rejeki CSV Tanpa Fitur Wajib** | Upload file CSV yang tidak memiliki 16 fitur wajib ditolak dengan pesan kesalahan yang jelas | Muncul ValueError/peringatan spesifik menyebutkan nama fitur wajib yang hilang | **PASS** |
| 7 | **Proteksi Format File Non-CSV** | Upload file selain format `.csv` ditolak oleh sistem | Streamlit file uploader membatasi tipe file hanya `type=['csv']` | **PASS** |
| 8 | **Penanganan Data Kosong** | File CSV kosong (0 baris) ditangani dengan aman tanpa *unhandled crash* | Sistem mengembalikan DataFrame kosong dengan struktur kolom yang tetap utuh tanpa crash model | **PASS** |
| 9 | **Imputasi Missing Values** | Kolom fitur yang memiliki nilai `NaN` diimputasi dengan nilai median training | Seluruh nilai NaN diimputasi otomatis dan memunculkan peringatan transparan ke pengguna | **PASS** |
| 10 | **Normalisasi Nilai Infinity** | Nilai `+inf` atau `-inf` pada fitur dinormalisasi menjadi nilai riil batas | Nilai infinity berhasil dinormalisasi dan tidak menimbulkan error konversi skalar | **PASS** |
| 11 | **Deteksi Kelas Legitimate** | Sistem berhasil mengidentifikasi dan memberi label 'LEGITIMATE' pada URL normal | Model memprediksi kelas 0 dengan label visual hijau neon terkonfirmasi aman | **PASS** |
| 12 | **Deteksi Kelas Phishing** | Sistem berhasil mengidentifikasi dan memberi label 'PHISHING' pada URL berbahaya | Model memprediksi kelas 1 dengan label visual merah ancaman terkonfirmasi phishing | **PASS** |
| 13 | **Tampilan Probabilitas Prediksi** | Skor estimasi probabilitas phishing tampil dalam rentang $0.0\% - 100.0\%$ | Probabilitas dihitung via `predict_proba` dan disajikan dalam persentase desimal presisi | **PASS** |
| 14 | **Visualisasi Hasil Deteksi** | Donut chart proporsi kelas dan histogram probabilitas ter-render secara dinamis | Grafik visualisasi interaktif berhasil dirender menggunakan Matplotlib & Seaborn dark theme | **PASS** |
| 15 | **Ekspor & Unduh Hasil (CSV)** | Tombol unduh menghasilkan file CSV dengan kolom prediksi dan probabilitas | Tombol download menghasilkan `phishguard_detection_results.csv` lengkap beserta fitur asli | **PASS** |
| 16 | **Pencegahan Data Leakage** | Kolom `ClassLabel` (jika ada pada input) tidak boleh masuk ke matriks $X$ | `ClassLabel` secara otomatis dipisahkan sebagai Ground Truth evaluasi, tidak diikutsertakan dalam fitur prediksi | **PASS** |
| 17 | **Retensi Metadata URL Asli** | Kolom `URL` dipertahankan sebagai penanda identitas baris untuk audit | Kolom teks mentah URL dipisahkan dari fitur prediktor namun disematkan di tabel laporan akhir | **PASS** |
| 18 | **Konsistensi Inferensi Pasca Reload** | Model menghasilkan output identik ketika dimuat ulang dari disk | Uji reload pada 5 sampel acak menghasilkan prediksi konsisten deterministik: `[1, 1, 0, 1, 1]` | **PASS** |

---

## 3. Hasil Pengujian Otomatis (Unit & Integration Test Suite)

Pengujian skrip otomatis `src/test_integration.py` menggunakan framework standar Python `unittest`:

```text
Ran 10 tests in 3.320s

OK
```

**Rincian Unit Test:**
1. `test_01_model_loading`: PASS
2. `test_02_metadata_features`: PASS
3. `test_03_valid_csv_upload_inference`: PASS
4. `test_04_missing_required_features_rejection`: PASS
5. `test_05_empty_dataframe_handling`: PASS
6. `test_06_missing_values_imputation`: PASS
7. `test_07_infinity_values_handling`: PASS
8. `test_08_class_label_leakage_protection`: PASS
9. `test_09_url_metadata_preservation`: PASS
10. `test_10_heuristic_url_feature_extractor`: PASS

---

## 4. Evaluasi Ulang Metrik Model pada Data Testing Independen

Validasi ulang dilakukan terhadap $20.175$ baris data pada `dataset/processed/test_set.csv`:
- **Accuracy**: $0.999356$ ($99.9356\%$)
- **Precision (Phishing)**: $0.999866$ ($99.9866\%$)
- **Recall (Phishing)**: $0.998395$ ($99.8395\%$)
- **F1-Score (Phishing)**: $0.999130$ ($99.9130\%$)
- **ROC-AUC Score**: $0.999995$
- **True Negative (TN)**: $12.698$
- **False Positive (FP)**: **Hanya 1 kasus** ($0.0079\%$)
- **False Negative (FN)**: $12$ kasus ($0.16\%$)
- **True Positive (TP)**: $7.464$

---

## 5. Kesimpulan Kesiapan Sistem

Aplikasi **PhishGuard AI** telah memenuhi seluruh standar kualitas perangkat lunak, bebas dari *unhandled exception*, menerapkan proteksi *data leakage*, dan siap digunakan untuk demonstrasi serta pelaporan akademik.

