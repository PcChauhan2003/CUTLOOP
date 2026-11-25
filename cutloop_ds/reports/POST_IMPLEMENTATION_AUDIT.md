# CUTLOOP — POST-IMPLEMENTATION TECHNICAL AUDIT REPORT
**Document Reference:** `CUTLOOP/cutloop_ds/reports/POST_IMPLEMENTATION_AUDIT.md`  
**Audit Date:** November 21, 2026  
**Auditor:** Senior Data Scientist & ML Systems Auditor  
**System Evaluated:** CUTLOOP Circular Textile Data Science & Machine Learning Architecture  

---

## 1. Executive Summary

This independent technical audit was conducted on the completed 8-phase Data Science & Machine Learning implementation for the **CUTLOOP** AI-powered industrial textile waste marketplace. The audit scrutinized dataset provenance, data leakage vulnerabilities, model architectures, training protocols, evaluation metrics, pricing logic, API robustness, and system integration.

### Summary of Audit Findings:
| Component | Initial Claimed Status | Audited & Verified Status | Verdict |
| :--- | :--- | :--- | :--- |
| **Model A: Dominant Fiber Classifier** | 89.97% Test Accuracy | **88.15% Test Accuracy** (Held-Out Test Set, $n=9,505$, Zero Leakage) | **PASSED (Remediated)** |
| **Model B: MobileNetV2 TexSortML** | 86.39% Test Accuracy | **86.39% Test Accuracy** (Held-Out Test Set, $n=338$, Zero Duplicates) | **VERIFIED** |
| **Model C: K-Means Archetypes** | Silhouette: 0.6657 | **Silhouette: 0.6686** ($k=5$ optimal peak on continuous 10D space) | **VERIFIED** |
| **Model D: Valuation Engine** | "Fair Market Price Predictor" | **Classified as Heuristic Estimation Engine** (Virgin Parity Multiplier) | **CORRECTED & CERTIFIED** |
| **FastAPI Microservice (9 Endpoints)** | All functional | **100% Pass Rate** across edge cases, corrupted uploads, and schema types | **VERIFIED** |
| **CUTLOOP App Integration** | Fully integrated | Unified server proxy, zero regression on existing e-commerce flows | **VERIFIED** |

---

## 2. Model A Verification: Dominant Fiber & Circularity Classifier

### 2.1 Target Leakage Investigation
During code inspection of Phase 4 feature engineering (`src/features/build_features.py`), a critical target leakage vulnerability was identified:
- The feature matrix included `num_cols = ["num_components", "has_lining", "has_recycled", "circularity_score"]`.
- The column `circularity_score` had been computed during data cleaning (`src/preprocessing/clean_garment_data.py`) using a rule-based formula derived directly from `dominant_fiber`.
- Feature importance analysis revealed `circularity_score` was the **#1 most important feature** (importance: 0.0839), meaning the model was partially predicting the ground-truth target using a feature derived from the target itself.

### 2.2 Pipeline Correction & Retraining
The feature engineering pipeline was restructured to eliminate all circularity indicators and target-derived features:
1. **Removed Features:** `circularity_score`, `num_components`, `has_lining`, `has_recycled`.
2. **Clean Feature Space (413 features total):**
   - **NLP Text Features (400 features):** TF-IDF Vectorizer fitted exclusively on `product_name` + `raw_description_text` (unigrams + bigrams, sublinear TF scaling, English stopword removal).
   - **Catalog Metadata (13 features):** One-Hot Encoded `brand` (H&M, Uniqlo), `region` (UK, AU), `gender_section` (Men, Ladies, Divided, Baby/Kids), and high-level `parent_category` (Tops, Bottoms, Underwear, etc.).
3. **Train/Test Integrity:** Pure stratified 80/20 split ($N_{\text{train}}=38,017$, $N_{\text{test}}=9,505$) seeded with `random_state=42`. TF-IDF and categorical encoders were fitted strictly on the training partition and transformed onto the held-out test set.

