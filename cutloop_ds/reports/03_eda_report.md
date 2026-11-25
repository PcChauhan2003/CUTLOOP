# CUTLOOP — Phase 3: Exploratory Data Analysis (EDA) Report

## 1. Executive Summary & Key Findings
This report presents comprehensive exploratory data analysis of the fast-fashion garment inventory dataset (47,522 variants) and the TexSortML vision dataset (2,252 images across 11 categories).

### Critical Discoveries for CUTLOOP Circular Marketplace:
1. **Pervasiveness of Fiber Blends**:
   - **23,775 garments (50.0%)** are single-fiber mono-materials ($\ge 95\%$). These represent prime targets for mechanical recycling and high-value resale.
   - **23,747 garments (50.0%)** are blended materials. Poly-cotton and cotton-elastane blends dominate, requiring chemical separation or specialized downcycling.
2. **Dominant Textile Streams**:
   - Cotton is the leading natural fiber (present in over 57% of garments).
   - Polyester is the leading synthetic fiber (present in over 55% of garments).
   - Elastane (spandex) is present in 40.9% of items (typically 1-5% for stretch), which significantly complicates standard mechanical cotton recycling.
3. **Vision Classifier Feasibility**:
   - TexSortML contains 11 distinct classes with clean labels. Class imbalance exists (poloshirt: 363 images vs jacket-zipper: 51 images). Stratified 70/15/15 sampling guarantees balanced training and evaluation.

---

## 2. Visualizations Generated

| Visualization ID | Filename | Description |
| :--- | :--- | :--- |
| **Figure 1** | `1_brand_distribution.png` | Retailer brand market share (H&M vs Uniqlo) |
| **Figure 2** | `2_category_distribution.png` | Top 12 garment product categories |
| **Figure 3** | `3_top_fibers_distribution.png` | Primary dominant fiber breakdown |
| **Figure 4** | `4_blend_vs_mono_distribution.png` | Recyclability donut: Mono-material vs multi-fiber blends |
| **Figure 5** | `5_circularity_score_distribution.png` | Distribution of circularity index with mean/median markers |
| **Figure 6** | `6_fiber_cooccurrence_heatmap.png` | Correlation matrix of fiber combinations |
| **Figure 7** | `7_texsort_class_distribution.png` | TexSortML image vision classes and stratified split breakdown |
| **Figure 8** | `8_region_gender_cross.png` | Regional sourcing and gender section breakdown |

---

## 3. Detailed Statistics

### Top Garment Categories
- **Tops**: 22,051 garments (46.4%)
- **Bottoms**: 12,076 garments (25.4%)
- **Overall**: 7,664 garments (16.1%)
- **Underwear**: 5,731 garments (12.1%)

### Top Dominant Fibers
- **Cotton**: 23,985 garments (50.5%)
- **Polyester**: 13,176 garments (27.7%)
- **Polyamide**: 3,328 garments (7.0%)
- **Viscose**: 3,316 garments (7.0%)
- **Wool**: 997 garments (2.1%)
- **Acrylic**: 737 garments (1.6%)
- **Linen**: 703 garments (1.5%)
- **Other**: 675 garments (1.4%)

### TexSortML Vision Benchmark Split Summary
- **poloshirt**: 363 images (Train: 254, Val: 55, Test: 54)
- **sweatshirt**: 348 images (Train: 243, Val: 52, Test: 53)
- **short**: 305 images (Train: 213, Val: 46, Test: 46)
- **jacket**: 288 images (Train: 202, Val: 43, Test: 43)
- **shirt**: 240 images (Train: 168, Val: 36, Test: 36)
- **tshirt**: 168 images (Train: 118, Val: 25, Test: 25)
- **dress**: 165 images (Train: 115, Val: 25, Test: 25)
- **trouser**: 123 images (Train: 86, Val: 19, Test: 18)
- **jeans**: 117 images (Train: 82, Val: 18, Test: 17)
- **top**: 84 images (Train: 59, Val: 12, Test: 13)
- **jacket-zipper**: 51 images (Train: 36, Val: 7, Test: 8)

---

## 4. Circular Economy & Machine Learning Implications
1. **Target for Model A (Tabular ML)**: Predict dominant textile fiber and circularity archetype based on garment description and category metadata.
2. **Target for Model B (Vision DL)**: Classify garment image type using transfer learning on MobileNetV2 with class-weighted cross-entropy loss to handle imbalance.
3. **Clustering Strategy (Model C)**: Unsupervised K-Means clustering on the 10-dimensional fiber composition vectors to identify industrial recycling archetypes.
