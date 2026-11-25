"""
CUTLOOP Data Science API — Material & Circularity Routes
Author: CUTLOOP Data Science Team
Script: api/routes/material_routes.py
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from scipy.sparse import hstack
from fastapi import APIRouter, HTTPException

from api.schemas.payloads import (
    MaterialPredictRequest, MaterialPredictResponse,
    CompositionAnalysisRequest, CompositionAnalysisResponse,
    PricingEstimateRequest, PricingEstimateResponse
)
from src.models.pricing_engine import TextilePricingEngine

router = APIRouter(prefix="", tags=["Material & Textile Intelligence"])

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")

# Lazy model loaders
_feature_pipeline = None
_model_a = None
_model_c = None
_archetypes = None
_pricing_engine = TextilePricingEngine()

def get_material_models():
    global _feature_pipeline, _model_a, _model_c, _archetypes
    if _feature_pipeline is None:
        pipe_path = os.path.join(SAVED_MODELS_DIR, "feature_pipeline.joblib")
        if os.path.exists(pipe_path):
            _feature_pipeline = joblib.load(pipe_path)
            
    if _model_a is None:
        rf_path = os.path.join(SAVED_MODELS_DIR, "model_a_random_forest.joblib")
        if os.path.exists(rf_path):
            _model_a = joblib.load(rf_path)
            
    if _model_c is None:
        c_path = os.path.join(SAVED_MODELS_DIR, "model_c_kmeans.joblib")
        if os.path.exists(c_path):
            _model_c = joblib.load(c_path)
            
    if _archetypes is None:
        arch_path = os.path.join(SAVED_MODELS_DIR, "archetype_profiles.json")
        if os.path.exists(arch_path):
            with open(arch_path, "r", encoding="utf-8") as f:
                _archetypes = json.load(f)
                
    return _feature_pipeline, _model_a, _model_c, _archetypes

@router.post("/predict/material", response_model=MaterialPredictResponse)
def predict_material(payload: MaterialPredictRequest):
    """
    Model A: Predicts dominant textile fiber via NLP text extraction & categorization from listing title and description.
    Note: Operates on textual mentions in product copy; this is NOT spectroscopic or chemical fabric analysis.
    """
    pipe, model_a, _, _ = get_material_models()
    if not pipe or not model_a:
        raise HTTPException(status_code=503, detail="Model A is not loaded or still training.")
        
    combined_text = f"{payload.product_name} {payload.description}".strip().lower()
    
    # Transform text
    X_text = pipe["tfidf"].transform([combined_text])
    
    # Transform categorical using DataFrame to preserve feature names
    cat_df = pd.DataFrame([{
        "brand": payload.brand.upper() if payload.brand else "Unknown",
        "region": payload.region.upper() if payload.region else "Unknown",
        "gender_section": payload.gender_section.title() if payload.gender_section else "Unisex",
        "parent_category": payload.parent_category.title() if payload.parent_category else "Unknown"
    }])
    X_cat = pipe["ohe"].transform(cat_df)
    
    # Approximate circularity indicator for response
    has_rec = 1.0 if "recycled" in combined_text else 0.0
    approx_circ = 75.0 if has_rec else 60.0
    
    # Stack features (Leak-free pure NLP + Categorical pipeline)
    if pipe.get("scaler") is not None and pipe.get("num_cols"):
        num_vals = np.array([[1.0, 0.0, has_rec, approx_circ]])
        X_num = pipe["scaler"].transform(num_vals)
        X_input = hstack([X_text, X_cat, X_num]).tocsr()
    else:
        X_input = hstack([X_text, X_cat]).tocsr()
    
    probs = model_a.predict_proba(X_input)[0]
    classes = pipe["target_classes"]
    
    best_idx = int(np.argmax(probs))
    best_fiber = classes[best_idx]
    confidence = round(float(probs[best_idx]), 4)
    
    prob_dict = {classes[i]: round(float(probs[i]), 4) for i in range(len(classes))}
    
    # Recyclability recommendation
    is_mono = confidence > 0.80
    if best_fiber in ["cotton", "wool", "linen"]:
        rec = f"Natural fiber ({best_fiber}). Suitable for mechanical fraying, shoddy carding, or cotton-to-cotton re-spinning."
    elif best_fiber in ["polyester", "polyamide"]:
        rec = f"Synthetic polymer ({best_fiber}). Prime candidate for thermal granulating or chemical depolymerization."
    else:
        rec = f"Mixed/Specialty fiber ({best_fiber}). Sorting inspection recommended prior to bulk consignment."
        
    return MaterialPredictResponse(
        status="success",
        predicted_dominant_fiber=best_fiber,
        confidence=confidence,
        top_probabilities=prob_dict,
        circularity_score=approx_circ,
        is_mono_material=is_mono,
        recycling_recommendation=rec
    )

@router.post("/analyze/composition", response_model=CompositionAnalysisResponse)
def analyze_composition(payload: CompositionAnalysisRequest):
    """
    Model C: Clusters continuous fiber percentages into 5 industrial archetypes and suggests preliminary theoretical recycling pathways.
    Note: Suggested pathways are preliminary theoretical recommendations based on archetype centroids, NOT lab-validated industrial processing guarantees.
    """
    _, _, model_c, archetypes = get_material_models()
    if not model_c or not archetypes:
        raise HTTPException(status_code=503, detail="Model C is not loaded.")
        
    fiber_cols = [
        "cotton", "polyester", "elastane", "polyamide", 
        "viscose", "wool", "acrylic", "linen", "silk", "lyocell"
    ]
    vec = [float(payload.fiber_percentages.get(f, 0.0)) for f in fiber_cols]
    vec_arr = np.array([vec])
    
    cluster_id = int(model_c.predict(vec_arr)[0])
    profile = archetypes.get(f"cluster_{cluster_id}", {})
    
    # Calculate score & blend flags
    dom_fiber = max(payload.fiber_percentages.items(), key=lambda x: x[1])[0] if payload.fiber_percentages else "unknown"
    dom_pct = max(payload.fiber_percentages.values()) if payload.fiber_percentages else 0.0
    is_mono = dom_pct >= 95.0
    fibers_over_2 = [k for k, v in payload.fiber_percentages.items() if v > 2.0]
    is_blend = len(fibers_over_2) > 1
    
    if is_mono:
        score = 85.0 if dom_fiber in ["cotton", "wool", "linen"] else 70.0
    elif len(fibers_over_2) == 2 and dom_pct >= 90.0:
        score = 75.0
    else:
        score = 40.0
        
    return CompositionAnalysisResponse(
        status="success",
        assigned_cluster_id=cluster_id,
        archetype_name=profile.get("archetype_name", "Textile Archetype"),
        circularity_score=score,
        is_mono_material=is_mono,
        is_blend=is_blend,
        dominant_fiber=dom_fiber,
        recycling_pathway=profile.get("recycling_pathway", "Standard recycling stream"),
        centroid_composition_pct=profile.get("centroid_composition_pct", {})
    )

@router.post("/estimate/price", response_model=PricingEstimateResponse)
def estimate_price(payload: PricingEstimateRequest):
    """
    Model D: Computes heuristic benchmark valuation, demand liquidity score, and expected days-to-clear.
    Note: Heuristic benchmark estimation engine based on virgin commodity spot rates and scrap grade multipliers. No historical transaction dataset exists.
    """
    val = _pricing_engine.estimate_price(
        fiber_percentages=payload.fiber_percentages,
        grade=payload.grade,
        weight_kg=payload.weight_kg,
        has_defects=payload.has_defects,
        defect_severity=payload.defect_severity,
        is_recycled_origin=payload.is_recycled_origin
    )
    return PricingEstimateResponse(status="success", **val)
