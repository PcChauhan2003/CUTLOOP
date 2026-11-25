# Deep Learning Confusion Matrix & Error Analysis

**Academic Program**: 3rd-Year B.Tech Computer Science & Engineering (Semester 5)  
**Subject Area**: Deep Learning (20 Marks)  
**Project**: CUTLOOP — AI-Powered Industrial Textile & Fabric Waste Marketplace  
**Evaluation Set**: Held-Out Test Set Split ($N = 338$ images, 11 categories)  

---

## 1. Overview & Evaluation Metrics

In multi-class textile classification, global accuracy can obscure systematic failures on rare or subtle apparel categories. To ensure complete scientific transparency, both deep learning models are evaluated using full **$11 \times 11$ Confusion Matrices**, per-class **Precision**, **Recall**, and **F1-Scores**:

$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

- **Macro-Averaged F1**: Calculates metrics independently for each of the 11 classes, treating rare classes (e.g., `jacket-zipper`, $N=8$) with equal weight to dominant classes (e.g., `poloshirt`, $N=54$).
- **Weighted-Averaged F1**: Weights each class metric by its true support in the test dataset.

---

## 2. Component 1: MobileNetV2 (Transfer Learning) Confusion Matrix

**Total Test Samples**: $N = 338$ | **Correct Predictions**: $292$ | **Test Accuracy**: **86.39%**  
**Macro Precision**: 0.8023 | **Macro Recall**: 0.8087 | **Macro F1**: **0.8015**  
**Weighted Precision**: 0.8644 | **Weighted Recall**: 0.8639 | **Weighted F1**: **0.8604**  

### 2.1 Full $11 \times 11$ Matrix (Ground Truth Rows vs. Predicted Columns)

| Ground Truth \ Predicted | dress | jacket | jacket-zip | jeans | polo | shirt | short | sweat | top | trouser | tshirt | Total | Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **dress** | **23** | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | **92.00%** |
| **jacket** | 1 | **37** | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 1 | 1 | 43 | **86.05%** |
| **jacket-zipper** | 0 | 0 | **0** | 0 | 0 | 1 | 0 | 6 | 0 | 0 | 1 | 8 | **0.00%** |
| **jeans** | 0 | 0 | 0 | **15** | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 17 | **88.24%** |
| **poloshirt** | 2 | 0 | 0 | 0 | **52** | 0 | 0 | 0 | 0 | 0 | 0 | 54 | **96.30%** |
| **shirt** | 0 | 0 | 0 | 0 | 0 | **32** | 0 | 2 | 0 | 0 | 2 | 36 | **88.89%** |
| **short** | 0 | 0 | 0 | 0 | 0 | 0 | **41** | 1 | 0 | 0 | 4 | 46 | **89.13%** |
| **sweatshirt** | 0 | 0 | 0 | 0 | 2 | 3 | 0 | **42** | 0 | 0 | 6 | 53 | **79.25%** |
| **top** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **13** | 0 | 0 | 13 | **100.0%** |
| **trouser** | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **14** | 2 | 18 | **77.78%** |
| **tshirt** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | **23** | 25 | **92.00%** |
| **Total Predicted** | 28 | 37 | 0 | 16 | 57 | 38 | 41 | 53 | 13 | 16 | 39 | 338 | - |
| **Precision** | **82.14%**| **100.0%**| **0.00%**| **93.75%**| **91.23%**| **84.21%**| **100.0%**| **79.25%**| **100.0%**| **87.50%**| **58.97%**| - | - |

---

## 3. Component 2: Custom Lightweight CNN (From Scratch) Confusion Matrix

**Total Test Samples**: $N = 338$ | **Correct Predictions**: $244$ | **Test Accuracy**: **72.19%**  
**Macro Precision**: 0.6998 | **Macro Recall**: 0.6492 | **Macro F1**: **0.6503**  
**Weighted Precision**: 0.7231 | **Weighted Recall**: 0.7219 | **Weighted F1**: **0.6988**  

### 3.1 Full $11 \times 11$ Matrix (Ground Truth Rows vs. Predicted Columns)

