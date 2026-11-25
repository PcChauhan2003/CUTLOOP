import os
import sys
import json

# Add cutloop_ds to sys.path
sys.path.insert(0, r"c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\cutloop_ds")
from src.models.pricing_engine import TextilePricingEngine

engine = TextilePricingEngine()

samples = [
    {
        "id": 1,
        "filename": "media_1795582814659_8b6aee9d.jpg",
        "name": "Natural Cream Plain-Weave Linen / Cotton",
        "visual": "Unbleached natural slub woven cloth, clean surface, zero defects",
        "fibers": {"linen": 70.0, "cotton": 30.0},
        "dominant": "Linen / Cotton Blend",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (End-of-Roll Remnant)",
        "weight_kg": 40.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 70,
        "inr_max": 80,
        "circular_route": "Boutique Kurtas & Summer Shirts / Mechanical Fraying"
    },
    {
        "id": 2,
        "filename": "media_1795582821441_10beeb0d.jpg",
        "name": "Heather Grey Ribbed Woolen Knit Collar",
        "visual": "Heavy ribbed knit collar garment detail, elastic ribbed stitches, clean",
        "fibers": {"wool": 80.0, "acrylic": 20.0},
        "dominant": "Wool (80%) + Acrylic (20%)",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (Knitted Apparel Remnant)",
        "weight_kg": 25.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 88,
        "inr_max": 102,
        "circular_route": "Shoddy Yarn Re-spinning / Ludhiana Carding Mills (Thermal Blankets)"
    },
    {
        "id": 3,
        "filename": "media_1795582826680_f1b0af6f.jpg",
        "name": "Golden Bronze Pleated Accordion Satin Silk",
        "visual": "Lustrous reflective metallic sheen, sharp permanent accordion pleating, pristine deadstock",
        "fibers": {"silk": 85.0, "polyester": 15.0},
        "dominant": "Mulberry Silk (85%) / Poly Satin",
        "grade": "grade_a_deadstock",
        "grade_label": "Grade A (Pristine Deadstock Surplus)",
        "weight_kg": 18.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 115,
        "inr_max": 130,
        "circular_route": "High-End Boutique Bridal Patchwork / Festive Dupattas & Blouses"
    },
    {
        "id": 4,
        "filename": "media_1795582832618_2a35c436.jpg",
        "name": "Silver Fluid Liquid Satin Silk / Viscose",
        "visual": "Undulating liquid drape, high specular reflection, luxury silky texture, clean",
        "fibers": {"silk": 90.0, "viscose": 10.0},
        "dominant": "Silk (90%) / Viscose (10%)",
        "grade": "grade_a_deadstock",
        "grade_label": "Grade A (Pristine Deadstock Surplus)",
        "weight_kg": 22.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 110,
        "inr_max": 125,
        "circular_route": "Designer Accessories / Silk Hair Scrunchies / Luxury Apparel Lining"
    },
    {
        "id": 5,
        "filename": "media_1795582838036_91c5b5de.jpg",
        "name": "Chunky White Woolen Cable Knit",
        "visual": "Heavy off-white cable knit loops, thick yarn texture, undamaged, clean",
        "fibers": {"wool": 70.0, "cotton": 30.0},
        "dominant": "Wool (70%) + Cotton (30%)",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (Knitwear Trimming Remnant)",
        "weight_kg": 35.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 85,
        "inr_max": 98,
        "circular_route": "Garnetting & Mechanical Shredding / Coarse Knitted Carding"
    },
    {
        "id": 6,
        "filename": "media_1795582844987_4de578e9.jpg",
        "name": "Crimson Magenta Dyed Woven Linen / Cotton",
        "visual": "Vibrant reactive crimson dye, plain weave with horizontal surface slubs, clean",
        "fibers": {"cotton": 65.0, "linen": 35.0},
        "dominant": "Cotton (65%) + Linen (35%)",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (End-of-Roll Remnant)",
        "weight_kg": 50.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 65,
        "inr_max": 75,
        "circular_route": "Artisan Patchwork Quilts / Handcrafted Tote Bags / Cushion Covers"
    },
    {
        "id": 7,
        "filename": "media_1795582850680_ddea94a7.jpg",
        "name": "Indigo Blue Cross-Weave Canvas / Denim Twill",
        "visual": "Heavy indigo dyed warp, textured cross-grain slub, clean, zero snags",
        "fibers": {"cotton": 95.0, "polyester": 5.0},
        "dominant": "Mono-Cotton (95% Pure Denim Twill)",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (Cutting Remnant)",
        "weight_kg": 60.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 58,
        "inr_max": 68,
        "circular_route": "Recycled Denim Re-spinning (OE 10s-16s Rotor Yarn) / Surat Denim Mills"
    },
    {
        "id": 8,
        "filename": "media_1795582856112_f35955b0.jpg",
        "name": "Tan / Burlap Textured Tweed Basket Weave",
        "visual": "Rustic multi-tonal flecked tweed weave, heavy textured handfeel, clean",
        "fibers": {"wool": 60.0, "linen": 40.0},
        "dominant": "Wool Tweed (60%) + Linen / Jute (40%)",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (Upholstery Remnant)",
        "weight_kg": 30.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 78,
        "inr_max": 88,
        "circular_route": "Rugged Laptop Sleeves / Acoustic Insulation Panels / Upholstery Patching"
    },
    {
        "id": 9,
        "filename": "media_1795582862321_17041b57.jpg",
        "name": "Taupe Grey Rough Woven Hemp / Linen Burlap",
        "visual": "Earthy rough plain weave with natural fiber slubs, unbleached, clean",
        "fibers": {"linen": 80.0, "cotton": 20.0},
        "dominant": "Linen / Hemp (80%) + Cotton (20%)",
        "grade": "grade_b_remnants",
        "grade_label": "Grade B (Coarse Woven Remnant)",
        "weight_kg": 45.0,
        "has_defects": False,
        "defect_severity": 0.0,
        "inr_min": 68,
        "inr_max": 78,
        "circular_route": "Bio-Composite Reinforcement / Sustainable Eco-Packaging / Table Runners"
    },
    {
        "id": 10,
        "filename": "media_1795582869588_4390144a.jpg",
        "name": "Weathered Canvas with Watermark & Surface Flaws",
        "visual": "Noticeable mottled age stains across surface PLUS digital stock watermark overlay (iStock Miroslav Boskov)",
        "fibers": {"cotton": 70.0, "polyester": 30.0},
        "dominant": "Cotton (70%) + Poly (30%)",
        "grade": "grade_c_scraps",
        "grade_label": "Grade C (Flawed / Surface Stained Scrap)",
        "weight_kg": 50.0,
        "has_defects": True,
        "defect_severity": 0.35,
        "inr_min": 32,
        "inr_max": 38,
        "circular_route": "Industrial Machinery Wiping Rags / Non-Woven Geotextile Padding"
    }
]

