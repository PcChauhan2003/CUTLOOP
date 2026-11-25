# CUTLOOP Java Backend — Installation, Configuration & Execution Guide

**Document Reference:** `submission/03_java/JAVA_README.md`  
**Application Component:** `CUTLOOP/cutloop-backend`  
**Language & Framework:** Java 21 LTS / Spring Boot 3.2.x  

---

## 1. Prerequisites

Before running the CUTLOOP Java backend, ensure the following software tools are installed:

* **Java Development Kit (JDK):** Version 21 (LTS) or higher (`Eclipse Temurin 21` or `Oracle JDK 21`).
  ```bash
  java -version
  # Expected output: openjdk version "21.x.x" ...
  ```
* **Apache Maven:** Version 3.8.x or 3.9.x.
  ```bash
  mvn -version
  ```
* **Git:** For source control repository management.
* **Database (Optional for testing):** In-memory H2 database is enabled by default. For production MySQL testing, MySQL Server 8.0+ is supported.

---

## 2. Directory & Source Layout
The Java source code is located at:
```text
c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\cutloop-backend\
├── pom.xml
└── src\
    ├── main\
    │   ├── java\com\cutloop\       # Source packages (config, controller, model, service)
    │   └── resources\
    │       ├── application.properties         # Default profile (H2 in-memory DB)
    │       └── application-mysql.properties   # Production MySQL profile
    └── test\
        └── java\com\cutloop\       # Automated unit tests
```

---

## 3. Configuration Profiles

### 3.1 Default Academic Profile (`application.properties`)
Configured out-of-the-box for academic demonstration and zero-setup evaluation using the in-memory H2 database:

```properties
spring.application.name=cutloop-backend
server.port=8080

# In-memory H2 Database configuration
spring.datasource.url=jdbc:h2:mem:cutloopdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# JPA & Hibernate Settings
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false

# H2 Web Console (Accessible at http://localhost:8080/h2-console)
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

# Python AI Microservice URL
cutloop.ai.service.url=http://localhost:8000
```

### 3.2 Production MySQL Profile (`application-mysql.properties`)
To run against a local MySQL database:
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=mysql
```

---

## 4. Compilation & Execution

### 4.1 Build with Maven
Navigate to the `cutloop-backend` directory and compile the application:
```powershell
cd c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\cutloop-backend
mvn clean compile
```

### 4.2 Run the Application
Start the Spring Boot application on port `8080`:
```powershell
mvn spring-boot:run
```

Once started, the console will confirm:
```text
[main] com.cutloop.CutloopApplication : Started CutloopApplication in 2.85 seconds (process running for 3.2)
[main] com.cutloop.config.DataInitializer : Seeded 12 sample fabric listings across 4 scrap grades
```

---

## 5. Automated Testing & Verification

Run the comprehensive JUnit test suite:
```powershell
mvn test
```

### Test Coverage Highlights:
1. **User Authentication Tests:** Validates password hashing and session token issuance.
2. **Inventory Stock Tests:** Confirms `InsufficientStockException` is thrown when order quantity exceeds physical inventory.
3. **CSV Export Tests:** Verifies that `exportInventoryToCsv()` generates valid RFC 4180 comma-separated records.
4. **Multithreaded AI Dispatch Tests:** Verifies that `AIService` asynchronously handles background analysis requests without blocking HTTP workers.

---

## 6. Key Endpoints Quick Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `http://localhost:8080/api/health` | Backend service health and database connection status |
| `GET` | `http://localhost:8080/api/materials` | Retrieve active surplus fabric listings |
| `POST`| `http://localhost:8080/api/materials/upload-and-analyze` | Multipart listing upload + background AI analysis |
| `GET` | `http://localhost:8080/api/inventory/export-csv` | Download complete inventory CSV report |
| `POST`| `http://localhost:8080/api/inventory/import-csv` | Upload CSV file to bulk import fabric listings |
| `POST`| `http://localhost:8080/api/orders` | Submit cart checkout order |
| `POST`| `http://localhost:8080/api/payment/process` | Execute simulated sandbox payment |

---

## 7. Troubleshooting

* **Port 8080 in use:** If port 8080 is occupied by another application, pass a custom port parameter:
  ```powershell
  mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=8082"
  ```
* **AI Service Unreachable:** If the Python FastAPI service is offline, the Java `AIService` automatically logs a warning and enters **Fallback Mode**, saving the material listing as a draft without crashing the user interface.
* **H2 Console Access:** Visit `http://localhost:8080/h2-console`, set JDBC URL to `jdbc:h2:mem:cutloopdb`, and username to `sa` (password blank) to inspect tables directly.
