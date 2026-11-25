"""
CUTLOOP Data Science Post-Implementation Verification Script
Covers Section 2 (Model B Vision Audit) & Section 3 (Model C K-Means Audit)
"""

import os
import sys
import json
import hashlib
import zipfile
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, accuracy_score, f1_score, classification_report, confusion_matrix
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
WORKSPACE_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
PROCESSED_DIR = os.path.join(DATASETS_DIR, "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ZIP_PATH = os.path.join(WORKSPACE_ROOT, "TexSortML-Pictures.zip")
MANIFEST_PATH = os.path.join(PROCESSED_DIR, "image_splits_manifest.csv")
MODEL_B_PATH = os.path.join(SAVED_MODELS_DIR, "texsort_model.pt")
CLASSES_PATH = os.path.join(SAVED_MODELS_DIR, "texsort_classes.json")

results = {}

print("=======================================================")
print("=== 1. VERIFY MODEL B (MobileNetV2 TexSortML Audit) ===")
print("=======================================================")

# 1.1 Inspect raw zip file
if os.path.exists(ZIP_PATH):
    print(f"Opening raw archive: {ZIP_PATH} ({os.path.getsize(ZIP_PATH)/(1024*1024):.1f} MB)...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        all_files = [f for f in z.namelist() if not f.endswith('/') and not f.startswith('__MACOSX') and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Total image files in TexSortML-Pictures.zip: {len(all_files)}")
        
        stages = {}
        for f in all_files:
            parts = f.replace('\\', '/').split('/')
            # E.g. TexSortML-Pictures/stage-mixed/category/file
            for part in parts:
                if 'stage' in part.lower():
                    stages[part] = stages.get(part, 0) + 1
                    break
        print("Stage breakdown in zip:", stages)
        results["zip_total_images"] = len(all_files)
        results["zip_stage_breakdown"] = stages
else:
    print(f"Warning: {ZIP_PATH} not found.")

# 1.2 Inspect image splits manifest
if os.path.exists(MANIFEST_PATH):
    df_manifest = pd.read_csv(MANIFEST_PATH)
    print(f"\nManifest total rows: {len(df_manifest)}")
    print("Split distribution:")
    print(df_manifest["split"].value_counts())
    print("\nClass distribution across full manifest:")
    print(df_manifest["category"].value_counts())
    
    # 1.3 Check for image duplicates across splits via MD5
    print("\n[*] Checking for image duplicates across train/val/test splits via MD5 hashes...")
    split_hashes = {"train": {}, "val": {}, "test": {}}
    duplicates_across_splits = []
    
    for idx, row in df_manifest.iterrows():
        filepath = os.path.join(PROCESSED_DIR, row["relative_path"])
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()
            current_split = row["split"]
            for other_split, hash_dict in split_hashes.items():
                if other_split != current_split and h in hash_dict:
                    duplicates_across_splits.append({
                        "file": row["filename"],
                        "current_split": current_split,
                        "other_split": other_split,
                        "matched_file": hash_dict[h]
                    })
            split_hashes[current_split][h] = row["filename"]
            
    print(f"Unique files: train={len(split_hashes['train'])}, val={len(split_hashes['val'])}, test={len(split_hashes['test'])}")
    print(f"Duplicate images found across splits: {len(duplicates_across_splits)}")
    results["cross_split_duplicates_count"] = len(duplicates_across_splits)
    
    # 1.4 Evaluate Model B on held-out test split
    print("\n[*] Evaluating Model B Checkpoint on held-out test set...")
    with open(CLASSES_PATH, "r", encoding="utf-8") as f:
        class_meta = json.load(f)
    categories = class_meta["categories"]
    class_to_idx = {c: i for i, c in enumerate(categories)}
    print(f"Loaded {len(categories)} categories: {categories}")
    
    # Load model architecture
    model_b = models.mobilenet_v2(weights=None)
    in_features = model_b.classifier[1].in_features
    model_b.classifier = nn.Sequential(
        nn.Dropout(p=0.2),
        nn.Linear(in_features, 256),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.2),
        nn.Linear(256, len(categories))
    )
    
    state_dict = torch.load(MODEL_B_PATH, map_location="cpu")
    model_b.load_state_dict(state_dict)
    model_b.eval()
    
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    test_df = df_manifest[df_manifest["split"] == "test"].copy()
    y_true = []
    y_pred = []
    
    with torch.no_grad():
        for _, row in test_df.iterrows():
            img_path = os.path.join(PROCESSED_DIR, row["relative_path"])
            if os.path.exists(img_path):
                img = Image.open(img_path).convert("RGB")
                tensor = eval_transform(img).unsqueeze(0)
                out = model_b(tensor)
                pred_idx = torch.argmax(out, dim=1).item()
                true_idx = class_to_idx[row["category"]]
                y_true.append(true_idx)
                y_pred.append(pred_idx)
                
    test_acc = accuracy_score(y_true, y_pred)
    test_macro_f1 = f1_score(y_true, y_pred, average="macro")
    test_weighted_f1 = f1_score(y_true, y_pred, average="weighted")
    cm = confusion_matrix(y_true, y_pred)
    
    print(f"\nModel B Held-Out Test Set Verification (n={len(y_true)}):")
    print(f"  Test Accuracy:    {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"  Test Macro F1:    {test_macro_f1:.4f}")
    print(f"  Test Weighted F1: {test_weighted_f1:.4f}")
    
    report_dict = classification_report(y_true, y_pred, target_names=categories, output_dict=True)
    report_text = classification_report(y_true, y_pred, target_names=categories)
    print("\nClassification Report:\n", report_text)
    
    results["model_b"] = {
        "test_samples": len(y_true),
        "test_accuracy": float(test_acc),
        "test_macro_f1": float(test_macro_f1),
        "test_weighted_f1": float(test_weighted_f1),
        "categories": categories,
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict
    }

print("\n=======================================================")
print("=== 2. VERIFY MODEL C (K-Means Clustering Audit) ======")
print("=======================================================")

garments_path = os.path.join(PROCESSED_DIR, "garments_cleaned.csv.gz")
df_garments = pd.read_csv(garments_path)
fiber_cols = [
    "cotton", "polyester", "elastane", "polyamide", 
    "viscose", "wool", "acrylic", "linen", "silk", "other"
]
X_fibers = df_garments[fiber_cols].fillna(0.0).values
print(f"Garments dataset rows: {len(df_garments)}")
print(f"Input features for K-Means (10D continuous fiber percentages): {fiber_cols}")
print(f"Feature ranges (min, max): min={X_fibers.min()}, max={X_fibers.max()}")

# Elbow & Silhouette Analysis for k=2..8
np.random.seed(42)
sample_idx = np.random.choice(len(X_fibers), size=min(10000, len(X_fibers)), replace=False)
X_sub = X_fibers[sample_idx]

elbow_results = {}
silhouette_results = {}
print("\n[*] Running Elbow & Silhouette sweep across k=2..8 (10,000 stratified samples):")
for k in range(2, 9):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_sub)
    inertia = km.inertia_
    sil = silhouette_score(X_sub, km.labels_)
    elbow_results[k] = float(inertia)
    silhouette_results[k] = float(sil)
    print(f"  k={k}: Inertia={inertia:,.1f}, Silhouette Score={sil:.4f}")

