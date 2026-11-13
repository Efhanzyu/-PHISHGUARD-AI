"""
PhishGuard AI — Hybrid Cyber Intelligence Platform v3.5
Enterprise-grade Threat Triage, Topology Graph Visualization, and Heuristic Feature Extraction
"""

import os
import json
import tempfile
from pathlib import Path

# Setup Matplotlib cache
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.dashboard_utils import (
    load_model_and_metadata,
    validate_and_preprocess_input,
    run_prediction_pipeline,
    REQUIRED_FEATURES
)
from src.url_feature_extractor import extract_features_from_url
from src.network_visualization import render_network_graph
from src.ui_components import render_top_header, render_metric_card

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="PhishGuard AI — Hybrid Cyber Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Muat Styling Kustom Deep Teal & Cyber Intelligence Tokens
css_path = os.path.join("assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Muat Model (Cached) dan Metadata (Fresh dari Disk)
@st.cache_resource
def get_cached_model():
    model, _ = load_model_and_metadata("models")
    return model

try:
    best_model = get_cached_model()
    # Muat metadata langsung dari file JSON agar selalu sinkron dengan disk
    meta_path = os.path.join("models", "model_metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    else:
        _, metadata = load_model_and_metadata("models")
except Exception as e:
    st.error(f"Gagal memuat artefak model: {e}")
    st.stop()

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 16px 0;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <div style="width: 34px; height: 34px; border-radius: 9px; background: rgba(53, 214, 192, 0.16); border: 1px solid #35D6C0; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 14px rgba(53, 214, 192, 0.4);">
                <span style="font-size: 18px;">🛡️</span>
            </div>
            <div style="font-size: 17px; font-weight: 700; color: #E8F5F1; letter-spacing: 0.04em;">PHISHGUARD <span style="color: #35D6C0;">AI</span></div>
        </div>
        <div style="font-size: 10.5px; color: #89AAA2; text-transform: uppercase; letter-spacing: 0.09em;">Hybrid Cyber Intelligence v3.5</div>
    </div>
    <hr style="border-color: rgba(53, 214, 192, 0.16); margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    menu_options = [
        "🌐 Intelligence Core (Topology)",
        "🧪 Threat Scanner (Single URL)",
        "🔍 Batch Threat Triage (CSV)",
        "📊 Analytics & Validation",
        "ℹ️ Neural Architecture",
        "📖 Defensive Protocol (Guide)"
    ]
    
    page_param = st.query_params.get("page", "").lower()
    default_idx = 0
    if "single" in page_param or "scanner" in page_param:
        default_idx = 1
    elif "batch" in page_param or "triage" in page_param:
        default_idx = 2
    elif "eval" in page_param or "analytics" in page_param:
        default_idx = 3
    elif "spec" in page_param or "arch" in page_param:
        default_idx = 4
    elif "guide" in page_param or "protocol" in page_param:
        default_idx = 5

    menu = st.radio("SISTEM NAVIGASI", menu_options, index=default_idx)
    
    st.markdown("""
    <hr style="border-color: rgba(53, 214, 192, 0.16); margin-top: 24px; margin-bottom: 18px;">
    <div style="background: rgba(16, 39, 34, 0.7); border: 1px solid rgba(53, 214, 192, 0.16); border-radius: 11px; padding: 13px 14px; font-size: 11px; color: #89AAA2;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>STATUS:</span>
            <span style="color: #35D6C0; font-weight: 700;">● ACTIVE SHIELD</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>ACTIVE MODEL:</span>
            <span style="color: #E8F5F1; font-weight: 600;">Random Forest</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>TEST F1-SCORE:</span>
            <span style="color: #35D6C0; font-weight: 700; font-family: monospace;">99.91%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render Global Header
render_top_header()

# ==============================================================================
# 1. INTELLIGENCE CORE (OVERVIEW & TOPOLOGY GRAPH)
# ==============================================================================
if menu == "🌐 Intelligence Core (Topology)":
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #E8F5F1; margin-bottom: 4px;">Peta Topologi Intelijen & Arsitektur Fitur</h2>
        <p style="font-size: 13px; color: #89AAA2; margin: 0;">Eksplorasi graf topologi 16 dimensi fitur URL yang terhubung ke PhishGuard Core. Klik atau arahkan kursor pada simpul untuk menganalisis kontribusi fitur.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 5 Balanced Metric Cards Banner
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_metric_card("Accuracy", "99.94%", "Overall Test Accuracy", "turquoise")
    with c2:
        render_metric_card("Precision", "99.99%", "Phishing Target Precision", "gold")
    with c3:
        render_metric_card("Recall", "99.84%", "Attack Catch Rate", "purple")
    with c4:
        render_metric_card("F1-Score", "99.91%", "Harmonic Precision-Recall", "pink")
    with c5:
        render_metric_card("ROC-AUC", "0.99999", "Perfect Discrimination", "turquoise")

    # Render HTML5 Canvas Network Topology Component
    components.html(render_network_graph(), height=620, scrolling=False)
    
    # Model Comparison Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="cyber-card">
        <h3 style="font-size: 16px; font-weight: 700; color: #E8F5F1; margin-bottom: 12px;">📊 Verifikasi Komparatif: Random Forest vs Decision Tree</h3>
    """, unsafe_allow_html=True)
    comp_path = os.path.join("reports", "model_comparison.csv")
    if os.path.exists(comp_path):
        comp_df = pd.read_csv(comp_path)
        st.dataframe(comp_df, width="stretch" if hasattr(st, "dataframe") else True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 2. THREAT SCANNER (SINGLE URL)
# ==============================================================================
elif menu == "🧪 Threat Scanner (Single URL)":
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #E8F5F1; margin-bottom: 4px;">Pemindai Ancaman URL Tunggal</h2>
        <p style="font-size: 13px; color: #89AAA2; margin: 0;">Ekstraksi instan 16 fitur leksikal dan struktural dari string URL untuk analisis keamanan mendalam.</p>
    </div>
    """, unsafe_allow_html=True)
    
    input_url = st.text_input(
        "MASUKKAN TARGET URL UNTUK DIANALISIS:",
        value="https://secure-login-update-paypal-verification.com/login.php"
    )
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        scan_clicked = st.button("⚡ INITIALIZE SCAN", type="primary")

    if scan_clicked:
        if not input_url.strip():
            st.warning("Mohon masukkan tautan URL terlebih dahulu.")
        else:
            with st.spinner("Mengekstrak 16 fitur leksikal & mengkuantifikasi vektor ancaman..."):
                extracted_dict = extract_features_from_url(input_url)
                input_feature_df = pd.DataFrame([extracted_dict])
                X_single = input_feature_df[REQUIRED_FEATURES]
                
                pred = best_model.predict(X_single)[0]
                prob = best_model.predict_proba(X_single)[0, 1] if hasattr(best_model, "predict_proba") else (1.0 if pred == 1 else 0.0)

            st.markdown("<br>", unsafe_allow_html=True)
            if pred == 1:
                st.markdown(f"""
                <div class="threat-verdict-card threat-phishing" style="background: rgba(255, 85, 102, 0.12); border: 2px solid #FF5566; border-radius: 14px; padding: 20px 24px; box-shadow: 0 0 32px rgba(255, 85, 102, 0.35); margin-bottom: 24px;">
                    <div class="threat-verdict-box" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                        <div style="flex: 1 1 280px;">
                            <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.1em; color: #FF5566; text-transform: uppercase;">⚠️ CRITICAL THREAT DETECTED</div>
                            <div style="font-size: 24px; font-weight: 800; color: #ffffff; margin-top: 4px; line-height: 1.25;">VERDICT: PHISHING / MALICIOUS URL</div>
                            <div style="font-size: 13px; color: #E8F5F1; margin-top: 6px; line-height: 1.4;">URL ini memiliki karakteristik manipulasi path, entropi tinggi, dan token tidak wajar yang sering digunakan dalam credential harvesting.</div>
                        </div>
                        <div class="verdict-prob-col" style="text-align: right; min-width: 140px;">
                            <div style="font-size: 11px; color: #FFA1AC; text-transform: uppercase; font-weight: 600;">PHISHING PROBABILITY</div>
                            <div style="font-size: 32px; font-weight: 800; color: #FF5566; font-family: 'JetBrains Mono', monospace; line-height: 1.1;">{prob*100:.2f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="threat-verdict-card threat-legit" style="background: rgba(53, 214, 192, 0.12); border: 2px solid #35D6C0; border-radius: 14px; padding: 20px 24px; box-shadow: 0 0 32px rgba(53, 214, 192, 0.35); margin-bottom: 24px;">
                    <div class="threat-verdict-box" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                        <div style="flex: 1 1 280px;">
                            <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.1em; color: #35D6C0; text-transform: uppercase;">✅ THREAT VERIFICATION PASSED</div>
                            <div style="font-size: 24px; font-weight: 800; color: #ffffff; margin-top: 4px; line-height: 1.25;">VERDICT: LEGITIMATE / SAFE URL</div>
                            <div style="font-size: 13px; color: #E8F5F1; margin-top: 6px; line-height: 1.4;">Struktur leksikal, protokol, dan domain URL konsisten dengan karakteristik situs bereputasi sah.</div>
                        </div>
                        <div class="verdict-prob-col" style="text-align: right; min-width: 140px;">
                            <div style="font-size: 11px; color: #89AAA2; text-transform: uppercase; font-weight: 600;">PHISHING PROBABILITY</div>
                            <div style="font-size: 32px; font-weight: 800; color: #35D6C0; font-family: 'JetBrains Mono', monospace; line-height: 1.1;">{prob*100:.2f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Rincian 16 Fitur (Opsi A: Single Cyber Table HTML + CSS)
            feature_descriptions = {
                "url_length": "Panjang total karakter string URL",
                "has_ip_address": "Deteksi host berupa IP address langsung (1=Ya, 0=Tidak)",
                "dot_count": "Jumlah karakter tanda titik (.) dalam URL",
                "https_flag": "Penggunaan protokol HTTPS aman (1=Ya, 0=Tidak)",
                "url_entropy": "Tingkat keacakan string (Shannon Entropy)",
                "token_count": "Jumlah pemisah token/segmen kata dalam URL",
                "subdomain_count": "Jumlah tingkatan subdomain pada domain host",
                "query_param_count": "Jumlah parameter query (?) pada URL",
                "tld_length": "Panjang karakter Top-Level Domain (TLD)",
                "path_length": "Panjang karakter direktori path URL",
                "has_hyphen_in_domain": "Tanda hubung (-) pada domain (indikator typosquatting)",
                "number_of_digits": "Jumlah karakter angka numerik (0-9)",
                "tld_popularity": "Popularitas TLD terdaftar (1=Populer, 0=Jarang/Berisiko)",
                "suspicious_file_extension": "Ekstensi file mencurigakan (.exe, .zip, dll)",
                "domain_name_length": "Panjang nama domain utama",
                "percentage_numeric_chars": "Rasio karakter numerik terhadap panjang URL"
            }

            table_rows_html = []
            for k, v in extracted_dict.items():
                formatted_val = f"{v:.4f}" if isinstance(v, float) else str(int(v)) if isinstance(v, (int, np.integer)) else str(v)
                desc = feature_descriptions.get(k, "-")
                table_rows_html.append(
                    f'<tr>'
                    f'<td style="font-family: \'JetBrains Mono\', monospace; font-weight: 600; color: #E8F5F1; width: 32%;">'
                    f'<span style="color: #35D6C0; margin-right: 6px;">›</span>{k}'
                    f'</td>'
                    f'<td style="width: 22%;">'
                    f'<span class="cyber-badge-val">{formatted_val}</span>'
                    f'</td>'
                    f'<td style="color: #89AAA2; font-size: 12.5px; width: 46%;">'
                    f'{desc}'
                    f'</td>'
                    f'</tr>'
                )

            rows_joined = "".join(table_rows_html)

            table_markup = (
                '<div class="cyber-card" style="margin-top: 10px;">'
                '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">'
                '<div>'
                '<h3 style="font-size: 16px; font-weight: 700; color: #E8F5F1; margin: 0;">📋 Rincian Ekstraksi 16 Fitur Leksikal & Struktural</h3>'
                '<p style="font-size: 12px; color: #89AAA2; margin: 4px 0 0 0;">Parameter leksikal URL dianalisis secara murni offline tanpa DNS/HTTP request.</p>'
                '</div>'
                '<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #35D6C0; background: rgba(53, 214, 192, 0.12); border: 1px solid rgba(53, 214, 192, 0.3); padding: 4px 10px; border-radius: 20px;">'
                '16 PARAMETERS VERIFIED'
                '</span>'
                '</div>'
                '<div class="cyber-table-container">'
                '<table class="cyber-table">'
                '<thead>'
                '<tr>'
                '<th style="width: 32%;">Parameter Fitur Leksikal</th>'
                '<th style="width: 22%;">Nilai Terukur</th>'
                '<th style="width: 46%;">Deskripsi & Indikator Keamanan</th>'
                '</tr>'
                '</thead>'
                f'<tbody>{rows_joined}</tbody>'
                '</table>'
                '</div>'
                '</div>'
            )
            st.markdown(table_markup, unsafe_allow_html=True)

# ==============================================================================
# 3. BATCH THREAT TRIAGE (CSV UPLOAD)
# ==============================================================================
elif menu == "🔍 Batch Threat Triage (CSV)":
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #E8F5F1; margin-bottom: 4px;">Triase Massal Dataset URL (Batch Mode)</h2>
        <p style="font-size: 13px; color: #89AAA2; margin: 0;">Pemrosesan file CSV berkecepatan tinggi (~276.000 URL/detik) dengan proteksi kebocoran data terintegrasi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_sample, tab_upload = st.tabs(["🚀 Gunakan Dataset Pengujian Resmi (test_set.csv)", "📁 Unggah File CSV Mandiri"])
    df_to_process = None
    
    with tab_sample:
        st.markdown("""
        <div style="background: rgba(16, 39, 34, 0.6); border: 1px solid rgba(53, 214, 192, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <p style="font-size: 13px; color: #E8F5F1; margin: 0;">Ingin menguji kinerja sistem secara langsung? Muat <b>20.175 sampel independen</b> dari partisi data testing resmi.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ MUAT DATA TESTING INDEPENDEN (20.175 SAMPEL)"):
            sample_path = os.path.join("dataset", "processed", "test_set.csv")
            if os.path.exists(sample_path):
                df_to_process = pd.read_csv(sample_path)
                st.success("20.175 sampel testing berhasil dimuat ke buffer memori!")
            else:
                st.error("File test_set.csv tidak ditemukan.")

    with tab_upload:
        uploaded_file = st.file_uploader("Pilih file CSV masukan:", type=["csv"])
        if uploaded_file is not None:
            try:
                df_to_process = pd.read_csv(uploaded_file)
                st.success(f"File '{uploaded_file.name}' dimuat ({len(df_to_process):,} baris).")
            except Exception as e:
                st.error(f"Gagal membaca file CSV: {e}")

    if df_to_process is not None:
        try:
            X_input, url_meta, ground_truth, warnings_list = validate_and_preprocess_input(df_to_process)
            
            for w in warnings_list:
                st.warning(f"⚠️ {w}")
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🛡️ EKSEKUSI TRIASE ANCAMAN", type="primary"):
                with st.spinner("Random Forest sedang memindai seluruh vektor ancaman..."):
                    results_df = run_prediction_pipeline(best_model, X_input, url_meta)
                    
                total_urls = len(results_df)
                phishing_count = (results_df["Prediction"] == "PHISHING").sum()
                legitimate_count = (results_df["Prediction"] == "LEGITIMATE").sum()
                phishing_pct = (phishing_count / total_urls) * 100
                legitimate_pct = (legitimate_count / total_urls) * 100
                
                # Tiga kartu metrik ringkasan
                st.markdown("<br>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                with m1:
                    render_metric_card("Total URL Teranalisis", f"{total_urls:,}", "Vektor Input Terproses", "turquoise")
                with m2:
                    render_metric_card("Terkonfirmasi Legitimate", f"{legitimate_count:,}", f"{legitimate_pct:.2f}% dari populasi", "turquoise")
                with m3:
                    render_metric_card("Teridentifikasi Serangan", f"{phishing_count:,}", f"{phishing_pct:.2f}% dari populasi", "phishing")

                # Visualisasi Donut dan Histogram Sebaran
                st.markdown("""
                <div class="cyber-card">
                    <h3 style="font-size: 16px; font-weight: 700; color: #E8F5F1; margin-bottom: 12px;">📊 Sebaran Proporsi & Probabilitas Serangan</h3>
                """, unsafe_allow_html=True)
                v1, v2 = st.columns(2)
                with v1:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.pie(
                        [legitimate_count, phishing_count],
                        labels=["Legitimate", "Phishing"],
                        autopct="%1.2f%%",
                        colors=["#35D6C0", "#FF5566"],
                        startangle=140,
                        wedgeprops=dict(width=0.4, edgecolor="#061411")
                    )
                    ax.set_title("Proporsi Klasifikasi Ancaman", fontsize=11, fontweight="bold", color="#E8F5F1")
                    fig.patch.set_facecolor('#102722')
                    ax.set_facecolor('#102722')
                    for text in ax.texts:
                        text.set_color("#E8F5F1")
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                    
                with v2:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.histplot(results_df["Phishing_Probability"], bins=30, kde=True, color="#35D6C0", ax=ax)
                    ax.set_title("Distribusi Skor Probabilitas Phishing (%)", fontsize=11, fontweight="bold", color="#E8F5F1")
                    ax.set_xlabel("Probabilitas Phishing (%)", color="#E8F5F1")
                    ax.set_ylabel("Frekuensi URL", color="#E8F5F1")
                    fig.patch.set_facecolor('#102722')
                    ax.set_facecolor('#102722')
                    ax.tick_params(colors='#E8F5F1')
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                st.markdown("</div>", unsafe_allow_html=True)

                # Evaluasi Ground Truth jika ada
                if ground_truth is not None:
                    st.markdown("""
                    <div class="cyber-card">
                        <h3 style="font-size: 16px; font-weight: 700; color: #E8F5F1; margin-bottom: 10px;">🎯 Verifikasi Ground Truth (Label Aktual)</h3>
                    """, unsafe_allow_html=True)
                    from sklearn.metrics import accuracy_score, confusion_matrix
                    acc = accuracy_score(ground_truth, results_df["Predicted_Class"])
                    cm = confusion_matrix(ground_truth, results_df["Predicted_Class"])
                    st.write(f"**Akurasi Pengujian Aktual:** `{acc*100:.4f}%`")
                    cm_df = pd.DataFrame(cm, index=["Actual Legitimate (0)", "Actual Phishing (1)"], columns=["Pred Legitimate (0)", "Pred Phishing (1)"])
                    st.dataframe(cm_df, width="stretch" if hasattr(st, "dataframe") else True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Tabel Hasil & Download
                st.markdown("""
                <div class="cyber-card">
                    <h3 style="font-size: 16px; font-weight: 700; color: #E8F5F1; margin-bottom: 12px;">📋 Log Triase Hasil Prediksi (Menampilkan 200 Sampel Pertama)</h3>
                """, unsafe_allow_html=True)
                st.dataframe(
                    results_df[["URL", "Prediction", "Phishing_Probability", "Confidence_Score"]].head(200),
                    width="stretch" if hasattr(st, "dataframe") else True
                )
                
                export_df = pd.concat([df_to_process, results_df[["Prediction", "Phishing_Probability"]]], axis=1)
                csv_bytes = export_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 UNDUH SELURUH HASIL PREDIKSI (CSV)",
                    data=csv_bytes,
                    file_name="phishguard_detection_results.csv",
                    mime="text/csv"
                )
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Kesalahan validasi data masukan: {e}")

# ==============================================================================
# 4. ANALYTICS & VALIDATION
# ==============================================================================
elif menu == "📊 Analytics & Validation":
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #E8F5F1; margin-bottom: 4px;">Analitika Kinerja Model & Verifikasi Ilmiah</h2>
        <p style="font-size: 13px; color: #89AAA2; margin: 0;">Inspeksi kurva evaluasi empiris pada 20.175 data uji unseen.</p>
    </div>
    """, unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Confusion Matrix & ROC Curve", "Feature Importance & Heatmap"])
    
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="cyber-card" style="margin-bottom: 12px; padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="font-size: 15px; font-weight: 700; color: #E8F5F1; margin: 0;">🎯 Confusion Matrix (DT vs RF)</h3>
                    <span style="font-size: 10px; font-weight: 700; color: #35D6C0; background: rgba(53, 214, 192, 0.12); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(53, 214, 192, 0.25);">20.175 TEST SAMPLES</span>
                </div>
                <p style="font-size: 12px; color: #89AAA2; margin: 4px 0 0 0;">Komparasi False Positive (RF: 1 vs DT: 7) & False Negative.</p>
            </div>
            """, unsafe_allow_html=True)
            cm_path = os.path.join("reports", "confusion_matrix.png")
            if os.path.exists(cm_path):
                st.image(cm_path, caption="Confusion Matrix Decision Tree vs Random Forest", use_container_width=True)
        with c2:
            st.markdown("""
            <div class="cyber-card" style="margin-bottom: 12px; padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="font-size: 15px; font-weight: 700; color: #E8F5F1; margin: 0;">📈 Receiver Operating Characteristic</h3>
                    <span style="font-size: 10px; font-weight: 700; color: #F2C96D; background: rgba(242, 201, 109, 0.12); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(242, 201, 109, 0.25);">AUC = 0.999995</span>
                </div>
                <p style="font-size: 12px; color: #89AAA2; margin: 4px 0 0 0;">Kurva daya pembeda diskriminasi model pada berbagai threshold.</p>
            </div>
            """, unsafe_allow_html=True)
            roc_path = os.path.join("reports", "figures", "roc_curve_comparison.png")
            if os.path.exists(roc_path):
                st.image(roc_path, caption="ROC Curve Comparison (AUC = 0.999995)", use_container_width=True)
            
    with t2:
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("""
            <div class="cyber-card" style="margin-bottom: 12px; padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="font-size: 15px; font-weight: 700; color: #E8F5F1; margin: 0;">🏆 Peringkat Gini Feature Importance</h3>
                    <span style="font-size: 10px; font-weight: 700; color: #9587FF; background: rgba(149, 135, 255, 0.12); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(149, 135, 255, 0.25);">16 FITUR PREDIKTOR</span>
                </div>
                <p style="font-size: 12px; color: #89AAA2; margin: 4px 0 0 0;">Kontribusi relatif fitur prediktor (path_length dominan 38.79%).</p>
            </div>
            """, unsafe_allow_html=True)
            fi_path = os.path.join("reports", "figures", "feature_importance_comparison.png")
            if os.path.exists(fi_path):
                st.image(fi_path, caption="Peringkat Gini Importance 16 Fitur Prediktor", use_container_width=True)
        with c4:
            st.markdown("""
            <div class="cyber-card" style="margin-bottom: 12px; padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="font-size: 15px; font-weight: 700; color: #E8F5F1; margin: 0;">🔥 Heatmap Korelasi Pearson</h3>
                    <span style="font-size: 10px; font-weight: 700; color: #E77DB8; background: rgba(231, 125, 184, 0.12); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(231, 125, 184, 0.25);">MULTIKOLINEARITAS</span>
                </div>
                <p style="font-size: 12px; color: #89AAA2; margin: 4px 0 0 0;">Evaluasi korelasi silang antar-fitur untuk memastikan independensi.</p>
            </div>
            """, unsafe_allow_html=True)
            corr_path = os.path.join("reports", "figures", "correlation_heatmap.png")
            if os.path.exists(corr_path):
                st.image(corr_path, caption="Heatmap Korelasi Pearson Matriks Fitur Asli", use_container_width=True)

# ==============================================================================
# 5. NEURAL ARCHITECTURE (SPECIFICATIONS)
# ==============================================================================
elif menu == "ℹ️ Neural Architecture":
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #E8F5F1; margin-bottom: 4px;">Arsitektur & Spesifikasi Metadata Model</h2>
        <p style="font-size: 13px; color: #89AAA2; margin: 0;">Spesifikasi hyperparameter, lingkungan dependensi, dan jejak pelatihan model Random Forest.</p>
    </div>
    <div class="cyber-card">
    """, unsafe_allow_html=True)
    st.json(metadata)
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 6. DEFENSIVE PROTOCOL (GUIDE)
# ==============================================================================
elif menu == "📖 Defensive Protocol (Guide)":
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #E8F5F1; margin-bottom: 4px;">Protokol Pertahanan & Panduan Metodologis</h2>
        <p style="font-size: 13px; color: #89AAA2; margin: 0;">Dokumentasi teknis peran Defensive AI dalam memitigasi serangan Social Engineering.</p>
    </div>
    
    <div class="cyber-card">
        <h3 style="font-size: 16px; font-weight: 700; color: #35D6C0; margin-bottom: 8px;">1. Analisis False Positive vs False Negative</h3>
        <p style="font-size: 13px; color: #E8F5F1; line-height: 1.6;">
            Dalam domain Keamanan Informasi, trade-off klasifikasi biner menentukan efektivitas operasional SOC (Security Operations Center):
        </p>
        <ul style="font-size: 13px; color: #89AAA2; line-height: 1.7;">
            <li><b style="color: #FF5566;">False Positive (Alarm Palsu):</b> URL sah yang terblokir. Menyebabkan <i>alert fatigue</i> dan mengganggu produktivitas. Model Random Forest kami berhasil menekan FP hingga <b>hanya 1 kasus</b> dari 12.699 URL normal (<b>0.0079%</b>).</li>
            <li><b style="color: #F2C96D;">False Negative (Serangan Lolos):</b> URL phishing yang tidak terdeteksi. Merupakan ancaman fatal pencurian kredensial. Model kami mempertahankan Recall sebesar <b>99.84%</b> (hanya 12 serangan lolos dari 7.476 sampel uji).</li>
        </ul>
    </div>

    <div class="cyber-card">
        <h3 style="font-size: 16px; font-weight: 700; color: #35D6C0; margin-bottom: 8px;">2. Batasan Metodologis Sistem</h3>
        <p style="font-size: 13px; color: #89AAA2; line-height: 1.6;">
            PhishGuard AI menganalisis karakteristik sintaksis, leksikal, dan struktural URL secara offline/batch. Sistem tidak melakukan crawling aktif terhadap konten HTML dinamis halaman web target. Hasil estimasi probabilitas merupakan skor keyakinan statistik ensemble Random Forest, bukan vonis mutlak hukum atas suatu situs web.
        </p>
    </div>
    """, unsafe_allow_html=True)
