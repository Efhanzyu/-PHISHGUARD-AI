# Security Policy — PhishGuard AI

## 1. Kebijakan Keamanan Sistem (Security Policy)
**PhishGuard AI** dikembangkan dengan mematuhi prinsip *Security by Design* dan *Defensive Cybersecurity Engineering*. Sistem dirancang untuk menganalisis karakteristik leksikal dan struktural URL phishing secara offline tanpa melakukan koneksi jaringan langsung ke target yang mencurigakan.

---

## 2. Arsitektur & Mitigasi Celah Keamanan Utama

### A. Pencegahan Server-Side Request Forgery (SSRF)
* **Karakteristik**: Pustaka `src/url_feature_extractor.py` hanya melakukan penguraian string (*string parsing*) menggunakan pustaka standar Python `urllib.parse.urlparse`.
* **Proteksi**: Sistem **tidak pernah membuka koneksi socket TCP/IP, HTTP GET/POST, DNS resolving, atau web crawling** ke alamat URL yang dianalisis. Analisis murni berbasis matematika dan statistik leksikal (Shannon Entropy).

### B. Pencegahan Remote Code Execution (RCE)
* **Proteksi**: Tidak ada penggunaan fungsi eksekusi dinamis seperti `eval()`, `exec()`, `os.system()`, atau deserialisasi yang tidak tepercaya. 
* Seluruh input diperlakukan sebagai string murni dan array numerik tipe data skalar.

### C. Mitigasi CSV Formula Injection (CWE-1236)
* **Proteksi**: Pada modul ekspor dan unduhan CSV (`src/dashboard_utils.py`), seluruh string yang diawali oleh karakter pemicu formula spreadsheet (`=`, `+`, `-`, `@`, `\t`, `\r`) disanitasi otomatis dengan menambahkan tanda kutip tunggal (`'`).

### D. Pencegahan Denial of Service (DoS) & Resource Exhaustion
* **Proteksi**: 
  - Batas ukuran file unggahan dibatasi maksimal **20 MB** melalui konfigurasi `.streamlit/config.toml`.
  - Batas baris data masukan dibatasi maksimal **50.000 baris** per eksekusi batch untuk mencegah ledakan alokasi memori RAM.
  - Batas panjang string URL dibatasi maksimal **2.048 karakter** untuk memitigasi serangan *Regular Expression Denial of Service (ReDoS)*.

### E. Pencegahan Data Leakage
* **Proteksi**: Kolom `ClassLabel` (label aktual) secara otomatis dikeluarkan dari matriks prediktor masukan model saat proses inferensi.
* Data yang diunggah diproses murni di buffer memori sementara (*in-memory*) dan tidak disimpan secara permanen di disk server.

---

## 3. Pelaporan Kerentanan (Vulnerability Reporting)
Jika Anda menemukan potensi kerentanan keamanan pada sistem ini, silakan buat laporan terperinci melalui issue pelacakan privat atau hubungi tim pengembang proyek Keamanan Informasi Universitas Siliwangi.

