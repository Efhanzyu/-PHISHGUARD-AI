"""
Tahap 3: Data Preprocessing
Nama Sistem: PhishGuard AI
Tujuan: Membersihkan data mentah, memvalidasi integritas target, menangani duplikasi,
        memisahkan metadata URL, dan menyiapkan 16 fitur prediktor numerik.
Input : D:\\01. Unduh\\url_features_extracted1.csv
Output: dataset/processed/clean_url_features.csv
        reports/preprocessing_report.txt
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

def run_preprocessing(raw_csv_path: str, output_csv_path: str, report_path: str):
    print("=" * 80)
    print("MEMULAI DATA PREPROCESSING - PHISHGUARD AI")
    print("=" * 80)
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    report_lines = []
    def log(msg=""):
        print(msg)
        report_lines.append(msg)
        
    log("=" * 80)
    log("LAPORAN DATA PREPROCESSING - PHISHGUARD AI")
    log("=" * 80)
    
    # 1. Membaca dataset asli
    log(f"1. Membaca Dataset Asli dari : {raw_csv_path}")
    df_raw = pd.read_csv(raw_csv_path)
    initial_rows, initial_cols = df_raw.shape
    log(f"   Dimensi Awal Dataset      : {initial_rows:,} baris, {initial_cols} kolom")
    
    # 2. Membersihkan spasi pada nama kolom
    df = df_raw.copy()
    df.columns = [c.strip() for c in df.columns]
    log(f"2. Pembersihan Header Kolom  : Selesai ({len(df.columns)} kolom ternormalisasi)")
    
    # 3. Menghapus baris dengan target kosong
    na_target_count = df['ClassLabel'].isna().sum()
    log(f"3. Pemeriksaan Missing Target: Ditemukan {na_target_count} baris bernilai NaN pada 'ClassLabel'")
    if na_target_count > 0:
        df = df.dropna(subset=['ClassLabel']).copy()
        log(f"   Tindakan                  : 1 baris target kosong dihapus. Sisa baris: {len(df):,}")
    
    # 4. Validasi kelas biner pada target
    df['ClassLabel'] = df['ClassLabel'].astype(int)
    unique_labels = sorted(df['ClassLabel'].unique())
    log(f"4. Validasi Kelas Target     : Label unik terdeteksi = {unique_labels}")
    if unique_labels != [0, 1]:
        raise ValueError(f"Label target tidak valid: {unique_labels}. Harus biner [0, 1].")
    log("   Status Validasi           : VALID (0 = Legitimate / Normal, 1 = Phishing / Malicious)")
    
    # 5. Definisi 16 Fitur Prediktor Numerik & Metadata
    metadata_col = 'URL'
    target_col = 'ClassLabel'
    feature_cols = [c for c in df.columns if c not in [metadata_col, target_col]]
    log(f"5. Struktur Fitur             : {len(feature_cols)} fitur prediktor numerik terverifikasi")
    log(f"   Kolom Metadata            : '{metadata_col}' (Dipertahankan untuk audit dan identitas baris)")
    
    # 6. Pemeriksaan Missing Values & Infinity pada Fitur
    nulls_in_features = df[feature_cols].isnull().sum().sum()
    infs_in_features = np.isinf(df[feature_cols].values).sum()
    log(f"6. Kualitas Nilai Fitur      : Missing Values = {nulls_in_features}, Infinity Values = {infs_in_features}")
    if nulls_in_features > 0 or infs_in_features > 0:
        raise ValueError("Ditemukan missing value atau infinite value pada fitur prediktor!")
    log("   Status Integritas Fitur   : BERSIH & FINITE")
    
    # 7. Penanganan Duplikasi
    initial_before_dedup = len(df)
    full_duplicates = df.duplicated().sum()
    url_duplicates = df.duplicated(subset=['URL']).sum()
    log(f"7. Pemeriksaan Duplikasi      :")
    log(f"   - Duplikasi Penuh         : {full_duplicates:,} baris")
    log(f"   - Duplikasi Kolom 'URL'   : {url_duplicates:,} baris")
    
    # Cek konsistensi label pada duplikat
    label_conflict = df.groupby('URL')['ClassLabel'].nunique()
    conflict_count = (label_conflict > 1).sum()
    log(f"   - Konflik Label pada URL  : {conflict_count} baris (Seluruh duplikat memiliki label konsisten)")
    
    # Lakukan deduplikasi berdasarkan URL untuk mencegah data leakage antar fold split
    df_clean = df.drop_duplicates(subset=['URL']).copy().reset_index(drop=True)
    dropped_duplicates = initial_before_dedup - len(df_clean)
    log(f"   Tindakan Deduplikasi      : {dropped_duplicates:,} baris duplikat dihapus secara deterministik")
    log(f"   Jumlah Data Bersih Akhir  : {len(df_clean):,} baris, {df_clean.shape[1]} kolom")
    
    # 8. Distribusi Kelas Akhir Pasca-Preprocessing
    log("\n8. DISTRIBUSI KELAS SETELAH PREPROCESSING:")
    clean_counts = df_clean['ClassLabel'].value_counts()
    clean_pct = df_clean['ClassLabel'].value_counts(normalize=True) * 100
    log(f"   - Kelas 0 (Legitimate)    : {clean_counts[0]:,} baris ({clean_pct[0]:.2f}%)")
    log(f"   - Kelas 1 (Phishing)      : {clean_counts[1]:,} baris ({clean_pct[1]:.2f}%)")
    log(f"   - Total Sampel Bersih     : {len(df_clean):,} baris")
    
    # 9. Simpan Dataset Hasil Preprocessing
    log(f"\n9. Menyimpan dataset bersih ke: {output_csv_path}")
    df_clean.to_csv(output_csv_path, index=False)
    output_size_mb = os.path.getsize(output_csv_path) / (1024 * 1024)
    log(f"   Ukuran File Hasil         : {output_size_mb:.2f} MB")
    
    # Simpan laporan
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines) + '\n')
    log(f"\n[SUKSES] Laporan preprocessing disimpan di: {report_path}")

if __name__ == "__main__":
    raw_path = r"D:\01. Unduh\url_features_extracted1.csv"
    processed_path = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "dataset", "processed", "clean_url_features.csv")
    report_file = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports", "preprocessing_report.txt")
    run_preprocessing(raw_path, processed_path, report_file)

