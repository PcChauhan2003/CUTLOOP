# CUTLOOP — E-Commerce Architecture, Security & Digital Marketing Plan
**Integrated Assignment | JG University — 5th Semester B.Tech**
**Subject Covered:** E-Commerce & Web Platforms (10 Marks)

---

## 1. Platform Flow & User Journeys

```
+-----------------------------------------------------------------------------------+
|                              CUTLOOP PLATFORM FLOW                                |
+-----------------------------------------------------------------------------------+
       │
       ▼
 [ Home Page ] ───► [ Sustainability Metrics (CO₂ & Waste Diverted) ]
       │
       ├─────────────────────────────────┬─────────────────────────────────┐
       ▼                                 ▼                                 ▼
[ Browse Marketplace ]         [ AI Fabric Scanner ]            [ Seller Dashboard ]
       │                                 │                                 │
       ▼                                 ▼                                 ▼
[ Filter / AI Matcher ]        [ MobileNetV2 Weave + ]          [ 1-Click Material ]
       │                       [ YOLO Defect Bounding]          [ Inventory Upload ]
       ▼                                 │                                 │
[ Product Detail Page ] ◄────────────────┘                                 ▼
       │                                                        [ Manage Factory Orders]
       ▼
 [ Shopping Cart ]
       │
       ▼
[ Select Payment Method ] (UPI · Card · Net Banking · B2B NEFT)
       │
       ▼
[ Razorpay Sandbox Gateway ] ───► [ OTP Simulation: 123456 ]
       │
       ▼
[ Order Confirmed & Receipt ]
       │
       ▼
[ 5-Stage Logistics Stepper ] (Pending ➔ Confirmed ➔ Preparing ➔ Dispatched ➔ Delivered)
```

---

## 2. Revenue Model & Commercial Viability

1. **Transaction Commission (5%):** Automatically deducted from seller payouts upon successful order delivery.
2. **Logistics Fulfillment Margin:** Flat ₹150 base delivery fee + tiered weight margin.
3. **SaaS Analytics Subscription:** ₹1,999/month for factories needing automated CSV batch synchronization and predictive regional demand forecasts.
4. **Physical Quality Verification Testing:** Optional ₹499 fee per lot for third-party lab GSM/tensile certification.

---

## 3. Payment Approach & Gateway Integration

* **Sandbox Gateway:** Complete Razorpay Test Gateway integration supporting 4 modern Indian B2B payment modalities:
  * **Instant UPI:** Dynamic QR code simulation and VPA handler (Google Pay, PhonePe, Paytm, BHIM).
  * **Credit / Debit Cards:** Visa, Mastercard, and RuPay card simulation with CVV and expiry validation.
  * **Net Banking:** Direct simulation of top Indian corporate banking channels (SBI, HDFC, ICICI, Axis).
  * **B2B NEFT / RTGS Escrow:** Virtual industrial escrow account with unique IFSC code for transactions exceeding ₹50,000.
* **Failure Handling:** Integrated toggle testing `PaymentFailedException` ensuring zero inventory is deducted if a transaction declines.

---

## 4. Regional Logistics & Delivery Plan

* **Four Active Hubs:**
  * **Western Cluster:** Ahmedabad (Narol/Vatva) & Surat (Ring Road Fabric Hub).
  * **Southern Cluster:** Tirupur (Netaji Apparel Park).
  * **Northern Cluster:** Ludhiana (Industrial Area A).
* **3PL Integration:** Contracted with B2B cargo logistics carriers (Delhivery Cargo, V-Trans, SpotOn) with guaranteed 48-hour pickup from textile mills.
* **5-Stage Tracking:** Transparent status progression visible to both buyer and seller.

---

## 5. Digital Marketing & Customer Acquisition Plan

* **Cluster In-Person Direct Sales:** Onboarding 30 primary mills across Narol and Surat via direct association seminars (ATIRA).
* **B2B Content Marketing & SEO:** High-intent search ranking for *"surplus fabric wholesale Ahmedabad"*, *"cotton cutoffs supplier Surat"*, *"deadstock fabric bulk"*.
* **LinkedIn Creator Outreach:** Partnering with 50 sustainable fashion designers and zero-waste studios in Bangalore and Mumbai.
* **Circular Fashion Grant:** Monthly ₹25,000 fabric scholarship awarded to emerging sustainable student fashion designers.

---

## 6. Legal & Security Checklist (Ethics & Compliance)

| Requirement | CUTLOOP Implementation | Compliance Status |
| :--- | :--- | :---: |
| **Data Privacy & Minimization** | No personal phone numbers or residential addresses displayed publicly. Only city/cluster locations visible until order confirmation. | ✅ Compliant (DPDP Act 2023) |
| **Authentication Security** | BCrypt cryptographic salted hashing on all stored user passwords. | ✅ Compliant |
| **Anti-Fake Review Protection** | Product reviews strictly locked to confirmed database `orderId` records. Non-buyers cannot post reviews. | ✅ Enforced in Domain Logic |
| **Zero Dark Patterns** | No hidden checkout fees, no pre-selected unwanted add-ons, transparent price per kg, clear cancel buttons. | ✅ Guidelines Compliant |
| **Inspection Disclaimer** | Prominent warning that smartphone image inspection is visual surface review only and does not replace lab tensile testing. | ✅ Displayed on Details Modal |
