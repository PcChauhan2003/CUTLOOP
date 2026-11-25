"""
CUTLOOP Data Science API — TexSortML Vision Routes
Author: CUTLOOP Data Science Team
Script: api/routes/vision_routes.py
"""

import os
import sys
import io
import time
import json
import numpy as np
from typing import Optional
from PIL import Image

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from fastapi import APIRouter, File, UploadFile, HTTPException, Form

from api.schemas.payloads import VisionPredictionResponse

router = APIRouter(prefix="", tags=["Computer Vision & Garment Sorting"])

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")

_vision_model = None
_categories = None
_transform = None

def get_vision_model():
    global _vision_model, _categories, _transform
    if _vision_model is None:
        classes_path = os.path.join(SAVED_MODELS_DIR, "texsort_classes.json")
        model_path = os.path.join(SAVED_MODELS_DIR, "texsort_model.pt")
        
        if os.path.exists(classes_path):
            with open(classes_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                _categories = data["categories"]
        else:
            _categories = [
                "dress", "jacket", "jacket-zipper", "jeans", "poloshirt",
                "shirt", "short", "sweatshirt", "top", "trouser", "tshirt"
            ]
            
        num_classes = len(_categories)
        model = models.mobilenet_v2(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(256, num_classes)
        )
        
        if os.path.exists(model_path):
            try:
                model.load_state_dict(torch.load(model_path, map_location="cpu"))
            except Exception as e:
                print(f"[!] Warning loading weights: {e}")
                
        model.eval()
        _vision_model = model
        
        _transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
    return _vision_model, _categories, _transform

@router.post("/predict/image", response_model=VisionPredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Model B: Classifies macro garment category / apparel silhouette type (TexSortML benchmark: 11 apparel classes).
    Note: Garment-category classification ONLY (e.g., tshirt, jacket, jeans). This model DOES NOT identify textile fiber composition or fabric blends from RGB images.
    """
    t0 = time.time()
    model, categories, transform = get_vision_model()
    
    try:
        contents = await file.read()
        if not contents or len(contents) == 0:
            raise ValueError("Uploaded file is empty")
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
    img_tensor = transform(pil_img).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)[0].numpy()
        
    top_indices = np.argsort(probs)[::-1][:3]
    top_3 = [
        {"category": categories[idx], "confidence": round(float(probs[idx]), 4)}
        for idx in top_indices
    ]
    
    best_cat = categories[top_indices[0]]
    best_conf = round(float(probs[top_indices[0]]), 4)
    proc_time = round((time.time() - t0) * 1000.0, 2)
    
    return VisionPredictionResponse(
        status="success",
        predicted_category=best_cat,
        confidence=best_conf,
        top_3_predictions=top_3,
        processing_time_ms=proc_time
    )
