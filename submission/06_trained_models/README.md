# CUTLOOP — Trained Machine Learning & Deep Learning Models Submission Package

**Academic Course:** 3rd Year B.Tech CSE (Semester 5 Integrated Capstone)  
**Track:** Data Science (15 Marks) & Deep Learning (20 Marks)  
**Verification Script:** Run `python verify_submission_models.py` to inspect and test all models with sample inference.

---

## 1. Directory Inventory & Model Checkpoints

This folder contains all trained and evaluated models, weights, schemas, and pipelines for the CUTLOOP platform:

| File Name | Framework | Size | Model Function & Role | Test Benchmark Metric |
| :--- | :--- | :---: | :--- | :--- |
| **`model_a_random_forest.joblib`** | Scikit-Learn | 35.4 MB | **Model A Champion:** Balanced Random Forest classifier (100 trees) predicting dominant fiber from marketing text & metadata | **88.15% Test Accuracy**<br>**0.8257 Macro F1** |
| **`model_a_decision_tree.joblib`** | Scikit-Learn | 138 KB | **Model A Baseline:** CART Decision Tree (`max_depth=15`) used to evaluate ensemble performance delta | 78.09% Test Accuracy<br>0.7036 Macro F1 |
| **`feature_pipeline.joblib`** | Scikit-Learn | 18 KB | TF-IDF n-gram vectorizer (400 features) + One-Hot categorical encoders with zero target leakage | Leak-free transformations |
| **`texsort_model.pt`** | PyTorch | 10.4 MB | **Model B Champion:** MobileNetV2 Transfer Learning classifier fine-tuned on TexSortML industrial benchmark | **86.39% Test Accuracy**<br>**0.8015 Macro F1** |
| **`custom_cnn_model.pt`** | PyTorch | 2.03 MB | **Model B Baseline:** Custom 4-block deep CNN built from scratch to scientifically quantify transfer learning premium | 72.19% Test Accuracy<br>0.6503 Macro F1 |
| **`texsort_classes.json`** | JSON | 644 B | Standardized 11 TexSortML apparel classes (`dress`, `jacket`, `jeans`, `shirt`, etc.) | 11 categories |
| **`model_c_kmeans.joblib`** | Scikit-Learn | 191 KB | **Model C:** Unsupervised K-Means clustering algorithm partitioning 10D blend vectors into circular streams | **Global Peak Silhouette = 0.6686 ($k=5$)** |
| **`archetype_profiles.json`** | JSON | 2.0 KB | Profiles, composition distributions, and recommended recycling pathways for the 5 archetypes | 5 recycling streams |
| **`pricing_transaction_schema.json`**| JSON | 882 B | Input/output schema for Model D's MCX-calibrated hedonic clearing price engine | Commodity base: ₹62.50/kg |
| **`verify_submission_models.py`** | Python | ~5 KB | Automated verification script that loads each model and runs test sample forward pass | 100% verified on CPU |

---

## 2. Quick-Start Model Verification

You can verify all models with a single command from your terminal:

```bash
# Activate your python environment and run:
python verify_submission_models.py
```

