# CUTLOOP — Investor Pitch Deck (12 Slides)
**Integrated Assignment | JG University — 5th Semester B.Tech**
**Startup Lead & Technical Founders**
**Tagline:** *One factory's leftover material is another creator's raw material.*

---

## Slide 1: Cover Slide
* **Company Name:** CUTLOOP Technologies Pvt. Ltd.
* **Tagline:** One factory's leftover material is another creator's raw material.
* **Presenters:** Product & Startup Lead, Java Lead, Data Lead, AI Lead, Marketing & Operations Lead.
* **Category:** B2B Circular Economy · AI-Driven Industrial Marketplace.
* **Institution:** JG University — Department of Computer Science & Engineering.

---

## Slide 2: The Problem
* **Massive Industrial Inefficiency:** India produces over 1.4 million tons of pre-consumer textile waste annually. Garment factories in Ahmedabad, Surat, Tirupur, and Ludhiana discard **12% to 22% of virgin material** as cutting table remnants, end-of-roll deadstock, and sampling cut-offs.
* **Warehouse Sinking Costs:** Surplus rolls sit idle in factory warehouses, locking up working capital and incurring monthly storage expenses.
* **Small Creator Bottleneck:** Sustainable fashion labels, craft studios, and boutique artisans struggle to purchase small fabric batches at reasonable rates, forced to pay 100% virgin retail prices.
* **Lack of Trust:** No standard exists to verify weave quality, fiber authenticity, or detect hidden weave flaws without traveling to distant factories in person.

---

## Slide 3: The Solution — CUTLOOP Platform
* **AI-Assisted Circular Marketplace:** A closed-loop B2B exchange where factories convert surplus waste into cash and creators source verified fabrics at **40%–60% below market price**.
* **Multi-Modal AI Scanner:** Sellers upload a single photograph. The AI automatically:
  1. Identifies garment category across 11 classes (`dress`, `jacket`, `jeans`, `shirt`, `tshirt`, etc.) via MobileNetV2 with **86.39% accuracy**.
  2. Extracts and verifies fiber composition using a Balanced Random Forest with **88.15% accuracy**.
  3. Maps blend composition to one of 5 circular recycling archetypes using K-Means clustering ($k=5$, Silhouette: 0.6686).
* **Transparent Pricing Engine:** Recommends fair spot clearing prices based on MCX commodity benchmarks, fiber multipliers, purity scores, and defect discounts.
* **Guaranteed B2B Fulfillment:** Integrated payment escrow (UPI, Cards, Net Banking, NEFT) and regional logistics routing across 4 major textile clusters.

---

## Slide 4: Market Opportunity & Target Audience
* **Total Addressable Market (TAM):** Indian industrial textile and apparel sector — **$165 Billion**.
* **Serviceable Addressable Market (SAM):** Pre-consumer textile waste & remnants market — **$4.2 Billion**.
* **Serviceable Obtainable Market (SOM):** Initial focus on Gujarat & Tamil Nadu garment clusters (Ahmedabad, Surat, Tirupur) — **$45 Million (5-Year Target)**.
* **Primary Target Personas:**
  * **Sellers:** Weaving mills, garment exporters, denim processing units.
  * **Buyers:** Eco-conscious fashion startups, handicraft exporters, industrial recyclers, craft studios.

---

## Slide 5: The Technology Stack & Architecture
* **Frontend:** Responsive Mobile-First Web Application (HTML5, CSS3, ES6+ JavaScript, Mobile Native Bottom Bar).
* **Backend Core (Java 21 & Spring Boot):** Enterprise-grade RESTful API, object-oriented domain hierarchy, atomic database transactions (`InsufficientStockException`), multithreaded order worker pools (`ThreadPoolTaskExecutor`), and persistent CSV file management.
* **AI & Machine Learning Microservice (Python & FastAPI):**
  * *DL Model 1:* MobileNetV2 Transfer Learning classifier (**86.39% test accuracy**, **0.8015 Macro F1** on TexSortML 11 categories).
  * *DL Model 2 (Baseline):* Custom 4-Block CNN built from scratch (**72.19% test accuracy**, quantifying a **+14.20% transfer learning premium**).
  * *DS Model 1:* Balanced Random Forest Dominant Fiber Classifier (**88.15% test accuracy**, **0.8257 Macro F1**, outperforming Decision Tree baseline by +10.06%).
  * *DS Model 2:* Unsupervised K-Means Material Archetype Clusterer ($k=5$, **Global Silhouette: 0.6686** isolating 5 circular streams).
  * *Valuation Engine:* Hedonic Commodity Clearing Model calibrated to Multi Commodity Exchange (MCX) Cotton benchmarks.
  * *Explainability:* Grad-CAM activation heatmaps highlighting fabric weave and seam contours.

---