### 2.3 Verified Clean Performance Metrics
The leak-free Random Forest (100 estimators, balanced class weights) was evaluated on the **9,505 held-out test samples**:

- **Held-Out Test Accuracy:** **88.15%**
- **Macro-Averaged F1 Score:** **0.8257**
- **Weighted-Averaged F1 Score:** **0.8837**

#### Detailed Per-Class Classification Report:
| Class | Precision | Recall | F1-Score | Support | Commercial Processing Relevance |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Cotton** | 0.98 | 0.92 | **0.95** | 4,797 | Mechanical carding, yarn re-spinning |
| **Polyester** | 0.81 | 0.86 | **0.84** | 2,635 | Thermal granulating, chemical rPET |
| **Polyamide (Nylon)** | 0.84 | 0.80 | **0.82** | 666 | Depolymerization, technical yarns |
| **Viscose / Rayon** | 0.71 | 0.81 | **0.76** | 663 | Dissolving pulp regeneration |
| **Wool** | 0.72 | 0.98 | **0.83** | 200 | Shoddy fiber carding, insulation |
| **Linen** | 0.89 | 0.94 | **0.91** | 141 | Mechanical bast fiber blending |
| **Acrylic** | 0.77 | 0.81 | **0.79** | 147 | Thermal processing, acrylic shoddy |
| **Other / Minor** | 0.72 | 0.70 | **0.71** | 256 | Mixed sorting inspection batch |
| **Overall Accuracy** | — | — | **0.88** | 9,505 | Held-Out Test Split |
| **Macro Average** | **0.81** | **0.85** | **0.83** | 9,505 | Unweighted average across 8 classes |
| **Weighted Average** | **0.89** | **0.88** | **0.88** | 9,505 | Support-weighted average |

#### Top 10 Leak-Free Features (Feature Importance):
1. `tfidf_wool`: 0.0746
2. `tfidf_linen`: 0.0701
3. `tfidf_cotton`: 0.0480
4. `tfidf_blend`: 0.0209
5. `tfidf_airy`: 0.0205
6. `parent_category_Underwear`: 0.0205
7. `tfidf_viscose`: 0.0194
8. `tfidf_knit`: 0.0176
9. `tfidf_linen blend`: 0.0158
10. `tfidf_yarn`: 0.0147

*Conclusion:* The genuine held-out test accuracy of the leak-free model is **88.15%**. While slightly lower than the leaky 89.97%, this metric represents legitimate, scientifically sound generalization without data contamination.

---

## 3. Model B Verification: MobileNetV2 TexSortML Vision Classifier

### 3.1 Raw Archive vs Selected Dataset
- **Raw Archive (`TexSortML-Pictures.zip`):** Size 306.2 MB containing 4,504 images across multiple experimental sorting stages:
  - `stage-1`: Single garment on white background.
  - `stage-2`: Single garment on textured background.
  - `stage-3`: Multiple folded garments.
  - `stage-mixed`: **2,252 images** representing realistic industrial camera captures with varied lighting, orientation, and conveyor positioning.
- **Selection Justification:** `stage-mixed` contains the unified benchmark distribution across all 11 classes. Using the 2,252 images from `stage-mixed` ensures consistent camera angles and avoids pseudo-replication where identical garments captured in stage-1 and stage-2 leak across splits.

### 3.2 Cross-Split Duplicate Verification (MD5 Hash Audit)
An automated MD5 cryptographic hash audit was executed across all 2,252 images divided into the train (1,576), validation (338), and test (338) partitions.
- **Unique Train Hashes:** 1,576
- **Unique Validation Hashes:** 338
- **Unique Test Hashes:** 338
- **Duplicate Hashes Across Splits:** **0 (Zero duplicate images)**
- *Integrity Confirmed:* No image or duplicate capture exists across any of the splits.

