# CUTLOOP Data Science & Machine Learning Architecture

## 1. Overview
The **CUTLOOP Data Science Module** provides circular textile intelligence, garment category classification, material archetype clustering, and secondary market valuation models for the CUTLOOP B2B waste-to-value marketplace.

It is developed against two empirical datasets:
1. **Fast-Fashion Sourced Inventory Dataset** (`6_JSONL_component_normalized_public.jsonl`): 47,522 garment variant records from H&M and Uniqlo across the UK and Australia with detailed multi-component fiber compositions.
2. **TexSortML Garment Vision Benchmark** (`TexSortML-Pictures.zip`): 2,252 images ($730 \times 730$ RGB) across 11 garment macro categories (`poloshirt`, `sweatshirt`, `short`, `jacket`, `shirt`, `tshirt`, `dress`, `trouser`, `jeans`, `top`, `jacket-zipper`).

---

## 2. Machine Learning Models: Capabilities & Technical Boundaries

### Model A: Dominant Fiber & Material Classifier (Supervised NLP + Tabular)
- **Primary Function:** Predicts the dominant textile fiber category (`cotton`, `polyester`, `polyamide`, `viscose`, `wool`, `linen`, `acrylic`, `other`) from listing product title, marketing description, and catalog metadata.
- **Source Features (413 Total Features):**
  - **Text Features (400 dimensions):** TF-IDF Vectorizer (unigrams + bigrams, sublinear TF scaling, English stopword removal) fitted strictly on `product_name` + `raw_description_text`.
  - **Catalog Metadata (13 dimensions):** One-Hot Encoded `brand` (H&M, Uniqlo), `region` (UK, AU), `gender_section` (Men, Ladies, Divided, Baby/Kids), and high-level `parent_category` (Tops, Bottoms, Underwear, etc.).
- **Material Extraction vs. Material Inference:**
  - *Material Extraction:* When product titles or marketing descriptions explicitly mention fiber tokens (e.g., "soft cotton jersey", "merino wool-blend", "linen trousers"), the model acts as an automated keyword/entity extraction and disambiguation classifier, driven by high TF-IDF weights (`tfidf_cotton`, `tfidf_linen`, `tfidf_wool`).
  - *Material Inference:* When explicit fiber tokens are absent, the model infers the most probable fiber based on contextual garment categories and brand tendencies (e.g., denim $\rightarrow$ cotton, activewear tights $\rightarrow$ polyamide/polyester).
  - *Critical Boundary:* Model A is an **NLP text categorization model**, NOT a spectroscopic or physical fiber sensor. It cannot verify actual fabric composition from physical textiles without descriptive metadata.
- **Verified Clean Performance (Held-Out Test Set, $N=9,505$, Zero Target Leakage):**
  - **Accuracy:** **88.15%**
  * **Macro F1:** **0.8257** | **Weighted F1:** **0.8837**
  - **Per-Class F1:** Cotton: 0.95, Linen: 0.91, Polyester: 0.84, Wool: 0.83, Polyamide: 0.82, Acrylic: 0.79, Viscose: 0.76, Other: 0.71.

---

### Model B: TexSortML Garment Vision Classifier (Deep Learning CNN)
- **Primary Function:** Classifies macro apparel silhouettes / garment categories from 2D RGB photographs.
- **Algorithm & Architecture:** MobileNetV2 with inverted residual bottlenecks and pre-trained ImageNet feature extractor, fine-tuned with a custom classification head (`Linear(1280, 256) -> ReLU -> Dropout(0.2) -> Linear(256, 11)`).
- **The 11 Target Classes (Garment Types ONLY):**
  1. `dress`
  2. `jacket`
  3. `jacket-zipper`
  4. `jeans`
  5. `poloshirt`
  6. `shirt`
  7. `short`
  8. `sweatshirt`
  9. `top`
  10. `trouser`
  11. `tshirt`
- **Explicit Boundary (Garment Category vs. Fiber Identification):**
  - Model B classifies **garment types only** (apparel silhouette).
  - **DO NOT describe Model B as fiber identification or fabric blend analysis.** Standard RGB photography at $224 \times 224$ resolution cannot resolve yarn twist, polymer chemistry, or fiber blends (e.g., it cannot distinguish a 100% cotton t-shirt from a 100% polyester t-shirt).
