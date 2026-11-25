"""
CUTLOOP Data Science Module — Phase 2: Tabular Garment Data Cleaning & Preprocessing
Author: CUTLOOP Data Science Team
Script: src/preprocessing/clean_garment_data.py

Processes 6_JSONL_component_normalized_public.jsonl:
- Quantifies missingness
- Standardizes text fields (descriptions, names, raw materials)
- Parses components_structured into fiber percentages & circularity indicators:
    - Dominant fiber & percentage (using key 'pct')
    - Mono-material (>=95%) vs Blend flag
    - Recycled content indicator
    - Fiber count & composition vector (cotton, polyester, elastane, polyamide, viscose, wool, acrylic, linen, other)
- Standardizes categories (parent_category, detail_category, brand, gender, region)
- Saves outputs to datasets/processed/garments_cleaned.csv.gz
"""

import os
import sys
import json
import re
import pandas as pd
import numpy as np
from collections import Counter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RAW_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
JSONL_PATH = os.path.join(RAW_DATA_DIR, "6_JSONL_component_normalized_public.jsonl")
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

TARGET_FIBERS = [
    "cotton", "polyester", "elastane", "polyamide", 
    "viscose", "wool", "acrylic", "linen", "silk", "lyocell"
]

def clean_text(text: str) -> str:
    """Normalize text: lowercase, remove html/boilerplate, collapse whitespace."""
    if not text or not isinstance(text, str):
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[^\w\s\-\.\,\%\/]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def extract_composition(components_structured):
    """
    Parse components_structured to extract surface/shell/body or overall fiber percentages.
    """
    fiber_pcts = {f: 0.0 for f in TARGET_FIBERS}
    fiber_pcts["other"] = 0.0
    
    if not components_structured or not isinstance(components_structured, list):
        return {
            **fiber_pcts,
            "dominant_fiber": "unknown",
            "dominant_pct": 0.0,
            "fiber_count": 0,
            "is_blend": False,
            "is_mono_material": False,
            "num_components": 0,
            "has_lining": False,
            "has_recycled": False
        }
        
    num_components = len(components_structured)
    has_lining = False
    has_recycled = False
    
    # Priority: surface_component / shell / body
    chosen_materials = None
    for comp in components_structured:
        c_class = str(comp.get("component_class", "")).lower()
        c_name = str(comp.get("component_name_norm", "")).lower()
        if "lining" in c_class or "lining" in c_name:
            has_lining = True
            
        mats = comp.get("materials", [])
        if mats:
            for m in mats:
                if m.get("recycled_pct") is not None or "recycled" in str(m.get("material", "")).lower():
                    has_recycled = True
                    
        if (c_class == "surface_component" or c_name in ["shell", "body", "main"]) and mats:
            chosen_materials = mats
            break
            
    if not chosen_materials and components_structured:
        for comp in components_structured:
            mats = comp.get("materials", [])
            if mats:
                chosen_materials = mats
                break
                
    if chosen_materials:
        for m in chosen_materials:
            m_name = str(m.get("material", "")).strip().lower()
            val = m.get("pct") if m.get("pct") is not None else m.get("percentage")
            try:
                pct = float(val or 0.0)
            except (ValueError, TypeError):
                pct = 0.0
                
            if m.get("recycled_pct") or "recycled" in m_name:
                has_recycled = True
                
            # Map synonymous materials
            if "nylon" in m_name:
                m_name = "polyamide"
            elif "spandex" in m_name or "elastomeric" in m_name:
                m_name = "elastane"
            elif "rayon" in m_name:
                m_name = "viscose"
                
            matched = False
            for target in TARGET_FIBERS:
                if target in m_name:
                    fiber_pcts[target] += pct
                    matched = True
                    break
            if not matched and pct > 0:
                fiber_pcts["other"] += pct
                
    # Normalize if total exceeds 105
    tot = sum(fiber_pcts.values())
    if tot > 105.0:
        for k in fiber_pcts:
            fiber_pcts[k] = round((fiber_pcts[k] / tot) * 100.0, 2)
            
    # Find dominant fiber
    fibers_present = {k: v for k, v in fiber_pcts.items() if v > 2.0}
    if fibers_present:
        dom_fiber, dom_pct = max(fibers_present.items(), key=lambda x: x[1])
    else:
        dom_fiber = "unknown"
        dom_pct = 0.0
        
    fiber_count = len(fibers_present)
    is_blend = fiber_count > 1
    is_mono_material = dom_pct >= 95.0
    
    return {
        **fiber_pcts,
        "dominant_fiber": dom_fiber,
        "dominant_pct": round(dom_pct, 2),
        "fiber_count": fiber_count,
        "is_blend": is_blend,
        "is_mono_material": is_mono_material,
        "num_components": num_components,
        "has_lining": has_lining,
        "has_recycled": has_recycled
    }

