"""
CUTLOOP Data Science Module — Phase 4: Feature Engineering Pipeline
Author: CUTLOOP Data Science Team
Script: src/features/build_features.py

Constructs model-ready features from garments_cleaned.csv.gz:
1. Text Features: TF-IDF (max 350 features, sublinear tf, n-grams 1-2) on product_name + description
2. Categorical Encoders: One-Hot Encoding for brand, gender_section, region, parent_category
3. Numerical Scaling: Standard scaling for continuous circularity indicators
4. Target Encoding: Stratified 80/20 train/test split for Model A (Dominant Fiber Classifier & Circularity Tier)
5. Saves artifacts to saved_models/ and datasets/processed/
6. Generates reports/04_feature_engineering_report.md and notebooks/04_feature_engineering.ipynb
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from scipy.sparse import hstack, save_npz

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

TOP_FIBER_CLASSES = [
    "cotton", "polyester", "polyamide", "viscose", 
    "wool", "acrylic", "linen", "other"
]

def build_features():
    print("[*] Loading cleaned garments dataset...")
    garments_path = os.path.join(PROCESSED_DIR, "garments_cleaned.csv.gz")
    df = pd.read_csv(garments_path)
    print(f"    Loaded {len(df)} records.")
    
    # Target mapping
    def map_target_fiber(f):
        f_str = str(f).lower().strip()
        if f_str in TOP_FIBER_CLASSES:
            return f_str
        return "other"
        
    df["target_fiber"] = df["dominant_fiber"].apply(map_target_fiber)
    
    valid_df = df[df["target_fiber"] != "unknown"].copy()
    print(f"    Valid records for dominant fiber modeling: {len(valid_df)}")
    print("    Target distribution:\n", valid_df["target_fiber"].value_counts())
    
    # Stratified Train/Test split (80/20)
    train_df, test_df = train_test_split(
        valid_df,
        test_size=0.20,
        random_state=42,
        stratify=valid_df["target_fiber"]
    )
    print(f"    Split: {len(train_df)} Train, {len(test_df)} Test.")
    
    # Text Pipeline: TF-IDF
    print("[*] Fitting TF-IDF Vectorizer on garment descriptions...")
    tfidf = TfidfVectorizer(
        max_features=350,
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True
    )
    X_train_text = tfidf.fit_transform(train_df["text_combined"].fillna(""))
    X_test_text = tfidf.transform(test_df["text_combined"].fillna(""))
    
    # Categorical Pipeline: Brand, Region, Gender, Category
    print("[*] Encoding Categorical Attributes...")
    cat_cols = ["brand", "region", "gender_section", "parent_category"]
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    X_train_cat = ohe.fit_transform(train_df[cat_cols].fillna("Unknown"))
    X_test_cat = ohe.transform(test_df[cat_cols].fillna("Unknown"))
    
    # Numerical Pipeline: num_components, has_lining, has_recycled, circularity_score
    num_cols = ["num_components", "has_lining", "has_recycled", "circularity_score"]
    scaler = StandardScaler()
    X_train_num = scaler.fit_transform(train_df[num_cols].astype(float))
    X_test_num = scaler.transform(test_df[num_cols].astype(float))
    
    # Combine sparse matrices
    X_train_combined = hstack([X_train_text, X_train_cat, X_train_num]).tocsr()
    X_test_combined = hstack([X_test_text, X_test_cat, X_test_num]).tocsr()
    
    # Label encode target
    le = LabelEncoder()
    y_train = le.fit_transform(train_df["target_fiber"])
    y_test = le.transform(test_df["target_fiber"])
    
    print(f"[*] Combined Feature Matrix Shape: Train {X_train_combined.shape}, Test {X_test_combined.shape}")
    
    # Save Pipeline and Transformers
    pipeline_bundle = {
        "tfidf": tfidf,
        "ohe": ohe,
        "scaler": scaler,
        "label_encoder": le,
        "cat_cols": cat_cols,
        "num_cols": num_cols,
        "target_classes": list(le.classes_)
    }
    pipeline_path = os.path.join(SAVED_MODELS_DIR, "feature_pipeline.joblib")
    joblib.dump(pipeline_bundle, pipeline_path)
    print(f"[*] Saved feature transformation pipeline to: {pipeline_path}")
    
    # Save Matrices
    save_npz(os.path.join(PROCESSED_DIR, "X_train_features.npz"), X_train_combined)
    save_npz(os.path.join(PROCESSED_DIR, "X_test_features.npz"), X_test_combined)
    np.save(os.path.join(PROCESSED_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(PROCESSED_DIR, "y_test.npy"), y_test)
    
    # Save feature names
    feature_names = (
        [f"tfidf_{w}" for w in tfidf.get_feature_names_out()] +
        list(ohe.get_feature_names_out(cat_cols)) +
        num_cols
    )
    with open(os.path.join(PROCESSED_DIR, "feature_names.json"), "w", encoding="utf-8") as f:
        json.dump(feature_names, f, indent=2)
        
    # Generate Phase 4 Report
    report_path = os.path.join(REPORTS_DIR, "04_feature_engineering_report.md")
    report_content = f"""# CUTLOOP — Phase 4: Feature Engineering Report

## 1. Feature Engineering Overview
- **Raw Samples Available**: {len(valid_df):,}
- **Train Partition (80%)**: {len(train_df):,}
- **Test Partition (20%)**: {len(test_df):,}
- **Total Engineered Feature Dimension**: {X_train_combined.shape[1]} features

---

## 2. Feature Modalities & Transformation Architecture

### A. Textual Representations (TF-IDF)
- **Input**: Concatenated product name and product description (`text_combined`).
- **Configuration**:
  - `max_features`: 350
  - `ngram_range`: (1, 2) unigrams and bigrams
  - `sublinear_tf`: True (logarithmic term frequency scaling $1 + \log(tf)$)
  - `stop_words`: Standard English

### B. Categorical Features (One-Hot Encoding)
- Categorical Columns: `brand`, `region`, `gender_section`, `parent_category`
- Total One-Hot Dimensions: {X_train_cat.shape[1]} binary indicator channels
- `handle_unknown`: 'ignore' (guarantees runtime resilience on unseen categories)

### C. Continuous Circularity & Metadata Metrics
- Features: `num_components`, `has_lining`, `has_recycled`, `circularity_score`
- Normalization: `StandardScaler` (zero mean, unit variance)

### D. Target Class Distribution (`target_fiber`)
| Class Name | Train Count | Test Count | Total | Class % |
| :--- | :--- | :--- | :--- | :--- |
"""
    for cls_name, cls_idx in zip(le.classes_, range(len(le.classes_))):
        c_tr = int((y_train == cls_idx).sum())
        c_te = int((y_test == cls_idx).sum())
        tot = c_tr + c_te
        report_content += f"| `{cls_name}` | {c_tr:,} | {c_te:,} | {tot:,} | {tot/len(valid_df)*100:.2f}% |\n"
        
    report_content += f"""
---

## 3. Persistent Feature Artifacts Produced
- **Scikit-learn Transformers Bundle**: `saved_models/feature_pipeline.joblib`
- **Sparse Feature Matrices**:
  - `datasets/processed/X_train_features.npz` ({X_train_combined.shape})
  - `datasets/processed/X_test_features.npz` ({X_test_combined.shape})
- **Target Arrays**: `y_train.npy`, `y_test.npy`
- **Feature Names Index**: `datasets/processed/feature_names.json`
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Feature Engineering Report saved to: {report_path}")

if __name__ == "__main__":
    build_features()
