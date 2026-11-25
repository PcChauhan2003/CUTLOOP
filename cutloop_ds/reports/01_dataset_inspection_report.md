# CUTLOOP Data Science Module — Phase 1: Comprehensive Dataset Inspection Report
**Project:** CUTLOOP — Industrial Waste-to-Value Marketplace
**Phase:** 1 (Dataset Inspection & Quality Assessment)
**Date:** 2026-11-21

---

## 1. Executive Summary & Datasets Overview

In this phase, we conducted an exhaustive, empirical inspection of the four supplied dataset files:
1. `6_JSONL_component_normalized_public.jsonl`: Curated fast-fashion garment variant dataset (Zenodo DOI: 10.5281/zenodo.20006389).
2. `TexSortML-Pictures.zip`: Garment sorting image benchmark containing 4,504 high-resolution JPEG images.
3. `README.md`: Dataset provenance, licensing (CC-BY 4.0), and research reuse guidelines.
4. `6_JSONL_component_normalized_public_summary.txt`: Field filtering and curation audit log.

### Key Statistical Highlights:
- **Total Garment Records (JSONL):** 47,522
- **Exact Duplicate Records:** 0
- **Unique URLs:** 43,404 (multiple color variants share parent URLs)
- **Unique Parent Product IDs:** 35,860
- **Total Garment Images (TexSortML):** 4,504 images across 11 sorting classes
- **Image Dimensions:** Consistent 730 × 730 RGB JPEG (0 corrupt files)

## 2. Critical Dataset Limitations & Ethical Boundary Analysis

> [!IMPORTANT]
> **Explicit Disclaimer on Marketplace Targets:**
> Neither of these research datasets provides actual CUTLOOP secondary marketplace transaction prices (₹/kg) or industrial waste demand / sales history.
> - **JSONL Dataset Limitation:** Does not contain product photographs, consumer reviews, ratings, sales counts, or transaction prices. It is strictly a retailer-disclosed material composition and product categorization dataset.
> - **TexSortML Dataset Limitation:** Contains post-consumer / pre-sorted garment photographs across 11 apparel silhouettes (`poloshirt`, `tshirt`, `jeans`, etc.), but does NOT contain raw textile offcut roll defect labels.
> - **CUTLOOP Integration Principle:** We must NOT fabricate price models or demand models on these datasets. Instead, we use the JSONL dataset for **Material Composition Analysis, Circularity Profiling, and Garment Classification**, and TexSortML for **Garment Silhouette & Category Computer Vision**, keeping transaction pricing linked to verified marketplace logs.

## 3. Garment Dataset (JSONL) Inspection & Schema Analysis

| Field Name | Inferred Data Type | Populated Count | Missing Count | Completeness % |
| :--- | :---: | :---: | :---: | :---: |
| `parent_product_id` | `str` | 47,522 | 0 | 100.00% |
| `brand` | `str` | 47,522 | 0 | 100.00% |
| `region` | `str` | 47,522 | 0 | 100.00% |
| `url` | `str` | 47,522 | 0 | 100.00% |
| `url_collected_at` | `str` | 47,522 | 0 | 100.00% |
| `scraped_at` | `str` | 47,522 | 0 | 100.00% |
| `gender_section` | `str` | 47,522 | 0 | 100.00% |
| `raw_category` | `str` | 47,522 | 0 | 100.00% |
| `product_name` | `str` | 47,522 | 0 | 100.00% |
| `variant_colour` | `str` | 47,522 | 0 | 100.00% |
| `all_colour_labels` | `list` | 47,522 | 0 | 100.00% |
| `raw_material_text` | `str` | 47,522 | 0 | 100.00% |
| `raw_material_text_full` | `str` | 47,522 | 0 | 100.00% |
| `composition_assignment_type` | `str` | 47,522 | 0 | 100.00% |
| `raw_material_text_norm` | `str` | 47,522 | 0 | 100.00% |
| `detail_category` | `str` | 47,522 | 0 | 100.00% |
| `detail_rule_source` | `str` | 47,522 | 0 | 100.00% |
| `detail_rule_hit` | `str` | 47,522 | 0 | 100.00% |
| `parent_category` | `str` | 47,522 | 0 | 100.00% |
| `components_structured` | `list` | 47,522 | 0 | 100.00% |
| `raw_description_text` | `str` | 47,429 | 93 | 99.80% |
| `raw_function_text` | `str` | 44,945 | 2577 | 94.58% |

### Categorical Distributions in JSONL:
#### Brand Distribution:
- **HM**: 41,077 (86.44%)
- **UNIQLO**: 6,445 (13.56%)

#### Regional Distribution:
- **GB**: 26,839 (56.48%)
- **AU**: 17,063 (35.91%)
- **UK**: 3,620 (7.62%)

