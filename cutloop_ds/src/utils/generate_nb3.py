"""
Generate Phase 3 Jupyter Notebook: 03_exploratory_data_analysis.ipynb
"""

import os
import json
from generate_notebooks import create_notebook, make_cell

cells_nb3 = [
    make_cell("markdown", "# CUTLOOP — Phase 3: Exploratory Data Analysis (EDA)\n## Statistical & Visual Analysis of Fast-Fashion Garments & TexSortML Benchmark\nThis notebook visualizes brand representation, category frequency, material blend ratios, circularity index distribution, and image class splits."),
    make_cell("code", "import os\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nbase_dir = os.path.abspath('..')\ngarments_path = os.path.join(base_dir, 'datasets', 'processed', 'garments_cleaned.csv.gz')\nmanifest_path = os.path.join(base_dir, 'datasets', 'processed', 'image_splits_manifest.csv')\n\ndf_g = pd.read_csv(garments_path)\ndf_img = pd.read_csv(manifest_path)\nprint('Garments:', df_g.shape, '| Images:', df_img.shape)"),
    make_cell("markdown", "### 1. Brand & Category Breakdown"),
    make_cell("code", "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\ndf_g['brand'].value_counts().plot(kind='bar', ax=axes[0], color=['#1b4332', '#40916c'], title='Garments by Brand')\ndf_g['parent_category'].value_counts().head(10).plot(kind='barh', ax=axes[1], color='#2d6a4f', title='Top 10 Categories')\nplt.tight_layout()\nplt.show()"),
    make_cell("markdown", "### 2. Recyclability & Material Composition"),
    make_cell("code", "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\ndf_g['dominant_fiber'].value_counts().head(8).plot(kind='bar', ax=axes[0], color=sns.color_palette('mako', 8), title='Dominant Fiber Frequency')\nsns.histplot(df_g['circularity_score'], bins=20, kde=True, ax=axes[1], color='#2d6a4f')\naxes[1].set_title('Circularity Index Distribution')\nplt.tight_layout()\nplt.show()"),
    make_cell("markdown", "### 3. TexSortML Image Benchmark Split Breakdown"),
    make_cell("code", "pd.crosstab(df_img['category'], df_img['split']).plot(kind='bar', stacked=True, figsize=(12, 5), color=['#1b4332', '#52b788', '#b7e4c7'], title='TexSortML Splits')\nplt.show()")
]

create_notebook("03_exploratory_data_analysis.ipynb", cells_nb3)
