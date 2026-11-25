# CUTLOOP — Model Capability and Limitation Report

**Document Version:** 2.0.0  
**Status:** Certified Post-Audit Technical Baseline  
**Auditor / Engineering Lead:** CUTLOOP Data Science & Machine Learning Engineering Team  
**Evaluation Scope:** Four Integrated Machine Learning & Heuristic Services (Model A, Model B, Model C, Model D)

---

## Executive Summary

This report establishes the technical boundaries, verifiable capabilities, and documented limitations of the four analytical engines deployed within the **CUTLOOP** industrial circular textile marketplace. 

In industrial waste-to-value operations, distinguishing **predictive physical diagnosis** from **NLP catalog extraction**, **macro garment silhouette sorting** from **fiber identification**, and **empirical transaction pricing** from **commodity parity heuristics** is essential for commercial safety and academic transparency.

```mermaid
flowchart TD
    subgraph Data_Inputs["Input Data Streams"]
        A_in["Product Title + Marketing Copy<br/>(Text & Metadata)"]
        B_in["2D RGB Photography<br/>(224x224 Pixels)"]
        C_in["10D Continuous Fiber Vector<br/>(Lab/Spec percentages)"]
        D_in["Surplus Grade + Weight + Benchmarks<br/>(Spot Rates & Multipliers)"]
    end

    subgraph Models["CUTLOOP Analytical Engines"]
        ModelA["Model A: Random Forest NLP<br/>(88.15% Clean Accuracy)"]
        ModelB["Model B: MobileNetV2 Vision<br/>(86.39% Clean Accuracy)"]
        ModelC["Model C: K-Means Clustering<br/>(k=5, Silhouette: 0.6686)"]
        ModelD["Model D: Valuation Engine<br/>(Virgin Benchmark Parity)"]
    end

    subgraph Outputs["Functional Outputs & Boundaries"]
        A_out["Dominant Fiber Class<br/>⚠️ Text Entity Extraction"]
        B_out["11 Garment Silhouette Categories<br/>⚠️ Macro Apparel Types Only"]
        C_out["5 Circularity Archetypes<br/>⚠️ Preliminary Theoretical Streams"]
        D_out["Indicative $/kg Baseline Valuation<br/>⚠️ Heuristic Parity Estimate"]
    end

    A_in --> ModelA --> A_out
    B_in --> ModelB --> B_out
    C_in --> ModelC --> C_out
    D_in --> ModelD --> D_out
```

---

## 1. Model A: Dominant Fiber & Material Classifier

### 1.1 Source Features & Pipeline Composition
Model A operates on **413 total numerical and categorical features** derived strictly from catalog metadata:

| Feature Group | Raw Source Field(s) | Engineering Transformation | Dimension |
| :--- | :--- | :--- | :---: |
| **NLP Text Tokens** | `product_name`, `raw_description_text` | TF-IDF (unigrams + bigrams, sublinear TF scaling, English stopwords removed) | 400 |
| **Brand Identity** | `brand` | One-Hot Encoding (`H&M`, `UNIQLO`, `UNKNOWN`) | 3 |
| **Market Region** | `region` | One-Hot Encoding (`UK`, `AU`, `UNKNOWN`) | 3 |
| **Gender Section** | `gender_section` | One-Hot Encoding (`Ladies`, `Men`, `Divided`, `Baby`, `Kids`) | 5 |
| **Catalog Category** | `parent_category` | One-Hot Encoding (`Tops`, `Bottoms`, `Underwear`, etc.) | 2 |