### Expected Output:
```text
===========================================================================
     CUTLOOP: TRAINED MODEL VERIFICATION & INFERENCE SUITE
===========================================================================
Model Directory: .../submission/06_trained_models

[1/4] Testing Model A (NLP Dominant Fiber Classifier)...
  ✓ Random Forest Model Loaded Successfully (33.75 MB)
  ✓ Sample Input: '100% pure organic cotton crewneck casual t-shirt'
  ✓ Model A Predicted Fiber: 'cotton' (Confidence: 72.1%)
  ✓ Benchmark Test Accuracy: 88.15% (Baseline Decision Tree: 78.09%, +10.06% gain)

[2/4] Testing Model C (Unsupervised Material Archetype Clusterer)...
  ✓ K-Means Model Loaded Successfully (186.7 KB)
  ✓ Sample 10D Fiber Vector: 95% Cotton, 5% Elastane
  ✓ Assigned Cluster: Cluster 1 (Cotton Dominant)
  ✓ Recommended Recycling: Mechanical Garnetting
  ✓ Optimal Clustering Metric: Peak Global Silhouette = 0.6686 (k=5)

[3/4] Testing Model B Champion (MobileNetV2 Transfer Learning)...
  ✓ MobileNetV2 Weights Loaded (9.98 MB)
  ✓ Target Classes (11): dress, jacket, jacket-zipper, jeans, poloshirt, shirt, short, sweatshirt, top, trouser, tshirt
  ✓ Dummy Image Tensor (1, 3, 224, 224) Forward Pass: Success
  ✓ Top Output: Class 'shirt'
  ✓ Held-Out Test Accuracy: 86.39% | Macro F1: 0.8015

[4/4] Testing Model B Baseline (Custom 4-Block CNN From Scratch)...
  ✓ Custom CNN Weights Loaded (1.94 MB)
  ✓ Checkpoint Metadata: Epoch 5 | Val Acc: 73.96% | Val F1: 0.6953
  ✓ Held-Out Test Accuracy: 72.19% | Macro F1: 0.6503
  ✓ Transfer Learning Premium Proven: MobileNetV2 achieves +14.20% over Custom CNN
===========================================================================
     ALL 4 MODELS & BASELINES VERIFIED SUCCESSFULLY!
===========================================================================
```

---

## 3. How to Load and Run Inference (Code Snippets)

### A. Load Model A (Dominant Fiber Classifier)
```python
import joblib, numpy as np, pandas as pd
from scipy.sparse import hstack

rf_model = joblib.load("model_a_random_forest.joblib")
pipe = joblib.load("feature_pipeline.joblib")

text = "Men's slim fit organic cotton crewneck t-shirt"
X_text = pipe["tfidf"].transform([text.lower()])
X_cat = pipe["ohe"].transform(pd.DataFrame([{"brand": "H&M", "region": "UK", "gender_section": "Men", "parent_category": "Tops"}]))
X_input = hstack([X_text, X_cat]).tocsr()

probs = rf_model.predict_proba(X_input)[0]
predicted_fiber = pipe["target_classes"][int(np.argmax(probs))]
print("Predicted Fiber:", predicted_fiber)
```

### B. Load Model B (MobileNetV2 Vision Classifier)
```python
import torch, torchvision.models as models, torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms

num_classes = 11
model = models.mobilenet_v2(weights=None)
in_features = model.classifier[1].in_features
model.classifier = nn.Sequential(
    nn.Dropout(p=0.2),
    nn.Linear(in_features, 256),
    nn.ReLU(inplace=True),
    nn.Dropout(p=0.2),
    nn.Linear(256, num_classes)
)
model.load_state_dict(torch.load("texsort_model.pt", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
# img_tensor = transform(Image.open("fabric.jpg")).unsqueeze(0)
# output = model(img_tensor)
```

### C. Load Model C (K-Means Recycling Archetype Clusterer)
```python
import joblib, json

kmeans = joblib.load("model_c_kmeans.joblib")
with open("archetype_profiles.json", "r") as f:
    profiles = json.load(f)

# Input 10D percentages: [cotton, poly, elastane, nylon, viscose, wool, acrylic, linen, silk, other]
blend_10d = [[90.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
cluster_id = kmeans.predict(blend_10d)[0]
print("Assigned Archetype:", profiles[str(cluster_id)]["name"])
print("Recommended Pathway:", profiles[str(cluster_id)]["pathway"])
```

---

## 4. Academic Integrity & Dataset Splits
All models were trained, validated, and evaluated on static, non-overlapping held-out splits to guarantee reproducible scientific integrity:
- **Fast-Fashion Inventory ($N=47,522$):** Stratified 80% Train ($N=38,017$), 20% Held-Out Test ($N=9,505$) with zero target leakage.
- **TexSortML Benchmark ($N=2,252$):** Stratified 70% Train ($N=1,576$), 15% Validation ($N=338$), 15% Held-Out Test ($N=338$) in `cutloop_ds/datasets/processed/image_splits_manifest.csv`.
