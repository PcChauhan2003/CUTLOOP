"""
CUTLOOP Data Science API — Analytics & Sourced Inventory Routes
Author: CUTLOOP Data Science Team
Script: api/routes/analytics_routes.py
"""

import os
import sys
import json
import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/analytics", tags=["Marketplace Sourced Inventory Analytics"])

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")

_cached_stats = None

def get_inventory_stats():
    global _cached_stats
    if _cached_stats is None:
        garments_path = os.path.join(PROCESSED_DIR, "garments_cleaned.csv.gz")
        manifest_path = os.path.join(PROCESSED_DIR, "image_splits_manifest.csv")
        
        if os.path.exists(garments_path) and os.path.exists(manifest_path):
            df_g = pd.read_csv(garments_path)
            df_img = pd.read_csv(manifest_path)
            
            top_fibers = df_g["dominant_fiber"].value_counts().head(8).to_dict()
            top_categories = df_g["parent_category"].value_counts().head(10).to_dict()
            brand_dist = df_g["brand"].value_counts().to_dict()
            mono_cnt = int(df_g["is_mono_material"].sum())
            blend_cnt = int(df_g["is_blend"].sum())
            
            _cached_stats = {
                "total_garments": len(df_g),
                "total_benchmark_images": len(df_img),
                "mono_material_count": mono_cnt,
                "mono_material_percentage": round(mono_cnt / len(df_g) * 100, 2),
                "blend_material_count": blend_cnt,
                "blend_material_percentage": round(blend_cnt / len(df_g) * 100, 2),
                "average_circularity_score": round(float(df_g["circularity_score"].mean()), 2),
                "top_fibers": top_fibers,
                "top_categories": top_categories,
                "brand_distribution": brand_dist,
                "vision_categories": df_img["category"].value_counts().to_dict()
            }
        else:
            _cached_stats = {"status": "Datasets still processing"}
            
    return _cached_stats

@router.get("/summary")
def get_summary():
    """Returns platform-wide textile inventory analytics, circularity index, and blend ratios."""
    return get_inventory_stats()

@router.get("/materials")
def get_materials_analytics():
    """Returns top dominant fibers and recyclability fractions."""
    stats = get_inventory_stats()
    return {
        "dominant_fibers": stats.get("top_fibers", {}),
        "mono_material_ratio": stats.get("mono_material_percentage", 0),
        "blend_ratio": stats.get("blend_material_percentage", 0),
        "circularity_index_mean": stats.get("average_circularity_score", 0)
    }

@router.get("/categories")
def get_category_analytics():
    """Returns top garment categories and TexSortML vision classes."""
    stats = get_inventory_stats()
    return {
        "inventory_categories": stats.get("top_categories", {}),
        "vision_classes": stats.get("vision_categories", {})
    }
