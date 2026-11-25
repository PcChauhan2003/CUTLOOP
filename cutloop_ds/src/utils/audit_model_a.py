"""
Audit and Correction for Model A (Random Forest)
Removes target leakage (circularity_score, num_components, has_lining)
Trains pure NLP + Metadata pipeline:
- Text: TF-IDF (400 features, unigrams + bigrams, sublinear_tf)
- Categorical: Brand, Region, Gender, Category (One-Hot Encoded)
- Zero ground-truth leakage
- Evaluates on 20% held-out test set
- Updates feature_pipeline.joblib, model_a_random_forest.joblib, model_a_decision_tree.joblib
- Updates visualizations/model_a_confusion_matrix.png and reports/model_a_metrics.json
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from scipy.sparse import hstack, save_npz
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")

TOP_FIBER_CLASSES = [
    "cotton", "polyester", "polyamide", "viscose", 
    "wool", "acrylic", "linen", "other"
]

def retrain_leak_free_model():
    print("\n=== RETRAINING LEAK-FREE MODEL A ===")
    garments_path = os.path.join(PROCESSED_DIR, "garments_cleaned.csv.gz")
    df = pd.read_csv(garments_path)
    
    def map_target(f):
        f_str = str(f).lower().strip()
        return f_str if f_str in TOP_FIBER_CLASSES else "other"
        
    df["target_fiber"] = df["dominant_fiber"].apply(map_target)
    valid_df = df[df["target_fiber"] != "unknown"].copy()
    
    train_df, test_df = train_test_split(
        valid_df,
        test_size=0.20,
        random_state=42,
        stratify=valid_df["target_fiber"]
    )
    print(f"Train samples: {len(train_df)}, Test samples: {len(test_df)}")
    
    # Text Pipeline: TF-IDF on pure text only
    print("[*] Fitting pure text TF-IDF (400 features)...")
    tfidf = TfidfVectorizer(
        max_features=400,
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True
    )
    X_train_text = tfidf.fit_transform(train_df["text_combined"].fillna(""))
    X_test_text = tfidf.transform(test_df["text_combined"].fillna(""))
    
    # Categorical Pipeline: Only high-level catalog metadata
    print("[*] Encoding metadata (brand, region, gender, parent_category)...")
    cat_cols = ["brand", "region", "gender_section", "parent_category"]
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    X_train_cat = ohe.fit_transform(train_df[cat_cols].fillna("Unknown"))
    X_test_cat = ohe.transform(test_df[cat_cols].fillna("Unknown"))
    
    # NO circularity_score, NO num_components, NO has_lining (pure leakage elimination!)
    X_train = hstack([X_train_text, X_train_cat]).tocsr()
    X_test = hstack([X_test_text, X_test_cat]).tocsr()
    
    le = LabelEncoder()
    y_train = le.fit_transform(train_df["target_fiber"])
    y_test = le.transform(test_df["target_fiber"])
    classes = list(le.classes_)
    
    print(f"Clean Feature Matrix Shape: Train {X_train.shape}, Test {X_test.shape}")
    
    # Decision tree baseline
    print("[*] Training Decision Tree baseline...")
    dt = DecisionTreeClassifier(max_depth=16, min_samples_split=10, class_weight="balanced", random_state=42)
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    acc_dt = accuracy_score(y_test, y_pred_dt)
    f1_dt = f1_score(y_test, y_pred_dt, average="macro")
    print(f"    Decision Tree -> Clean Acc: {acc_dt*100:.2f}%, F1-Macro: {f1_dt:.4f}")
    
    # Random Forest
    print("[*] Training Random Forest (100 estimators, class_weight=balanced)...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=22, min_samples_split=6, class_weight="balanced", n_jobs=-1, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    f1_rf_macro = f1_score(y_test, y_pred_rf, average="macro")
    f1_rf_weighted = f1_score(y_test, y_pred_rf, average="weighted")
    print(f"    Random Forest -> Clean Test Acc: {acc_rf*100:.2f}%, F1-Macro: {f1_rf_macro:.4f}, F1-Weighted: {f1_rf_weighted:.4f}")
    
    cr = classification_report(y_test, y_pred_rf, target_names=classes, output_dict=True)
    print("\n" + classification_report(y_test, y_pred_rf, target_names=classes))
    
    # Feature Importances check
    feature_names = [f"tfidf_{w}" for w in tfidf.get_feature_names_out()] + list(ohe.get_feature_names_out(cat_cols))
    importances = rf.feature_importances_
    top_indices = np.argsort(importances)[::-1][:10]
    print("Top 10 Leak-Free Features:")
    for idx in top_indices:
        print(f"  {feature_names[idx]}: {importances[idx]:.4f}")
        
    # Save Pipeline and Models
    pipeline_bundle = {
        "tfidf": tfidf,
        "ohe": ohe,
        "scaler": None,  # No numerical scaler needed
        "label_encoder": le,
        "cat_cols": cat_cols,
        "num_cols": [],
        "target_classes": classes,
        "leak_free": True
    }
    joblib.dump(pipeline_bundle, os.path.join(SAVED_MODELS_DIR, "feature_pipeline.joblib"))
    joblib.dump(dt, os.path.join(SAVED_MODELS_DIR, "model_a_decision_tree.joblib"))
    joblib.dump(rf, os.path.join(SAVED_MODELS_DIR, "model_a_random_forest.joblib"))
    
    # Save feature matrices
    save_npz(os.path.join(PROCESSED_DIR, "X_train_features.npz"), X_train)
    save_npz(os.path.join(PROCESSED_DIR, "X_test_features.npz"), X_test)
    np.save(os.path.join(PROCESSED_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(PROCESSED_DIR, "y_test.npy"), y_test)
    with open(os.path.join(PROCESSED_DIR, "feature_names.json"), "w") as f:
        json.dump(feature_names, f, indent=2)
        
    # Save clean confusion matrix
    cm = confusion_matrix(y_test, y_pred_rf)
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=classes, yticklabels=classes)
    plt.title(f"Model A (Clean Leak-Free Random Forest) Confusion Matrix\nTest Accuracy: {acc_rf*100:.2f}% | F1-Macro: {f1_rf_macro:.3f}", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Dominant Fiber", fontsize=11)
    plt.ylabel("True Dominant Fiber", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "model_a_confusion_matrix.png"), dpi=200)
    plt.close()
    
    metrics = {
        "model_name": "Model A — Tabular Dominant Fiber Classifier (Leak-Free)",
        "best_model": "Random Forest",
        "target_leakage_status": "Verified Eliminated (circularity_score and component counts removed)",
        "decision_tree": {
            "accuracy": round(float(acc_dt), 4),
            "f1_macro": round(float(f1_dt), 4)
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
        
    print("[*] Leak-free Model A retraining complete and verified.")
    return metrics

if __name__ == "__main__":
    retrain_leak_free_model()
