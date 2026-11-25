"""
CUTLOOP Data Science Module — Automated Unit & Integration Tests
Author: CUTLOOP Data Science Team
Script: tests/test_api.py

Tests all model endpoints and schemas directly:
- health_check()
- list_models()
- predict_material()
- analyze_composition()
- estimate_price()
- get_summary()
- get_materials_analytics()
- get_category_analytics()
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from api.main import health_check, list_models
from api.routes.material_routes import predict_material, analyze_composition, estimate_price
from api.routes.analytics_routes import get_summary, get_materials_analytics, get_category_analytics
from api.schemas.payloads import (
    MaterialPredictRequest, CompositionAnalysisRequest, PricingEstimateRequest
)

class TestCutloopAPI(unittest.TestCase):
    def test_01_health_check(self):
        res = health_check()
        self.assertEqual(res["status"], "healthy")
        self.assertIn("model_a_random_forest", res["models_available"])
        print("[PASS] health_check():", res["status"])
        
    def test_02_list_models(self):
        res = list_models()
        self.assertEqual(len(res["models"]), 4)
        for m in res["models"]:
            print(f"       Model: {m['id']} -> {m['name']} ({m['status']})")
        print("[PASS] list_models(): 4 models registered.")
        
    def test_03_predict_material(self):
        req = MaterialPredictRequest(
            product_name="Slim Fit Washed Cotton Denim Jacket",
            description="Classic rigid cotton twill jacket with chest flap pockets and metal button fasteners.",
            brand="H&M",
            region="UK",
            gender_section="Men",
            parent_category="Jacket"
        )
        res = predict_material(req)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.predicted_dominant_fiber, "cotton")
        self.assertGreater(res.confidence, 0.50)
        print(f"[PASS] predict_material(): {res.predicted_dominant_fiber} (Confidence: {res.confidence*100:.1f}%)")
        print(f"       Recommendation: {res.recycling_recommendation}")
        
    def test_04_analyze_composition(self):
        req = CompositionAnalysisRequest(
            fiber_percentages={"cotton": 95.0, "elastane": 5.0}
        )
        res = analyze_composition(req)
        self.assertEqual(res.status, "success")
        self.assertIn("Cotton", res.archetype_name)
        print(f"[PASS] analyze_composition(): {res.archetype_name} (Circularity Score: {res.circularity_score}/100)")
        print(f"       Pathway: {res.recycling_pathway}")
        
    def test_05_estimate_price(self):
        req = PricingEstimateRequest(
            fiber_percentages={"cotton": 100.0},
            grade="grade_b_remnants",
            weight_kg=85.0,
            has_defects=False
        )
        res = estimate_price(req)
        self.assertEqual(res.status, "success")
        self.assertGreater(res.estimated_price_per_kg_usd, 0.5)
        self.assertGreater(res.estimated_lot_total_usd, 10.0)
        print(f"[PASS] estimate_price(): ${res.estimated_price_per_kg_usd}/kg | Total: ${res.estimated_lot_total_usd}")
        print(f"       Liquidity: {res.demand_liquidity_score}/100 ({res.demand_category}, {res.expected_days_to_sell})")
        
    def test_06_analytics_endpoints(self):
        summary = get_summary()
        self.assertGreaterEqual(summary["total_garments"], 40000)
        mats = get_materials_analytics()
        self.assertIn("cotton", mats["dominant_fibers"])
        cats = get_category_analytics()
        self.assertIn("inventory_categories", cats)
        print(f"[PASS] analytics: {summary['total_garments']} garments, {summary['total_benchmark_images']} images")

if __name__ == "__main__":
    unittest.main()
