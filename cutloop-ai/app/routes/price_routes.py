from fastapi import APIRouter, HTTPException
from app.services.pricing_service import pricing_service
from app.schemas.request_models import PricePredictRequest, PricePredictResponse

router = APIRouter(prefix="/api/ai", tags=["Price Estimation"])

@router.post("/price-predict", response_model=PricePredictResponse)
async def predict_price_endpoint(req: PricePredictRequest):
    try:
        res = pricing_service.predict_price(
            material_type=req.material_type,
            condition=req.condition,
            quantity_kg=req.quantity_kg,
            width_inches=req.width_inches,
            colour=req.colour,
            location=req.location,
            reference_price=req.reference_price
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Price estimation failed: {str(e)}")

@router.get("/price-metrics")
async def get_price_metrics():
    return {
        "model": "Random Forest Regressor (200 trees)",
        "metrics": pricing_service.metrics
    }
