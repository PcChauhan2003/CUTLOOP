"""
CUTLOOP Data Science Module — FastAPI Machine Learning Application
Author: CUTLOOP Data Science Team
Script: api/main.py

Exposes:
- GET  /health               Service health, uptime, model status
- GET  /models               Catalog of Model A, Model B, Model C, Model D
- POST /predict/material     Model A: Dominant fiber & circularity predictor
- POST /analyze/composition  Model C: Fiber archetype clustering & circular pathways
- POST /estimate/price       Model D: B2B secondary fabric pricing & demand score
- POST /predict/image        Model B: TexSortML deep vision garment sorting
- GET  /analytics/summary    Sourced fast-fashion & TexSortML platform analytics
- GET  /analytics/materials  Fiber & blend distribution
- GET  /analytics/categories Garment & vision class breakdown
"""

import os
import sys
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add cutloop_ds to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from api.routes.material_routes import router as material_router
from api.routes.vision_routes import router as vision_router
from api.routes.analytics_routes import router as analytics_router

START_TIME = time.time()

app = FastAPI(
    title="CUTLOOP Circular Textile AI & ML Service",
    description="Intelligent Data Science service powering fabric classification, fiber composition analysis, circularity index estimation, and secondary textile pricing.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for CUTLOOP frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(material_router)
app.include_router(vision_router)
app.include_router(analytics_router)

# Mount Visualizations as static files so frontend can display them directly
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
if os.path.exists(VIZ_DIR):
    app.mount("/visualizations", StaticFiles(directory=VIZ_DIR), name="visualizations")

@app.get("/health")
def health_check():
    """Returns real-time health, uptime, and loaded model availability."""
    uptime_sec = round(time.time() - START_TIME, 1)
    saved_dir = os.path.join(BASE_DIR, "saved_models")
    return {
        "status": "healthy",
        "service": "CUTLOOP AI & Data Science Microservice",
        "uptime_seconds": uptime_sec,
        "models_available": {
            "model_a_random_forest": os.path.exists(os.path.join(saved_dir, "model_a_random_forest.joblib")),
            "model_b_texsort_vision": os.path.exists(os.path.join(saved_dir, "texsort_model.pt")),
            "model_c_material_kmeans": os.path.exists(os.path.join(saved_dir, "model_c_kmeans.joblib")),
            "model_d_pricing_engine": True
        }
    }

@app.get("/models")
def list_models():
    """Returns detailed technical specification of all 4 deployed models."""
    return {
        "models": [
            {
                "id": "model_a",
                "name": "Dominant Fiber & Circularity Classifier",
                "algorithm": "Random Forest (100 Estimators, Class Balanced)",
                "input": "Product title, catalog description text, brand, region, gender section, parent category",
                "output": "Dominant fiber class (Cotton, Polyester, Polyamide, Viscose, Wool, Linen, etc.)",
                "accuracy": "88.15% (Held-Out Test Set, Zero Target Leakage)",
                "capability": "Text-based NLP fiber entity extraction and catalog categorization from marketing text. Does NOT infer fiber from physical fabric.",
                "status": "active"
            },
            {
                "id": "model_b",
                "name": "TexSortML Garment Vision Category Classifier",
                "algorithm": "MobileNetV2 Transfer Learning (PyTorch)",
                "input": "224x224 RGB image",
                "output": "11 garment apparel categories (poloshirt, sweatshirt, short, jacket, shirt, tshirt, dress, trouser, jeans, top, jacket-zipper)",
                "accuracy": "86.39% (Held-Out Test Set)",
                "capability": "Macro garment apparel silhouette sorting. Does NOT perform fiber identification or fabric blend detection from RGB images.",
                "status": "active"
            },
            {
                "id": "model_c",
                "name": "Material Archetype & Recycling Pathway Clusterer",
                "algorithm": "K-Means (k=5 Clusters, Peak Silhouette: 0.6686)",
                "input": "10-dimensional continuous fiber composition percentage vector",
                "output": "Industrial recycling archetype & preliminary theoretical pathway",
                "capability": "Unsupervised grouping in 10D fiber space. Suggested recycling pathways are preliminary theoretical recommendations requiring mill validation.",
                "status": "active"
            },
            {
                "id": "model_d",
                "name": "Secondary Textile Waste Valuation Engine",
                "algorithm": "Industrial Heuristic Valuation Engine (Virgin Parity Multiplier Model)",
                "input": "Fiber percentages, lot weight (kg), quality grade, defect severity",
                "output": "Heuristic benchmark price ($/kg), lot valuation, heuristic liquidity score (0-100), estimated days to clear",
                "classification": "Heuristic Estimation Engine (Not trained on transaction history)",
                "disclaimer": "Valuation is a heuristic estimate based on published virgin spot commodity benchmarks and scrap grade multipliers. No historical transaction dataset exists in the fast-fashion dataset; this is NOT a trained empirical regression model.",
                "status": "active"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=False)
