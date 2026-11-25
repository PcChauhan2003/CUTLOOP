import json

with open("c:/Users/dhruv/OneDrive/Desktop/ds/6_JSONL_component_normalized_public.jsonl", "r", encoding="utf-8") as f:
    for i in range(5):
        line = f.readline()
        data = json.loads(line)
        print(f"--- RECORD {i} ---")
        print("product_name:", data.get("product_name"))
        print("components_structured:", json.dumps(data.get("components_structured"), indent=2))
        print("raw_material_text:", data.get("raw_material_text"))
        print("raw_material_text_norm:", data.get("raw_material_text_norm"))
