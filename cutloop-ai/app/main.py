from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.fabric_routes import router as fabric_router
from app.routes.defect_routes import router as defect_router
from app.routes.price_routes import router as price_router
from app.routes.demand_routes import router as demand_router

app = FastAPI(
    title="CUTLOOP AI Services",
    description="Deep Learning and Machine Learning API Services for CUTLOOP Marketplace",
    version="1.0.0"
)

# Enable CORS for frontend and Spring Boot backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fabric_router)
app.include_router(defect_router)
app.include_router(price_router)
app.include_router(demand_router)

# Mount CUTLOOP Circular Data Science & Machine Learning Service
try:
    import os
    import sys
    DS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "cutloop_ds"))
    if DS_ROOT not in sys.path:
        sys.path.insert(0, DS_ROOT)
    from api.routes.material_routes import router as ds_material_router
    from api.routes.vision_routes import router as ds_vision_router
    from api.routes.analytics_routes import router as ds_analytics_router

    app.include_router(ds_material_router, prefix="/api/ai/ds")
    app.include_router(ds_vision_router, prefix="/api/ai/ds")
    app.include_router(ds_analytics_router, prefix="/api/ai/ds")
    print("[*] Successfully integrated CUTLOOP Circular Data Science routes at /api/ai/ds")
except Exception as e:
    print(f"[!] Warning integrating cutloop_ds routes: {e}")


@app.get("/api/ai/health", tags=["Health"])
def health():
    """
    Requirement 7.2: Health check endpoint
    """
    return {
        "status": "running",
        "service": "CUTLOOP AI Services",
        "models": {
            "fabric_classifier": "MobileNetV2 (Transfer Learning)",
            "defect_detector": "YOLO (Visual Defect Inspection)",
            "price_estimator": "Random Forest Regressor",
            "demand_forecaster": "Random Forest Time-Series"
        },
        "explainability": "Grad-CAM Enabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