- **Verified Performance (Held-Out Test Set, $N=338$, Zero Cross-Split Duplicates):**
  - **Classification Accuracy:** **86.39%**
  - **Macro F1:** **0.8015** | **Weighted F1:** **0.8604**
  - **Top Classes:** `top` (1.00 F1), `short` (0.94 F1), `poloshirt` (0.94 F1), `jacket` (0.93 F1), `jeans` (0.91 F1), `shirt` (0.88 F1), `dress` (0.87 F1), `trouser` (0.82 F1), `sweatshirt` (0.79 F1), `tshirt` (0.74 F1).
  - *Class Imbalance Note:* `jacket-zipper` ($n=8$ in test split) has 0.00 F1 due to severe visual overlap with standard `jacket`. Merging them yields 88.76% test accuracy.

---

### Model C: Material Composition Archetype Clusterer (Unsupervised K-Means)
- **Primary Function:** Partitions continuous multi-component fiber percentage vectors into 5 commercial circularity archetypes.
- **Input Feature Space:** Continuous 10D fiber space: `['cotton', 'polyester', 'elastane', 'polyamide', 'viscose', 'wool', 'acrylic', 'linen', 'silk', 'other']`. Proportions range from $0.0\%$ to $100.0\%$ and sum to $\approx 100\%$. Unscaled natural percentage space is used to preserve true physical Euclidean distances.
- **Missing Data Handling:** Non-present fibers are imputed with $0.0\%$. Records without structured component breakdowns are flagged and excluded or assigned from normalized text.
- **Cluster Number Justification:** Silhouette sweep across $k=2..8$ confirmed $k=5$ as the **global maximum silhouette peak (0.6686)**.
- **The 5 Discovered Archetype Profiles ($N=47,522$):**
  1. **Cluster 0 — Pure Cotton Mono-Material & High-Cotton Blends ($n=23,766$, 50.0%):**
     - *Centroid:* 89.3% Cotton, 6.1% Polyester, 1.1% Polyamide.
     - *Theoretical Pathway:* Mechanical shredding, rag garnetting, yarn re-spinning, and industrial composting.
  2. **Cluster 1 — Synthetic / Polyester Dominant ($n=12,985$, 27.3%):**
     - *Centroid:* 82.9% Polyester, 4.6% Viscose, 3.8% Elastane.
     - *Theoretical Pathway:* Thermal granulating, extrusion pelletizing, and chemical glycolysis to rPET chip.
  3. **Cluster 2 — Technical Stretch & Polyamide Nylon ($n=3,183$, 6.7%):**
     - *Centroid:* 84.1% Polyamide, 12.6% Elastane.
     - *Theoretical Pathway:* Chemical depolymerization to caprolactam; requires elastomeric separation.
  4. **Cluster 3 — Cellulosic & Semi-Synthetic Blends ($n=3,680$, 7.7%):**
     - *Centroid:* 71.9% Viscose, 9.7% Polyamide, 6.5% Linen.
     - *Theoretical Pathway:* Dissolving pulp regeneration via Lyocell/NMMO solvent spinning.
  5. **Cluster 4 — Animal & Specialty Warm Blends ($n=3,908$, 8.2%):**
     - *Centroid:* 23.5% Wool, 18.3% Other, 12.9% Acrylic, 11.2% Polyester.
     - *Theoretical Pathway:* Shoddy wool carding, acoustic insulation batting, non-woven geotextiles.
- **Critical Limitation & Labeling:**
  - Cluster assignments reflect mathematical proximity in 10D percentage space, not chemical solubility or fiber staple length.
  - **All suggested recycling pathways are PRELIMINARY THEORETICAL RECOMMENDATIONS**, NOT lab-certified or commercially guaranteed industrial processing outcomes.

---

### Model D: Secondary Textile Waste Valuation Engine (Heuristic Benchmark Model)
- **Primary Function:** Computes indicative baseline pricing (\$USD/kg), total lot valuation, liquidity score (0-100), and expected days to clear for factory surplus fabric and scrap.
- **Dataset Limitation:** The uploaded fast-fashion dataset lacks B2B transaction spot prices, buyer bids, and clearing history. **No actual transaction dataset exists.**
- **Model Classification:** Strictly classified as an **Industrial Heuristic Estimation Engine** (Virgin Parity Multiplier Model), NOT a trained machine learning regression model.
- **Valuation Formula:**
  $$\text{Base Commodity Rate} = \sum_{i=1}^{m} \left( \frac{\text{Fiber Pct}_i}{100} \times \text{Virgin Spot Benchmark}_i \right)$$
  $$\text{Suggested Price/kg} = \text{Base Rate} \times M_{\text{grade}} \times M_{\text{circularity}} \times M_{\text{defect}} \times M_{\text{volume}}$$
  - *Virgin Spot Benchmarks (USD/kg):* Cotton: \$2.40, Polyester: \$1.35, Polyamide: \$2.80, Viscose: \$1.90, Wool: \$9.50, Linen: \$4.50, Silk: \$28.00.
  - *Quality Grade Multipliers:* Deadstock Rolls ($0.85\times$), Fabric Remnants ($0.55\times$), Cutting Table Scraps ($0.30\times$), Rag Shred ($0.15\times$).
  - *Circularity Multiplier:* Mono-material ($\ge 95\%$ pure): $+25\%$ premium; complex blend: $-20\%$ penalty.
