"""
CUTLOOP Data Science Module — Phase 5: Model A (Material & Textile Classifier)
Author: CUTLOOP Data Science Team
Script: src/models/train_model_a.py

Trains and compares:
1. Decision Tree Classifier (Fast baseline, interpretable)
2. Random Forest Classifier (Ensemble, balanced class weights, robust generalization)

Predicts dominant fiber class from multi-modal text + categorical + metadata features.
Evaluates accuracy, macro/weighted precision, recall, F1, and saves:
- saved_models/model_a_random_forest.joblib
- saved_models/model_a_decision_tree.joblib
- visualizations/model_a_confusion_matrix.png
- reports/model_a_evaluation.json
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def train_model_a():
    print("[*] Loading feature matrices for Model A...")
    X_train = load_npz(os.path.join(PROCESSED_DIR, "X_train_features.npz"))
    X_test = load_npz(os.path.join(PROCESSED_DIR, "X_test_features.npz"))
    y_train = np.load(os.path.join(PROCESSED_DIR, "y_train.npy"))
    y_test = np.load(os.path.join(PROCESSED_DIR, "y_test.npy"))
    
    pipeline_info = joblib.load(os.path.join(SAVED_MODELS_DIR, "feature_pipeline.joblib"))
    classes = pipeline_info["target_classes"]
    
    print(f"    Train: {X_train.shape}, Test: {X_test.shape}, Classes: {classes}")
    
    # ---------------------------------------------------------
    # 1. Decision Tree Baseline
    # ---------------------------------------------------------
    print("[*] Training Decision Tree Classifier...")
    dt = DecisionTreeClassifier(
        max_depth=16,
        min_samples_split=10,
        class_weight="balanced",
        random_state=42
    )
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    acc_dt = accuracy_score(y_test, y_pred_dt)
    f1_dt_macro = f1_score(y_test, y_pred_dt, average="macro")
    f1_dt_weighted = f1_score(y_test, y_pred_dt, average="weighted")
    print(f"    Decision Tree -> Acc: {acc_dt*100:.2f}%, F1-Macro: {f1_dt_macro:.4f}, F1-Weighted: {f1_dt_weighted:.4f}")
    
    dt_path = os.path.join(SAVED_MODELS_DIR, "model_a_decision_tree.joblib")
    joblib.dump(dt, dt_path)
    
    # ---------------------------------------------------------
    # 2. Random Forest Ensemble
    # ---------------------------------------------------------
    print("[*] Training Random Forest Classifier (100 estimators)...")
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=6,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    f1_rf_macro = f1_score(y_test, y_pred_rf, average="macro")
    f1_rf_weighted = f1_score(y_test, y_pred_rf, average="weighted")
    print(f"    Random Forest -> Acc: {acc_rf*100:.2f}%, F1-Macro: {f1_rf_macro:.4f}, F1-Weighted: {f1_rf_weighted:.4f}")
    
    rf_path = os.path.join(SAVED_MODELS_DIR, "model_a_random_forest.joblib")
    joblib.dump(rf, rf_path)
    
    # Detailed Classification Report
    cr = classification_report(y_test, y_pred_rf, target_names=classes, output_dict=True)
    print("\n" + classification_report(y_test, y_pred_rf, target_names=classes))
    
    # Confusion Matrix Visualization
    print("[*] Generating model_a_confusion_matrix.png...")
    cm = confusion_matrix(y_test, y_pred_rf)
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=classes, yticklabels=classes)
    plt.title(f"Model A (Random Forest) Confusion Matrix\nTest Accuracy: {acc_rf*100:.2f}% | F1-Macro: {f1_rf_macro:.3f}", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Dominant Fiber", fontsize=11)
    plt.ylabel("True Dominant Fiber", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "model_a_confusion_matrix.png"), dpi=200)
    plt.close()
    
    # Save Metrics JSON
    metrics = {
        "model_name": "Model A — Tabular Dominant Fiber Classifier",
        "best_model": "Random Forest",
        "decision_tree": {
            "accuracy": round(float(acc_dt), 4),
            "f1_macro": round(float(f1_dt_macro), 4),
            "f1_weighted": round(float(f1_dt_weighted), 4)
        },
        "random_forest": {
            "accuracy": round(float(acc_rf), 4),
            "f1_macro": round(float(f1_rf_macro), 4),
            "f1_weighted": round(float(f1_rf_weighted), 4)
        },
        "classification_report": cr,
        "classes": classes
    }
    with open(os.path.join(REPORTS_DIR, "model_a_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"[*] Model A trained, evaluated, and saved to {rf_path}")
    return metrics

if __name__ == "__main__":
    train_model_a()
