# CUTLOOP — Phase 4: Feature Engineering Report

## 1. Feature Engineering Overview
- **Raw Samples Available**: 47,522
- **Train Partition (80%)**: 38,017
- **Test Partition (20%)**: 9,505
- **Total Engineered Feature Dimension**: 367 features

---

## 2. Feature Modalities & Transformation Architecture

### A. Textual Representations (TF-IDF)
- **Input**: Concatenated product name and product description (`text_combined`).
- **Configuration**:
  - `max_features`: 350
  - `ngram_range`: (1, 2) unigrams and bigrams
  - `sublinear_tf`: True (logarithmic term frequency scaling $1 + \log(tf)$)
  - `stop_words`: Standard English

### B. Categorical Features (One-Hot Encoding)
- Categorical Columns: `brand`, `region`, `gender_section`, `parent_category`
- Total One-Hot Dimensions: 13 binary indicator channels
- `handle_unknown`: 'ignore' (guarantees runtime resilience on unseen categories)

### C. Continuous Circularity & Metadata Metrics
- Features: `num_components`, `has_lining`, `has_recycled`, `circularity_score`
- Normalization: `StandardScaler` (zero mean, unit variance)

### D. Target Class Distribution (`target_fiber`)
| Class Name | Train Count | Test Count | Total | Class % |
| :--- | :--- | :--- | :--- | :--- |
| `acrylic` | 590 | 147 | 737 | 1.55% |
| `cotton` | 19,188 | 4,797 | 23,985 | 50.47% |
| `linen` | 562 | 141 | 703 | 1.48% |
| `other` | 1,024 | 256 | 1,280 | 2.69% |
| `polyamide` | 2,662 | 666 | 3,328 | 7.00% |
| `polyester` | 10,541 | 2,635 | 13,176 | 27.73% |
| `viscose` | 2,653 | 663 | 3,316 | 6.98% |
| `wool` | 797 | 200 | 997 | 2.10% |

---

## 3. Persistent Feature Artifacts Produced
- **Scikit-learn Transformers Bundle**: `saved_models/feature_pipeline.joblib`
- **Sparse Feature Matrices**:
  - `datasets/processed/X_train_features.npz` ((38017, 367))
  - `datasets/processed/X_test_features.npz` ((9505, 367))
- **Target Arrays**: `y_train.npy`, `y_test.npy`
- **Feature Names Index**: `datasets/processed/feature_names.json`
