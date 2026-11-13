"""
Tahap 5: Model Training
Nama Sistem: PhishGuard AI
Tujuan: Melatih model pembanding (Decision Tree) dan model utama (Random Forest)
        hanya menggunakan data training (80,697 sampel) dengan 16 fitur numerik.
Input : dataset/processed/train_set.csv
Output: models/decision_tree_model.joblib
        models/random_forest_model.joblib
        reports/training_log.txt
"""

import os
import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

def run_model_training(train_csv_path: str, models_dir: str, log_path: str):
    print("=" * 80)
    print("MEMULAI MODEL TRAINING - PHISHGUARD AI")
    print("=" * 80)
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    log_lines = []
    def log(msg=""):
        print(msg)
        log_lines.append(msg)
        
    log("=" * 80)
    log("LOG PELATIHAN MODEL MACHINE LEARNING - PHISHGUARD AI")
    log("=" * 80)
    
    # 1. Membaca data training
    train_df = pd.read_csv(train_csv_path)
    log(f"1. Membaca Data Training dari : {train_csv_path}")
    log(f"   Dimensi Data Training      : {train_df.shape[0]:,} baris, {train_df.shape[1]} kolom")
    
    # Pisahkan X dan y
    feature_cols = [c for c in train_df.columns if c not in ['URL', 'ClassLabel']]
    X_train = train_df[feature_cols].copy()
    y_train = train_df['ClassLabel'].copy()
    
    log(f"   Jumlah Fitur Prediktor (X) : {len(feature_cols)} fitur")
    log(f"   Daftar Fitur               : {', '.join(feature_cols)}")
    log(f"   Distribusi Target (y)      : 0 (Legitimate) = {(y_train == 0).sum():,}, 1 (Phishing) = {(y_train == 1).sum():,}")
    
    # 2. Pelatihan Model 1: Decision Tree Classifier (Pembanding)
    log("\n" + "-" * 80)
    log("2. PELATIHAN MODEL 1: DECISION TREE CLASSIFIER (PEMBANDING)")
    log("-" * 80)
    dt_params = {
        'max_depth': 15,
        'min_samples_split': 10,
        'min_samples_leaf': 5,
        'class_weight': 'balanced',
        'random_state': 42
    }
    log("Hyperparameter Decision Tree:")
    for k, v in dt_params.items():
        log(f"  - {k:20s}: {v}")
        
    dt_model = DecisionTreeClassifier(**dt_params)
    
    # 5-Fold Cross Validation pada Training Data
    log("\nMenjalankan 5-Fold Stratified Cross-Validation pada Training Data...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    start_cv = time.time()
    dt_cv_scores = cross_val_score(dt_model, X_train, y_train, cv=cv, scoring='f1', n_jobs=-1)
    cv_time_dt = time.time() - start_cv
    log(f"CV F1-Scores: {[round(s, 4) for s in dt_cv_scores]}")
    log(f"Mean CV F1  : {dt_cv_scores.mean():.4f} (+/- {dt_cv_scores.std():.4f}) (Waktu CV: {cv_time_dt:.2f} detik)")
    
    # Fit pada seluruh data training
    start_train_dt = time.time()
    dt_model.fit(X_train, y_train)
    dt_train_time = time.time() - start_train_dt
    log(f"Waktu Pelatihan Penuh (Fit)   : {dt_train_time:.2f} detik")
    
    # Simpan Model Decision Tree
    dt_path = os.path.join(models_dir, "decision_tree_model.joblib")
    joblib.dump(dt_model, dt_path)
    log(f"Model disimpan ke             : {dt_path} ({os.path.getsize(dt_path)/(1024*1024):.2f} MB)")
    
    # 3. Pelatihan Model 2: Random Forest Classifier (Model Utama)
    log("\n" + "-" * 80)
    log("3. PELATIHAN MODEL 2: RANDOM FOREST CLASSIFIER (MODEL UTAMA)")
    log("-" * 80)
    rf_params = {
        'n_estimators': 100,
        'max_depth': 20,
        'min_samples_split': 10,
        'min_samples_leaf': 4,
        'class_weight': 'balanced',
        'n_jobs': -1,
        'random_state': 42
    }
    log("Hyperparameter Random Forest:")
    for k, v in rf_params.items():
        log(f"  - {k:20s}: {v}")
        
    rf_model = RandomForestClassifier(**rf_params)
    
    # 5-Fold Cross Validation pada Training Data
    log("\nMenjalankan 5-Fold Stratified Cross-Validation pada Training Data...")
    start_cv = time.time()
    rf_cv_scores = cross_val_score(rf_model, X_train, y_train, cv=cv, scoring='f1', n_jobs=-1)
    cv_time_rf = time.time() - start_cv
    log(f"CV F1-Scores: {[round(s, 4) for s in rf_cv_scores]}")
    log(f"Mean CV F1  : {rf_cv_scores.mean():.4f} (+/- {rf_cv_scores.std():.4f}) (Waktu CV: {cv_time_rf:.2f} detik)")
    
    # Fit pada seluruh data training
    start_train_rf = time.time()
    rf_model.fit(X_train, y_train)
    rf_train_time = time.time() - start_train_rf
    log(f"Waktu Pelatihan Penuh (Fit)   : {rf_train_time:.2f} detik")
    
    # Simpan Model Random Forest
    rf_path = os.path.join(models_dir, "random_forest_model.joblib")
    joblib.dump(rf_model, rf_path)
    log(f"Model disimpan ke             : {rf_path} ({os.path.getsize(rf_path)/(1024*1024):.2f} MB)")
    
    # 4. Ringkasan Pelatihan
    log("\n" + "=" * 80)
    log("RINGKASAN WAKTU DAN HASIL PELATIHAN PADA DATA TRAINING:")
    log("=" * 80)
    log(f"Decision Tree  -> Waktu Fit: {dt_train_time:.2f}s | CV F1: {dt_cv_scores.mean():.4f}")
    log(f"Random Forest  -> Waktu Fit: {rf_train_time:.2f}s | CV F1: {rf_cv_scores.mean():.4f}")
    log("Status Pelatihan: SUKSES (Kedua model siap dievaluasi pada data testing)")
    
    # Tulis laporan
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines) + '\n')
    print(f"\n[SUKSES] Seluruh model telah dilatih dan disimpan. Log di: {log_path}")

if __name__ == "__main__":
    train_file = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "dataset", "processed", "train_set.csv")
    models_folder = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "models")
    training_log_file = os.path.join(r"E:\01. Matkul\Semester 5\01. KI\UAS", "reports", "training_log.txt")
    run_model_training(train_file, models_folder, training_log_file)

