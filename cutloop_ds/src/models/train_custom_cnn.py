"""
CUTLOOP Deep Learning Module — Component 2: Custom CNN Garment Classifier
Trains a genuine from-scratch Custom Lightweight Convolutional Neural Network
on the TexSortML dataset using the identical train/val/test splits as MobileNetV2.
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
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
PROCESSED_DIR = os.path.join(DATASETS_DIR, "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
MANIFEST_PATH = os.path.join(PROCESSED_DIR, "image_splits_manifest.csv")
CLASSES_PATH = os.path.join(SAVED_MODELS_DIR, "texsort_classes.json")
CUSTOM_MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "custom_cnn_model.pt")

torch.manual_seed(42)
np.random.seed(42)

# Load class index
with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_meta = json.load(f)
CATEGORIES = class_meta["categories"]
CLASS_TO_IDX = {c: i for i, c in enumerate(CATEGORIES)}
NUM_CLASSES = len(CATEGORIES)

# Dataset class
class TexSortDataset(Dataset):
    def __init__(self, df, transform=None):
        self.df = df.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(PROCESSED_DIR, row["relative_path"])
        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        label = CLASS_TO_IDX[row["category"]]
        return img, label

# 4-block Custom CNN Architecture
class CustomGarmentCNN(nn.Module):
    def __init__(self, num_classes=11):
        super(CustomGarmentCNN, self).__init__()
        self.features = nn.Sequential(
            # Block 1: 3 -> 32
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2), # 112x112
            
            # Block 2: 32 -> 64
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2), # 56x56
            
            # Block 3: 64 -> 128
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2), # 28x28
            
            # Block 4: 128 -> 128
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4)) # 4x4
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(p=0.4),
            nn.Linear(128 * 4 * 4, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        feat = self.features(x)
        out = self.classifier(feat)
        return out

def train_and_evaluate():
    print("==========================================================")
    print("=== Training Custom Lightweight CNN on TexSortML (CPU) ===")
    print("==========================================================")
    
    df_manifest = pd.read_csv(MANIFEST_PATH)
    train_df = df_manifest[df_manifest["split"] == "train"]
    val_df = df_manifest[df_manifest["split"] == "val"]
    test_df = df_manifest[df_manifest["split"] == "test"]
    
    print(f"Dataset Splits: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
    
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    train_loader = DataLoader(TexSortDataset(train_df, train_transform), batch_size=32, shuffle=True)
    val_loader = DataLoader(TexSortDataset(val_df, eval_transform), batch_size=32, shuffle=False)
    test_loader = DataLoader(TexSortDataset(test_df, eval_transform), batch_size=32, shuffle=False)
    
    device = torch.device("cpu")
    model = CustomGarmentCNN(num_classes=NUM_CLASSES).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    
    num_epochs = 5
    best_val_f1 = 0.0
    history = []
    
    t0 = time.time()
    for epoch in range(1, num_epochs + 1):
        # Training
        model.train()
        train_loss = 0.0
        train_correct = 0
        total_train = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * len(labels)
            preds = torch.argmax(outputs, dim=1)
            train_correct += (preds == labels).sum().item()
            total_train += len(labels)
            
        epoch_train_loss = train_loss / total_train
        epoch_train_acc = train_correct / total_train
        
        # Validation
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                preds = torch.argmax(outputs, dim=1)
                val_preds.extend(preds.cpu().numpy())
                val_targets.extend(labels.cpu().numpy())
                
        val_acc = accuracy_score(val_targets, val_preds)
        val_macro_f1 = f1_score(val_targets, val_preds, average="macro", zero_division=0)
        
        print(f"Epoch [{epoch}/{num_epochs}] - Train Loss: {epoch_train_loss:.4f}, Train Acc: {epoch_train_acc*100:.2f}% | Val Acc: {val_acc*100:.2f}%, Val F1: {val_macro_f1:.4f}")
        
        history.append({
            "epoch": epoch,
            "train_loss": epoch_train_loss,
            "train_acc": epoch_train_acc,
            "val_acc": val_acc,
            "val_f1": val_macro_f1
        })
        
        if val_macro_f1 >= best_val_f1:
            best_val_f1 = val_macro_f1
            torch.save({
                "model_state_dict": model.state_dict(),
                "classes": CATEGORIES,
                "epoch": epoch,
                "val_f1": val_macro_f1,
                "val_acc": val_acc
            }, CUSTOM_MODEL_PATH)
            
    train_time = round(time.time() - t0, 1)
    print(f"[*] Training finished in {train_time}s. Best checkpoint saved to {CUSTOM_MODEL_PATH}")
    
    # Evaluate best checkpoint on held-out test split
    print("\n[*] Evaluating Best Custom CNN Checkpoint on Held-Out Test Set (n=338)...")
    checkpoint = torch.load(CUSTOM_MODEL_PATH, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    
    test_preds, test_targets = [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            preds = torch.argmax(outputs, dim=1)
            test_preds.extend(preds.cpu().numpy())
            test_targets.extend(labels.numpy())
            
    test_acc = accuracy_score(test_targets, test_preds)
    test_macro_f1 = f1_score(test_targets, test_preds, average="macro", zero_division=0)
    test_weighted_f1 = f1_score(test_targets, test_preds, average="weighted", zero_division=0)
    cm = confusion_matrix(test_targets, test_preds)
    report_dict = classification_report(test_targets, test_preds, target_names=CATEGORIES, output_dict=True, zero_division=0)
    report_text = classification_report(test_targets, test_preds, target_names=CATEGORIES, zero_division=0)
    
    print(f"Custom CNN Held-Out Test Results:")
    print(f"  Accuracy:    {test_acc*100:.2f}%")
    print(f"  Macro F1:    {test_macro_f1:.4f}")
    print(f"  Weighted F1: {test_weighted_f1:.4f}")
    print("\nClassification Report:\n", report_text)
    
    # Save confusion matrix visualization
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=CATEGORIES, yticklabels=CATEGORIES)
    plt.title("Custom CNN: Garment Category Confusion Matrix (Test N=338)", fontsize=12, pad=12)
    plt.xlabel("Predicted Class", fontsize=10)
    plt.ylabel("Ground Truth Class", fontsize=10)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    cm_path = os.path.join(VIZ_DIR, "custom_cnn_confusion_matrix.png")
    plt.savefig(cm_path, dpi=200)
    plt.close()
    print(f"[*] Confusion matrix chart saved to {cm_path}")
    
    # Save evaluation metrics json
    metrics = {
        "model_name": "Custom Lightweight CNN (From Scratch)",
        "test_accuracy": float(test_acc),
        "test_macro_f1": float(test_macro_f1),
        "test_weighted_f1": float(test_weighted_f1),
        "training_time_seconds": train_time,
        "epochs_trained": num_epochs,
        "history": history,
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict
    }
    
    json_path = os.path.join(REPORTS_DIR, "custom_cnn_metrics.json")
    with open(json_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[*] Metrics saved to {json_path}")

if __name__ == "__main__":
    train_and_evaluate()
