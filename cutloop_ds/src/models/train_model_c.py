"""
CUTLOOP Data Science Module — Phase 5: Model C (Material Composition Clustering & Circular Archetypes)
Author: CUTLOOP Data Science Team
Script: src/models/train_model_c.py

Performs unsupervised machine learning (K-Means) on continuous fiber composition vectors
to discover industrial textile recycling archetypes:
- 10-dimensional composition space (Cotton, Polyester, Elastane, Polyamide, Viscose, Wool, Acrylic, Linen, Silk, Lyocell)
- Determines optimal clusters (k=5 industrial circularity archetypes)
- Computes Silhouette score and centroid interpretations
- Saves:
  - saved_models/model_c_kmeans.joblib
  - saved_models/archetype_profiles.json
  - visualizations/model_c_material_clusters.png
  - reports/model_c_metrics.json
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

FIBER_COLS = [
    "cotton", "polyester", "elastane", "polyamide", 
    "viscose", "wool", "acrylic", "linen", "silk", "lyocell"
]

def train_model_c():
    print("[*] Loading cleaned garments dataset for Model C clustering...")
    garments_path = os.path.join(PROCESSED_DIR, "garments_cleaned.csv.gz")
    df = pd.read_csv(garments_path)
    
    X_fiber = df[FIBER_COLS].fillna(0.0).values
    print(f"    Fiber composition vector shape: {X_fiber.shape}")
    
    # K-Means with k=5 circular archetypes
    n_clusters = 5
    print(f"[*] Fitting K-Means Clustering (k={n_clusters})...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_fiber)
    
    # Calculate Silhouette score on a representative sample (for fast execution)
    sample_idx = np.random.RandomState(42).choice(len(X_fiber), size=min(10000, len(X_fiber)), replace=False)
    sil_score = silhouette_score(X_fiber[sample_idx], cluster_labels[sample_idx])
    print(f"    Silhouette Score (Sample 10k): {sil_score:.4f}")
    
    # Analyze Centroids to define industrial archetypes
    centroids = kmeans.cluster_centers_
    archetype_profiles = {}
    
    # Heuristic names for archetypes based on dominant centroid fiber
    for k in range(n_clusters):
        cent = centroids[k]
        top_fib_idx = np.argsort(cent)[::-1]
        top_fibers = {FIBER_COLS[i]: round(float(cent[i]), 1) for i in top_fib_idx if cent[i] > 2.0}
        
        # Name heuristic
        primary = FIBER_COLS[top_fib_idx[0]]
        if primary == "cotton" and top_fibers.get("elastane", 0) > 0:
            name = "Cotton-Dominant Stretch / Denim"
            recyclability = "High mechanical recycling potential; elastane strip required"
        elif primary == "cotton":
            name = "Pure Cotton Mono-Material"
            recyclability = "Ideal for mechanical shredding, yarn re-spinning & composting"
        elif primary in ["polyester", "polyamide"]:
            name = "Synthetic Technical / Sportswear"
            recyclability = "High thermo-mechanical & chemical pellet recycling potential"
        elif primary == "viscose":
            name = "Regenerated Cellulosic (Rayon/Viscose)"
            recyclability = "Chemical dissolving pulp recycling & closed-loop lyocell recovery"
        else:
            name = "Wool / Luxury Blend Archetype"
            recyclability = "Premium garnetting, post-consumer shoddy & carded yarn spinning"
            
        archetype_profiles[f"cluster_{k}"] = {
            "cluster_id": k,
            "archetype_name": name,
            "centroid_composition_pct": top_fibers,
            "garment_count": int((cluster_labels == k).sum()),
            "garment_pct": round(float((cluster_labels == k).sum() / len(cluster_labels) * 100), 2),
            "recycling_pathway": recyclability
        }
        
    print("\n[*] Discovered Circular Archetype Profiles:")
    for k, prof in archetype_profiles.items():
        print(f"    [{k}] {prof['archetype_name']} ({prof['garment_pct']}%): {prof['centroid_composition_pct']}")
        
    # PCA Visualization for 2D Projection
    print("[*] Generating model_c_material_clusters.png via PCA...")
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_fiber[sample_idx])
    
    plt.figure(figsize=(9, 7))
    palette = sns.color_palette("tab10", n_clusters)
    for k in range(n_clusters):
        mask = cluster_labels[sample_idx] == k
        plt.scatter(
            X_pca[mask, 0], X_pca[mask, 1], 
            s=12, alpha=0.5, color=palette[k], 
            label=f"C{k}: {archetype_profiles[f'cluster_{k}']['archetype_name']} ({archetype_profiles[f'cluster_{k}']['garment_pct']}%)"
        )
    plt.title(f"CUTLOOP Model C: Textile Material Archetype Clusters (PCA)\nSilhouette Score: {sil_score:.3f}", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% Variance)", fontsize=10)
    plt.ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% Variance)", fontsize=10)
    plt.legend(frameon=True, facecolor="#ffffff", loc="upper right", markerscale=2.5, fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "model_c_material_clusters.png"), dpi=200)
    plt.close()
    
    # Save Model Artifacts
    joblib.dump(kmeans, os.path.join(SAVED_MODELS_DIR, "model_c_kmeans.joblib"))
    with open(os.path.join(SAVED_MODELS_DIR, "archetype_profiles.json"), "w", encoding="utf-8") as f:
        json.dump(archetype_profiles, f, indent=2)
        
    metrics = {
        "model_name": "Model C — Material Composition Clustering",
        "algorithm": "K-Means",
        "n_clusters": n_clusters,
        "silhouette_score": round(float(sil_score), 4),
        "inertia": round(float(kmeans.inertia_), 2),
        "archetypes": archetype_profiles
    }
    with open(os.path.join(REPORTS_DIR, "model_c_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"[*] Model C completed. Artifacts saved in saved_models/")
    return metrics

if __name__ == "__main__":
    train_model_c()