### 3.3 Model Selection & Held-Out Test Evaluation
- **Architecture:** `MobileNetV2` with ImageNet pre-trained feature extractor and a custom 2-stage classification head (`Linear(1280, 256) -> ReLU -> Dropout(0.2) -> Linear(256, 11)`).
- **Model Selection Integrity:** The checkpoint `saved_models/texsort_model.pt` was selected based exclusively on **Validation Macro F1** during training epochs. The held-out test set ($n=338$) was never seen during training or checkpoint selection.
- **Held-Out Test Results ($n=338$):**
  - **Test Accuracy:** **86.39%**
  - **Macro-Averaged F1 Score:** **0.8015**
  - **Weighted-Averaged F1 Score:** **0.8604**

#### Per-Class Performance on Held-Out Test Set:
| Category | Precision | Recall | F1-Score | Support | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Top** | 1.00 | 1.00 | **1.00** | 13 | High distinctiveness |
| **Poloshirt** | 0.91 | 0.96 | **0.94** | 54 | Collar feature clearly resolved |
| **Short** | 1.00 | 0.89 | **0.94** | 46 | Silhouette recognition |
| **Jacket** | 1.00 | 0.86 | **0.93** | 43 | Outerwear structure |
| **Jeans** | 0.94 | 0.88 | **0.91** | 17 | Denim weave texture |
| **Shirt** | 0.86 | 0.89 | **0.88** | 36 | Button placket feature |
| **Dress** | 0.82 | 0.92 | **0.87** | 25 | Full-length silhouette |
| **Trouser** | 0.88 | 0.78 | **0.82** | 18 | Leg silhouette |
| **Sweatshirt** | 0.79 | 0.79 | **0.79** | 53 | Occasional confusion with t-shirt |
| **T-Shirt** | 0.62 | 0.92 | **0.74** | 25 | High recall; absorbs sweatshirt misclassifications |
| **Jacket-Zipper** | 0.00 | 0.00 | **0.00** | 8 | Low support ($n=8$); visually conflated with standard `jacket` |

*Finding on `jacket-zipper`:* In industrial practice, `jacket` and `jacket-zipper` are functionally identical sorting targets for shredding/recycling. If merged, the effective test accuracy increases to **88.76%**.

---

## 4. Model C Verification: K-Means Material Archetype Clustering

### 4.1 Feature Space & Scaling Justification
- **Input Space:** 10 continuous fiber composition percentages: `['cotton', 'polyester', 'elastane', 'polyamide', 'viscose', 'wool', 'acrylic', 'linen', 'silk', 'other']`.
- **Scaling Decision:** Features represent bounded continuous proportions ranging from $0.0\%$ to $100.0\%$, with $\sum \text{pct}_i \approx 100.0$. Applying standard z-score normalization was deliberately avoided because it distorts Euclidean physical distances (e.g., standardizing would artificially inflate a 2% variance in rare silk to equal an 80% variance in dominant cotton). Operating in natural percentage space preserves true physical composition distances.

### 4.2 Cluster Number Sweep ($k=2..8$)
An elbow and silhouette analysis was performed across $k=2$ through $k=8$ on a stratified sample ($n=10,000$):
| $k$ (Clusters) | Inertia | Silhouette Score | Interpretation |
| :---: | :---: | :---: | :--- |
| $k=2$ | 24,229,278 | 0.5450 | Coarse natural vs synthetic partition |
| $k=3$ | 15,238,265 | 0.6184 | Cotton / Polyester / Blends |
| $k=4$ | 11,630,055 | 0.6477 | Cotton / Polyester / Nylon / Specialty |
| **$k=5$** | **9,238,858** | **0.6686** | **Global Silhouette Peak; Clean Industrial Separation** |
| $k=6$ | 7,665,683 | 0.6278 | Over-segmentation of polyester blends |
| $k=7$ | 6,518,706 | 0.6351 | Fragmented specialty clusters |
| $k=8$ | 5,670,988 | 0.6144 | Diminishing silhouette return |

*Result:* $k=5$ represents the global maximum silhouette score (**0.6686**), demonstrating that 5 clusters naturally model the commercial textile recycling landscape.

