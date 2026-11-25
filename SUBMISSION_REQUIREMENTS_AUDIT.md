# CUTLOOP — 5th Semester Integrated Project Submission Requirements Audit

**Document Reference:** `CUTLOOP/SUBMISSION_REQUIREMENTS_AUDIT.md`  
**Evaluation Program:** 3rd Year B.Tech CSE (5th Semester Integrated Capstone)  
**Institution:** JG University  
**Auditor:** Senior Academic Project Documentation & Software Audit Engineer  
**Audit Date:** November 21, 2026  
**System Evaluated:** CUTLOOP — AI-Powered Circular Textile Waste Platform  

---

## 1. Academic Evaluation Matrix Overview

The 5th Semester Integrated Academic Capstone combines five core subjects totaling **100 marks + 5 bonus marks**:
1. **Java Core (20 Marks):** OOP hierarchy, inheritance, interfaces, custom exception handling, multithreading (`CompletableFuture`/`ThreadPoolExecutor`), file management (CSV export/import).
2. **E-Commerce (10 Marks):** Marketplace design, buyer/seller registration & authentication, search/filtering, cart, simulated checkout, order lifecycle, security, digital marketing.
3. **Data Science (15 Marks):** Dataset cleaning, EDA, preprocessing, feature engineering, Model A (Dominant Fiber Classification vs. Decision Tree baseline), Model C (K-Means Clustering), statistical analysis, notebook pipeline.
4. **Deep Learning (20 Marks):** Two genuine deep learning components — Model B (MobileNetV2 Transfer Learning for 11 garment classes) and Model B-Baseline (Custom 4-block CNN trained from scratch on TexSortML), comparative evaluation, Grad-CAM explainability.
5. **Startup & Innovation Policies (10 Marks):** Project proposal, Lean Canvas, Business Model Canvas, SWOT, PESTEL, MVP funding roadmap, IP & dataset compliance.
6. **Integration & Polish Bonus (+5 Marks):** Unified REST proxy architecture (`serve.py`), live interactive frontend dashboard, cross-module synchronization, comprehensive documentation.

---

## 2. Requirement-by-Requirement Audit & Status Tracking

