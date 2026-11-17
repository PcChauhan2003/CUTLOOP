from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.fabric_service import fabric_service
from app.schemas.request_models import FabricClassifyResponse

router = APIRouter(prefix="/api/ai", tags=["Fabric Classification"])

@router.post("/fabric-classify", response_model=FabricClassifyResponse)
async def classify_fabric_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = fabric_service.classify_fabric(contents, file.filename or "sample.jpg")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image classification failed: {str(e)}")
