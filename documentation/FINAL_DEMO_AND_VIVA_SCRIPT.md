# CUTLOOP — Final 5-Minute Live Demonstration & Viva Script
**Module 17 Compliance Guide**

This script outlines the exact live presentation sequence for faculty evaluations, investor pitches, and project viva examinations.

---

## 1. Five-Minute Live Demo Timeline

```mermaid
journey
    title 5-Minute CUTLOOP Demonstration Timeline
    section 0:00 - 0:40
      Introduce Problem & Mission: 5: Presenter
    section 0:40 - 1:30
      Seller Uploads Fabric: 4: Seller
    section 1:30 - 2:20
      AI Analysis & Grad-CAM: 5: AI Engine
    section 2:20 - 3:10
      Buyer Marketplace & Matching: 5: Buyer
    section 3:10 - 4:00
      Order & Sandbox Payment: 5: Transaction
    section 4:00 - 5:00
      Analytics & Sustainability: 5: Admin
```

### [0:00 – 0:40] Introduce the Problem
* **Speaker:** Startup / Integration Lead
* **Action:** Open Homepage (`/`).
* **Verbal Pitch:**
  > *"Good morning, esteemed evaluators. In India's major textile clusters like Ahmedabad and Surat, 15 to 20 percent of virgin fabrics end up as cutting remnants and surplus deadstock. Small artisans and upcycling brands desperately need these fabrics but have no trusted way to source them. CUTLOOP solves this with our AI-powered Waste-to-Value Marketplace: One factory's leftover material is another creator's raw material."*

---

### [0:40 – 1:30] Seller Uploads Fabric
* **Speaker:** Frontend Lead / Seller Lead
* **Action:** Click on **AI Scanner** (`/ai-scanner`), select a sample fabric photograph.
* **Verbal Pitch:**
  > *"Instead of manual typing, the factory supervisor simply uploads a photo of the cutting roll. Notice the interface preview is instant. Behind the scenes, Spring Boot securely creates a draft listing and dispatches an asynchronous task to our Python AI vision microservice via a managed ThreadPoolTaskExecutor."*

---

### [1:30 – 2:20] AI Analysis & Explainability
* **Speaker:** Deep Learning Lead
* **Action:** Click **⚡ Run AI Vision Pipeline**, toggle **Show Grad-CAM Heatmap**.
* **Verbal Pitch:**
  > *"In under 30 milliseconds, four AI models execute: First, MobileNetV2 classifies the fabric as Cotton with 94.2% confidence. Second, our Grad-CAM explainability map shows the user the exact weave intersections that influenced the decision. Third, our YOLO detector scans for surface defects like holes or tears. Fourth, our Random Forest price regressor analyzes 1,500 historical transactions and suggests a fair market range of ₹42 to ₹48 per kg."*
* **Action:** Click **✓ Publish as Marketplace Listing**.

---

### [2:20 – 3:10] Buyer Marketplace & AI Material Matching
* **Speaker:** Data Science Lead
* **Action:** Open **Marketplace** (`/marketplace`), demonstrate the **AI Material Requirement Matcher**.
* **Verbal Pitch:**
  > *"As a buyer, I might need 20 kg of Cotton under ₹50 per kg in Ahmedabad. Our backend applies weighted multi-attribute ranking: Score = 0.35M + 0.25P + 0.20Q + 0.10C + 0.10L. The most compatible factory listings appear at the very top with instant match scores."*

---

### [3:10 – 4:00] Atomic Order & Simulated Payment
* **Speaker:** Java Backend Lead
* **Action:** Click **Add to Cart**, open cart, and click **Pay with Test Gateway**.
* **Verbal Pitch:**
  > *"The buyer checks out. Inside Java Spring Boot, OrderService executes an atomic database transaction. If another buyer attempts to purchase the same stock, our custom InsufficientStockException prevents warehouse overselling. The simulated test payment generates a unique transaction reference and decrements inventory in real-time."*

---

### [4:00 – 5:00] Platform Analytics & Business Viability
* **Speaker:** Startup Lead
* **Action:** Switch to **Impact & Demand** (`/analytics`).
* **Verbal Pitch:**
  > *"Finally, we view our impact dashboard. Notice the 'Material Recovered Through CUTLOOP' metric updates dynamically, recording 650+ kg diverted from scrap, avoiding over 1,200 kg of CO₂. Under demand forecasting, our time-series model alerts suppliers to a 18% projected spike in cotton demand next month. CUTLOOP captures a 5% transaction commission, making sustainability economically rewarding."*

---

## 2. Key Viva Q&A Guide

**Q1: Why use both Spring Boot and FastAPI instead of building everything in Python?**
> **Answer:** *"Enterprise e-commerce requires strict relational transactions, role-based access control, and robust multithreaded queueing, where Spring Boot and Java excels. Conversely, modern Deep Learning frameworks (TensorFlow, PyTorch, Scikit-Learn) are native to Python. Splitting them into a polyglot microservice architecture connected via REST APIs follows industry best practices and ensures AI processing cannot crash core transaction services."*

**Q2: How does the AI price estimation prevent arbitrary predictions?**
> **Answer:** *"Our Random Forest model is trained on 1,500 observations incorporating virgin reference prices, fabric width, condition factors, and bulk quantity tiers. It achieves an R² of 0.9838 and an MAE of ₹3.19/kg. Furthermore, the AI output is an advisory range, allowing sellers the final decision."*

**Q3: How do you prevent data leakage in demand forecasting?**
> **Answer:** *"Standard random train-test splitting would leak future trends into past periods. We enforced strict chronological validation: the model was trained on historical records up to January 2026 and evaluated strictly on subsequent unseen months."*
