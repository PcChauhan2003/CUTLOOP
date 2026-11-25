"""
CUTLOOP Data Science Module — Phase 5: Model B (TexSortML Deep Learning Vision Classifier)
Author: CUTLOOP Data Science Team
Script: src/models/train_model_b.py

Trains a deep convolutional neural network for 11 garment categories on TexSortML:
- Categories: poloshirt, sweatshirt, short, jacket, shirt, tshirt, dress, trouser, jeans, top, jacket-zipper
- Stratified Splits: 1,576 Train (70%), 338 Val (15%), 338 Test (15%)
- Architecture: MobileNetV2 / Depthwise-Separable Residual ConvNet (lightweight, <15MB, fast inference)
- Augmentations: RandomResizedCrop, RandomHorizontalFlip, ColorJitter, Normalization
- Loss: Class-weighted CrossEntropyLoss
- Optimizer: AdamW + Cosine Annealing
- Evaluates on unseen Test split: Accuracy, F1-macro, F1-weighted, Confusion Matrix
- Saves:
  - saved_models/texsort_model.pt
  - saved_models/texsort_classes.json
  - visualizations/model_b_confusion_matrix.png
  - visualizations/model_b_training_curves.png
  - reports/model_b_metrics.json
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torchvision.models as models

from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
IMAGES_DIR = os.path.join(PROCESSED_DIR, "images")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

CATEGORIES = sorted([
    "poloshirt", "sweatshirt", "short", "jacket", "shirt", 
    "tshirt", "dress", "trouser", "jeans", "top", "jacket-zipper"
])
CAT_TO_IDX = {cat: idx for idx, cat in enumerate(CATEGORIES)}
IDX_TO_CAT = {idx: cat for cat, idx in CAT_TO_IDX.items()}

class TexSortDataset(Dataset):
    def __init__(self, df: pd.DataFrame, base_images_dir: str, transform=None):
        self.df = df.reset_index(drop=True)
        self.base_images_dir = base_images_dir
        self.transform = transform
        
    def __len__(self):
        return len(self.df)
        
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(self.base_images_dir, row["category"], row["filename"])
        
        # Load image RGB
        try:
            image = Image.open(img_path).convert("RGB")
        except Exception:
            # Fallback blank
            image = Image.new("RGB", (224, 224), color=(128, 128, 128))
            
        label = CAT_TO_IDX[row["category"]]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize((240, 240)),
        transforms.RandomResizedCrop(224, scale=(0.85, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_test_transform

def build_model(num_classes=11):
    """Builds MobileNetV2 with transfer learning or custom depthwise separable blocks."""
    print("[*] Instantiating MobileNetV2 vision architecture...")
    try:
        model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        # Freeze initial feature extractor for rapid adaptation
        for param in model.features[:10].parameters():
            param.requires_grad = False
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(256, num_classes)
        )
    except Exception as e:
        print(f"    Notice: Using local initialized MobileNetV2 ({e})")
        model = models.mobilenet_v2(weights=None, num_classes=num_classes)
        
    return model

def train_model_b(epochs=6, batch_size=32, lr=1e-3):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training Model B on device: {device}")
    
    # Load manifest
    manifest_path = os.path.join(PROCESSED_DIR, "image_splits_manifest.csv")
    df = pd.read_csv(manifest_path)
    
    train_df = df[df["split"] == "train"]
    val_df = df[df["split"] == "val"]
    test_df = df[df["split"] == "test"]
    
    print(f"    Splits -> Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    # Compute class weights for imbalanced classes
    cat_counts = train_df["category"].value_counts()
    class_weights = []
    for cat in CATEGORIES:
        class_weights.append(1.0 / (cat_counts.get(cat, 1.0) ** 0.5))
    class_weights = torch.tensor(class_weights, dtype=torch.float).to(device)
    class_weights = class_weights / class_weights.sum() * len(CATEGORIES)
    
    train_transform, val_transform = get_transforms()
    
    train_dataset = TexSortDataset(train_df, IMAGES_DIR, transform=train_transform)
    val_dataset = TexSortDataset(val_df, IMAGES_DIR, transform=val_transform)
    test_dataset = TexSortDataset(test_df, IMAGES_DIR, transform=val_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    model = build_model(num_classes=len(CATEGORIES)).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    best_val_acc = 0.0
    best_model_path = os.path.join(SAVED_MODELS_DIR, "texsort_model.pt")
    
    print("[*] Starting training loop...")
    for epoch in range(1, epochs + 1):
        t0 = time.time()
        # Train phase
        model.train()
        train_loss, train_correct = 0.0, 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * imgs.size(0)
            preds = outputs.argmax(dim=1)
            train_correct += (preds == labels).sum().item()
            
        scheduler.step()
        
        # Validation phase
        model.eval()
        val_loss, val_correct = 0.0, 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * imgs.size(0)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                
        epoch_tr_loss = train_loss / len(train_dataset)
        epoch_tr_acc = train_correct / len(train_dataset)
        epoch_val_loss = val_loss / len(val_dataset)
        epoch_val_acc = val_correct / len(val_dataset)
        
        history["train_loss"].append(round(epoch_tr_loss, 4))
        history["train_acc"].append(round(epoch_tr_acc, 4))
        history["val_loss"].append(round(epoch_val_loss, 4))
        history["val_acc"].append(round(epoch_val_acc, 4))
        
        elapsed = time.time() - t0
        print(f"    Epoch [{epoch}/{epochs}] ({elapsed:.1f}s) -> Train Loss: {epoch_tr_loss:.4f}, Acc: {epoch_tr_acc*100:.1f}% | Val Loss: {epoch_val_loss:.4f}, Acc: {epoch_val_acc*100:.1f}%")
        
        if epoch_val_acc >= best_val_acc:
            best_val_acc = epoch_val_acc
            torch.save(model.state_dict(), best_model_path)
            
    # Load best model for evaluation on held-out test split
    print(f"[*] Loading best model checkpoint (Val Acc: {best_val_acc*100:.1f}%) for test evaluation...")
    model.load_state_dict(torch.load(best_model_path))
    model.eval()
    
    all_preds, all_labels = [], []
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(device)
            outputs = model(imgs)
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.numpy())
            
    test_acc = accuracy_score(all_labels, all_preds)
    test_f1_macro = f1_score(all_labels, all_preds, average="macro")
    test_f1_weighted = f1_score(all_labels, all_preds, average="weighted")
    print(f"\n[*] Test Evaluation Results (Held-Out Split, N={len(test_df)}):")
    print(f"    Test Accuracy:    {test_acc*100:.2f}%")
    print(f"    Test F1 (Macro):   {test_f1_macro:.4f}")
    print(f"    Test F1 (Weighted): {test_f1_weighted:.4f}")
    
    cr = classification_report(all_labels, all_preds, target_names=CATEGORIES, output_dict=True)
    print("\n" + classification_report(all_labels, all_preds, target_names=CATEGORIES))
    
    # Save classes mapping
    with open(os.path.join(SAVED_MODELS_DIR, "texsort_classes.json"), "w", encoding="utf-8") as f:
        json.dump({"categories": CATEGORIES, "cat_to_idx": CAT_TO_IDX, "idx_to_cat": IDX_TO_CAT}, f, indent=2)
        
    # Plot Training Curves
    print("[*] Generating model_b_training_curves.png...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(range(1, epochs + 1), history["train_loss"], label="Train Loss", color="#1b4332", marker="o")
    axes[0].plot(range(1, epochs + 1), history["val_loss"], label="Val Loss", color="#d90429", marker="s")
    axes[0].set_title("Model B: Cross-Entropy Loss Curve", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    
    axes[1].plot(range(1, epochs + 1), [a*100 for a in history["train_acc"]], label="Train Acc", color="#1b4332", marker="o")
    axes[1].plot(range(1, epochs + 1), [a*100 for a in history["val_acc"]], label="Val Acc", color="#3a86ff", marker="s")
    axes[1].set_title("Model B: Accuracy Progression (%)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy (%)")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "model_b_training_curves.png"), dpi=200)
    plt.close()
    
    # Plot Confusion Matrix
    print("[*] Generating model_b_confusion_matrix.png...")
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=CATEGORIES, yticklabels=CATEGORIES)
    plt.title(f"Model B (TexSortML MobileNetV2) Test Confusion Matrix\nAccuracy: {test_acc*100:.2f}% | F1-Macro: {test_f1_macro:.3f}", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Predicted Garment Category", fontsize=10)
    plt.ylabel("Ground Truth Category", fontsize=10)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, "model_b_confusion_matrix.png"), dpi=200)
    plt.close()
    
    # Save Metrics JSON
    metrics = {
        "model_name": "Model B — TexSortML Vision Classifier",
        "architecture": "MobileNetV2 Transfer Learning",
        "input_resolution": "224x224 RGB",
        "num_classes": len(CATEGORIES),
        "test_accuracy": round(float(test_acc), 4),
        "test_f1_macro": round(float(test_f1_macro), 4),
        "test_f1_weighted": round(float(test_f1_weighted), 4),
        "history": history,
        "classification_report": cr
    }
    with open(os.path.join(REPORTS_DIR, "model_b_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"[*] Model B training and evaluation complete!")
    return metrics

if __name__ == "__main__":
    train_model_b(epochs=6, batch_size=32, lr=1e-3)
