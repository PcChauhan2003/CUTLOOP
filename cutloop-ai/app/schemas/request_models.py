from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Pricing Schemas
class PricePredictRequest(BaseModel):
    material_type: str = Field(..., example="Cotton")
    condition: str = Field(..., example="Good")
    quantity_kg: float = Field(..., gt=0, example=100.0)
    width_inches: float = Field(default=60.0, example=60.0)
    colour: str = Field(default="Blue", example="Blue")
    location: str = Field(default="Ahmedabad", example="Ahmedabad")
    reference_price: float = Field(default=95.0, gt=0, example=95.0)

class PricePredictResponse(BaseModel):
    suggested_price: float
    suggested_price_min: float
    suggested_price_max: float
    unit: str = "INR/kg"
    model_name: str = "Random Forest Regressor (200 trees)"
    input_summary: Dict[str, str]

# Demand Schemas
class DemandPredictRequest(BaseModel):
    material_type: str = Field(..., example="Cotton")
    season: Optional[str] = Field(default="Summer", example="Summer")
    recent_orders: Optional[int] = Field(default=120, example=120)

class DemandPredictResponse(BaseModel):
    material_type: str
    forecasted_orders_next_month: int
    expected_search_volume: int
    demand_trend: str
    supply_status: str
    recommendation: str

# Fabric Classification Schemas
class FabricClassifyResponse(BaseModel):
    predicted_class: str
    confidence: float
    class_probabilities: Dict[str, float]
    explainability: Dict[str, str]

# Defect Inspection Schemas
class DefectBoundingBox(BaseModel):
    defect_type: str
    confidence: float
    bbox: List[int] # [x_min, y_min, x_max, y_max]

class DefectInspectionResponse(BaseModel):
    defect_detected: bool
    total_defects: int
    defects: List[DefectBoundingBox]
    inspection_type: str = "Visual Defect Inspection (Ultralytics YOLO)"
    seller_action: str
