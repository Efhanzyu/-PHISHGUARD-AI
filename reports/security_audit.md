# LAPORAN AUDIT KEAMANAN SISTEM (SECURITY AUDIT REPORT)
## PHISHGUARD AI — DEFENSIVE CYBERSECURITY PLATFORM

**Tanggal Audit:** 12 November 2026  
**Auditor:** Application Security Engineer & Python Security Auditor  
**Lingkup Audit:** Source Code, Insecure Deserialization, SSRF, DoS, Formula Injection, Deployment Config, Data Privacy  
**Workspace:** `E:\01. Matkul\Semester 5\01. KI\UAS`  

---

## 1. Ringkasan Eksekutif Audit

Audit penguatan keamanan (*Security Hardening Audit*) dilakukan sebelum sistem PhishGuard AI dipublikasikan ke lingkungan pengujian publik atau cloud. Berdasarkan metodologi OWASP Top 10 dan CWE (*Common Weakness Enumeration*), sistem telah diaudit dan diperkuat pada 15 aspek kontrol keamanan.

> **Pernyataan Integritas Keamanan:**  
> Tidak ada sistem informasi di dunia yang dapat diklaim bebas dari celah atau aman 100%. Namun, seluruh celah keamanan umum (*high and medium risk vectors*) yang diidentifikasi telah diuji dan dimitigasi secara terukur melalui kontrol preventif di tingkat aplikasi dan konfigurasi server.

---

## 2. Matriks Penilaian Risiko dan Hasil Audit Keamanan

