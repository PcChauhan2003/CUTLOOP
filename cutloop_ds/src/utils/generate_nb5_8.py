"""
Generates notebooks 05, 06, 07, 08 for CUTLOOP Data Science Module.
"""

import os
from generate_notebooks import create_notebook, make_cell

# 05_material_analysis.ipynb
cells_05 = [
    make_cell("markdown", "# CUTLOOP — Phase 5: Material Composition Analysis & Circular Archetypes\n## Model C: K-Means Clustering on 10D Fiber Composition Vectors\nIdentifies industrial textile clusters (Pure Cotton, Synthetics, Cellulosics, Luxury Blends) to guide automated sorting and mechanical vs chemical recycling pathways."),
    make_cell("code", "import os\nimport json\nimport joblib\nimport pandas as pd\n\nbase_dir = os.path.abspath('..')\nprofiles_path = os.path.join(base_dir, 'saved_models', 'archetype_profiles.json')\nwith open(profiles_path) as f:\n    profiles = json.load(f)\nfor k, v in profiles.items():\n    print(f\"{v['archetype_name']}: {v['centroid_composition_pct']} (Circularity: {v['recycling_pathway']})\")"),
    make_cell("markdown", "### PCA Projection of Clusters"),
    make_cell("code", "from IPython.display import Image\nImage(os.path.join(base_dir, 'visualizations', 'model_c_material_clusters.png'))")
]
create_notebook("05_material_analysis.ipynb", cells_05)

# 06_image_classification.ipynb
cells_06 = [
    make_cell("markdown", "# CUTLOOP — Phase 5: Image Classification on TexSortML\n## Model B: MobileNetV2 Deep Vision Classifier for Textile & Garment Sorting\nClassifies 11 garment types from the TexSortML benchmark with class-weighted cross-entropy loss."),
    make_cell("code", "import os\nimport json\nimport pandas as pd\n\nbase_dir = os.path.abspath('..')\nmanifest_path = os.path.join(base_dir, 'datasets', 'processed', 'image_splits_manifest.csv')\ndf_img = pd.read_csv(manifest_path)\nprint('Test images count:', (df_img['split'] == 'test').sum())\ndf_img.head(3)"),
    make_cell("markdown", "### Performance Metrics & Confusion Matrix"),
    make_cell("code", "from IPython.display import Image\nImage(os.path.join(base_dir, 'visualizations', 'model_b_confusion_matrix.png'))")
]
create_notebook("06_image_classification.ipynb", cells_06)

# 07_model_training.ipynb
cells_07 = [
    make_cell("markdown", "# CUTLOOP — Phase 5: Tabular Model Training\n## Model A: Random Forest & Decision Tree for Dominant Fiber Prediction\nTrains supervised ensemble classifiers on multimodal text (TF-IDF), categorical, and circularity features."),
    make_cell("code", "import os\nimport json\n\nbase_dir = os.path.abspath('..')\nmetrics_path = os.path.join(base_dir, 'reports', 'model_a_metrics.json')\nwith open(metrics_path) as f:\n    metrics = json.load(f)\nprint('Model A Random Forest Accuracy:', metrics['random_forest']['accuracy'] * 100, '%')\nprint('Model A Random Forest F1-Macro:', metrics['random_forest']['f1_macro'])"),
    make_cell("markdown", "### Confusion Matrix"),
    make_cell("code", "from IPython.display import Image\nImage(os.path.join(base_dir, 'visualizations', 'model_a_confusion_matrix.png'))")
]
create_notebook("07_model_training.ipynb", cells_07)

# 08_model_evaluation.ipynb
cells_08 = [
    make_cell("markdown", "# CUTLOOP — Phase 6: Comprehensive Model Evaluation & Comparison\n## Cross-Model Benchmarking: Model A (Tabular), Model B (Vision), Model C (Clustering), Model D (Pricing)\nSynthesizes all machine learning metrics across the CUTLOOP circular textile pipeline."),
    make_cell("code", "import os\nimport json\nimport pandas as pd\n\nbase_dir = os.path.abspath('..')\nwith open(os.path.join(base_dir, 'reports', 'model_a_metrics.json')) as f:\n    mA = json.load(f)\nwith open(os.path.join(base_dir, 'reports', 'model_c_metrics.json')) as f:\n    mC = json.load(f)\nprint('Model A RF Accuracy:', mA['random_forest']['accuracy'])\nprint('Model C Silhouette Score:', mC['silhouette_score'])"),
    make_cell("markdown", "### Model A vs Model B Summary Comparison"),
    make_cell("code", "eval_df = pd.DataFrame([\n    {'Model': 'Model A (Random Forest)', 'Task': 'Dominant Fiber Classification', 'Accuracy': mA['random_forest']['accuracy'], 'F1_Macro': mA['random_forest']['f1_macro']},\n    {'Model': 'Model C (K-Means)', 'Task': 'Material Archetype Discovery', 'Accuracy': 'N/A (Unsupervised)', 'F1_Macro': f'Sil: {mC[\"silhouette_score\"]}'}\n])\neval_df")
]
create_notebook("08_model_evaluation.ipynb", cells_08)
