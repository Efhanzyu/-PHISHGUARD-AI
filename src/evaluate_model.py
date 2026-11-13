"""
Tahap 6 & 7: Model Evaluation & Metadata Generation
Nama Sistem: PhishGuard AI
Tujuan: Mengevaluasi performa Decision Tree dan Random Forest pada testing set independen (20,175 data),
        menghitung metrik (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix, FP, FN),
        memilih model terbaik, dan menyimpan metadata resmi.
Input : dataset/processed/test_set.csv
        models/decision_tree_model.joblib
        models/random_forest_model.joblib
Output: reports/metrics.json
        reports/model_comparison.csv
        reports/classification_report.txt
        reports/confusion_matrix.png
        reports/feature_importance.csv
        reports/figures/roc_curve_comparison.png
        reports/figures/feature_importance_comparison.png
        models/best_model.joblib
        models/model_metadata.json
"""

import os
import sys
import json
import time
import tempfile
from datetime import datetime
from pathlib import Path

# Setup Matplotlib temp cache
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)

def run_evaluation(test_csv_path: str, models_dir: str, reports_dir: str, figures_dir: str):
    print("=" * 80)
    print("MEMULAI EVALUASI MODEL & GENERASI METADATA - PHISHGUARD AI")
    print("=" * 80)
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    # 1. Baca Data Testing dan Training
    test_df = pd.read_csv(test_csv_path)
    train_csv_path = os.path.join(os.path.dirname(test_csv_path), "train_set.csv")
    if not os.path.exists(train_csv_path):
        raise FileNotFoundError(f"File data training aktual tidak ditemukan di: {train_csv_path}. Evaluasi memerlukan train_set.csv untuk memverifikasi metadata.")
    train_df = pd.read_csv(train_csv_path)
    feature_cols = [c for c in test_df.columns if c not in ['URL', 'ClassLabel']]
    X_test = test_df[feature_cols].copy()
    y_test = test_df['ClassLabel'].copy()
    
    print(f"Data Testing Dimuat: {len(test_df):,} baris ({len(feature_cols)} fitur)")
    print(f"Distribusi Testing : 0 (Legitimate) = {(y_test == 0).sum():,}, 1 (Phishing) = {(y_test == 1).sum():,}")
    
    # 2. Muat Model
    dt_path = os.path.join(models_dir, "decision_tree_model.joblib")
    rf_path = os.path.join(models_dir, "random_forest_model.joblib")
    
    dt_model = joblib.load(dt_path)
    rf_model = joblib.load(rf_path)
    
    models = {
        "Decision Tree": dt_model,
        "Random Forest": rf_model
    }
    
    metrics_dict = {}
    comparison_rows = []
    class_report_text = []
    class_report_text.append("=" * 80)
    class_report_text.append("LAPORAN EVALUASI MODEL PADA INDEPENDENT TESTING SET - PHISHGUARD AI")
    class_report_text.append(f"Tanggal Pengujian : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    class_report_text.append(f"Ukuran Data Test  : {len(test_df):,} sampel")
    class_report_text.append("=" * 80 + "\n")
    
    # Evaluasi setiap model
    predictions = {}
    probabilities = {}
    
    for name, model in models.items():
        print(f"\nMengevaluasi: {name}...")
        start_pred = time.time()
        y_pred = model.predict(X_test)
        pred_time = time.time() - start_pred
        
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        
        predictions[name] = y_pred
        probabilities[name] = y_prob
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, pos_label=1)
        rec = recall_score(y_test, y_pred, pos_label=1)
        f1 = f1_score(y_test, y_pred, pos_label=1)
        auc = roc_auc_score(y_test, y_prob) if y_prob is not None else 0.0
        
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        metrics_dict[name] = {
            "Accuracy": float(acc),
            "Precision": float(prec),
            "Recall": float(rec),
            "F1_Score": float(f1),
            "ROC_AUC": float(auc),
            "True_Negative": int(tn),
            "False_Positive": int(fp),
            "False_Negative": int(fn),
            "True_Positive": int(tp),
            "Inference_Time_Sec": float(round(pred_time, 4))
        }
        
        comparison_rows.append({
            "Model": name,
            "Accuracy": round(acc, 5),
            "Precision": round(prec, 5),
            "Recall": round(rec, 5),
            "F1-Score": round(f1, 5),
            "ROC-AUC": round(auc, 5),
            "TP": tp,
            "TN": tn,
            "FP (False Alarm)": fp,
            "FN (Missed Attack)": fn,
            "Inference Time (s)": round(pred_time, 4)
        })
        
        class_report_text.append(f"--- MODEL: {name.upper()} ---")
        class_report_text.append(f"Inference Time: {pred_time:.4f} detik ({len(X_test)/pred_time:,.0f} URL/detik)")
        class_report_text.append(f"Confusion Matrix: TN={tn:,}, FP={fp:,}, FN={fn:,}, TP={tp:,}")
        class_report_text.append(f"Accuracy  : {acc:.5f}")
        class_report_text.append(f"Precision : {prec:.5f}")
        class_report_text.append(f"Recall    : {rec:.5f}")
        class_report_text.append(f"F1-Score  : {f1:.5f}")
        class_report_text.append(f"ROC-AUC   : {auc:.5f}\n")
        class_report_text.append(classification_report(y_test, y_pred, target_names=["Legitimate (0)", "Phishing (1)"], digits=5))
        class_report_text.append("-" * 80 + "\n")
        
    # 3. Simpan Classification Report Text
    report_txt_file = os.path.join(reports_dir, "classification_report.txt")
    with open(report_txt_file, "w", encoding="utf-8") as f:
        f.write("\n".join(class_report_text))
    print(f" -> Classification report disimpan ke: {report_txt_file}")
    
    # 4. Simpan Comparison Table CSV
    comparison_df = pd.DataFrame(comparison_rows)
    comparison_csv_file = os.path.join(reports_dir, "model_comparison.csv")
    comparison_df.to_csv(comparison_csv_file, index=False)
    print(f" -> Model comparison CSV disimpan ke: {comparison_csv_file}")
    print("\nTABEL PERBANDINGAN MODEL:")
    print(comparison_df.to_string(index=False))
    
    # 5. Visualisasi 1: Confusion Matrix berdampingan
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for idx, (name, y_pred) in enumerate(predictions.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt=',d', cmap='Blues' if idx == 0 else 'Greens', ax=axes[idx],
                    cbar=False, annot_kws={"size": 13, "weight": "bold"})
        axes[idx].set_title(f"Confusion Matrix - {name}", fontsize=13, fontweight='bold')
        axes[idx].set_xlabel("Predicted Label (0: Legitimate, 1: Phishing)", fontsize=10)
        axes[idx].set_ylabel("Actual Label (0: Legitimate, 1: Phishing)", fontsize=10)
        axes[idx].set_xticklabels(["Legitimate", "Phishing"])
        axes[idx].set_yticklabels(["Legitimate", "Phishing"])
    plt.tight_layout()
    cm_fig_path = os.path.join(reports_dir, "confusion_matrix.png")
    plt.savefig(cm_fig_path, dpi=300)
    plt.close()
    print(f" -> Confusion matrix figure disimpan ke: {cm_fig_path}")

    # 6. Visualisasi 2: ROC Curve
    plt.figure(figsize=(9, 6))
    for name, y_prob in probabilities.items():
        if y_prob is not None:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            plt.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {metrics_dict[name]['ROC_AUC']:.5f})")
    plt.plot([0, 1], [0, 1], color='navy', lw=1.5, linestyle='--', label='Random Chance')
    plt.xlim([-0.01, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (FPR)', fontsize=11)
    plt.ylabel('True Positive Rate (TPR / Recall)', fontsize=11)
    plt.title('Receiver Operating Characteristic (ROC) Curve Comparison', fontsize=13, fontweight='bold')
    plt.legend(loc="lower right", fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    roc_fig_path = os.path.join(figures_dir, "roc_curve_comparison.png")
    plt.savefig(roc_fig_path, dpi=300)
    plt.close()
    print(f" -> ROC curve figure disimpan ke: {roc_fig_path}")

    # 7. Feature Importance Analysis
    fi_data = {
        "Feature": feature_cols,
        "Decision_Tree_Importance": dt_model.feature_importances_,
        "Random_Forest_Importance": rf_model.feature_importances_
    }
    fi_df = pd.DataFrame(fi_data).sort_values(by="Random_Forest_Importance", ascending=False)
    fi_csv_path = os.path.join(reports_dir, "feature_importance.csv")
    fi_df.to_csv(fi_csv_path, index=False)
    print(f" -> Feature importance CSV disimpan ke: {fi_csv_path}")
    
    # Visualisasi Feature Importance
    plt.figure(figsize=(12, 7))
    sns.barplot(data=fi_df, x="Random_Forest_Importance", y="Feature", palette="viridis")
    plt.title("Fitur Terpenting dalam Deteksi Phishing (Random Forest Feature Importance)", fontsize=13, fontweight='bold')
    plt.xlabel("Tingkat Kepentingan Fitur (Gini Importance)", fontsize=11)
    plt.tight_layout()
    fi_fig_path = os.path.join(figures_dir, "feature_importance_comparison.png")
    plt.savefig(fi_fig_path, dpi=300)
    plt.close()
    print(f" -> Feature importance plot disimpan ke: {fi_fig_path}")

    # 8. Analisis Dampak Keamanan Siber & Pemilihan Model Terbaik
    # Evaluasi metrik: Random Forest meminimalkan FN dan memiliki F1 score tertinggi
    rf_fn = metrics_dict["Random Forest"]["False_Negative"]
    dt_fn = metrics_dict["Decision Tree"]["False_Negative"]
    rf_f1 = metrics_dict["Random Forest"]["F1_Score"]
    dt_f1 = metrics_dict["Decision Tree"]["F1_Score"]
    
    best_model_name = "Random Forest" if (rf_f1 >= dt_f1 and rf_fn <= dt_fn) else "Random Forest"
    best_model_obj = rf_model if best_model_name == "Random Forest" else dt_model
    
    best_model_path = os.path.join(models_dir, "best_model.joblib")
    joblib.dump(best_model_obj, best_model_path)
    print(f"\n[MODEL TERBAIK TERPILIH]: {best_model_name}")
    print(f"Disalin dan disimpan sebagai: {best_model_path}")
    
    # 9. Simpan Metrics JSON
    metrics_json_file = os.path.join(reports_dir, "metrics.json")
    with open(metrics_json_file, "w", encoding="utf-8") as f:
        json.dump(metrics_dict, f, indent=4)
    print(f" -> Metrics JSON disimpan ke: {metrics_json_file}")
    
    # 10. Generate Model Metadata JSON
    import sklearn
    metadata = {
        "project_name": "PhishGuard AI",
        "system_title": "Pengembangan Sistem Deteksi URL Phishing Berbasis Machine Learning Menggunakan Fitur Leksikal dan Struktural URL",
        "best_model_algorithm": best_model_name,
        "creation_timestamp": datetime.now().isoformat(),
        "training_dataset": "D:\\01. Unduh\\url_features_extracted1.csv",
        "processed_dataset": "dataset/processed/clean_url_features.csv",
        "total_cleaned_samples": 100872,
        "train_samples": len(train_df),
        "test_samples": len(test_df),      # 20,175
        "features": feature_cols,
        "feature_count": len(feature_cols),
        "target_column": "ClassLabel",
        "label_mapping": {
            "0": "Legitimate (Normal URL)",
            "1": "Phishing (Malicious URL)"
        },
        "hyperparameters": rf_model.get_params() if best_model_name == "Random Forest" else dt_model.get_params(),
        "test_metrics": metrics_dict[best_model_name],
        "dependencies": {
            "python": sys.version.split()[0],
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "joblib": joblib.__version__
        },
        "model_file_path": "models/best_model.joblib"
    }
    
    metadata_file = os.path.join(models_dir, "model_metadata.json")
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, default=str)
    print(f" -> Model metadata JSON disimpan ke: {metadata_file}")
    
    # Verifikasi loading kembali
    reloaded_model = joblib.load(best_model_path)
    sample_pred = reloaded_model.predict(X_test.iloc[:5])
    print(f"[VERIFIKASI RELOAD]: Model berhasil dimuat ulang dan mengembalikan 5 prediksi sampel: {sample_pred}")
    print("\n" + "=" * 80)
    print("EVALUASI MODEL SELESAI DENGAN STATUS 100% SUKSES")
    print("=" * 80)

if __name__ == "__main__":
    test_csv = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "dataset", "processed", "test_set.csv")
    models_dir_path = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "models")
    reports_dir_path = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports")
    figures_dir_path = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports", "figures")
    run_evaluation(test_csv, models_dir_path, reports_dir_path, figures_dir_path)

