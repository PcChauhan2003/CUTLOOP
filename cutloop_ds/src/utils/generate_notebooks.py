"""
Helper to generate clean .ipynb notebooks for CUTLOOP Data Science Module.
"""

import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

def create_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    path = os.path.join(NOTEBOOKS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebook: {path}")

def make_cell(cell_type, source):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [s + "\n" for s in source.split("\n")]
    }

if __name__ == "__main__":
    cells_nb2 = [
        make_cell("markdown", "# CUTLOOP — Phase 2: Data Cleaning & Preprocessing\n## Fast-Fashion Garment Dataset & TexSortML Preprocessing\nThis notebook demonstrates the preprocessing pipeline: handling missing values, extracting fiber compositions, and preparing image splits."),
        make_cell("code", "import os\nimport pandas as pd\nimport numpy as np\n\nbase_dir = os.path.abspath('..')\ncleaned_csv = os.path.join(base_dir, 'datasets', 'processed', 'garments_cleaned.csv.gz')\nmanifest_csv = os.path.join(base_dir, 'datasets', 'processed', 'image_splits_manifest.csv')\n\ndf_garments = pd.read_csv(cleaned_csv)\nprint('Garments dataset shape:', df_garments.shape)\ndf_garments.head(3)"),
        make_cell("markdown", "### 1. Composition & Blend Statistics\nEvaluate single-fiber mono-material vs blended fabric distributions."),
        make_cell("code", "print('Mono-material (>=95% single fiber):', df_garments['is_mono_material'].value_counts(normalize=True).round(3))\nprint('\\nBlended materials (>1 fiber):', df_garments['is_blend'].value_counts(normalize=True).round(3))\nprint('\\nDominant Fiber Distribution:\\n', df_garments['dominant_fiber'].value_counts().head(8))"),
        make_cell("markdown", "### 2. TexSortML Image Splits Manifest\nInspect the stratified 70/15/15 train/val/test split."),
        make_cell("code", "df_images = pd.read_csv(manifest_csv)\nprint('Total image records:', len(df_images))\npd.crosstab(df_images['category'], df_images['split'], margins=True)")
    ]
    create_notebook("02_data_cleaning.ipynb", cells_nb2)