def clean_and_preprocess_garment_dataset():
    print(f"[*] Starting garment data preprocessing from: {JSONL_PATH}")
    rows = []
    missing_counters = Counter()
    total_records = 0
    
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line_str = line.strip()
            if not line_str:
                continue
            total_records += 1
            rec = json.loads(line_str)
            
            # Check missingness
            for field in [
                "product_name", "raw_description_text", "raw_material_text", 
                "raw_material_text_norm", "parent_category", "detail_category",
                "brand", "region", "gender_section", "components_structured"
            ]:
                if not rec.get(field):
                    missing_counters[field] += 1
                    
            comp_info = extract_composition(rec.get("components_structured"))
            
            # Text normalization
            prod_name = clean_text(rec.get("product_name", ""))
            desc = clean_text(rec.get("raw_description_text", ""))
            raw_mat = clean_text(rec.get("raw_material_text", ""))
            raw_mat_norm = clean_text(rec.get("raw_material_text_norm", ""))
            
            if "recycled" in prod_name or "recycled" in desc or "recycled" in raw_mat:
                comp_info["has_recycled"] = True
                
            # Circularity Heuristic Score (0-100)
            score = 50.0
            if comp_info["is_mono_material"]:
                if comp_info["dominant_fiber"] in ["cotton", "wool", "linen", "silk"]:
                    score = 85.0
                elif comp_info["dominant_fiber"] in ["polyester", "polyamide"]:
                    score = 70.0
                else:
                    score = 65.0
            elif comp_info["fiber_count"] == 2:
                if comp_info["dominant_pct"] >= 90.0:
                    score = 75.0
                else:
                    score = 45.0
            else:
                score = 30.0
                
            if comp_info["has_recycled"]:
                score = min(100.0, score + 15.0)
                
            cleaned_row = {
                "parent_product_id": str(rec.get("parent_product_id", "")),
                "url": str(rec.get("url", "")),
                "brand": str(rec.get("brand", "Unknown")).strip().upper(),
                "region": str(rec.get("region", "Unknown")).strip().upper(),
                "gender_section": str(rec.get("gender_section", "Unisex")).strip().title(),
                "parent_category": str(rec.get("parent_category", "Unknown")).strip().title(),
                "detail_category": str(rec.get("detail_category", "Unknown")).strip().title(),
                "product_name_clean": prod_name,
                "description_clean": desc,
                "material_text_clean": raw_mat_norm if raw_mat_norm else raw_mat,
                "text_combined": f"{prod_name} {desc}".strip(),
                "circularity_score": round(score, 1),
                **comp_info
            }
            rows.append(cleaned_row)
            
            if (idx + 1) % 10000 == 0:
                print(f"    Processed {idx + 1} records...")
                
    df = pd.DataFrame(rows)
    print(f"[*] Preprocessing complete. DataFrame shape: {df.shape}")
    print("Dominant Fiber Counts:\n", df["dominant_fiber"].value_counts().head(8))
    
    csv_path = os.path.join(PROCESSED_DIR, "garments_cleaned.csv.gz")
    print(f"[*] Saving cleaned csv.gz to: {csv_path}")
    df.to_csv(csv_path, index=False, compression="gzip")
    
    # Generate Preprocessing Report
    report_path = os.path.join(REPORTS_DIR, "02_preprocessing_report.md")
    print(f"[*] Writing preprocessing report to: {report_path}")
    
    mono_cnt = int(df["is_mono_material"].sum())
    blend_cnt = int(df["is_blend"].sum())
    recycled_cnt = int(df["has_recycled"].sum())
    top_dom_fibers = df["dominant_fiber"].value_counts().head(10).to_dict()
    top_parent_cats = df["parent_category"].value_counts().head(10).to_dict()
    
    report_content = f"""# CUTLOOP — Phase 2: Data Cleaning & Preprocessing Report

## 1. Executive Summary
- **Input Records Processed**: {total_records:,}
- **Output Cleaned Features**: {len(df.columns)} standardized columns
- **Single-Fiber (Mono-Material >=95%)**: {mono_cnt:,} ({mono_cnt/total_records*100:.1f}%)
- **Blended Materials (>1 fiber)**: {blend_cnt:,} ({blend_cnt/total_records*100:.1f}%)
- **Recycled Fiber Claims Identified**: {recycled_cnt:,} ({recycled_cnt/total_records*100:.1f}%)
- **Average Heuristic Circularity Score**: {df['circularity_score'].mean():.1f} / 100

---

## 2. Missing Value Analysis & Imputation Strategy

| Feature | Missing Count | Missing % | Treatment Applied |
| :--- | :--- | :--- | :--- |
| `product_name` | {missing_counters['product_name']} | {missing_counters['product_name']/total_records*100:.2f}% | Imputed with empty string, combined with description |
| `raw_description_text` | {missing_counters['raw_description_text']} | {missing_counters['raw_description_text']/total_records*100:.2f}% | Imputed with empty string |
| `raw_material_text` | {missing_counters['raw_material_text']} | {missing_counters['raw_material_text']/total_records*100:.2f}% | Normalized via `components_structured` |
| `raw_material_text_norm` | {missing_counters['raw_material_text_norm']} | {missing_counters['raw_material_text_norm']/total_records*100:.2f}% | Fallback to raw_material_text |
| `parent_category` | {missing_counters['parent_category']} | {missing_counters['parent_category']/total_records*100:.2f}% | Imputed as 'Unknown' |
| `detail_category` | {missing_counters['detail_category']} | {missing_counters['detail_category']/total_records*100:.2f}% | Imputed as 'Unknown' |
| `brand` | {missing_counters['brand']} | {missing_counters['brand']/total_records*100:.2f}% | Normalized uppercase ('H&M', 'UNIQLO') |
| `region` | {missing_counters['region']} | {missing_counters['region']/total_records*100:.2f}% | Normalized uppercase ('UK', 'AU') |
| `gender_section` | {missing_counters['gender_section']} | {missing_counters['gender_section']/total_records*100:.2f}% | Normalized Title Case |
| `components_structured` | {missing_counters['components_structured']} | {missing_counters['components_structured']/total_records*100:.2f}% | Extracted fiber breakdown with default zero vector |

---

## 3. Fiber Composition Extraction & Standardization

Standardized industrial textile categories extracted using `components_structured` and `pct` key:
- Target Fibers: `cotton`, `polyester`, `elastane`, `polyamide`, `viscose`, `wool`, `acrylic`, `linen`, `silk`, `lyocell`, and `other`.
- Synonyms mapped: `nylon` -> `polyamide`, `spandex` / `elastomeric` -> `elastane`, `rayon` -> `viscose`.

### Top Dominant Fibers in Dataset:
"""
    for fib, count in top_dom_fibers.items():
        report_content += f"- **{fib.title()}**: {count:,} ({count/total_records*100:.2f}%)\n"
        
    report_content += f"""
### Top Standardized Categories:
"""
    for cat, count in top_parent_cats.items():
        report_content += f"- **{cat}**: {count:,} ({count/total_records*100:.2f}%)\n"
        
    report_content += """
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
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"[*] Preprocessing report updated at: {report_path}")
    return df

if __name__ == "__main__":
    clean_and_preprocess_garment_dataset()