# Full dataset fit for k=5
km5 = KMeans(n_clusters=5, random_state=42, n_init=10)
km5.fit(X_fibers)
df_garments["cluster"] = km5.labels_

full_sil = silhouette_score(X_sub, km5.predict(X_sub))
print(f"\nFinal k=5 Silhouette Score on sample: {full_sil:.4f}")

cluster_counts = df_garments["cluster"].value_counts().to_dict()
print("\nCluster counts (k=5):", cluster_counts)

# Centroid profiles
centroids = km5.cluster_centers_
centroid_df = pd.DataFrame(centroids, columns=fiber_cols)
print("\nCentroid fiber percentages (top fibers per cluster):")
for c_id in range(5):
    top_fibers = centroid_df.iloc[c_id].sort_values(ascending=False).head(3)
    fibers_str = ", ".join([f"{f}: {v:.1f}%" for f, v in top_fibers.items() if v > 1.0])
    print(f"  Cluster {c_id} (n={cluster_counts.get(c_id, 0)}): {fibers_str}")

results["model_c"] = {
    "k": 5,
    "input_features": fiber_cols,
    "elbow_inertia": elbow_results,
    "silhouette_scores": silhouette_results,
    "final_silhouette_score": float(full_sil),
    "cluster_counts": {str(k): int(v) for k, v in cluster_counts.items()},
    "centroids": centroid_df.to_dict(orient="records")
}

# Save verification results
AUDIT_RESULTS_PATH = os.path.join(REPORTS_DIR, "audit_verification_results.json")
with open(AUDIT_RESULTS_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n[*] Audit verification complete. Results saved to {AUDIT_RESULTS_PATH}")