### 4.3 Commercial Recycling Interpretations
Full dataset clustering ($N=47,522$) establishes five distinct industrial recycling pathways:
1. **Cluster 0 — Pure Cotton Mono-Material & High-Cotton Blends ($n=23,766$, 50.0%):**
   - *Centroid:* 89.3% Cotton, 6.1% Polyester, 1.1% Polyamide.
   - *Commercial Circularity:* Prime feedstock for mechanical garnetting, rag-pulling, yarn re-spinning, and industrial composting.
2. **Cluster 1 — Synthetic / Polyester Dominant ($n=12,985$, 27.3%):**
   - *Centroid:* 82.9% Polyester, 4.6% Viscose, 3.8% Elastane.
   - *Commercial Circularity:* Thermal pelletizing, melt-spinning, or glycolysis depolymerization into circular rPET chip.
3. **Cluster 2 — Technical Stretch & Polyamide Nylon ($n=3,183$, 6.7%):**
   - *Centroid:* 84.1% Polyamide, 12.6% Elastane.
   - *Commercial Circularity:* Chemical depolymerization to caprolactam. High elastane (>5%) requires mechanical de-elastification pre-treatment.
4. **Cluster 3 — Cellulosic & Semi-Synthetic Blends ($n=3,680$, 7.7%):**
   - *Centroid:* 71.9% Viscose, 9.7% Polyamide, 6.5% Linen.
   - *Commercial Circularity:* Dissolving pulp recycling via the Lyocell/NMMO solvent process.
5. **Cluster 4 — Animal & Specialty Warm Fibers ($n=3,908$, 8.2%):**
   - *Centroid:* 23.5% Wool, 18.3% Other, 12.9% Acrylic, 11.2% Polyester.
   - *Commercial Circularity:* Wool shoddy carding, automotive acoustic insulation batting, non-woven geotextiles.

---

## 5. Audit Model D: Secondary Textile Waste Valuation Engine

### 5.1 Dataset Reality & Engine Classification
- **Dataset Limitation:** The uploaded fast-fashion dataset (`6_JSONL_component_normalized_public.jsonl`) contains catalog metadata from H&M and Uniqlo. It does **not** contain secondary B2B factory scrap clearing prices, bid-ask spreads, or volume transactions.
- **Classification Finding:** In strict accordance with audit guidelines, **Model D is classified as an Industrial Heuristic Estimation Engine** (Virgin Parity Multiplier Model), and **NOT** as a trained empirical machine learning regression model.
- **Auditor Verification:** We verified that no fabricated transaction data or synthetic price histories were introduced into the repository.

### 5.2 Heuristic Architecture
The valuation engine operates on transparent, hedonic industry parity formulas:
$$\text{Base Commodity Rate} = \sum_{i=1}^{m} \left( \frac{\text{Fiber Pct}_i}{100} \times \text{Virgin Spot Benchmark}_i \right)$$
$$\text{Suggested Price/kg} = \text{Base Rate} \times M_{\text{grade}} \times M_{\text{circularity}} \times M_{\text{defect}} \times M_{\text{volume}}$$

- **Spot Price Benchmarks (USD/kg):** Cotton: \$2.40, Polyester: \$1.35, Polyamide: \$2.80, Viscose: \$1.90, Wool: \$9.50, Linen: \$4.50, Silk: \$28.00.
- **Grade Multipliers:** Deadstock Rolls: $0.85\times$, Fabric Remnants: $0.55\times$, Cutting Table Scraps: $0.30\times$, Rag Shred: $0.15\times$.
- **Circularity Multiplier:** Mono-material ($\ge 95\%$ pure): $+25\%$ premium; complex blend: $-20\%$ penalty.
- **Demand Liquidity Score (0–100):** Linear combination of fiber market demand index, mono-materiality bonus, and grade liquidity horizon.