| Ground Truth \ Predicted | dress | jacket | jacket-zip | jeans | polo | shirt | short | sweat | top | trouser | tshirt | Total | Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **dress** | **8** | 4 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | **32.00%** |
| **jacket** | 0 | **39** | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 43 | **90.70%** |
| **jacket-zipper** | 0 | 0 | **0** | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 6 | 8 | **0.00%** |
| **jeans** | 1 | 0 | 0 | **9** | 5 | 0 | 0 | 0 | 0 | 2 | 0 | 17 | **52.94%** |
| **poloshirt** | 0 | 8 | 0 | 0 | **45** | 1 | 0 | 0 | 0 | 0 | 0 | 54 | **83.33%** |
| **shirt** | 0 | 1 | 0 | 0 | 8 | **14** | 0 | 11 | 0 | 1 | 1 | 36 | **38.89%** |
| **short** | 0 | 0 | 0 | 0 | 0 | 0 | **37** | 4 | 0 | 0 | 5 | 46 | **80.43%** |
| **sweatshirt** | 0 | 1 | 0 | 0 | 0 | 0 | 2 | **49** | 0 | 0 | 1 | 53 | **92.45%** |
| **top** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **13** | 0 | 0 | 13 | **100.0%** |
| **trouser** | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | **15** | 0 | 18 | **83.33%** |
| **tshirt** | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | **15** | 25 | **60.00%** |
| **Total Predicted** | 9 | 53 | 0 | 11 | 73 | 18 | 51 | 64 | 13 | 18 | 28 | 338 | - |
| **Precision** | **88.89%**| **73.58%**| **0.00%**| **81.82%**| **61.64%**| **77.78%**| **72.55%**| **76.56%**| **100.0%**| **83.33%**| **53.57%**| - | - |

---

## 4. Side-by-Side Per-Class Performance Comparison

| Garment Class | Support ($N$) | MobileNetV2 Precision | MobileNetV2 Recall | MobileNetV2 F1 | Custom CNN Precision | Custom CNN Recall | Custom CNN F1 | F1 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **dress** | 25 | 82.14% | **92.00%** | **0.8679** | 88.89% | 32.00% | 0.4706 | **+0.3973 (TL Wins)** |
| **jacket** | 43 | 100.0% | 86.05% | **0.9250** | 73.58% | **90.70%** | 0.8125 | **+0.1125 (TL Wins)** |
| **jacket-zipper** | 8 | 0.00% | 0.00% | 0.0000 | 0.00% | 0.00% | 0.0000 | Tied (Zero Recall) |
| **jeans** | 17 | 93.75% | **88.24%** | **0.9091** | 81.82% | 52.94% | 0.6429 | **+0.2662 (TL Wins)** |
| **poloshirt** | 54 | 91.23% | **96.30%** | **0.9369** | 61.64% | 83.33% | 0.7087 | **+0.2282 (TL Wins)** |
| **shirt** | 36 | 86.49% | **88.89%** | **0.8767** | 77.78% | 38.89% | 0.5185 | **+0.3582 (TL Wins)** |
| **short** | 46 | 100.0% | **89.13%** | **0.9425** | 72.55% | 80.43% | 0.7629 | **+0.1796 (TL Wins)** |
| **sweatshirt** | 53 | 79.25% | 79.25% | 0.7925 | 76.56% | **92.45%** | **0.8376** | **+0.0451 (Custom Wins)** |
| **top** | 13 | 100.0% | 100.0% | **1.0000** | 100.0% | 100.0% | **1.0000** | Tied (Perfect Score) |
| **trouser** | 18 | 87.50% | 77.78% | 0.8235 | 83.33% | **83.33%** | **0.8333** | **+0.0098 (Custom Wins)** |
| **tshirt** | 25 | 62.16% | **92.00%** | **0.7419** | 53.57% | 60.00% | 0.5660 | **+0.1759 (TL Wins)** |
| **Macro Average** | **338** | **80.23%** | **80.87%** | **0.8015** | **69.98%** | **64.92%** | **0.6503** | **+0.1512 (TL Wins)** |
| **Weighted Average**| **338** | **86.44%** | **86.39%** | **0.8604** | **72.31%** | **72.19%** | **0.6988** | **+0.1616 (TL Wins)** |

---

## 5. Key Error Diagnoses & Empirical Insights

### 5.1 Why Dress Recognition Collapsed on Custom CNN
- MobileNetV2 achieved **92.00% recall** on `dress`, whereas Custom CNN achieved only **32.00% recall** (misclassifying 13 dresses as `poloshirt` and 4 as `jacket`).
- **Explanation**: A dress requires synthesizing long-range spatial context (the continuous flow from neckline through waist down to knees). MobileNetV2's deep 53-layer receptive field captures this global span. The 4-block Custom CNN has a maximum receptive field of only $31 \times 31$ pixels before pooling; when encountering the upper bodice of a dress, it recognizes fabric around the neck and misidentifies it as a collared polo shirt.

### 5.2 The Surprising Strength of Custom CNN on Sweatshirt and Trouser
- Custom CNN achieved **92.45% recall** on `sweatshirt` and **83.33% recall** on `trouser`, slightly outperforming MobileNetV2 on those specific classes.
- **Explanation**: Sweatshirts and trousers exhibit prominent, repetitive textural signatures (heavy fleece surface texture and long parallel leg seams) that do not require complex hierarchical abstractions. A 4-block network with batch normalization readily captures these immediate mid-frequency patterns.

### 5.3 Stored Visualization Evidence
- MobileNetV2 Confusion Matrix: `cutloop_ds/visualizations/model_b_confusion_matrix.png`
- Custom CNN Confusion Matrix: `cutloop_ds/visualizations/custom_cnn_confusion_matrix.png`
