from fastapi import APIRouter, HTTPException
from app.services.demand_service import demand_service
from app.schemas.request_models import DemandPredictRequest, DemandPredictResponse

router = APIRouter(prefix="/api/ai", tags=["Demand Forecasting"])

@router.post("/demand-predict", response_model=DemandPredictResponse)
async def predict_demand_endpoint(req: DemandPredictRequest):
    try:
        res = demand_service.forecast_demand(
            material_type=req.material_type,
            season=req.season or "Summer",
            recent_orders=req.recent_orders or 120
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Demand forecasting failed: {str(e)}")

@router.get("/demand-trends")
async def get_demand_trends():
    return demand_service.get_market_trends()
