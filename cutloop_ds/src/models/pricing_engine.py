"""
CUTLOOP Data Science Module — Phase 5: Model D (Marketplace Waste Pricing & Demand Architecture)
Author: CUTLOOP Data Science Team
Script: src/models/pricing_engine.py

Mathematically grounded pricing and demand estimation engine for secondary industrial textile waste.
Addresses dataset reality: fast-fashion retail metadata lacks secondary B2B transaction spot prices.
Provides:
1. Virgin Parity Baseline & Circular Waste Discounting Model:
   - Spot price benchmarks (Cotton: $2.40/kg, Polyester: $1.35/kg, Wool: $9.50/kg, Polyamide: $2.80/kg, Viscose: $1.90/kg)
   - Quality / Grade multipliers (Deadstock rolls: 0.85, Fabric remnants: 0.55, Cutting table scraps: 0.30)
   - Mono-material circularity multiplier (Pure >=95%: +25%, Blends: -20%)
   - Volume discount / tier weighting
2. Demand Liquidity Score (0-100) based on circularity, material archetype, and grade
3. Formal Data Collection & Model Training Schema for real-world marketplace transaction feedback loops
"""

import os
import sys
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Benchmark virgin market spot prices in USD per kg (Industry average benchmarks)
VIRGIN_SPOT_PRICES_PER_KG = {
    "cotton": 2.40,
    "polyester": 1.35,
    "polyamide": 2.80,
    "viscose": 1.90,
    "wool": 9.50,
    "acrylic": 1.70,
    "linen": 4.50,
    "silk": 28.00,
    "lyocell": 2.60,
    "other": 1.20
}

GRADE_MULTIPLIERS = {
    "grade_a_deadstock": 0.85,    # Full unused rolls, pristine condition
    "grade_b_remnants": 0.55,     # Large cuttings, end of roll remnants (>1 meter)
    "grade_c_scraps": 0.30,       # Small cutting table clippings, post-industrial scrap
    "grade_d_shred": 0.15         # Mutilated shreds, unravelling waste
}

class TextilePricingEngine:
    def __init__(self):
        self.virgin_benchmarks = VIRGIN_SPOT_PRICES_PER_KG
        self.grade_multipliers = GRADE_MULTIPLIERS
        
    def estimate_price(
        self,
        fiber_percentages: dict,
        grade: str = "grade_b_remnants",
        weight_kg: float = 50.0,
        has_defects: bool = False,
        defect_severity: float = 0.0,
        is_recycled_origin: bool = False
    ) -> dict:
        """
        Calculates suggested marketplace price per kg and total lot valuation.
        """
        # 1. Base intrinsic fiber commodity value
        base_commodity_rate = 0.0
        total_pct = sum(fiber_percentages.values())
        if total_pct <= 0:
            total_pct = 100.0
            fiber_percentages = {"other": 100.0}
            
        for fiber, pct in fiber_percentages.items():
            f_norm = fiber.lower().strip()
            rate = self.virgin_benchmarks.get(f_norm, self.virgin_benchmarks["other"])
            base_commodity_rate += (pct / total_pct) * rate
            
        # 2. Grade Multiplier
        grade_norm = grade.lower().strip()
        grade_mult = self.grade_multipliers.get(grade_norm, 0.50)
        
        # 3. Circularity / Mono-material adjustment
        dom_pct = max(fiber_percentages.values())
        if dom_pct >= 95.0:
            circularity_mult = 1.25  # Premium for mono-material mechanical recycling
            recycling_readiness = "Excellent (Mono-material)"
        elif dom_pct >= 85.0:
            circularity_mult = 1.05
            recycling_readiness = "Good (Low-blend)"
        else:
            circularity_mult = 0.80  # Penalty for complex multi-fiber blend separation
            recycling_readiness = "Challenging (Intimate blend separation required)"
            
        # 4. Defect penalty
        defect_mult = max(0.40, 1.0 - (defect_severity * 0.50)) if has_defects else 1.0
        
        # 5. Volume scale adjustment (larger lots command industrial processing premiums)
        volume_mult = 1.0 + min(0.15, max(-0.10, np.log10(max(1.0, weight_kg) / 50.0) * 0.08))
        
        # Recycled origin bonus
        origin_mult = 1.10 if is_recycled_origin else 1.0
        
        # Final rate per kg
        unit_price = round(
            base_commodity_rate * grade_mult * circularity_mult * defect_mult * volume_mult * origin_mult, 
            2
        )
        total_valuation = round(unit_price * weight_kg, 2)
        
        # Demand Liquidity Index (0 - 100)
        # High demand for mono-cotton, pure polyester, and low defect rolls
        demand_score = round(min(100.0, max(15.0, (
            (circularity_mult / 1.25) * 40.0 + 
            (grade_mult / 0.85) * 35.0 + 
            (1.0 - (defect_severity if has_defects else 0.0)) * 25.0
        ))), 1)
        
        if demand_score >= 75:
            demand_category = "High Market Liquidity"
            expected_days_to_sell = "3 - 7 days"
        elif demand_score >= 50:
            demand_category = "Moderate Liquidity"
            expected_days_to_sell = "8 - 21 days"
        else:
            demand_category = "Low Liquidity / Specialty Buyer Required"
            expected_days_to_sell = "22 - 45 days"
            
        return {
            "estimated_price_per_kg_usd": unit_price,
            "estimated_lot_total_usd": total_valuation,
            "weight_kg": weight_kg,
            "grade": grade,
            "demand_liquidity_score": demand_score,
            "demand_category": demand_category,
            "expected_days_to_sell": expected_days_to_sell,
            "recycling_readiness": recycling_readiness,
            "factors": {
                "base_commodity_rate_usd": round(base_commodity_rate, 2),
                "grade_multiplier": grade_mult,
                "circularity_multiplier": circularity_mult,
                "defect_multiplier": round(defect_mult, 2),
                "volume_multiplier": round(volume_mult, 2)
            }
        }