- **Transparent Disclaimers:** All API responses and frontend views explicitly state that outputs are heuristic benchmark estimates and not guaranteed market clearing prices.

---

## 3. Comprehensive Model Capability Matrix

| Feature / Dimension | Model A (Dominant Fiber) | Model B (TexSortML Vision) | Model C (K-Means Archetypes) | Model D (Valuation Engine) |
| :--- | :--- | :--- | :--- | :--- |
| **Model Type** | Supervised NLP Random Forest | Deep Learning CNN (MobileNetV2) | Unsupervised K-Means ($k=5$) | Heuristic Valuation Engine |
| **Input Data** | Product title, description text, catalog metadata | 2D RGB Image ($224 \times 224 \times 3$) | Continuous 10D fiber composition percentages | Fiber percentages, grade, lot weight, defect severity |
| **Primary Output** | Dominant fiber category (8 classes) | Garment macro category (11 classes) | Cluster archetype ID (0-4) + Centroid stats | Indicative price (\$/kg), lot value, liquidity score (0-100) |
| **Benchmark Metric** | 88.15% Held-Out Accuracy ($n=9,505$) | 86.39% Held-Out Accuracy ($n=338$) | Peak Silhouette Score: 0.6686 | Virgin benchmark spot price parity |
| **What It CAN Do** | • Extract fiber mentions from text<br>• Disambiguate fiber blends in catalog copy<br>• Infer dominant fiber from category context | • Identify garment apparel type<br>• Sort apparel silhouettes (jacket, jeans, shirt)<br>• Operate on low-latency CPU (~35 ms) | • Group blends into 5 recycling archetypes<br>• Quantify Euclidean composition proximity<br>• Suggest preliminary recycling streams | • Compute indicative price baseline (\$/kg)<br>• Apply grade and mono-material discounts<br>• Estimate heuristic demand liquidity horizon |
| **What It CANNOT Do** | • Cannot analyze physical fabric swatches<br>• Cannot detect unmentioned synthetic coatings<br>• Low accuracy on blank/uninformative text | • **CANNOT identify fiber type (cotton, poly)**<br>• Cannot detect fabric blends<br>• Struggles with `jacket-zipper` vs `jacket` | • Cannot assess dye chemistry or finishes<br>• Cannot evaluate fiber staple length<br>• Does NOT guarantee industrial recycling yield | • **NOT an empirical regression model**<br>• Cannot reflect real-time marketplace bids<br>• Does not have transaction history backing |
| **Reliability Boundary** | High when descriptive text is present; falls back to category priors on sparse text | High on macro silhouette sorting; zero capability on textile composition | High mathematical stability ($k=5$ peak); recommendations are theoretical only | Heuristic guideline only; requires commercial buyer negotiation |

---

## 4. API Endpoints Reference

All endpoints are hosted at `http://localhost:8001` (standalone) or proxied through `http://localhost:3000/api/ai/ds/*`.

| Method | Endpoint | Function & Boundary |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health, uptime, and loaded model availability. |
| `GET` | `/models` | Model specifications, audited accuracies, capabilities, and disclaimers. |
| `POST` | `/predict/material` | Model A: NLP text-based fiber extraction and category classification. |
| `POST` | `/analyze/composition`| Model C: Archetype clustering and preliminary theoretical recycling stream. |
| `POST` | `/estimate/price` | Model D: Heuristic benchmark valuation, liquidity score, and days-to-clear. |
| `POST` | `/predict/image` | Model B: TexSortML macro garment category vision classification. |
| `GET` | `/analytics/summary` | Dataset overview (47,522 garments, 2,252 images, circularity averages). |
| `GET` | `/analytics/materials` | Sourced inventory fiber distributions and mono-material ratios. |
| `GET` | `/analytics/categories`| Garment inventory categories and TexSortML vision classes. |

---

## 5. Verification & Test Suite Execution

To verify all model capabilities, run the automated test suites:
```powershell
# 1. Run baseline unit tests
python tests/test_api.py

# 2. Run edge case, invalid input, and corrupted byte tests
python tests/test_api_edge_cases.py

# 3. Verify Model B and Model C metrics
python src/utils/audit_verification.py
```
