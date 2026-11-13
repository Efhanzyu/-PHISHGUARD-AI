"""
Tahap 2: Exploratory Data Analysis (EDA)
Nama Sistem: PhishGuard AI
Dataset: D:\\01. Unduh\\url_features_extracted1.csv
Output Visualisasi: reports/figures/
Output Ringkasan   : reports/eda_summary.txt
"""

import os
import sys
import tempfile
from pathlib import Path

# Set cache matplotlib agar tidak memicu permission warning
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(csv_path: str, figures_dir: str, report_path: str):
    print("=" * 80)
    print("MEMULAI EXPLORATORY DATA ANALYSIS (EDA) - PHISHGUARD AI")
    print("=" * 80)
    
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    # Baca dataset
    print(f"[1/8] Membaca dataset dari: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"      Total data mentah: {df.shape[0]:,} baris, {df.shape[1]} kolom")
    
    report_lines = []
    def log(msg=""):
        print(msg)
        report_lines.append(msg)
        
    log("=" * 80)
    log("RINGKASAN HASIL EXPLORATORY DATA ANALYSIS (EDA) - PHISHGUARD AI")
    log("=" * 80)
    log(f"Lokasi Dataset : {csv_path}")
    log(f"Dimensi Awal   : {df.shape[0]:,} baris, {df.shape[1]} kolom")
    
    # 1. Bersihkan 1 baris NaN pada ClassLabel untuk analisis statistik yang konsisten
    initial_count = len(df)
    df_clean = df.dropna(subset=['ClassLabel']).copy()
    df_clean['ClassLabel'] = df_clean['ClassLabel'].astype(int)
    dropped_na = initial_count - len(df_clean)
    log(f"Baris dengan target NaN di-exclude untuk EDA: {dropped_na} baris")
    
    # 2. Distribusi Kelas
    log("\n[1. DISTRIBUSI KELAS]")
    class_counts = df_clean['ClassLabel'].value_counts()
    class_percentages = df_clean['ClassLabel'].value_counts(normalize=True) * 100
    label_map = {0: "Legitimate (Normal)", 1: "Phishing (Malicious)"}
    
    for c in [0, 1]:
        cnt = class_counts.get(c, 0)
        pct = class_percentages.get(c, 0.0)
        log(f" - Kelas {c} ({label_map[c]}): {cnt:,} sampel ({pct:.2f}%)")
        
    # Visualisasi 1: Distribusi Kelas (Bar chart & Donut chart)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = ['#2ecc71', '#e74c3c']
    
    # Bar plot
    sns.barplot(x=[label_map[c] for c in class_counts.index], y=class_counts.values, ax=axes[0], palette=colors)
    axes[0].set_title("Distribusi Jumlah Sampel per Kelas", fontsize=13, fontweight='bold')
    axes[0].set_ylabel("Jumlah Sampel", fontsize=11)
    for p in axes[0].patches:
        axes[0].annotate(f"{int(p.get_height()):,}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                         ha='center', va='center', color='white', fontweight='bold', fontsize=12)
        
    # Donut plot
    axes[1].pie(class_counts.values, labels=[label_map[c] for c in class_counts.index], autopct='%1.2f%%',
                colors=colors, startangle=140, explode=(0.03, 0.03), wedgeprops=dict(width=0.4, edgecolor='white'))
    axes[1].set_title("Proporsi Kelas (Class Balance)", fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    dist_fig_path = os.path.join(figures_dir, "class_distribution.png")
    plt.savefig(dist_fig_path, dpi=300)
    plt.close()
    log(f" -> Grafik tersimpan: {dist_fig_path}")

    # 3. Fitur Numerik dan Statistik Deskriptif
    feature_cols = [c for c in df_clean.columns if c not in ['URL', 'ClassLabel']]
    desc_df = df_clean[feature_cols].describe().T
    desc_df['skewness'] = df_clean[feature_cols].skew()
    log("\n[2. STATISTIK DESKRIPTIF FITUR NUMERIK]")
    log(desc_df[['mean', 'std', 'min', '50%', 'max', 'skewness']].to_string())

    # 4. Korelasi Antarfitur dan Terhadap Target
    corr_matrix = df_clean[feature_cols + ['ClassLabel']].corr()
    target_corr = corr_matrix['ClassLabel'].drop('ClassLabel').sort_values(ascending=False)
    
    log("\n[3. KORELASI FITUR TERHADAP TARGET (ClassLabel)]")
    for f, c in target_corr.items():
        log(f" - {f:27s}: {c:+.4f}")
        
    # Visualisasi 2: Heatmap Korelasi
    plt.figure(figsize=(16, 12))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmin=-1.0, vmax=1.0, annot=True, fmt=".2f",
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("Heatmap Korelasi Matriks Fitur & Target", fontsize=15, fontweight='bold', pad=15)
    plt.tight_layout()
    corr_fig_path = os.path.join(figures_dir, "correlation_heatmap.png")
    plt.savefig(corr_fig_path, dpi=300)
    plt.close()
    log(f" -> Grafik tersimpan: {corr_fig_path}")

    # Visualisasi 3: Bar chart korelasi fitur terhadap target
    plt.figure(figsize=(12, 7))
    palette_target = ['#e74c3c' if x > 0 else '#3498db' for x in target_corr.values]
    sns.barplot(x=target_corr.values, y=target_corr.index, palette=palette_target)
    plt.title("Korelasi Linear (Pearson) Setiap Fitur terhadap ClassLabel", fontsize=13, fontweight='bold')
    plt.xlabel("Koefisien Korelasi", fontsize=11)
    plt.axvline(0, color='grey', linestyle='--', alpha=0.7)
    plt.tight_layout()
    target_corr_path = os.path.join(figures_dir, "top_features_correlation.png")
    plt.savefig(target_corr_path, dpi=300)
    plt.close()
    log(f" -> Grafik tersimpan: {target_corr_path}")

    # 5. Investigasi Khusus: https_flag & Fitur Korelasi Tinggi
    log("\n[4. INVESTIGASI FITUR KORELASI TINGGI: https_flag]")
    https_ct = pd.crosstab(df_clean['https_flag'], df_clean['ClassLabel'], margins=True)
    https_ct_pct = pd.crosstab(df_clean['https_flag'], df_clean['ClassLabel'], normalize='index') * 100
    log(f"Tabel Kontinjensi https_flag vs ClassLabel:\n{https_ct.to_string()}")
    log(f"\nPersentase Baris:\n{https_ct_pct.round(2).to_string()}")
    
    # Visualisasi 4: Analisis https_flag
    plt.figure(figsize=(8, 5))
    https_plot_data = pd.crosstab(df_clean['https_flag'], df_clean['ClassLabel'])
    https_plot_data.plot(kind='bar', stacked=True, color=['#2ecc71', '#e74c3c'], figsize=(8, 5))
    plt.title("Distribusi Phishing vs Legitimate Berdasarkan Protokol HTTPS (https_flag)", fontsize=12, fontweight='bold')
    plt.xlabel("https_flag (0 = HTTP / Non-HTTPS, 1 = HTTPS)", fontsize=10)
    plt.ylabel("Jumlah URL", fontsize=10)
    plt.legend(["0 (Legitimate)", "1 (Phishing)"], title="ClassLabel")
    plt.xticks(ticks=[0, 1], labels=["0 (Non-HTTPS)", "1 (HTTPS)"], rotation=0)
    plt.tight_layout()
    https_fig_path = os.path.join(figures_dir, "https_flag_analysis.png")
    plt.savefig(https_fig_path, dpi=300)
    plt.close()
    log(f" -> Grafik tersimpan: {https_fig_path}")
    log("Catatan Investigasi: Fitur https_flag memiliki korelasi kuat (+0.93) karena sebagian besar URL legitimate pada dataset menggunakan format non-https / HTTP biasa, sedangkan dataset phishing memuat URL dengan https atau sebaliknya. Namun fitur ini TIDAK mengalami leakage 100% (bukan korelasi 1.0) sehingga tetap dipertahankan dengan pembobotan fitur oleh tree model.")

    # 6. Analisis Distribusi & Histogram Fitur Penting
    top_4_features = ['url_length', 'url_entropy', 'percentage_numeric_chars', 'number_of_digits']
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    for idx, f in enumerate(top_4_features):
        sns.histplot(data=df_clean, x=f, hue='ClassLabel', palette=['#2ecc71', '#e74c3c'],
                     bins=40, kde=True, ax=axes[idx], element='step', common_norm=False)
        axes[idx].set_title(f"Distribusi Fitur: {f}", fontsize=12, fontweight='bold')
        axes[idx].set_xlabel(f, fontsize=10)
        axes[idx].set_ylabel("Densitas / Frekuensi", fontsize=10)
    plt.tight_layout()
    hist_fig_path = os.path.join(figures_dir, "important_features_histograms.png")
    plt.savefig(hist_fig_path, dpi=300)
    plt.close()
    log(f" -> Grafik tersimpan: {hist_fig_path}")

    # 7. Analisis Outlier (Metode IQR)
    log("\n[5. ANALISIS OUTLIER (INTERQUARTILE RANGE - IQR)]")
    outlier_summary = {}
    for col in feature_cols:
        q1 = df_clean[col].quantile(0.25)
        q3 = df_clean[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
        outlier_summary[col] = len(outliers)
        log(f" - {col:27s}: {len(outliers):6,} outlier ({len(outliers)/len(df_clean)*100:5.2f}%)")
    log("Catatan Outlier: Fitur berbasis pohon (Decision Tree & Random Forest) secara inheren sangat tangguh (robust) terhadap outlier karena keputusan split dilakukan berdasarkan urutan nilai fitur (rank-based thresholds), bukan jarak euclidian.")

    # 8. Analisis Duplikasi URL dan Potensi Label Konflik
    log("\n[6. ANALISIS DUPLIKASI DAN KONFLIK LABEL URL]")
    url_counts = df_clean.groupby('URL')['ClassLabel'].nunique()
    conflicting_urls = url_counts[url_counts > 1]
    log(f"Jumlah URL unik                               : {df_clean['URL'].nunique():,}")
    log(f"Jumlah URL yang memiliki label konflik (>1)   : {len(conflicting_urls)}")
    if len(conflicting_urls) > 0:
        log("[PERINGATAN KONFLIK LABEL]: Ditemukan URL dengan label 0 dan 1 sekaligus!")
        for u in conflicting_urls.index[:5]:
            log(f"  - URL Konflik: {u}")
    else:
        log("Status: TIDAK ADA KONFLIK LABEL pada URL duplikat. Seluruh URL identik memiliki label konsisten.")

    # Simpan laporan
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines) + '\n')
    print(f"\n[SUKSES] Seluruh visualisasi dan ringkasan EDA selesai. Disimpan di: {report_path}")

if __name__ == "__main__":
    csv_file = r"D:\01. Unduh\url_features_extracted1.csv"
    fig_dir = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports", "figures")
    rep_file = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports", "eda_summary.txt")
    run_eda(csv_file, fig_dir, rep_file)