def save_pricing_architecture():
    engine = TextilePricingEngine()
    
    # Example benchmark test
    sample_val = engine.estimate_price(
        fiber_percentages={"cotton": 98.0, "elastane": 2.0},
        grade="grade_b_remnants",
        weight_kg=120.0,
        has_defects=False
    )
    print("[*] Tested TextilePricingEngine on 120kg Cotton/Elastane Remnants:")
    print(json.dumps(sample_val, indent=2))
    
    # Transaction Schema definition for future machine learning
    transaction_schema = {
        "title": "CUTLOOP Marketplace Transaction Log Contract",
        "description": "Standardized schema for logging actual trades to continuously train gradient boosted pricing models",
        "fields": {
            "transaction_id": "string (UUID)",
            "timestamp": "ISO 8601 datetime",
            "seller_id": "string",
            "buyer_id": "string",
            "fiber_cotton_pct": "float (0-100)",
            "fiber_polyester_pct": "float (0-100)",
            "fiber_other_pct": "float (0-100)",
            "is_mono_material": "boolean",
            "material_archetype": "string (cluster_0 through cluster_4)",
            "grade": "enum [grade_a_deadstock, grade_b_remnants, grade_c_scraps, grade_d_shred]",
            "weight_kg": "float",
            "defect_count": "integer",
            "cleared_price_per_kg_usd": "float (target)",
            "initial_ask_price_per_kg_usd": "float",
            "time_to_clear_hours": "float",
            "bid_count": "integer"
        }
    }
    
    with open(os.path.join(SAVED_MODELS_DIR, "pricing_transaction_schema.json"), "w", encoding="utf-8") as f:
        json.dump(transaction_schema, f, indent=2)
        
    with open(os.path.join(REPORTS_DIR, "pricing_engine_spec.json"), "w", encoding="utf-8") as f:
        json.dump({"sample_valuation": sample_val, "schema": transaction_schema}, f, indent=2)
        
    print("[*] Pricing architecture and transaction schema saved.")

if __name__ == "__main__":
    save_pricing_architecture()