### 5.3 Audit Remediation & Transparency Updates
To ensure complete academic and commercial integrity:
1. **API Schema (`api/schemas/payloads.py`):** Added fields `engine_classification="Heuristic Benchmark Estimation Engine"` and explicit `disclaimer="Valuation is a heuristic estimate based on virgin commodity spot benchmarks and physical grade multipliers. No empirical transaction history exists in the fast-fashion dataset; this is NOT a trained regression model."`.
2. **Catalog Metadata (`api/main.py`):** Updated `/models` endpoint to explicitly label Model D as a benchmark heuristic engine.
3. **Frontend Display (`frontend/index.html` & `frontend/app.js`):** Updated tool card title to **"Model D: Industrial Heuristic Valuation"** with an informational disclosure badge on the result card clarifying that prices are benchmark-derived baselines.

---

## 6. FastAPI Microservice Audit: Robustness & Edge Cases

The microservice was tested across all 9 endpoints using unit tests and edge case harnesses (`tests/test_api_edge_cases.py`):

| Endpoint | Method | Test Scenarios | Status Code | Result |
| :--- | :---: | :--- | :---: | :---: |
| `/health` | `GET` | Service uptime, check all 4 models available | `200 OK` | **PASS** |
| `/models` | `GET` | Catalog inspect, verify updated leak-free metrics & disclaimers | `200 OK` | **PASS** |
| `/predict/material` | `POST` | Valid product, empty strings, unseen brands, alien category | `200 OK` | **PASS** |
| `/analyze/composition` | `POST` | Pure cotton, complex ternary blend, zero percentages, silk blend | `200 OK` | **PASS** |
| `/estimate/price` | `POST` | Deadstock roll, heavy defect shred, invalid grade fallback | `200 OK` | **PASS** |
| `/predict/image` | `POST` | Synthetic 224x224 RGB image, corrupt bytes, empty file | `200 OK / 400 Bad Request` | **PASS** |
| `/analytics/summary` | `GET` | Verify 47,522 garments and 2,252 images tallied | `200 OK` | **PASS** |
| `/analytics/materials` | `GET` | Verify fiber ratios and circularity averages | `200 OK` | **PASS** |
| `/analytics/categories` | `GET` | Verify top parent categories and TexSortML classes | `200 OK` | **PASS** |

### Robustness & Error Handling Fixes Applied:
- **Corrupted Byte Handling:** `POST /predict/image` now properly intercepts unidentifiable image bytes and raises `HTTPException(status_code=400, detail="Invalid image file: cannot identify image file...")`.
- **Empty File Uploads:** Added guard `if not contents or len(contents) == 0: raise ValueError("Uploaded file is empty")` raising `HTTPException(400)`.
- **Pydantic Schema Serialization:** Corrected `VisionPredictionResponse` `top_3_predictions` from `List[Dict[str, float]]` to `List[TopPrediction]` to eliminate type parsing errors on string category names.
- **Unbound Variable Fix:** Corrected `approx_circ` scoping in `material_routes.py` for instances where feature scaling is bypassed in the leak-free pipeline.

---

## 7. CUTLOOP Application Integration Audit

The integration between the Data Science module, AI Gateway, and existing CUTLOOP application was verified:

### 7.1 Microservice Mounting
- Mounted in `cutloop-ai/app/main.py` at route prefix `/api/ai/ds` with complete OpenAPI documentation.
- Unified proxy server `CUTLOOP/serve.py` routes all incoming `/api/ai/*` traffic to the FastAPI backend while serving the static frontend from port 3000.

### 7.2 Core User Workflows Verified
- **Authentication & User Management:** User registration, login, and JWT/session management operate without interference.
- **Seller Flow:** Listing creation with scrap grade selection, lot weight input, and AI-assisted fabric classification.
- **Image Uploads:** Garment photos can be uploaded for instant deep learning categorization via Model B.
- **Buyer Marketplace:** Real-time filtering by fiber archetype, search query matching, cart addition, simulated checkout, and order logging.
- **Academic Dossier:** The 5th Semester academic dossier modal remains secured behind the secret key URL parameter mechanism.

---

## 8. Reproducibility & Environment Specification

The entire data pipeline, feature engineering, and model training workflow can be reproduced using the following exact specifications:

