"""
CUTLOOP Data Science Module — FastAPI Pydantic Schemas
Author: CUTLOOP Data Science Team
Script: api/schemas/payloads.py
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class MaterialPredictRequest(BaseModel):
    product_name: str = Field(..., example="Vintage Denim Utility Jacket")
    description: Optional[str] = Field("", example="Heavyweight rigid cotton twill jacket with brass button closures.")
    brand: Optional[str] = Field("H&M", example="H&M")
    region: Optional[str] = Field("UK", example="UK")
    gender_section: Optional[str] = Field("Men", example="Men")
    parent_category: Optional[str] = Field("Jacket", example="Jacket")

class MaterialPredictResponse(BaseModel):
    status: str
    predicted_dominant_fiber: str
    confidence: float
    top_probabilities: Dict[str, float]
    circularity_score: float
    is_mono_material: bool
    recycling_recommendation: str

class CompositionAnalysisRequest(BaseModel):
    fiber_percentages: Dict[str, float] = Field(..., example={"cotton": 95.0, "elastane": 5.0})

class CompositionAnalysisResponse(BaseModel):
    status: str
    assigned_cluster_id: int
    archetype_name: str
    circularity_score: float
    is_mono_material: bool
    is_blend: bool
    dominant_fiber: str
    recycling_pathway: str
    centroid_composition_pct: Dict[str, float]
    pathway_validation_status: str = "Preliminary Theoretical Guidance"
    disclaimer: str = "Recycling pathway recommendations are preliminary theoretical suggestions derived from archetype centroids, not lab-certified or industrially validated outcomes."

class PricingEstimateRequest(BaseModel):
    fiber_percentages: Dict[str, float] = Field(..., example={"cotton": 98.0, "elastane": 2.0})
    grade: Optional[str] = Field("grade_b_remnants", example="grade_b_remnants")
    weight_kg: Optional[float] = Field(50.0, example=120.0)
    has_defects: Optional[bool] = Field(False, example=False)
    defect_severity: Optional[float] = Field(0.0, example=0.0)
    is_recycled_origin: Optional[bool] = Field(False, example=False)

class PricingEstimateResponse(BaseModel):
    status: str
    estimated_price_per_kg_usd: float
    estimated_lot_total_usd: float
    weight_kg: float
    grade: str
    demand_liquidity_score: float
    demand_category: str
    expected_days_to_sell: str
    recycling_readiness: str
    factors: Dict[str, float]
    engine_classification: str = "Heuristic Benchmark Estimation Engine"
    disclaimer: str = "Valuation is a heuristic estimate based on virgin commodity spot benchmarks and physical grade multipliers. No empirical transaction history exists in the fast-fashion dataset; this is NOT a trained regression model."

class TopPrediction(BaseModel):
    category: str
    confidence: float

class VisionPredictionResponse(BaseModel):
    status: str
    predicted_category: str
    confidence: float
    top_3_predictions: List[TopPrediction]
    processing_time_ms: float
