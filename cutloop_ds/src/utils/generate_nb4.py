"""
Generate Phase 4 Jupyter Notebook: 04_feature_engineering.ipynb
"""

import os
import json
from generate_notebooks import create_notebook, make_cell

cells_nb4 = [
    make_cell("markdown", "# CUTLOOP — Phase 4: Feature Engineering\n## Multimodal Feature Pipelines for Circular Fabric & Garment Modeling\nThis notebook demonstrates text TF-IDF vectorization, categorical one-hot encoding, circularity indicator scaling, and persistent sparse feature matrix creation."),
    make_cell("code", "import os\nimport joblib\nimport numpy as np\nfrom scipy.sparse import load_npz\n\nbase_dir = os.path.abspath('..')\npipeline_path = os.path.join(base_dir, 'saved_models', 'feature_pipeline.joblib')\nX_train = load_npz(os.path.join(base_dir, 'datasets', 'processed', 'X_train_features.npz'))\nX_test = load_npz(os.path.join(base_dir, 'datasets', 'processed', 'X_test_features.npz'))\ny_train = np.load(os.path.join(base_dir, 'datasets', 'processed', 'y_train.npy'))\ny_test = np.load(os.path.join(base_dir, 'datasets', 'processed', 'y_test.npy'))\n\npipe = joblib.load(pipeline_path)\nprint('Feature dimensions: Train', X_train.shape, '| Test', X_test.shape)\nprint('Target classes:', pipe['target_classes'])"),
    make_cell("markdown", "### 1. TF-IDF Vocabulary Inspection"),
    make_cell("code", "tfidf = pipe['tfidf']\nfeature_names = tfidf.get_feature_names_out()\nprint('Top 20 TF-IDF features:', feature_names[:20])"),
    make_cell("markdown", "### 2. Target Class Representation"),
    make_cell("code", "import pandas as pd\npd.Series(y_train).value_counts().rename(index=dict(enumerate(pipe['target_classes'])))")
]

create_notebook("04_feature_engineering.ipynb", cells_nb4)