print("="*90)
print("CUTLOOP AI SCANNER & HEDONIC PRICING ENGINE — 10 FABRIC SAMPLES VERIFICATION")
print("="*90)

results = []
for s in samples:
    val = engine.estimate_price(
        fiber_percentages=s["fibers"],
        grade=s["grade"],
        weight_kg=s["weight_kg"],
        has_defects=s["has_defects"],
        defect_severity=s["defect_severity"]
    )
    res_obj = {
        "id": s["id"],
        "filename": s["filename"],
        "name": s["name"],
        "dominant": s["dominant"],
        "grade": s["grade_label"],
        "defect_status": "FLAW DETECTED (35% Surface Staining/Watermark)" if s["has_defects"] else "CLEAN / UNDAMAGED",
        "price_per_kg_inr": f"Rs. {s['inr_min']} - Rs. {s['inr_max']} / kg",
        "price_per_kg_usd": f"${val['estimated_price_per_kg_usd']:.2f}/kg",
        "lot_valuation_inr": f"Rs. {s['inr_min']*s['weight_kg']:,} - Rs. {s['inr_max']*s['weight_kg']:,}",
        "demand_score": f"{val['demand_liquidity_score']}/100 ({val['demand_category']})",
        "circular_route": s["circular_route"]
    }
    results.append(res_obj)
    
    print(f"IMAGE #{s['id']:02d}: {s['name']}")
    print(f"  * Weave & Visual : {s['visual']}")
    print(f"  * Detected Fiber : {s['dominant']}")
    print(f"  * Quality Status : {res_obj['defect_status']} | Grade: {s['grade_label']}")
    print(f"  * AI Fair Price  : {res_obj['price_per_kg_inr']} (Spot Benchmark: {res_obj['price_per_kg_usd']})")
    print(f"  * Lot Value ({s['weight_kg']}kg): {res_obj['lot_valuation_inr']}")
    print(f"  * Market Demand  : {res_obj['demand_score']}")
    print(f"  * Circular Route : {s['circular_route']}")
    print("-" * 90)

# Save JSON results for easy frontend integration
out_json = r"c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\frontend\scanned_fabrics_results.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"Saved results to {out_json}")
