# CUTLOOP — Verification & Testing Report
**Module 15 Compliance Document**

This document records the end-to-end testing matrix for the CUTLOOP Waste-to-Value platform across the Java Spring Boot core, Python FastAPI AI engine, and Frontend client.

---

## 1. Test Execution Matrix

| Test ID | Test Scenario | Execution Vector | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Python AI Service Health | `GET /api/ai/health` | HTTP 200 with service name & active models | HTTP 200; `{"status":"running", "explainability":"Grad-CAM Enabled"}` | **PASSED** |
| **TC-02** | Deep Learning Fabric Classifier | `POST /api/ai/fabric-classify` (Multipart) | Predicted class (e.g. Denim), confidence > 90%, probability distribution & Grad-CAM layer info | Returned `Denim (92.6% conf)` + 5 secondary probabilities + Grad-CAM `Conv_1` | **PASSED** |
| **TC-03** | YOLO Visual Defect Inspection | `POST /api/ai/defect-detect` (Multipart) | Bounding box coordinates `[x1, y1, x2, y2]`, defect type & seller recommendation | Returned `Broken thread (92% conf)` + Bounding box `[87, 84, 129, 133]` | **PASSED** |
| **TC-04** | AI Price Estimation Model | `POST /api/ai/price-predict` (JSON) | Suggested price range for material characteristics | Predicted `₹43.45/kg (Range: ₹40.41–₹46.50/kg)` (R² = 0.9838) | **PASSED** |
| **TC-05** | Demand Forecasting Model | `POST /api/ai/demand-predict` (JSON) | Next month predicted order volume & market trend | Predicted `129 orders (+14% growth)` for Cotton in Summer | **PASSED** |
| **TC-06** | Weighted AI Material Matching | `GET /api/materials/match` | Listings ranked by $Score = 0.35M + 0.25P + 0.20Q + 0.10C + 0.10L$ | Correctly computed and ranked candidates by compatibility percentage | **PASSED** |
| **TC-07** | Custom InsufficientStockException | `OrderService.placeOrder` | Throws exception when requested order quantity > available inventory | Atomic rejection prevents negative warehouse stock | **PASSED** |
| **TC-08** | Multithreaded Async Upload | `POST /api/materials/upload-and-analyze` | Saves listing draft immediately and processes AI in background `ExecutorService` | Fast response with `SUBMITTED_FOR_ANALYSIS`; non-blocking UI | **PASSED** |
| **TC-09** | CSV Inventory Export | `GET /api/inventory/export-csv` | Returns valid CSV file of seller materials | Clean CSV formatted with IDs, quantities, prices, and status | **PASSED** |
| **TC-10** | Simulated Payment Sandbox | `POST /api/payments/process` | Generates unique transaction reference and updates order to `CONFIRMED` | TxnRef generated; Order and Payment recorded atomically | **PASSED** |
| **TC-11** | AI Service Outage Fallback | RestClient timeout / outage | Listing saved as `DRAFT` with manual verification pending flag | Zero data loss; seller listing preserved gracefully | **PASSED** |

---

## 2. Model Performance Benchmarks

### Deep Learning Model 1: MobileNetV2 Fabric Classifier
* **Input Resolution:** 224 × 224 × 3
* **Classes:** Cotton, Denim, Polyester, Silk, Wool, Linen
* **Transfer Learning Backbone:** MobileNetV2 pre-trained on ImageNet
* **Feature Head:** GlobalAveragePooling2D → Dropout(0.3) → Dense(128, ReLU) → Dropout(0.2) → Dense(6, Softmax)
* **Average Inference Latency:** ~28 ms on RTX 3050 / CPU fallback

### Deep Learning Model 2: Ultralytics YOLO Visual Defect Inspection
* **Classes:** Hole, Stain, Tear, Broken thread, No defect
* **Task:** Object Detection & Bounding Box Localization
* **Output Format:** `[x_min, y_min, x_max, y_max]` normalized to image dimensions

### Data Science Model 1: Random Forest Price Regressor
* **Dataset:** 1,500 observed industrial transactions (`material_prices.csv`)
* **Features:** Material Type, Condition, Quantity (kg), Width (in), Colour, Location, Virgin Reference Price
* **Evaluation:**
  * **Mean Absolute Error (MAE):** ₹3.19 / kg
  * **Root Mean Squared Error (RMSE):** ₹4.38 / kg
  * **Coefficient of Determination ($R^2$):** 0.9838

### Data Science Model 2: Chronological Demand Forecaster
* **Dataset:** 46 months historical observations (`material_demand.csv`)
* **Validation Split:** Chronological 80/20 train/test split (no future data leakage)
* **Evaluation:**
  * **Mean Absolute Error (MAE):** 16.18 monthly orders
  * **Root Mean Squared Error (RMSE):** 25.27
