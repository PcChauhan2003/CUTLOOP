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
