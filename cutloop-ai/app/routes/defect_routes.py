from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.defect_service import defect_service
from app.schemas.request_models import DefectInspectionResponse

router = APIRouter(prefix="/api/ai", tags=["Defect Inspection"])

@router.post("/defect-detect", response_model=DefectInspectionResponse)
async def detect_defects_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = defect_service.inspect_image(contents, file.filename or "sample.jpg")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Defect inspection failed: {str(e)}")