## Slide 6: Product Demo & Platform Flow
1. **Snap & List:** Factory seller uploads fabric roll picture with 1-click sample presets.
2. **AI Vision & Valuation:** AI scans image, confirms fabric type, highlights any flaw line with red bounding box, and estimates resale price.
3. **Marketplace Discovery:** Buyers filter by fiber, price, hub, or run the AI Weighted Requirement Matcher ($Score = 0.35M + 0.25P + 0.20Q + 0.10C + 0.10L$).
4. **Checkout & Escrow:** Seamless checkout via UPI, Cards, Net Banking, or B2B NEFT in Razorpay sandbox.
5. **Logistics Stepper:** 5-stage live dispatch tracking (*Pending $\rightarrow$ Confirmed $\rightarrow$ Preparing $\rightarrow$ Dispatched $\rightarrow$ Delivered*).

---

## Slide 7: Business Model & Revenue Streams
* **5% Transaction Commission:** CUTLOOP charges a 5% commission on each completed transaction value paid by the seller.
* **Fulfillment Surcharge:** Flat ₹150 base delivery fee + weight tier handling margin.
* **Premium Seller Analytics (SaaS Tier):** ₹1,999/month for factories requiring regional demand forecasting, automated bulk CSV inventory sync, and priority buyer matching.
* **Quality Certification Lab Fee:** ₹499 per physical lab test swatch for luxury export-grade remnants.
* **Unit Economics (100 kg Lot):**
  * Average GMV per transaction: ₹5,000
  * Platform Commission (5%): ₹250
  * Fulfillment Margin: ₹75
  * Net Platform Revenue per Order: **₹325**

---

## Slide 8: Competitive Advantage & Moat
| Feature | Local Scrap Brokers ("Chindi") | General B2B (IndiaMART) | CUTLOOP |
| :--- | :---: | :---: | :---: |
| **AI Fabric Identification** | ❌ None | ❌ None | ✅ MobileNetV2 Vision |
| **Visual Surface Defect Detection**| ❌ Visual in-person only | ❌ None | ✅ Automated YOLO Bounding Box |
| **Instant Fair Price Guidance** | ❌ Arbitrary bargaining | ❌ Unregulated | ✅ Random Forest Regressor |
| **Digital Payment Escrow** | ❌ Cash informal | ❌ Offline direct | ✅ Instant UPI / Card Sandbox |
| **Environmental Impact Tracking**| ❌ None | ❌ None | ✅ Live CO₂ & Waste Diverted Metrics |

---

## Slide 9: Digital Marketing & Customer Acquisition Strategy
* **Direct Factory Cluster Onboarding:** Field representatives stationed in industrial GIDC estates (Narol, Vatva, Surat GIDC, Tirupur Netaji Apparel Park).
* **B2B Partnerships:** Partnering with Textile Associations (ATIRA, SIMA, CMAI) for zero-commission trial onboarding.
* **Digital Inbound Marketing:**
  * SEO content marketing targeting "surplus cotton fabric wholesale Ahmedabad", "deadstock denim rolls Gujarat".
  * LinkedIn B2B campaigns targeted at Sustainable Sourcing Directors & Design Heads.
* **Community Engagement:** Sponsoring student upcycling hackathons and circular fashion showcases at National Institute of Design (NID) and NIFT.

---

## Slide 10: Traction & MVP Validation (Bonus Proof)
* **Working Prototype:** Fully functional, publicly accessible web app hosted on global CDN.
* **Tested with 20 Real Users:** Documented beta trials conducted with 8 textile mill supervisors, 7 boutique fashion makers, and 5 academic evaluators.
* **Key Beta Findings:**
  * 100% of sellers preferred 1-click sample presets over manual multi-field forms.
  * AI defect detection prevented 4 mislabeled listings during trial.
  * Average transaction checkout completed in under 45 seconds.

---

## Slide 11: Financial Plan & Seed Fund Allocation (₹50,000 Budget)
* **Startup India Seed Fund Scheme (SISFS) / MVP Allocation:**
  * **Product Engineering & Cloud Infrastructure:** ₹20,000 (Hosting, SSL, database persistence, CI/CD).
  * **Dataset Collection & Lab Annotation:** ₹10,000 (Gathering and labeling 1,200 industrial fabric samples).
  * **Beta Logistics Trials & Sample Baling:** ₹10,000 (Fulfilling test swatch deliveries for 20 beta creators).
  * **DPIIT Registration & Trademark Filing:** ₹5,000 (Pvt. Ltd. incorporation, digital signature, trademark class 35).
  * **Contingency Buffer:** ₹5,000.
* **Break-Even Horizon:** Month 9 with 200 monthly active transactions generating ₹65,000 net monthly revenue.

---

## Slide 12: The Team & Vision
* **Product & Startup Lead:** Drives business vision, user interviews, and Lean Canvas execution.
* **Java Lead:** Architects Spring Boot backend, OOP class hierarchies, thread pools, and custom exception handlers.
* **Data Lead:** Collects datasets, performs EDA, trains pricing regression and time-series demand models.
* **AI Lead:** Trains MobileNetV2 and YOLO vision models, handles Grad-CAM explainability and fairness checks.
* **Marketing & Operations Lead:** Oversees seller cluster outreach, customer onboarding, and logistics workflows.
* **Vision:** *"To become India's primary operating system for circular industrial materials, ensuring zero fabric is buried or burned."*
