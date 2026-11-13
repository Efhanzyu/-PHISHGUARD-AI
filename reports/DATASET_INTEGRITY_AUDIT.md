# PHISHGUARD AI — DATASET INTEGRITY & SPLIT VERIFICATION AUDIT
**Mata Kuliah:** Keamanan Informasi (Semester 5) — Ujian Akhir Semester (UAS)  
**Dokumen:** Laporan Investigasi Integritas Dataset & Verifikasi Partisi Data  
**Tanggal Investigasi:** 12 November 2026  
**Auditor:** Cyber Intelligence Data Integrity & Security Audit Agent  
**Status Audit:** **100% MATHEMATICAL & INTEGRITY PASS (METADATA TYPO IDENTIFIED)**  

---

## 1. RINGKASAN EKSEKUTIF INVESTIGASI

Investigasi mendalam dilakukan secara **READ-ONLY** untuk menjawab pertanyaan krusial terkait integritas dataset:
> *"Mengapa jumlah clean dataset tercatat 100.872 baris, sedangkan train + test sempat dilaporkan berjumlah 100.875 baris?"*

### Temuan Utama (Root Cause Analysis):
1. **Fisik Dataset Aktual Sempurna (100% Konsisten):**
   * `clean_url_features.csv` = **100.872 baris** (tanpa header).
   * `train_set.csv` = **80.697 baris** (tanpa header).
   * `test_set.csv` = **20.175 baris** (tanpa header).
   * **Total Train + Test = 80.697 + 20.175 = 100.872 baris**.
   * **Selisih Aktual Fisik: 0 baris (NOL)**. Tidak ada data yang hilang, tidak ada data yang bertambah, dan tidak ada kebocoran data (*zero leakage*).