| No | Kategori Risiko & Vektor Ancaman | Tingkat Risiko (Severity) | Hasil Pemeriksaan Aktual | Strategi Mitigasi Terverifikasi | Status Pengujian |
|:---:|:---|:---:|:---|:---|:---:|
| 1 | **Server-Side Request Forgery (SSRF)** *(CWE-918)* | **CRITICAL** | Kode `src/url_feature_extractor.py` diperiksa; tidak ditemukan pemanggilan socket jaringan, HTTP requests (`urllib.request.urlopen`, `requests.get`), atau koneksi keluar ke URL target. | URL target diperlakukan murni sebagai teks statis. Ekstraksi fitur berbasis penguraian leksikal dan perhitungan entropi matematis offline. | **PASS (Mitigated)** |
| 2 | **Remote Code Execution (RCE)** *(CWE-94 / CWE-95)* | **CRITICAL** | Pemindaian statis AST terhadap seluruh file `.py` di repositori; **0 pemanggilan fungsi berbahaya** (`eval`, `exec`, `os.system`). | Semua masukan pengguna dikonversi menjadi tipe data skalar numerik dan string terisolasi tanpa eksekusi dinamis. | **PASS (Mitigated)** |
| 3 | **Insecure Deserialization** *(CWE-502)* | **HIGH** | Pustaka `joblib` digunakan untuk memuat model `.joblib`. Joblib berpotensi mengeksekusi *arbitrary code* jika file model berasal dari pihak ketiga yang tidak tepercaya. | Path pemuatan model di-hardcode ke direktori lokal terverifikasi `models/best_model.joblib`. Sistem menolak pemuatan file model eksternal sembarangan dari masukan pengguna. | **PASS (Mitigated)** |
| 4 | **CSV Formula Injection** *(CWE-1236)* | **MEDIUM** | URL penipuan yang diawali karakter formula (`=`, `+`, `-`, `@`, `\t`, `\r`) dapat dieksekusi oleh Microsoft Excel/Calc saat file unduhan dibuka. | Fungsi `sanitize_csv_formula_injection()` diterapkan pada seluruh string unduhan. Karakter pemicu formula disanitasi dengan menambahkan tanda kutip tunggal (`'`). | **PASS (Mitigated)** |
| 5 | **Resource Exhaustion / DoS** *(CWE-400)* | **HIGH** | Pengguna dapat mengunggah file CSV raksasa (ratusan megabyte/jutaan baris) yang berpotensi memicu kegagalan memori *Out-of-Memory* (OOM). | 1. Batas ukuran unggahan di `.streamlit/config.toml` disetel maksimal **20 MB**.<br>2. Batas jumlah baris dibatasi maksimal **50.000 baris** di `src/dashboard_utils.py`. | **PASS (Mitigated)** |
| 6 | **Regular Expression Denial of Service (ReDoS)** *(CWE-1333)* | **MEDIUM** | Pola regex pada parsing IP address dan delimiter URL berpotensi mengalami *catastrophic backtracking* pada string sangat panjang. | 1. Panjang input URL dibatasi maksimal **2.048 karakter** (`url_str[:2048]`).<br>2. Regex diubah menjadi pola linier non-backtracking. | **PASS (Mitigated)** |
| 7 | **Data Leakage (Target Leak)** *(CWE-200)* | **HIGH** | Jika file CSV masukan memuat kolom `ClassLabel`, label tersebut berisiko mencemari fitur prediksi model. | Kolom `ClassLabel` secara otomatis dipisahkan dari matriks inferensi $X$ dan hanya dijadikan *Ground Truth* visual. | **PASS (Mitigated)** |
| 8 | **Path Traversal** *(CWE-22)* | **HIGH** | Pemanggilan path file berpotensi dimanipulasi dengan traversal sequence (`../`, `..\`). | Menggunakan `os.path.abspath` dan `os.path.join` yang terkunci di dalam direktori workspace proyek. | **PASS (Mitigated)** |
| 9 | **Kebocoran Kredensial & Secrets** *(CWE-798)* | **HIGH** | Riwayat git dan repositori diperiksa dari kemungkinan komit kunci API, token, atau file `.env`. | File `.gitignore` telah dikonfigurasi untuk mengecualikan `.env`, `.streamlit/secrets.toml`, file sertifikat `*.pem`, `*.key`, dan dataset mentah. | **PASS (Mitigated)** |
| 10 | **Privasi Data Pengguna** *(CWE-359)* | **MEDIUM** | File CSV yang diunggah pengguna berpotensi tersimpan permanen di media penyimpanan server. | Data diolah murni di memori RAM sementara (*in-memory buffer*) dan dibersihkan saat sesi browser berakhir tanpa penyimpanan permanen ke disk. | **PASS (Mitigated)** |
| 11 | **Cross-Site Request Forgery (CSRF)** *(CWE-352)* | **MEDIUM** | Request WebSocket dan HTTP rentan terhadap pemalsuan permintaan antar-situs. | Proteksi XSRF bawaan Streamlit diaktifkan secara tegas pada `.streamlit/config.toml` (`enableXsrfProtection = true`). | **PASS (Mitigated)** |
| 12 | **Information Disclosure via Error Stack Traces** *(CWE-209)* | **LOW** | Pesan error internal sistem berpotensi membocorkan struktur direktori server ke pengguna publik. | Penanganan exception menggunakan blok `try...except` terstruktur yang menampilkan pesan kesalahan ramah pengguna. | **PASS (Mitigated)** |

---

## 3. Hasil Pengujian Keamanan Otomatis (Security Test Suite)

Pengujian unit keamanan independen dijalankan melalui skrip `tests/test_security.py`:

```text
PS E:\01. Matkul\Semester 5\01. KI\UAS> .\.venv\Scripts\python.exe -m unittest tests\test_security.py
......
----------------------------------------------------------------------
Ran 6 tests in 0.260s

OK
```

**Rincian Kasus Uji Keamanan:**
1. `test_01_no_ssrf_socket_leakage`: **PASS** — Socket mock memvalidasi 0 koneksi jaringan luar saat ekstraksi URL (termasuk host internal AWS metadata `169.254.169.254` dan `localhost`).
2. `test_02_no_eval_exec_in_codebase`: **PASS** — Pemindaian statis AST mengonfirmasi 0 pemanggilan `eval`, `exec`, atau `os.system` pada kode aplikasi.
3. `test_03_csv_formula_injection_sanitization`: **PASS** — Seluruh payload formula (`=cmd`, `+123`, `@HYPERLINK`) disanitasi dengan tanda kutip tunggal (`'`).
4. `test_04_max_row_limit_dos_protection`: **PASS** — Masukan $> 50.000$ baris ditolak seketika dengan `ValueError`.
5. `test_05_class_label_leakage_mitigation`: **PASS** — Matriks $X$ terbebas dari kolom `ClassLabel`.
6. `test_06_redos_long_url_resilience`: **PASS** — String URL sepanjang $20.000$ karakter dipotong ke batas aman $2.048$ karakter tanpa lag ataupun crash.

---

## 4. Rekomendasi Deployment Cloud
Bila sistem di-deploy ke layanan cloud seperti **Streamlit Community Cloud**:
1. Pastikan repositori GitHub tidak memuat dataset berukuran $> 50$ MB (file model `best_model.joblib` sebesar 1.95 MB aman diunggah ke Git LFS atau repo standar).
2. Pastikan koneksi diakses melalui protokol terenkripsi **HTTPS (TLS 1.3)** yang disediakan otomatis oleh platform hosting.
3. Batasi akses publik menggunakan kata sandi aplikasi (*App Password/Auth*) jika platform hanya ditujukan untuk evaluasi dosen internal.

