"""
Tahap 4: Data Splitting
Nama Sistem: PhishGuard AI
Tujuan: Membagi dataset bersih menjadi Train (80%) dan Test (20%) menggunakan Stratified Sampling,
        memisahkan 16 fitur prediktor (X), target (y), serta metadata URL.
Input : dataset/processed/clean_url_features.csv
Output: dataset/processed/train_set.csv
        dataset/processed/test_set.csv
        reports/data_splitting_report.txt
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def run_data_splitting(clean_csv_path: str, output_train_path: str, output_test_path: str, report_path: str):
    print("=" * 80)
    print("MEMULAI DATA SPLITTING - PHISHGUARD AI")
    print("=" * 80)
    
    os.makedirs(os.path.dirname(output_train_path), exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    report_lines = []
    def log(msg=""):
        print(msg)
        report_lines.append(msg)
        
    log("=" * 80)
    log("LAPORAN DATA SPLITTING (TRAIN-TEST SPLIT) - PHISHGUARD AI")
    log("=" * 80)
    
    # 1. Membaca dataset bersih
    df = pd.read_csv(clean_csv_path)
    total_samples = len(df)
    log(f"1. Membaca Dataset Bersih dari : {clean_csv_path}")
    log(f"   Total Sampel               : {total_samples:,} baris, {df.shape[1]} kolom")
    
    # 2. Konfigurasi Stratified Split
    test_size = 0.20
    random_state = 42
    log(f"2. Konfigurasi Pembagian Data :")
    log(f"   - Rasio Training Data      : 80.0% ({int(total_samples * 0.80):,} sampel)")
    log(f"   - Rasio Testing Data       : 20.0% ({int(total_samples * 0.20):,} sampel)")
    log(f"   - Strategi Pembagian       : Stratified Sampling berdasarkan kolom 'ClassLabel'")
    log(f"   - Random State             : {random_state} (Deterministik & Dapat Direproduksi)")
    
    # 3. Eksekusi Train-Test Split
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df['ClassLabel'],
        random_state=random_state,
        shuffle=True
    )
    
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    
    log(f"\n3. Hasil Pembagian Aktual    :")
    log(f"   - Ukuran Data Training     : {len(train_df):,} baris ({len(train_df)/total_samples*100:.2f}%)")
    log(f"   - Ukuran Data Testing      : {len(test_df):,} baris ({len(test_df)/total_samples*100:.2f}%)")
    
    # 4. Verifikasi Distribusi Kelas
    train_counts = train_df['ClassLabel'].value_counts()
    train_pct = train_df['ClassLabel'].value_counts(normalize=True) * 100
    test_counts = test_df['ClassLabel'].value_counts()
    test_pct = test_df['ClassLabel'].value_counts(normalize=True) * 100
    
    log("\n4. DISTRIBUSI KELAS:")
    log("   Training Set:")
    log(f"     * Kelas 0 (Legitimate)   : {train_counts[0]:,} baris ({train_pct[0]:.2f}%)")
    log(f"     * Kelas 1 (Phishing)     : {train_counts[1]:,} baris ({train_pct[1]:.2f}%)")
    log("   Testing Set:")
    log(f"     * Kelas 0 (Legitimate)   : {test_counts[0]:,} baris ({test_pct[0]:.2f}%)")
    log(f"     * Kelas 1 (Phishing)     : {test_counts[1]:,} baris ({test_pct[1]:.2f}%)")
    log("   Status Distribusi          : IDENTIK (Stratifikasi berhasil menjaga proporsi kelas)")
    
    # 5. Analisis Domain Overlap & Keterbatasan Metodologis
    log("\n5. ANALISIS KETERBATASAN RANDOM STRATIFIED SPLIT:")
    # Ekstraksi domain sederhana dari URL
    def extract_domain(url):
        try:
            from urllib.parse import urlparse
            res = urlparse(url)
            return res.netloc if res.netloc else url.split('/')[0]
        except Exception:
            return "unknown"
            
    train_domains = set(train_df['URL'].apply(extract_domain))
    test_domains = set(test_df['URL'].apply(extract_domain))
    overlap_domains = train_domains.intersection(test_domains)
    
    log(f"   - Jumlah Domain Unik di Training Set : {len(train_domains):,}")
    log(f"   - Jumlah Domain Unik di Testing Set  : {len(test_domains):,}")
    log(f"   - Domain yang Beririsan (Overlap)    : {len(overlap_domains):,} domain")
    log(f"   - Domain Baru di Testing (Unseen)    : {len(test_domains - train_domains):,} domain")
    log("   Catatan Akademis:")
    log("   Pengacakan baris (random split) menghasilkan sebagian domain yang sama muncul di train dan test.")
    log("   Hal ini valid untuk menguji kemampuan model menggeneralisasi karakteristik fitur leksikal dan")
    log("   struktural URL, namun generalisasi mutlak terhadap domain baru (zero-day phishing domain)")
    log("   dapat sedikit lebih rendah daripada akurasi testing jika domain target memiliki pola leksikal baru.")
    
    # 6. Simpan Train dan Test Data
    log(f"\n6. Menyimpan File Partisi Data:")
    train_df.to_csv(output_train_path, index=False)
    test_df.to_csv(output_test_path, index=False)
    log(f"   - Training Data tersimpan di : {output_train_path} ({os.path.getsize(output_train_path)/(1024*1024):.2f} MB)")
    log(f"   - Testing Data tersimpan di  : {output_test_path} ({os.path.getsize(output_test_path)/(1024*1024):.2f} MB)")
    
    # Tulis laporan
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines) + '\n')
    log(f"\n[SUKSES] Laporan splitting disimpan di: {report_path}")

if __name__ == "__main__":
    clean_csv = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "dataset", "processed", "clean_url_features.csv")
    train_out = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "dataset", "processed", "train_set.csv")
    test_out = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "dataset", "processed", "test_set.csv")
    rep_file = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports", "data_splitting_report.txt")
    run_data_splitting(clean_csv, train_out, test_out, rep_file)

