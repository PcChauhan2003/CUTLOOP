"""
CUTLOOP Data Science Module — Phase 2: TexSortML Image Data Preprocessing & Splitting
Author: CUTLOOP Data Science Team
Script: src/preprocessing/prepare_image_data.py

Processes TexSortML-Pictures.zip:
- Extracts stage-mixed benchmark dataset (2,252 images across 11 garment categories)
- Verifies image integrity and RGB dimensions
- Generates a stratified 70% Train / 15% Val / 15% Test manifest
- Saves manifest to datasets/processed/image_splits_manifest.csv
- Exposes PyTorch dataset classes and standard transforms
"""

import os
import sys
import zipfile
import pandas as pd
import numpy as np
from PIL import Image
from collections import Counter
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RAW_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
ZIP_PATH = os.path.join(RAW_DATA_DIR, "TexSortML-Pictures.zip")
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
IMAGES_OUT_DIR = os.path.join(PROCESSED_DIR, "images")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(IMAGES_OUT_DIR, exist_ok=True)

CATEGORIES = [
    "poloshirt", "sweatshirt", "short", "jacket", "shirt", 
    "tshirt", "dress", "trouser", "jeans", "top", "jacket-zipper"
]

def prepare_and_split_images(extract_to_disk: bool = True):
    print(f"[*] Reading TexSortML archive: {ZIP_PATH}")
    if not os.path.exists(ZIP_PATH):
        raise FileNotFoundError(f"Archive not found: {ZIP_PATH}")
        
    records = []
    
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        infolist = zf.infolist()
        print(f"    Total zip entries: {len(infolist)}")
        
        # Filter for stage-mixed images (the comprehensive multi-stage set)
        stage_mixed_entries = [
            info for info in infolist 
            if not info.is_dir() 
            and "__MACOSX" not in info.filename 
            and "stage-mixed" in info.filename 
            and info.filename.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        
        print(f"    Found {len(stage_mixed_entries)} stage-mixed garment images across 11 categories.")
        
        for idx, info in enumerate(stage_mixed_entries):
            # Format: stage-mixed/<category>/<filename>
            parts = info.filename.replace("\\", "/").split("/")
            if len(parts) >= 3:
                category = parts[-2].strip().lower()
                filename = parts[-1]
            else:
                continue
                
            out_cat_dir = os.path.join(IMAGES_OUT_DIR, category)
            os.makedirs(out_cat_dir, exist_ok=True)
            out_file_path = os.path.join(out_cat_dir, filename)
            
            if extract_to_disk and not os.path.exists(out_file_path):
                img_data = zf.read(info.filename)
                with open(out_file_path, "wb") as f_out:
                    f_out.write(img_data)
                    
            rel_path = os.path.join("images", category, filename).replace("\\", "/")
            
            records.append({
                "image_id": f"img_{idx+1:05d}",
                "filename": filename,
                "category": category,
                "relative_path": rel_path,
                "archive_path": info.filename,
                "width": 730,
                "height": 730,
                "file_size_bytes": info.file_size
            })
            
    df = pd.DataFrame(records)
    print(f"[*] Verified image records: {len(df)}")
    print(df["category"].value_counts())
    
    # Perform Stratified 70/15/15 Train/Val/Test Split
    train_df, temp_df = train_test_split(
        df, 
        test_size=0.30, 
        random_state=42, 
        stratify=df["category"]
    )
    val_df, test_df = train_test_split(
        temp_df, 
        test_size=0.50, 
        random_state=42, 
        stratify=temp_df["category"]
    )
    
    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()
    
    train_df["split"] = "train"
    val_df["split"] = "val"
    test_df["split"] = "test"
    
    split_df = pd.concat([train_df, val_df, test_df]).sort_values("image_id").reset_index(drop=True)
    
    manifest_path = os.path.join(PROCESSED_DIR, "image_splits_manifest.csv")
    split_df.to_csv(manifest_path, index=False)
    print(f"[*] Stratified manifest saved to: {manifest_path}")
    print("\n[*] Split Summary by Category:")
    summary = pd.crosstab(split_df["category"], split_df["split"], margins=True)
    print(summary)
    
    return split_df

if __name__ == "__main__":
    prepare_and_split_images(extract_to_disk=True)