2. **Akar Masalah Angka 100.875 (Metadata Calculation Bug):**
   * Angka `80.700` baris training (sehingga $80.700 + 20.175 = 100.875$) **BUKAN** berasal dari file dataset aktual, melainkan dari kesalahan kalkulasi ekspresi metadata pada skrip [`src/evaluate_model.py`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/src/evaluate_model.py#L247) baris 247:
     ```python
     "train_samples": len(test_df) * 4, # 80,697
     ```
   * Penulis skrip menggunakan perkiraan matematis kasar bahwa jika data test adalah 20% (1 bagian), maka data train adalah 80% (4 bagian).
   * Karena `len(test_df)` bernilai **20.175**, maka operasi perkalian `20.175 * 4` menghasilkan **80.700**!
   * Nilai **80.700** inilah yang tersimpan secara keliru ke dalam [`models/model_metadata.json`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/models/model_metadata.json#L9).
   * Jika nilai metadata tersebut dijumlahkan dengan `test_samples` (20.175), hasilnya adalah **100.875** (selisih artefak komputasi $+3$ baris).

---

## 2. BUKTI EMPIRIS VERIFIKASI DATASET AKTUAL

Pemeriksaan dilakukan langsung menggunakan engine Python pandas terhadap file fisik di disk:

### A. Dimensi dan Jumlah Baris Fisik

| Nama File | Path Disk | Ukuran File | Jumlah Baris Fisik (Data) | Jumlah Kolom |
| :--- | :--- | :---: | :---: | :---: |
| **Clean Dataset** | `dataset/processed/clean_url_features.csv` | 9.013.861 bytes (8,60 MB) | **100.872** | 18 |
| **Training Set** | `dataset/processed/train_set.csv` | 7.209.369 bytes (6,88 MB) | **80.697** | 18 |
| **Testing Set** | `dataset/processed/test_set.csv` | 1.804.759 bytes (1,72 MB) | **20.175** | 18 |
| **Jumlah Train + Test** | *Kombinasi Train & Test* | 9.014.128 bytes | **100.872** | 18 |
| **Selisih (Delta)** | *Train + Test - Clean* | - | **0 (NOL)** | - |

```text
Eksekusi Python Pandas:
Clean shape : (100872, 18)
Train shape : (80697, 18)
Test shape  : (20175, 18)
Train + Test: 100872
Difference  : 0
```

---

## 3. AUDIT KONSISTENSI & ASAL-USUL DATA (PROVENANCE)

Untuk membuktikan secara mutlak bahwa `train_set.csv` dan `test_set.csv` murni berasal dari `clean_url_features.csv`:

### A. Uji Relasi Himpunan (Set Theory Verification)
* **Total Unique URLs di Clean Dataset:** `100.872` URL unik.
* **Total Unique URLs di Training Set:** `80.697` URL unik.
* **Total Unique URLs di Testing Set:** `20.175` URL unik.
* **Irisan URL Train dan Test (Overlap / Duplikasi Antar Partisi):**
  $$\text{Train URLs} \cap \text{Test URLs} = \mathbf{0}\text{ (NOL)}$$
  *Tidak ada 1 URL pun yang muncul bersamaan di data train dan data test.*
* **Gabungan URL Train dan Test (Union):**
  $$\text{Train URLs} \cup \text{Test URLs} = \mathbf{100.872}\text{ URL}$$
* **Uji Kesamaan Himpunan (Union == Clean):**
  $$\mathbf{True}\text{ (IDENTIK 100\%)}$$
* **Baris pada Clean yang Hilang dari Split:** **0 baris**.
* **Baris Asing pada Split yang Tidak Ada di Clean:** **0 baris**.

---

## 4. VERIFIKASI DISTRIBUSI TARGET (`ClassLabel`)

Pemeriksaan stratifikasi dilakukan untuk memastikan proporsi kelas target seimbang dan tidak mengalami pergeseran distribusi (*data drift*):

| Partisi Dataset | Kelas 0 (Legitimate) | Persentase Kelas 0 | Kelas 1 (Phishing) | Persentase Kelas 1 | Total Sampel |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Clean Dataset** | 63.492 | **62,9431%** | 37.380 | **37,0569%** | 100.872 |
| **Training Set (80%)** | 50.793 | **62,9429%** | 29.904 | **37,0571%** | 80.697 |
| **Testing Set (20%)** | 12.699 | **62,9442%** | 7.476 | **37,0558%** | 20.175 |
| **Jumlah Train + Test** | **63.492** | **62,9431%** | **37.380** | **37,0569%** | **100.872** |
| **Selisih Kelas 0 & 1** | **0 (Presisi Sempurna)** | - | **0 (Presisi Sempurna)** | - | **0** |

*Kesimpulan Distribusi:* Stratifikasi pada `ClassLabel` berjalan dengan presisi 4 desimal yang identik antara Clean, Train, dan Test.

---

## 5. AUDIT SKRIP SPLITTING (`src/split_dataset.py`)

Pemeriksaan parameter deterministik pada kode sumber [`src/split_dataset.py`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/src/split_dataset.py):

* **Ukuran Test Set (`test_size`):** `0.20` (20.0%)
* **Pengacakan (`random_state`):** `42` (Deterministik & Dapat Direproduksi)
* **Strategi Stratifikasi:** `stratify=df['ClassLabel']`
* **Pengacakan Data (`shuffle`):** `True`
* **Log Hasil Pembagian pada [`reports/data_splitting_report.txt`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/reports/data_splitting_report.txt):**
  * Training Set: **80.697 baris** (80.00%)
  * Testing Set: **20.175 baris** (20.00%)
  * Total: **100.872 baris**

---

## 6. PENJELASAN MENDALAM: ASAL USUL ANGKA 100.875

### Mengapa Angka 100.875 Sempat Muncul?

1. **Kalkulasi Matematis Split Nyata:**
   * Total sampel bersih: $N = 100.872$.
   * $20\% \times 100.872 = 20.174,4$.
   * Algoritma `train_test_split` Scikit-Learn membulatkan ukuran test set ke atas menjadi **20.175** sampel.
   * Maka ukuran training set yang tersisa adalah $100.872 - 20.175 = \mathbf{80.697}$ sampel.
2. **Kekeliruan Penulisan Ekspresi di `src/evaluate_model.py`:**
   Pada saat pembuatan file metadata model ([src/evaluate_model.py](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/src/evaluate_model.py#L247)), baris 247 ditulis:
   ```python
   # Kode sumber yang keliru:
   "train_samples": len(test_df) * 4, # 80,697
   ```
   * Penulis ingin mendapatkan angka $80\%$ dengan mengalikan $20\%$ sebanyak 4 kali.
   * Namun secara matematis:
     $$20.175 \times 4 = \mathbf{80.700}$$
   * Perhatikan komentar yang ditulis pembuat kode: `# 80,697`. Pembuat kode sebenarnya tahu bahwa nilai yang benar adalah **80.697**, namun menggunakan rumus shortcut yang menghasilkan **80.700**.
3. **Dampak ke File Metadata:**
   Akibat rumus shortcut tersebut, [`models/model_metadata.json`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/models/model_metadata.json#L9) menyimpan:
   ```json
   "total_cleaned_samples": 100872,
   "train_samples": 80700,
   "test_samples": 20175,
   ```
   Sehingga saat nilai `train_samples` (80.700) ditambahkan dengan `test_samples` (20.175), terciptalah angka semu **100.875** ($100.872 + 3$).
4. **Verifikasi Proses Training Sebenarnya:**
   Pada file log training aktual ([`reports/training_log.txt`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/reports/training_log.txt#L5)), model Machine Learning terbukti dilatih menggunakan:
   `Dimensi Data Training : 80,697 baris, 18 kolom`
   Artinya model Random Forest dan Decision Tree dilatih pada data aktual yang benar (**80.697 baris**), bukan 80.700 baris.

---

## 7. KESIMPULAN & STATUS AUDIT

| Butir Evaluasi | Hasil Investigasi | Status |
| :--- | :--- | :---: |
| **Integritas File Dataset** | Bersih, valid, tanpa data korup atau duplikasi. | **PASS** |
| **Konsistensi Baris** | Clean (100.872) = Train (80.697) + Test (20.175). | **PASS** |
| **Isolasi Train & Test** | Overlap 0 URL, zero data leakage antar partisi. | **PASS** |
| **Konsistensi Distribusi Kelas** | Identik 62,94% Legitimate dan 37,06% Phishing. | **PASS** |
| **Akar Angka 100.875** | Murni *typo* kalkulasi shortcut `len(test_df) * 4` pada metadata generator `src/evaluate_model.py`. Dataset aktual sama sekali tidak mengalami kelebihan baris. | **TERIDENTIFIKASI (BUG DOKUMENTASI/METADATA)** |

---

## 8. REKOMENDASI PERBAIKAN (MENUNGGU PERSETUJUAN USER)

Sesuai instruksi pengguna untuk **tidak melakukan perubahan otomatis**, berikut adalah usulan tindakan korektif non-destruktif:

1. **Koreksi File Metadata ([`models/model_metadata.json`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/models/model_metadata.json#L9)):**
   * Ubah nilai `"train_samples": 80700` menjadi `"train_samples": 80697`.
2. **Koreksi Skrip Generator ([`src/evaluate_model.py`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/src/evaluate_model.py#L247)):**
   * Ubah ekspresi `"train_samples": len(test_df) * 4` menjadi `"train_samples": 100872 - len(test_df)` atau membaca `len(train_df)` langsung.
3. **Koreksi Laporan Audit Sebelumnya ([`reports/FINAL_PROJECT_AUDIT.md`](file:///e:/01.%20Matkul/Semester%205/01.%20KI/UAS/reports/FINAL_PROJECT_AUDIT.md)):**
   * Perbarui penyebutan angka 80.700 menjadi 80.697 agar seluruh dokumen proyek sinkron dan konsisten 100%.

*Seluruh data dan model tetap dipertahankan tanpa perubahan sampai adanya persetujuan dari pengguna.*

