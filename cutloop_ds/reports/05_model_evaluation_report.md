# CUTLOOP — Phase 6: Comprehensive Model Evaluation & Optimization Report

## 1. Executive Summary & Model Portfolio
This report documents the rigorous evaluation, optimization, and validation of all four Data Science and Machine Learning models developed for the CUTLOOP Circular Textile Marketplace.

```
+----------------------------------------------------------------------------------------------------+
|                                    CUTLOOP AI & ML SYSTEM ARCHITECTURE                             |
+----------------------------------------------------------------------------------------------------+
|  [Tabular Garments (47,522)]                  [TexSortML Vision (2,252)]                           |
|         |                                                |                                         |
|         v                                                v                                         |
|  +-----------------------------+              +-----------------------------+                      |
|  | Model A: Dominant Fiber     |              | Model B: Deep Vision        |                      |
|  | Classifier (Random Forest)  |              | Classifier (MobileNetV2)    |                      |
|  | Accuracy: 89.97%            |              | 11 Garment Categories       |                      |
|  +-----------------------------+              +-----------------------------+                      |
|         |                                                |                                         |
|         +-----------------------+------------------------+                                         |
|                                 |                                                                  |
|                                 v                                                                  |
|               +-----------------------------------+                                                |
|               | Model C: Material Archetype       |                                                |
|               | Clustering (K-Means, k=5)         |                                                |
|               | Silhouette Score: 0.6657          |                                                |
|               +-----------------------------------+                                                |
|                                 |                                                                  |
|                                 v                                                                  |
|               +-----------------------------------+                                                |
|               | Model D: Secondary Waste          |                                                |
|               | Valuation Engine & Hedonic Price  |                                                |
|               | Parity, Liquidity & Clearing Days |                                                |
|               +-----------------------------------+                                                |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Model A — Tabular Dominant Fiber & Circularity Classifier

### Technical Setup
- **Dataset**: Fast-Fashion Sourced Inventory (47,522 records, 80/20 stratified split: 38,017 Train, 9,505 Test).
- **Features (367 dimensions)**: 350 TF-IDF n-grams from product titles/descriptions + One-Hot encoded categorical attributes (`brand`, `region`, `gender_section`, `parent_category`) + standard scaled continuous circularity metrics.
- **Handling Class Imbalance**: Heuristic inverse square-root class frequency weighting applied.

### Comparative Benchmark
| Model Candidate | Test Accuracy | F1-Score (Macro) | F1-Score (Weighted) | Inference Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Decision Tree Baseline** | 81.64% | 0.7374 | 0.8311 | < 1 ms |
| **Random Forest Ensemble (100 Trees)** | **89.97%** | **0.8381** | **0.9017** | **~3 ms** |

### Class-by-Class Classification Report (Random Forest)
| Target Fiber Class | Precision | Recall | F1-Score | Support (Test) | Industrial Recycling Feasibility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cotton` | **0.99** | **0.94** | **0.97** | 4,797 | Highest: Mechanical shoddy, carded yarn re-spinning |
| `polyester` | 0.87 | 0.87 | **0.87** | 2,635 | High: Thermo-mechanical pelletizing & chemical glycolysis |
| `polyamide` (nylon) | 0.84 | 0.79 | **0.82** | 666 | High: Chemical depolymerization back to caprolactam |
| `viscose` (rayon) | 0.69 | 0.86 | **0.77** | 663 | Medium: Dissolving pulp regeneration |
| `wool` | 0.75 | 0.97 | **0.85** | 200 | Very High: Luxury garnetting & post-consumer carding |
| `linen` | 0.86 | 0.94 | **0.90** | 141 | Very High: Bast fiber re-retting & compostable blending |
| `acrylic` | 0.76 | 0.82 | **0.79** | 147 | Specialized: Non-woven soundproofing & industrial felt |
| `other` | 0.75 | 0.76 | **0.75** | 256 | Mixed sorting stream |

Confusion Matrix artifact saved to `visualizations/model_a_confusion_matrix.png`.

---

## 3. Model B — TexSortML Deep Vision Garment Classifier

### Technical Setup & Evaluation Results
- **Dataset**: TexSortML Benchmark (2,252 images across 11 categories).
- **Split Strategy**: Stratified 70% Train (1,576), 15% Val (338), 15% Test (338).
- **Architecture**: MobileNetV2 with inverted residual bottlenecks and transfer learning.
- **Input Resolution**: $224 \times 224 \times 3$ RGB.
- **Loss**: Class-weighted Cross-Entropy loss.
- **Data Augmentation**: `RandomResizedCrop(224, scale=(0.85, 1.0))`, `RandomHorizontalFlip()`, `ColorJitter()`.
- **Target Classes (11)**: `dress`, `jacket`, `jacket-zipper`, `jeans`, `poloshirt`, `shirt`, `short`, `sweatshirt`, `top`, `trouser`, `tshirt`.

### Performance on Held-Out Test Split (N=338)
- **Test Classification Accuracy**: **86.39%**
- **F1-Score (Macro Avg)**: **0.8015**
- **F1-Score (Weighted Avg)**: **0.8604**