| Subject Area | Specific Requirement | Implementation Status | Code / Artifact Location | Audit Findings & Required Actions |
| :--- | :--- | :---: | :--- | :--- |
| **Java Core (20M)** | **Classes & Objects** | **COMPLETED** | `cutloop-backend/src/main/java/com/cutloop/model/` | Entities for `User`, `Material`, `Cart`, `Order`, `Payment`, `Inventory`, `AIAnalysis` implemented with JPA annotations. |
| **Java Core (20M)** | **Inheritance Hierarchy** | **COMPLETED** | `model/User.java`, `model/Buyer.java`, `model/Seller.java`, `model/Admin.java` | Clean OOP inheritance: `Buyer extends User`, `Seller extends User`, `Admin extends User` with distinct privileges. |
| **Java Core (20M)** | **Interfaces & Abstraction** | **COMPLETED** | `service/PaymentProcessor.java`, `service/PaymentService.java` | `PaymentProcessor` interface defines transaction lifecycle implemented by `PaymentService`. |
| **Java Core (20M)** | **Custom Exceptions** | **COMPLETED** | `exception/InsufficientStockException.java`, `exception/InvalidMaterialException.java`, `exception/PaymentFailedException.java` | Strongly typed domain exceptions mapped with Spring `@ExceptionHandler` and HTTP error codes. |
| **Java Core (20M)** | **Multithreading** | **COMPLETED** | `config/AsyncConfig.java`, `service/AIService.java`, `service/InventoryService.java` | Spring `@Async("cutloopAsyncExecutor")`, `CompletableFuture<AIAnalysis>`, and `Executors.newFixedThreadPool(3)` handle background image processing. |
| **Java Core (20M)** | **File Management** | **COMPLETED** | `service/InventoryService.java`, `controller/MaterialController.java` | `BufferedReader` and `InputStreamReader` CSV import (`importInventoryFromCsv`), CSV report export (`exportInventoryToCsv`), and `MultipartFile` upload handling. |
| **E-Commerce (10M)** | **Buyer / Seller Journey** | **COMPLETED** | `frontend/index.html`, `frontend/app.js`, `controller/AuthController.java` | Dual-role registration, persistent login tokens, role-specific views for buyers and textile composite mills. |
| **E-Commerce (10M)** | **Product Listing Workflow** | **COMPLETED** | `controller/MaterialController.java` (`uploadAndAnalyze`), `frontend/app.js` | Seller multi-step upload: image selection, scrap grade, weight, location, and asynchronous AI analysis trigger. |
| **E-Commerce (10M)** | **Search & Discovery Filters** | **COMPLETED** | `frontend/app.js` (`renderMarketplace`), `service/MaterialService.java` | Multi-criteria search by fiber type, scrap grade, location (Ahmedabad, Surat, etc.), and max price. |
| **E-Commerce (10M)** | **Cart, Checkout & Orders** | **COMPLETED** | `controller/CartController.java`, `controller/OrderController.java`, `frontend/app.js` | Persistent cart, stock deduction, simulated UPI/Card payment gateway, and immutable order history ledger. |
| **E-Commerce (10M)** | **Security & Privacy** | **COMPLETED** | `config/SecurityConfig.java`, `frontend/app.js` | CORS configuration, BCrypt password hashing, session tokens, fake review prevention, and dark-pattern avoidance principles. |
| **Data Science (15M)**| **Fast-Fashion Dataset EDA**| **COMPLETED** | `cutloop_ds/src/preprocessing/clean_garment_data.py`, `notebooks/01..03` | 47,522 garment records parsed, normalized components, handled missingness, statistical distributions. |
| **Data Science (15M)**| **Model A: Dominant Fiber** | **COMPLETED (REMEDIATED)** | `cutloop_ds/src/utils/audit_model_a.py`, `saved_models/model_a_random_forest.joblib` | Target leakage removed; pure NLP TF-IDF (400 features) + metadata achieves **88.15% clean held-out test accuracy** ($n=9,505$). |
| **Data Science (15M)**| **Model A Baseline Comparison** | **COMPLETED** | `saved_models/model_a_decision_tree.joblib`, `reports/POST_IMPLEMENTATION_AUDIT.md` | Decision Tree baseline achieves 78.09% accuracy vs. 88.15% for Random Forest (+10.06% gain). |
| **Data Science (15M)**| **Model C: K-Means Clustering** | **COMPLETED** | `cutloop_ds/src/models/train_clustering_model.py`, `saved_models/model_c_kmeans.joblib` | 5 distinct circularity archetypes discovered in continuous 10D fiber space; global silhouette peak of **0.6686**. |
| **Data Science (15M)**| **Model C Baseline Comparison** | **COMPLETED** | `reports/audit_verification_results.json` | Elbow and silhouette sweep evaluated across $k=2..8$; documented baseline comparison. |
| **Deep Learning (20M)**| **Model B: MobileNetV2 Vision** | **COMPLETED** | `cutloop_ds/src/models/train_vision_model.py`, `saved_models/texsort_model.pt` | Pretrained transfer learning classifier achieves **86.39% accuracy** on 11 macro garment categories ($n=338$). |
| **Deep Learning (20M)**| **Second Deep Learning Model** | **ACTION REQUIRED (PHASE 6)** | `submission/05_deep_learning/` | College requires TWO genuine DL models. Train a custom 4-block CNN from scratch on TexSortML to benchmark against MobileNetV2. |
| **Startup Policy (10M)**| **Business Documentation** | **ACTION REQUIRED (PHASE 2)** | `submission/01_startup/` | Compile academic proposal, Lean Canvas, Business Model Canvas, SWOT, PESTEL, and realistic MVP funding plan. |
| **E-Commerce Design**| **Architecture Spec** | **ACTION REQUIRED (PHASE 3)** | `submission/02_ecommerce/` | Compile complete 18-point design document with Mermaid sequence and architecture diagrams. |

---

## 3. Immediate Action Plan & Deliverables

1. **Phase 2 (Startup):** Author 8 comprehensive business strategy and policy documents in `submission/01_startup/`.
2. **Phase 3 (E-Commerce):** Author the 18-section architecture and user journey specification in `submission/02_ecommerce/`.
3. **Phase 4 (Java):** Author technical documentation, Mermaid UML class diagram, and Java README in `submission/03_java/`.
4. **Phase 5 (Data Science):** Author comprehensive EDA, dataset documentation, notebook index, and Model A/C comparisons in `submission/04_data_science/`.
5. **Phase 6 (Deep Learning):**
   - Implement and train the **Custom Lightweight CNN** from scratch on the TexSortML dataset on CPU.
   - Evaluate Custom CNN vs. MobileNetV2 on the held-out test set ($n=338$).
   - Author Model B and Custom CNN documentation, confusion matrices, and Grad-CAM explainability in `submission/05_deep_learning/`.
6. **Phase 7 (Integration & Verification):** Validate end-to-end consistency across all reports, schemas, and metrics.
