"""
CUTLOOP Data Science API - Robustness, Error Handling & Edge Case Test Suite
Tests:
- GET /health
- GET /models
- POST /predict/material (valid, empty strings, missing fields, unseen categories)
- POST /analyze/composition (valid, zero values, extreme blends)
- POST /estimate/price (valid, edge quantities, invalid grades, defect penalties)
- POST /predict/image (valid image bytes, corrupted image bytes, empty bytes)
- GET /analytics/summary
- GET /analytics/materials
- GET /analytics/categories
"""

import os
import sys
import io
import json
import asyncio
import unittest
from PIL import Image
from fastapi import HTTPException
from fastapi.datastructures import UploadFile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from api.main import health_check, list_models
from api.routes.analytics_routes import get_summary, get_materials_analytics, get_category_analytics
from api.routes.material_routes import predict_material, analyze_composition, estimate_price
from api.routes.vision_routes import predict_image
from api.schemas.payloads import (
    MaterialPredictRequest, CompositionAnalysisRequest, PricingEstimateRequest
)

class TestAPIRobustnessAndEdgeCases(unittest.TestCase):
    
    def test_01_health_and_models(self):
        print("\n--- Testing /health and /models ---")
        health = health_check()
        self.assertEqual(health["status"], "healthy")
        self.assertIn("models_available", health)
        print("Health status:", health["status"])
        
        models_resp = list_models()
        self.assertEqual(len(models_resp["models"]), 4)
        print(f"Registered models: {len(models_resp['models'])}")

    def test_02_predict_material_edge_cases(self):
        print("\n--- Testing /predict/material Edge Cases ---")
        # 1. Standard valid request
        req1 = MaterialPredictRequest(
            product_name="Cotton Poplin Shirt",
            description="100% fine cotton fabric remnant",
            brand="H&M",
            region="UK",
            gender_section="Men",
            parent_category="Tops"
        )
        res1 = predict_material(req1)
        self.assertEqual(res1.status, "success")
        self.assertEqual(res1.predicted_dominant_fiber, "cotton")
        print("Valid cotton prediction:", res1.predicted_dominant_fiber, f"({res1.confidence*100:.1f}%)")

        # 2. Completely empty strings
        req2 = MaterialPredictRequest(
            product_name="",
            description="",
            brand="",
            region="",
            gender_section="",
            parent_category=""
        )
        res2 = predict_material(req2)
        self.assertEqual(res2.status, "success")
        self.assertIsNotNone(res2.predicted_dominant_fiber)
        print("Empty string fallback prediction:", res2.predicted_dominant_fiber, f"({res2.confidence*100:.1f}%)")

        # 3. Unseen brand and bizarre category
        req3 = MaterialPredictRequest(
            product_name="Xylo-synthetic Space Suit",
            description="Unknown polymer mesh lining with recycled fibers",
            brand="NonExistentBrand999",
            region="Antarctica",
            gender_section="Cyber",
            parent_category="AlienWear"
        )
        res3 = predict_material(req3)
        self.assertEqual(res3.status, "success")
        print("Unseen metadata handled gracefully:", res3.predicted_dominant_fiber)

    def test_03_analyze_composition_edge_cases(self):
        print("\n--- Testing /analyze/composition Edge Cases ---")
        # 1. Multi-blend
        req1 = CompositionAnalysisRequest(
            fiber_percentages={"cotton": 60.0, "polyester": 35.0, "elastane": 5.0}
        )
        res1 = analyze_composition(req1)
        self.assertEqual(res1.status, "success")
        self.assertIsNotNone(res1.archetype_name)
        print("Multi-blend cluster:", res1.archetype_name)

        # 2. Zero values
        req2 = CompositionAnalysisRequest(
            fiber_percentages={"cotton": 0.0, "polyester": 0.0}
        )
        res2 = analyze_composition(req2)
        self.assertEqual(res2.status, "success")
        print("Zero composition handled:", res2.dominant_fiber)

        # 3. Rare fibers
        req3 = CompositionAnalysisRequest(
            fiber_percentages={"silk": 90.0, "viscose": 10.0}
        )
        res3 = analyze_composition(req3)
        self.assertEqual(res3.status, "success")
        print("Silk/Viscose blend handled:", res3.archetype_name)

    def test_04_estimate_price_edge_cases(self):
        print("\n--- Testing /estimate/price Edge Cases ---")
        # 1. Standard calculation
        req1 = PricingEstimateRequest(
            fiber_percentages={"cotton": 100.0},
            grade="grade_a_deadstock",
            weight_kg=100.0,
            has_defects=False,
            defect_severity=0.0
        )
        res1 = estimate_price(req1)
        self.assertEqual(res1.status, "success")
        self.assertGreater(res1.estimated_price_per_kg_usd, 0)
        self.assertGreater(res1.demand_liquidity_score, 0)
        print(f"Grade A Cotton lot price: ${res1.estimated_price_per_kg_usd}/kg (Total: ${res1.estimated_lot_total_usd})")

        # 2. Heavy defects
        req2 = PricingEstimateRequest(
            fiber_percentages={"cotton": 100.0},
            grade="grade_d_shred",
            weight_kg=10.0,
            has_defects=True,
            defect_severity=0.9
        )
        res2 = estimate_price(req2)
        self.assertLess(res2.estimated_price_per_kg_usd, res1.estimated_price_per_kg_usd)
        print(f"Severely defective shred price: ${res2.estimated_price_per_kg_usd}/kg (Liquidity: {res2.demand_liquidity_score})")

        # 3. Invalid grade fallback
        req3 = PricingEstimateRequest(
            fiber_percentages={"polyester": 100.0},
            grade="non_standard_grade",
            weight_kg=5.0
        )
        res3 = estimate_price(req3)
        self.assertEqual(res3.status, "success")
        print("Fallback grade handled successfully:", res3.estimated_price_per_kg_usd)

    def test_05_predict_image_edge_cases(self):
        print("\n--- Testing /predict/image Edge Cases ---")
        # 1. Valid image
        img = Image.new("RGB", (224, 224), color=(128, 50, 70))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)
        
        valid_upload = UploadFile(
            filename="test_swatch.jpg",
            file=img_bytes,
            headers={"content-type": "image/jpeg"}
        )
        res1 = asyncio.run(predict_image(valid_upload))
        self.assertEqual(res1.status, "success")
        self.assertIn(res1.predicted_category, [
            "dress", "jacket", "jacket-zipper", "jeans", "poloshirt",
            "shirt", "short", "sweatshirt", "top", "trouser", "tshirt"
        ])
        print("Valid synthetic image classification:", res1.predicted_category, f"({res1.confidence*100:.1f}%)")

        # 2. Corrupted image bytes (should raise HTTPException 400)
        corrupted_bytes = io.BytesIO(b"NOT_A_VALID_IMAGE_DATA_CORRUPT_BYTES_XYZ123")
        corrupt_upload = UploadFile(
            filename="corrupt.jpg",
            file=corrupted_bytes,
            headers={"content-type": "image/jpeg"}
        )
        with self.assertRaises(HTTPException) as cm:
            asyncio.run(predict_image(corrupt_upload))
        self.assertEqual(cm.exception.status_code, 400)
        print("Corrupted image correctly rejected with HTTP 400:", cm.exception.detail)

        # 3. Empty file bytes
        empty_bytes = io.BytesIO(b"")
        empty_upload = UploadFile(
            filename="empty.jpg",
            file=empty_bytes,
            headers={"content-type": "image/jpeg"}
        )
        with self.assertRaises(HTTPException) as cm2:
            asyncio.run(predict_image(empty_upload))
        self.assertEqual(cm2.exception.status_code, 400)
        print("Empty file correctly rejected with HTTP 400:", cm2.exception.detail)

    def test_06_analytics_endpoints(self):
        print("\n--- Testing /analytics Endpoints ---")
        summary = get_summary()
        self.assertEqual(summary["total_garments"], 47522)
        print(f"Summary analytics verified: {summary['total_garments']} garments")

        materials = get_materials_analytics()
        self.assertIn("cotton", materials["dominant_fibers"])
        print("Materials analytics verified:", list(materials["dominant_fibers"].keys())[:4])

        cats = get_category_analytics()
        self.assertIn("inventory_categories", cats)
        print("Categories analytics verified:", list(cats["inventory_categories"].keys())[:4])

if __name__ == "__main__":
    unittest.main()
