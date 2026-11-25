"""
Verify Model B inference on an actual TexSortML image.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from api.routes.vision_routes import get_vision_model
from PIL import Image
import torch

model, categories, transform = get_vision_model()
print("Loaded categories:", categories)

# Find first test image
manifest_path = os.path.join(BASE_DIR, "datasets", "processed", "image_splits_manifest.csv")
import pandas as pd
df = pd.read_csv(manifest_path)
test_sample = df[df["split"] == "test"].iloc[0]
img_path = os.path.join(BASE_DIR, "datasets", "processed", "images", test_sample["category"], test_sample["filename"])
print(f"Testing image: {img_path} (True label: {test_sample['category']})")

img = Image.open(img_path).convert("RGB")
tensor = transform(img).unsqueeze(0)
with torch.no_grad():
    out = model(tensor)
    probs = torch.softmax(out, dim=1)[0].numpy()
    
top3_idx = probs.argsort()[::-1][:3]
for idx in top3_idx:
    print(f"  -> {categories[idx]}: {probs[idx]*100:.2f}%")
print("Vision inference test passed!")
