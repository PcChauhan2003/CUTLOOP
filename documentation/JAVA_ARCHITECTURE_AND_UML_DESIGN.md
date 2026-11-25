# CUTLOOP — Java Architecture & UML Design Document
**Integrated Assignment | JG University — 5th Semester B.Tech**
**Subject Covered:** Java Core & Enterprise Backend (20 Marks)

---

## 1. Object-Oriented Design & Domain Architecture

The CUTLOOP backend is developed in **Java 21** using the **Spring Boot 3.x** framework, following clean domain-driven architecture and strict SOLID principles.

### 1.1 Inheritance & Class Hierarchy
```
                        +--------------------+
                        |     <<abstract>>   |
                        |        User        |
                        +--------------------+
                        | - id: Long         |
                        | - fullName: String |
                        | - email: String    |
                        | - passwordHash: Str|
                        | - role: UserRole   |
                        | - createdAt: Instant|
                        +--------------------+
                                   ▲
          +------------------------+------------------------+
          |                                                 |
+--------------------+                            +--------------------+
|       Buyer        |                            |       Seller       |
+--------------------+                            +--------------------+
| - shippingAddress  |                            | - companyName: Str |
| - organizationType |                            | - gstNumber: Str   |
| - totalOrdersPlaced|                            | - warehouseCity:Str|
| - preferredFabrics |                            | - verifiedMill:Bool|
+--------------------+                            +--------------------+
          |
+--------------------+
|       Admin        |
+--------------------+
| - department: Str  |
| - auditClearanceLvl|
| - moderationCount  |
+--------------------+
```

### 1.2 Core Domain Entities & Relationships
1. **Material (Entity):** Encapsulates leftover textile batch properties (`materialType`, `condition`, `quantityKg`, `pricePerKg`, `sellerId`).
2. **Inventory (Entity):** Tracks real-time warehouse physical availability and reservation locks.
3. **Cart & CartItem:** Session and user-bound shopping cart supporting dynamic order assembly.
4. **Order & OrderItem:** Purchase orders capturing buyer, seller, line items, timestamps, and 5-stage logistics state.
5. **Payment (Entity):** Captures financial transaction reference, payment gateway channel (UPI, Card, Net Banking, NEFT), and settlement status.
6. **AIAnalysis (Entity):** Stores MobileNetV2 classification probability vectors, YOLO defect bounding boxes, and Grad-CAM metadata.

---

## 2. Interfaces & Design Patterns

| Design Pattern | Implementation in CUTLOOP | Interface / Class |
| :--- | :--- | :--- |
| **Strategy Pattern** | Payment Processing Engine | `PaymentProcessor` interface implemented by `RazorpayPaymentProcessor`, `UpiPaymentProcessor`, `NeftEscrowProcessor`. |
| **Repository Pattern** | Decouples data persistence from business logic | `MaterialRepository`, `OrderRepository`, `UserRepository` extending `JpaRepository`. |
| **Observer / Async** | Multithreaded Event Dispatching | `OrderEventListener` notified asynchronously on state transitions. |
| **Factory Pattern** | Instantiates role-specific user instances | `UserFactory.createUser(role, dto)` |

---

## 3. Custom Exception Handling

CUTLOOP implements specific custom runtime exceptions to handle realistic e-commerce and industrial scenarios with clear HTTP error mapping:

```java
package com.cutloop.exception;

// 1. Thrown when a buyer attempts to purchase more volume than currently available in warehouse
public class InsufficientStockException extends RuntimeException {
    public InsufficientStockException(String message) {
        super(message);
    }
}

// 2. Thrown when a bank gateway authorization fails, OTP is invalid, or 3D-secure times out
public class PaymentFailedException extends RuntimeException {
    public PaymentFailedException(String message) {
        super(message);
    }
}

// 3. Thrown when a seller submits a material batch with negative weight or invalid specs
public class InvalidMaterialException extends RuntimeException {
    public InvalidMaterialException(String message) {
        super(message);
    }
}
```

### 3.1 Global Exception Handler (`@RestControllerAdvice`)
* Translates domain exceptions into structured JSON responses (`timestamp`, `status`, `error`, `message`, `path`).
* Prevents leaking internal database stack traces or SQL exceptions to platform clients.

---

## 4. Multithreading & Asynchronous Processing

* **Configuration:** `AsyncConfig.java` defines a dedicated `ThreadPoolTaskExecutor`:
  ```java
  @Bean(name = "cutloopTaskExecutor")
  public Executor taskExecutor() {
      ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
      executor.setCorePoolSize(4);
      executor.setMaxPoolSize(10);
      executor.setQueueCapacity(100);
      executor.setThreadNamePrefix("CutloopAsync-");
      executor.initialize();
      return executor;
  }
  ```
* **Real-World Multithreaded Tasks:**
  1. **Simultaneous Order Processing:** Concurrent transactions execute inside `@Transactional(isolation = Isolation.SERIALIZABLE)` locks to prevent overselling race conditions.
  2. **Background AI Image Classification:** Heavy visual inference requests are queued asynchronously without blocking the user checkout thread.
  3. **Logistics Notification Pipeline:** Dispatch status emails and SMS notifications run on asynchronous worker threads.

---

## 5. File Management & Data Export

1. **Persistent CSV File Export:** `InventoryService.exportInventoryToCSV(Long sellerId)` iterates active inventory and generates a comma-separated stream with RFC 4180 escaping.
2. **Batch CSV Import:** `InventoryService.importInventoryFromCSV(MultipartFile file)` parses bulk factory catalog uploads, performs schema validation, and inserts new `Material` records in bulk.
3. **Local Image Binary Storage:** Uploaded fabric photographs are stored securely under `frontend/images/materials/` with hashed filenames to avoid path traversal vulnerabilities.