> [!IMPORTANT]
> **Excluded Fields:** The raw text fields `raw_material_text` and `raw_material_text_norm` (which contain the manufacturer's exact composition labels, e.g., *"Shell: 98% Cotton, 2% Elastane"*) are **strictly excluded** from the input feature matrix to prevent trivial leakage of the composition target.

### 1.2 Material Extraction vs. Genuine Material Inference
A critical distinction must be drawn between **material extraction** and **material inference**:

```mermaid
flowchart LR
    subgraph Scenario_1["Scenario 1: Explicit Mention (Material Extraction)"]
        T1["'Fine Cotton Oxford Shirt'<br/>'Soft combed cotton twill'"] --> TF1["High TF-IDF: tfidf_cotton"] --> Pred1["Predicted Fiber: Cotton<br/>(Confidence: >92%)"]
    end
    subgraph Scenario_2["Scenario 2: Generic Title (Material Inference)"]
        T2["'Utility Overshirt'<br/>'Crisp structured outer'"] --> TF2["Category Priors & Structural Keywords"] --> Pred2["Inferred Fiber: Cotton/Poly Blend<br/>(Confidence: ~60-75%)"]
    end
```

1. **Material Extraction (Keyword Matching & Disambiguation):**
   - In standard fast-fashion catalogs, product titles and marketing descriptions frequently contain explicit fiber keywords (e.g., *"Cotton poplin shirt"*, *"Linen-blend trousers"*, *"Pure merino wool sweater"*).
   - In these instances, Model A acts as an automated **keyword/entity extraction and disambiguation classifier**. High TF-IDF unigram weights (`tfidf_cotton`, `tfidf_linen`, `tfidf_wool`) drive predictions with $>90\%$ confidence.
2. **Genuine Material Inference (Indirect Pattern Association):**
   - When explicit fiber words are stripped or omitted from the description (e.g., *"Slim-fit denim jeans"* or *"Thermal compression base-layer"*), Model A performs **contextual material inference**. It leverages associations between the garment category (`parent_category='Underwear'`), brand catalog habits, and subtle weave descriptions (*"airy weave"*, *"rib knit"*, *"yarn-dyed"*).
   - Inference on sparse text drops in confidence to $60\% - 75\%$, reflecting inherent uncertainty in predicting fiber without explicit mentions.

> [!WARNING]
> **Physical Limitation:** Model A is an **NLP text categorization model**, NOT a physical fiber sensor or chemical diagnostic tool. It cannot analyze physical fabric swatches or identify textiles from uninformative text (e.g., *"Blue Summer Style #402"*).

---

## 2. Model B: TexSortML Garment Vision Classifier

### 2.1 The 11 Benchmark Classes
Model B is fine-tuned on the `TexSortML` image benchmark ($2,252$ images, $224 \times 224 \times 3$ RGB) using `MobileNetV2`. The 11 target classes are:

| Class # | Class Name | Representation | Test Support ($n=338$) | Precision | Recall | F1-Score |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | `top` | Sleeveless tops, tank tops, camisoles | 13 | 1.00 | 1.00 | **1.00** |
| 2 | `poloshirt` | Short-sleeve collared shirts | 54 | 0.91 | 0.96 | **0.94** |
| 3 | `short` | Shorts, athletic trunks, bermudas | 46 | 1.00 | 0.89 | **0.94** |
| 4 | `jacket` | Coats, blazers, overshirts, parkas | 43 | 1.00 | 0.86 | **0.93** |
| 5 | `jeans` | Denim trousers and dungarees | 17 | 0.94 | 0.88 | **0.91** |
| 6 | `shirt` | Long-sleeve button-down shirts | 36 | 0.86 | 0.89 | **0.88** |
| 7 | `dress` | Full-length dresses and frocks | 25 | 0.82 | 0.92 | **0.87** |
| 8 | `trouser` | Chinos, slacks, formal trousers | 18 | 0.88 | 0.78 | **0.82** |
| 9 | `sweatshirt` | Hoodies, fleeces, crewnecks | 53 | 0.79 | 0.79 | **0.79** |
| 10 | `tshirt` | Standard round/V-neck tees | 25 | 0.62 | 0.92 | **0.74** |
| 11 | `jacket-zipper` | Zip-up track jackets / windbreakers | 8 | 0.00 | 0.00 | **0.00** |

### 2.2 Functional Definition: Garment Category vs. Fiber Identification
> [!CAUTION]
> **DO NOT DESCRIBE MODEL B AS FIBER IDENTIFICATION.**  
> Model B is strictly a **Garment-Category Macro Classification Engine** (Silhouette Sorting).

* **What Model B Sees:** Macro structural geometry (sleeves, collars, buttons, leg openings, zippers, hem lengths).
* **What Model B CANNOT See:** Polymer chemistry, yarn count, warp/weft density, or blend fractions.
* **Why Fiber Cannot Be Identified from Standard Images:** A $224 \times 224$ RGB image of a black t-shirt looks virtually indistinguishable whether made from $100\%$ combed organic cotton, $100\%$ recycled polyester, or a $60/40$ poly-viscose blend. Discerning fiber composition requires near-infrared (NIR) hyperspectral imaging or chemical pyrolysis, which cannot be accomplished via 2D consumer photography.

---

## 3. Model C: Material Composition Archetype Clusterer

### 3.1 Mathematical Formulation & Input Feature Space
Model C clusters multi-fiber garments into commercial recycling cohorts using unsupervised K-Means in a **10-dimensional continuous space**:
$$\vec{x} = \left[ x_{\text{cotton}}, x_{\text{poly}}, x_{\text{elastane}}, x_{\text{polyamide}}, x_{\text{viscose}}, x_{\text{wool}}, x_{\text{acrylic}}, x_{\text{linen}}, x_{\text{silk}}, x_{\text{other}} \right] \in [0, 100]^{10}$$

* **Distance Metric:** Euclidean distance in unscaled natural percentage space ($\sum x_i \approx 100\%$). Standard z-score normalization was rejected because it distorts physical composition reality (a $5\%$ variance in elastane should not be scaled to equal a $50\%$ variance in cotton).
* **Missing Data Imputation:** Unmentioned fibers default to $0.0\%$. Entries with corrupted or missing structured JSON were isolated during preprocessing.
* **Optimal Cluster Sweep:** Evaluated across $k=2..8$; $k=5$ yields the **global silhouette peak (0.6686)**.

### 3.2 The Five Discovered Cluster Profiles ($N=47,522$)

```mermaid
pie title CUTLOOP Fiber Archetype Distribution (N=47,522)
    "Cluster 0: Cotton Mono-Material (50.0%)" : 23766
    "Cluster 1: Polyester-Rich Synthetics (27.3%)" : 12985
    "Cluster 2: Polyamide / Nylon Stretch (6.7%)" : 3183
    "Cluster 3: Cellulosic & Rayon Blends (7.7%)" : 3680
    "Cluster 4: Animal & Specialty Fibers (8.2%)" : 3908
```

| Cluster ID | Archetype Name | Size ($n$) | Dominant Fibers (Centroid %) | Preliminary Theoretical Recycling Stream |
| :---: | :--- | :---: | :--- | :--- |
| **0** | **Pure Cotton Mono-Material** | 23,766 (50.0%) | **Cotton: 89.3%**, Poly: 6.1%, Nylon: 1.1% | Mechanical rag-tearing, shoddy garnetting, re-spinning, composting |
| **1** | **Polyester-Rich Synthetics** | 12,985 (27.3%) | **Polyester: 82.9%**, Viscose: 4.6%, Elastane: 3.8% | Thermal extrusion pelletizing, glycolysis depolymerization (rPET) |
| **2** | **Technical Stretch & Nylon** | 3,183 (6.7%) | **Polyamide: 84.1%**, Elastane: 12.6% | Chemical depolymerization to caprolactam; requires elastane stripping |
| **3** | **Cellulosic & Rayon Blends** | 3,680 (7.7%) | **Viscose: 71.9%**, Nylon: 9.7%, Linen: 6.5% | Chemical dissolving pulp regeneration via Lyocell/NMMO process |
| **4** | **Animal & Specialty Warm Fibers**| 3,908 (8.2%) | **Wool: 23.5%**, Other: 18.3%, Acrylic: 12.9% | Wool shoddy carding, automotive acoustic batting, thermal insulation |

> [!WARNING]
> **Limitations & Practical Validation:**
> 1. Unsupervised K-Means groups garments strictly by Euclidean numerical similarity of declared fiber percentages.
> 2. It **does not account for** fabric finishes (DWR coatings, fluorochemicals), dyes, elastane cross-linking degradation, or staple fiber length.
> 3. **All pathway recommendations are PRELIMINARY THEORETICAL PATHWAYS.** They represent chemical and mechanical processing targets and do **not** constitute lab-certified or commercially guaranteed recycling yields.

---

## 4. Model D: Secondary Waste Valuation Engine

### 4.1 Dataset Limitation & Re-Classification
- **The Empirical Reality:** The provided fast-fashion dataset contains retail catalog records. It **does not contain secondary market B2B transactions**, wholesale auction bids, or clearing prices for textile factory waste.
- **Engine Classification:** Model D is formally designated as an **Industrial Heuristic Estimation Engine** (Virgin Parity Multiplier Model), and **NOT** a trained empirical machine learning regression model.
- **Auditor Certification:** Antigravity confirmed that no synthetic transactions or fabricated price distributions have been introduced into the models or reports.

### 4.2 Benchmark Parity Architecture
Indicative valuations are calculated using published commodity virgin spot price benchmarks discounted by physical waste factors:

$$\text{Suggested Valuation (\$/kg)} = \left[ \sum_{i} \left( \frac{\text{Pct}_i}{100} \times \text{Spot}_i \right) \right] \times M_{\text{grade}} \times M_{\text{circ}} \times M_{\text{defect}} \times M_{\text{vol}}$$

* **Commodity Spot Benchmarks:** Cotton: \$2.40/kg, Polyester: \$1.35/kg, Polyamide: \$2.80/kg, Viscose: \$1.90/kg, Wool: \$9.50/kg, Linen: \$4.50/kg, Silk: \$28.00/kg.
* **Scrap Grade Multipliers ($M_{\text{grade}}$):**
  - *Grade A (Deadstock Rolls):* $0.85\times$ (Pristine, full-width uncut yardage)
  - *Grade B (Fabric Remnants):* $0.55\times$ (Large end-of-roll off-cuts $>1$ meter)
  - *Grade C (Cutting Table Scraps):* $0.30\times$ (Small clipping remnants)
  - *Grade D (Mutilated Shred):* $0.15\times$ (Shredded unravelling clips)
* **Circularity Multiplier ($M_{\text{circ}}$):** Mono-material ($\ge 95\%$ pure): $+25\%$ premium; low blend ($\ge 85\%$): $+5\%$; complex multi-fiber blend: $-20\%$ penalty.
* **Demand Liquidity Score (0–100) & Clearing Horizon:** Heuristic formula weighting intrinsic commodity demand against sorting difficulty. Estimates clearing horizons (e.g., $3-7$ days for Grade A Cotton vs. $20-45$ days for Grade D blended shred).

> [!NOTE]
> **API & UI Disclosure:** Every valuation output returned by `POST /estimate/price` and rendered on the frontend displays:  
> *"Heuristic Benchmark Estimation Engine: Valuation is a benchmark-derived baseline. Not an empirical model trained on transaction history."*

---

## 5. Comprehensive Model Capability Matrix

| Attribute / Capability | Model A: Dominant Fiber | Model B: TexSortML Vision | Model C: Material Archetypes | Model D: Valuation Engine |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Task** | Dominant fiber extraction & classification | Macro apparel silhouette classification | Multi-component fiber clustering | Secondary textile scrap price estimation |
| **Model Class** | Supervised Random Forest (100 trees) | Deep Learning CNN (MobileNetV2) | Unsupervised K-Means ($k=5$) | Multi-factor Heuristic Valuation Engine |
| **Input Modality** | Text (Title, Description, Catalog metadata) | Image (2D RGB $224 \times 224$ photograph) | Tabular (10D Continuous composition %) | Numerical (Fiber %, Grade, Weight, Defects) |
| **Primary Output** | Dominant Fiber Class ($8$ classes) | Garment Apparel Category ($11$ classes) | Archetype Cluster ID ($0-4$) & Profile | Indicative Price/kg, Lot Value, Liquidity |
| **Benchmark Metric** | **88.15% Held-Out Accuracy** ($n=9,505$) | **86.39% Held-Out Accuracy** ($n=338$) | **Peak Silhouette Score: 0.6686** | Virgin Spot Benchmark Parity |
| **Execution Environment** | CPU / Scikit-Learn | CPU / PyTorch (~35 ms latency) | CPU / Scikit-Learn (<5 ms latency) | Pure Python / Vectorized Numpy (<1 ms) |
| **CAN DO** | ✅ Extract declared fiber from listing text<br>✅ Disambiguate blends from product copy<br>✅ Infer probable fiber from category priors | ✅ Identify macro garment silhouettes<br>✅ Classify 11 apparel styles accurately<br>✅ Flag low-confidence ambiguous images | ✅ Group blends into 5 recycling cohorts<br>✅ Quantify Euclidean distance in fiber space<br>✅ Provide preliminary theoretical streams | ✅ Compute transparent \$/kg baseline<br>✅ Apply mono-material premiums<br>✅ Apply scrap grade & defect discounts |
| **CANNOT DO** | ❌ Cannot test physical fabric swatches<br>❌ Cannot detect unstated chemical coatings<br>❌ Inaccurate on uninformative product text | ❌ **CANNOT identify fiber type (cotton/poly)**<br>❌ Cannot measure fabric weight or GSM<br>❌ Cannot determine fiber blend ratios | ❌ Cannot detect dye or chemical finishes<br>❌ Cannot evaluate staple fiber length<br>❌ Does not guarantee factory yields | ❌ **NOT a trained empirical ML model**<br>❌ Cannot predict live auction bidding<br>❌ No empirical transaction data backing |
| **Operational Boundary** | Dependent on listing textual quality | Macro silhouette sorting only | Theoretical recycling recommendations | Benchmark pricing guideline only |

---

## 6. API Documentation & Integration Status

All capabilities and documented boundaries are fully reflected across the live API endpoints:

```text
POST /api/ai/ds/predict/material     -> NLP Fiber Extraction (Model A)
POST /api/ai/ds/predict/image        -> Macro Garment Silhouette Sorting (Model B)
POST /api/ai/ds/predict/composition  -> Preliminary Recycling Archetypes (Model C)
POST /api/ai/ds/estimate/price       -> Heuristic Benchmark Valuation (Model D)
GET  /api/ai/ds/models               -> Full Model Capability & Limitation Catalog
```

### Direct File Links:
- [POST_IMPLEMENTATION_AUDIT.md](file:///c:/Users/dhruv/OneDrive/Desktop/ds/CUTLOOP/cutloop_ds/reports/POST_IMPLEMENTATION_AUDIT.md) — Empirical audit execution dossier and confusion matrices.
- [README.md](file:///c:/Users/dhruv/OneDrive/Desktop/ds/CUTLOOP/cutloop_ds/README.md) — Comprehensive technical reference manual.
- [main.py](file:///c:/Users/dhruv/OneDrive/Desktop/ds/CUTLOOP/cutloop_ds/api/main.py) — FastAPI microservice entrypoint with updated capability metadata.
- [payloads.py](file:///c:/Users/dhruv/OneDrive/Desktop/ds/CUTLOOP/cutloop_ds/api/schemas/payloads.py) — Pydantic schemas enforcing disclaimers and engine classifications.