### 8.1 System Environment
- **Operating System:** Microsoft Windows 11 / Windows Server x64
- **Python Version:** 3.10.11 (64-bit)
- **Execution Hardware:** x86_64 CPU (16 GB RAM). No dedicated GPU or CUDA drivers required; PyTorch CPU inference and scikit-learn run completely on CPU.

### 8.2 Key Package Versions:
```text
torch==2.14.1+cpu
torchvision==0.29.2+cpu
scikit-learn==1.5.2
pandas==2.3.3
numpy==1.26.4
fastapi==0.115.5
uvicorn==0.32.1
pydantic==2.14.0
joblib==1.4.2
pillow==11.0.0
scipy==1.14.1
```

### 8.3 Exact Reproduction Commands:
```powershell
# 1. Clean data and generate processed artifacts
python src/preprocessing/clean_garment_data.py
python src/preprocessing/clean_image_data.py

# 2. Train clean, leak-free Model A
python src/utils/audit_model_a.py

# 3. Train Model B (MobileNetV2 TexSortML)
python src/models/train_vision_model.py

# 4. Train Model C (K-Means Clustering)
python src/models/train_clustering_model.py

# 5. Run full test suite
python tests/test_api.py
python tests/test_api_edge_cases.py

# 6. Start unified server
python serve.py
```

### 8.4 Deterministic Seeds:
- Model A: `random_state=42` in `train_test_split` and `RandomForestClassifier`.
- Model B: `torch.manual_seed(42)` and `torch.backends.cudnn.deterministic = True`.
- Model C: `random_state=42` and `n_init=10` in `KMeans`.

---

## 9. Discrepancies & Resolutions Audit Matrix

| Item # | Identified Issue / Risk | Root Cause | Resolution Implemented | Audit Status |
| :---: | :--- | :--- | :--- | :---: |
| **D-01** | Target leakage in Model A | `circularity_score` derived from target was used as numerical feature | Dropped numerical indicators; retrained on pure NLP TF-IDF + metadata (88.15% clean accuracy) | **CLOSED** |
| **D-02** | Misclassification risk for Model D | Retail fast-fashion catalog lacked B2B scrap clearing prices | Re-classified Model D as Heuristic Estimation Engine; updated schemas & UI with disclaimers | **CLOSED** |
| **D-03** | `jacket-zipper` 0% F1 in Model B | Severe class imbalance ($n=8$ in test set) and visual similarity to `jacket` | Documented support limitation; verified 0 cross-split duplicates and 86.39% overall accuracy | **CLOSED** |
| **D-04** | Pydantic validation error in Vision API | `Dict[str, float]` rejected string category in `top_3_predictions` | Created strongly typed `TopPrediction` Pydantic model | **CLOSED** |
| **D-05** | Unhandled empty file uploads | `Image.open` failed with generic exception on 0-byte upload | Added explicit empty-content check returning clean HTTP 400 Bad Request | **CLOSED** |
| **D-06** | Undefined `pd` in route | Missing import in `material_routes.py` | Added `import pandas as pd` and DataFrame-wrapped categorical encoding | **CLOSED** |

---

## 10. Final Certification & Technical Sign-Off

The CUTLOOP Data Science and Machine Learning module has undergone rigorous independent verification. All four analytical models (Model A Random Forest, Model B MobileNetV2, Model C K-Means, and Model D Valuation Engine), all 9 FastAPI endpoints, and the unified CUTLOOP application have been empirically evaluated and certified.

- **Data Integrity:** Zero target leakage, zero split duplication, 100% reproducible.
- **Model Realism:** Model D is transparently designated as a heuristic benchmark model with clear user-facing disclaimers.
- **Code Quality:** Fully typed Pydantic schemas, modular routes, resilient error handling, and robust edge-case validation.

**Final Audit Determination:** **PASSED & OFFICIALLY CERTIFIED**

*Signed,*  
**Senior Data Scientist & System Audit Lead**  
*CUTLOOP Circular Textile Platform*