#### Parent Garment Categories:
- **Tops**: 22,051 (46.40%)
- **Bottoms**: 12,076 (25.41%)
- **Overall**: 7,664 (16.13%)
- **Underwear**: 5,731 (12.06%)

#### Top 10 Detail Categories:
- **tshirt_polo**: 5,461 (11.49%)
- **dresses**: 4,854 (10.21%)
- **sweater_cardigan**: 4,378 (9.21%)
- **shirt_blouse**: 4,125 (8.68%)
- **trousers**: 4,116 (8.66%)
- **outerwear_jacket**: 2,978 (6.27%)
- **jeans**: 2,351 (4.95%)
- **sweatshirt_hoodie**: 2,008 (4.23%)
- **underwear_bottoms**: 1,926 (4.05%)
- **shorts**: 1,805 (3.80%)

#### Top 10 Textile Fiber Materials in `components_structured`:
| Fiber Material | Mention Frequency in Components | Percentage of Components |
| :--- | :---: | :---: |
| **Polyester** | 34,011 | 28.71% |
| **Cotton** | 33,690 | 28.44% |
| **Elastane** | 22,041 | 18.61% |
| **Nylon** | 9,712 | 8.20% |
| **Viscose** | 7,902 | 6.67% |
| **Wool** | 3,164 | 2.67% |
| **Acrylic** | 2,549 | 2.15% |
| **Linen** | 1,876 | 1.58% |
| **Lyocell** | 945 | 0.80% |
| **Elastomultiester** | 500 | 0.42% |

---

## 4. TexSortML Image Dataset Inspection & Verification

- **Total Images:** 4,504 JPEG files.
- **Resolution:** 100% of examined images are exactly **730 × 730 pixels** in **RGB 24-bit** color depth.
- **Corrupted / Unreadable Images:** **0** (All images have valid JPEG headers and decodable pixel streams).
- **Class Structure:** 11 distinct garment categories arranged across 4 logical stage directories:

### Distribution by Stage:
- **`stage-mixed`**: 2,252 images (50.00%)
- **`stage1`**: 751 images (16.67%)
- **`stage2`**: 751 images (16.67%)
- **`stage3`**: 750 images (16.65%)

### Distribution by Garment Category (All Stages Combined):
| Garment Class | Total Image Count | Class Proportion | Imbalance Ratio (vs max) |
| :--- | :---: | :---: | :---: |
| `poloshirt` | 726 | 16.12% | 1 : 1.00 |
| `sweatshirt` | 696 | 15.45% | 1 : 1.04 |
| `short` | 610 | 13.54% | 1 : 1.19 |
| `jacket` | 576 | 12.79% | 1 : 1.26 |
| `shirt` | 480 | 10.66% | 1 : 1.51 |
| `tshirt` | 336 | 7.46% | 1 : 2.16 |
| `dress` | 330 | 7.33% | 1 : 2.20 |
| `trouser` | 246 | 5.46% | 1 : 2.95 |
| `jeans` | 234 | 5.20% | 1 : 3.10 |
| `top` | 168 | 3.73% | 1 : 4.32 |
| `jacket-zipper` | 102 | 2.26% | 1 : 7.12 |

*Observation: `poloshirt` (726) and `sweatshirt` (696) have the highest representation, while `jacket-zipper` (102) and `top` (168) have the lowest. We must apply class weighting or stratified sampling during model training.*

## 5. Conclusions & Next Steps for Phase 2

### Key Findings from Phase 1:
1. The JSONL dataset is remarkably clean: 100% of records have `product_name`, `brand`, `parent_category`, `detail_category`, `raw_material_text_norm`, and `components_structured`. Only `raw_description_text` (0.2% missing) and `raw_function_text` (5.42% missing) have minor nulls.
2. `components_structured` provides granular, standardized percentages per component (e.g. `shell`: 98% cotton, 2% elastane; `lining`: 100% polyester), making it ideal for multi-label and fiber-ratio modeling.
3. TexSortML images are high-quality, uncorrupted, and consistently formatted ($730 \times 730$).
4. `stage-mixed` (2,252 images) precisely combines `stage1` (751) + `stage2` (751) + `stage3` (750). We can use `stage-mixed` with stratified train/val/test splits (e.g., 70% train, 15% val, 15% test).

### Action Items for Phase 2 (Data Cleaning and Preprocessing):
- Extract dominant fiber material and fiber composition vectors from `components_structured`.
- Standardize categorical strings (`region`, `gender_section`, `parent_category`).
- Clean minor missing text in `raw_description_text` and `raw_function_text`.
- Extract TexSortML images into `cutloop_ds/datasets/processed/images/` with stratified train/val/test manifests.
- Save cleaned JSONL / tabular data to `cutloop_ds/datasets/processed/`.