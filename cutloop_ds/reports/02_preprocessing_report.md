# CUTLOOP — Phase 2: Data Cleaning & Preprocessing Report

## 1. Executive Summary
- **Input Records Processed**: 47,522
- **Output Cleaned Features**: 31 standardized columns
- **Single-Fiber (Mono-Material >=95%)**: 23,775 (50.0%)
- **Blended Materials (>1 fiber)**: 27,814 (58.5%)
- **Recycled Fiber Claims Identified**: 2,085 (4.4%)
- **Average Heuristic Circularity Score**: 62.2 / 100

---

## 2. Missing Value Analysis & Imputation Strategy

| Feature | Missing Count | Missing % | Treatment Applied |
| :--- | :--- | :--- | :--- |
| `product_name` | 0 | 0.00% | Imputed with empty string, combined with description |
| `raw_description_text` | 93 | 0.20% | Imputed with empty string |
| `raw_material_text` | 0 | 0.00% | Normalized via `components_structured` |
| `raw_material_text_norm` | 0 | 0.00% | Fallback to raw_material_text |
| `parent_category` | 0 | 0.00% | Imputed as 'Unknown' |
| `detail_category` | 0 | 0.00% | Imputed as 'Unknown' |
| `brand` | 0 | 0.00% | Normalized uppercase ('H&M', 'UNIQLO') |
| `region` | 0 | 0.00% | Normalized uppercase ('UK', 'AU') |
| `gender_section` | 0 | 0.00% | Normalized Title Case |
| `components_structured` | 0 | 0.00% | Extracted fiber breakdown with default zero vector |

---

## 3. Fiber Composition Extraction & Standardization

Standardized industrial textile categories extracted using `components_structured` and `pct` key:
- Target Fibers: `cotton`, `polyester`, `elastane`, `polyamide`, `viscose`, `wool`, `acrylic`, `linen`, `silk`, `lyocell`, and `other`.
- Synonyms mapped: `nylon` -> `polyamide`, `spandex` / `elastomeric` -> `elastane`, `rayon` -> `viscose`.

### Top Dominant Fibers in Dataset:
- **Cotton**: 23,985 (50.47%)
- **Polyester**: 13,176 (27.73%)
- **Polyamide**: 3,328 (7.00%)
- **Viscose**: 3,316 (6.98%)
- **Wool**: 997 (2.10%)
- **Acrylic**: 737 (1.55%)
- **Linen**: 703 (1.48%)
- **Other**: 675 (1.42%)
- **Lyocell**: 544 (1.14%)
- **Elastane**: 33 (0.07%)

### Top Standardized Categories:
- **Tops**: 22,051 (46.40%)
- **Bottoms**: 12,076 (25.41%)
- **Overall**: 7,664 (16.13%)
- **Underwear**: 5,731 (12.06%)

---

## 4. Circularity Heuristic Index Definition
To bridge fast-fashion composition to CUTLOOP circular recycling, an industrial heuristic score (0-100) was defined:
- **Mono-material naturals (Cotton, Wool, Linen >=95%)**: 85 base + 15 bonus if recycled. High circular value for shredding & mechanical spinning.
- **Mono-material synthetics (Polyester, Polyamide >=95%)**: 70 base + 15 bonus if recycled. High chemical / pellet recycling value.
- **High-cotton low-stretch blends (>=90% cotton, <=5% elastane)**: 75 base. Readily processable in garment-to-garment recyclers.
- **Multi-material blends (>2 fibers or intimate poly-cotton)**: 30 base. Low circularity due to difficult chemical separation.

---

## 5. Artifacts Produced
- Cleaned Compressed CSV: `datasets/processed/garments_cleaned.csv.gz`
- Preprocessing Script: `src/preprocessing/clean_garment_data.py`