### Optimization & Hardware Footprint
- **Model Size on Disk**: 10.4 MB (`saved_models/texsort_model.pt`).
- **RAM / VRAM Utilization**: < 800 MB RAM during peak CPU execution; easily operates inside the 4 GB VRAM limit of an NVIDIA RTX 3050.
- **Inference Latency**: ~35 ms per single image on CPU, ~6 ms on CUDA GPU.

Confusion Matrix saved to `visualizations/model_b_confusion_matrix.png`, and loss/accuracy curves saved to `visualizations/model_b_training_curves.png`.

---

## 4. Model C — Material Composition Clustering & Circular Archetypes

### Unsupervised Discovery
Unsupervised K-Means clustering was executed on the continuous 10-dimensional fiber composition vectors ($R^{10}$) for all 47,522 garment records.

- **Silhouette Score**: **0.6657** (indicating well-separated, dense clusters).
- **Archetype Profiles Identified**:
  1. **Pure Cotton Mono-Material (49.84%)**: Centroid: 89.5% Cotton, 6.1% Polyester. Prime for circular cotton shredding and circular yarn re-spinning.
  2. **Synthetic Technical Sportswear (27.38%)**: Centroid: 82.8% Polyester, 4.6% Viscose, 3.8% Elastane. Prime for mechanical pelletizing and PET regeneration.
  3. **Synthetic Polyamide / Stretch (6.68%)**: Centroid: 84.2% Polyamide (Nylon), 12.6% Elastane. Technical swim/activewear requiring specialized depolymerization.
  4. **Regenerated Cellulosic (7.76%)**: Centroid: 71.9% Viscose, 9.7% Polyamide, 6.5% Linen. Suitable for chemical dissolving pulp recycling.
  5. **Wool & Luxury Blends (8.34%)**: Centroid: 23.2% Wool, 12.6% Acrylic, 12.5% Linen, 10.4% Lyocell. Suitable for premium shoddy carding.

PCA 2D projection saved to `visualizations/model_c_material_clusters.png`.

---

## 5. Model D — Secondary Textile Waste Valuation Engine

### Addressing Dataset Limitations with Mathematical Parity
A critical finding from Phase 1 is that the fast-fashion dataset contains retailer consumer prices, NOT secondary industrial waste clearing prices. Retail price reflects retail markup, branding, and finished garments—it cannot be used as ground truth for B2B fabric scraps or deadstock rolls.

CUTLOOP resolves this with an **Industrial Hedonic Parity Pricing Model**:

$$P_{\text{clearing}} = \left( \sum_{i} w_i \cdot S_i \right) \times M_{\text{grade}} \times M_{\text{circular}} \times M_{\text{defect}} \times M_{\text{volume}}$$

Where:
- $S_i$: Commodity spot price benchmark for fiber $i$ (Cotton: \$2.40/kg, Polyester: \$1.35/kg, Wool: \$9.50/kg, Nylon: \$2.80/kg).
- $M_{\text{grade}}$: Grade multiplier (Deadstock rolls: 0.85, Fabric remnants: 0.55, Cutting table scraps: 0.30, Rag shred: 0.15).
- $M_{\text{circular}}$: Mono-material recyclability bonus (+25% for $\ge 95\%$ single fiber, -20% for multi-fiber complex blends).
- $M_{\text{defect}}$: Visual defect severity penalty $(1 - 0.5 \times \text{severity})$.
- $M_{\text{volume}}$: Logarithmic batch scale bonus $(W / 50)^{0.08}$.

### Dynamic Liquidity & Clearing Horizon
The engine outputs a **Demand Liquidity Score (0-100)**:
- $\ge 75$: High Market Liquidity (Expected 3-7 days to clear)
- $50-74$: Moderate Liquidity (Expected 8-21 days to clear)
- $< 50$: Specialty Buyer Required (Expected 22-45 days to clear)

Transaction logging schema is formalized in `saved_models/pricing_transaction_schema.json` to enable automated Gradient Boosted regression once CUTLOOP accumulates live transaction data.

---

## 6. Comprehensive Cross-Model Summary Matrix

| Metric Dimension | Model A (Dominant Fiber) | Model B (Vision Sorting) | Model C (Material Archetypes) | Model D (Pricing & Demand) |
| :--- | :--- | :--- | :--- | :--- |
| **Task Type** | Multi-class Classification | Multi-class Classification | Unsupervised Clustering | Hedonic Commodity Valuation |
| **Algorithm** | Random Forest (100 Trees) | MobileNetV2 Transfer Learning | K-Means ($k=5$) | Multi-factor Hedonic Engine |
| **Input Modality** | Text (TF-IDF) + Categorical | $224 \times 224$ RGB Image | Continuous Composition Vector | Fiber Pcts, Grade, Weight |
| **Primary Metric** | **89.97% Accuracy (0.90 F1)** | **86.39% Accuracy (0.86 F1)** | **0.6657 Silhouette Score** | **Demand Liquidity Index** |
| **Model Size** | 31.4 MB | 10.4 MB | 0.19 MB | Code / Schema (< 1 MB) |
| **Inference Latency**| ~3 ms | ~35 ms (CPU) / ~6 ms (GPU) | < 1 ms | < 1 ms |
| **FastAPI Route** | `POST /predict/material` | `POST /predict/image` | `POST /analyze/composition` | `POST /estimate/price` |
| **Integration** | Automated Listing Tagger | AI Material Scanner | Circularity Badge | Listing Pricing Suggestion |
