-- =========================================================
-- CUTLOOP - Industrial Waste-to-Value Marketplace Database
-- Database Name: cutloop_db
-- =========================================================

CREATE DATABASE IF NOT EXISTS cutloop_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE cutloop_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('BUYER', 'SELLER', 'ADMIN') NOT NULL DEFAULT 'BUYER',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_role (role)
);

-- 2. Seller Profiles
CREATE TABLE IF NOT EXISTS seller_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE NOT NULL,
    company_name VARCHAR(200) NOT NULL,
    gst_number VARCHAR(50),
    factory_address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(20) NOT NULL,
    total_listings INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 5.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Buyer Profiles
CREATE TABLE IF NOT EXISTS buyer_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE NOT NULL,
    organization_name VARCHAR(200),
    industry_type VARCHAR(100),
    shipping_address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Materials (Leftover listings)
CREATE TABLE IF NOT EXISTS materials (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    seller_id BIGINT NOT NULL,
    material_name VARCHAR(200) NOT NULL,
    material_type VARCHAR(100) NOT NULL, -- Cotton, Denim, Polyester, Silk, Wool, Linen, etc.
    colour VARCHAR(50) NOT NULL,
    condition_type VARCHAR(50) NOT NULL, -- New, Good, Fair, Poor
    quantity_kg DECIMAL(10,2) NOT NULL,
    minimum_order_kg DECIMAL(10,2) NOT NULL DEFAULT 5.00,
    price_per_kg DECIMAL(10,2) NOT NULL,
    suggested_price_min DECIMAL(10,2),
    suggested_price_max DECIMAL(10,2),
    width_inches DECIMAL(6,2),
    location VARCHAR(150) NOT NULL,
    description TEXT,
    status ENUM('DRAFT', 'ACTIVE', 'SOLD', 'SUSPENDED') NOT NULL DEFAULT 'ACTIVE',
    primary_image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_material_type (material_type),
    INDEX idx_material_status (status),
    INDEX idx_material_location (location)
);

-- 5. Material Images
CREATE TABLE IF NOT EXISTS material_images (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    material_id BIGINT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
);

-- 6. AI Analysis Results
CREATE TABLE IF NOT EXISTS ai_analysis (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    material_id BIGINT NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    predicted_class VARCHAR(100),
    confidence DECIMAL(6,4),
    other_predictions_json JSON,
    defect_detected BOOLEAN DEFAULT FALSE,
    defects_json JSON,
    suggested_price DECIMAL(10,2),
    suggested_price_min DECIMAL(10,2),
    suggested_price_max DECIMAL(10,2),
    gradcam_image_url VARCHAR(500),
    analysis_status ENUM('PENDING', 'COMPLETED', 'FAILED') DEFAULT 'COMPLETED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
);

-- 7. Inventory Tracking
CREATE TABLE IF NOT EXISTS inventory (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    material_id BIGINT UNIQUE NOT NULL,
    available_quantity_kg DECIMAL(10,2) NOT NULL,
    reserved_quantity_kg DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    sold_quantity_kg DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
);

-- 8. Shopping Carts
CREATE TABLE IF NOT EXISTS carts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 9. Cart Items
CREATE TABLE IF NOT EXISTS cart_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cart_id BIGINT NOT NULL,
    material_id BIGINT NOT NULL,
    quantity_kg DECIMAL(10,2) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
    UNIQUE KEY uq_cart_material (cart_id, material_id)
);

-- 10. Orders
CREATE TABLE IF NOT EXISTS orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    buyer_id BIGINT NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    delivery_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    platform_commission DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL,
    total_kg DECIMAL(10,2) NOT NULL,
    order_status ENUM('PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    shipping_address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 11. Order Items (Snapshot historical price)
CREATE TABLE IF NOT EXISTS order_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    material_id BIGINT NOT NULL,
    material_name VARCHAR(200) NOT NULL,
    seller_id BIGINT NOT NULL,
    quantity_kg DECIMAL(10,2) NOT NULL,
    price_per_kg DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(id),
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- 12. Payments
CREATE TABLE IF NOT EXISTS payments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT UNIQUE NOT NULL,
    transaction_reference VARCHAR(100) UNIQUE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    payment_method VARCHAR(50) DEFAULT 'SIMULATED_GATEWAY',
    payment_status ENUM('INITIATED', 'SUCCESS', 'FAILED', 'REFUNDED') DEFAULT 'INITIATED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- 13. Demand History & Search Trends
CREATE TABLE IF NOT EXISTS demand_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    month_year VARCHAR(20) NOT NULL,
    material_type VARCHAR(100) NOT NULL,
    search_count INT DEFAULT 0,
    listing_count INT DEFAULT 0,
    order_count INT DEFAULT 0,
    average_price DECIMAL(10,2) DEFAULT 0.00,
    season VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. Buyer Reviews
CREATE TABLE IF NOT EXISTS reviews (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    material_id BIGINT NOT NULL,
    buyer_id BIGINT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 15. Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    type VARCHAR(50) DEFAULT 'INFO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 16. Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(50),
    entity_id BIGINT,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- SEED DATA FOR IMMEDIATE VERTICAL SLICE & TESTING
-- =========================================================

-- Seed Users (Password is bcrypt for 'password123')
INSERT INTO users (id, full_name, email, password_hash, phone, role) VALUES
(1, 'Admin Moderation Team', 'admin@cutloop.com', '$2a$10$7vN34tH6W5E3j3hK8BwQ7OHiJb9Z6E6RkL9uE9wY1k2Z3w4x5y6z.', '+919876543210', 'ADMIN'),
(2, 'Gujarat Textile Mills (Rajesh)', 'rajesh@gujarattextiles.com', '$2a$10$7vN34tH6W5E3j3hK8BwQ7OHiJb9Z6E6RkL9uE9wY1k2Z3w4x5y6z.', '+919825000001', 'SELLER'),
(3, 'Surat Fabric Hub (Vikram)', 'vikram@suratfabric.in', '$2a$10$7vN34tH6W5E3j3hK8BwQ7OHiJb9Z6E6RkL9uE9wY1k2Z3w4x5y6z.', '+919825000002', 'SELLER'),
(4, 'Aarti Sharma - Artisans Co', 'aarti@craftstudio.in', '$2a$10$7vN34tH6W5E3j3hK8BwQ7OHiJb9Z6E6RkL9uE9wY1k2Z3w4x5y6z.', '+919825000003', 'BUYER'),
(5, 'GreenThreads Apparel (Pooja)', 'pooja@greenthreads.org', '$2a$10$7vN34tH6W5E3j3hK8BwQ7OHiJb9Z6E6RkL9uE9wY1k2Z3w4x5y6z.', '+919825000004', 'BUYER')
ON DUPLICATE KEY UPDATE full_name=VALUES(full_name);

INSERT INTO seller_profiles (user_id, company_name, gst_number, factory_address, city, state, pincode, total_listings) VALUES
(2, 'Gujarat Textile Mills', '24AAACG1234F1Z5', 'Plot 42, Narol Industrial Area', 'Ahmedabad', 'Gujarat', '382405', 3),
(3, 'Surat Fabric Hub', '24AABCS5678K1Z8', 'GIDC Pandesara, Surat', 'Surat', 'Gujarat', '394221', 2)
ON DUPLICATE KEY UPDATE company_name=VALUES(company_name);

INSERT INTO buyer_profiles (user_id, organization_name, industry_type, shipping_address, city, state, pincode) VALUES
(4, 'Artisans Craft Studio', 'Handmade Craft & Bags', '14 Green Park Society, Ambawadi', 'Ahmedabad', 'Gujarat', '380015'),
(5, 'GreenThreads Upcycled Fashion', 'Sustainable Apparel', '102 Indiranagar 100ft Road', 'Bengaluru', 'Karnataka', '560038')
ON DUPLICATE KEY UPDATE organization_name=VALUES(organization_name);

-- Seed Materials
INSERT INTO materials (id, seller_id, material_name, material_type, colour, condition_type, quantity_kg, minimum_order_kg, price_per_kg, suggested_price_min, suggested_price_max, width_inches, location, description, status, primary_image_url) VALUES
(1, 2, 'Surplus Raw Cotton Fabric Rolls', 'Cotton', 'Blue', 'Good', 120.00, 10.00, 45.00, 42.00, 48.00, 60.0, 'Ahmedabad', 'High quality 100% natural cotton cut-offs from shirting production. Clean and dry stored.', 'ACTIVE', '/images/samples/cotton_blue.jpg'),
(2, 2, 'Stonewashed Indigo Denim Offcuts', 'Denim', 'Blue', 'Good', 85.00, 15.00, 62.00, 58.00, 65.00, 58.0, 'Ahmedabad', 'Heavyweight 12oz denim leftovers, ideal for tote bags, jackets, and accessories.', 'ACTIVE', '/images/samples/denim_indigo.jpg'),
(3, 3, 'Pure Mulberry Raw Silk Scraps', 'Silk', 'Ivory', 'New', 35.00, 5.00, 120.00, 110.00, 130.00, 44.0, 'Surat', 'Premium mulberry silk remnants from saree border trimming. High sheen, unblemished.', 'ACTIVE', '/images/samples/silk_ivory.jpg'),
(4, 3, 'Organic Breathable Linen Remnants', 'Linen', 'Natural Beige', 'Good', 60.00, 10.00, 75.00, 70.00, 80.00, 54.0, 'Surat', 'Pre-washed pure linen rolls from luxury summer collection overruns.', 'ACTIVE', '/images/samples/linen_beige.jpg'),
(5, 2, 'Recycled Polyester Mesh Fabric', 'Polyester', 'Black', 'Good', 150.00, 20.00, 38.00, 35.00, 42.00, 62.0, 'Ahmedabad', 'Lightweight polyester mesh remnants suitable for lining, activewear, and pocket bags.', 'ACTIVE', '/images/samples/polyester_black.jpg')
ON DUPLICATE KEY UPDATE material_name=VALUES(material_name);

-- Seed Inventory
INSERT INTO inventory (material_id, available_quantity_kg, reserved_quantity_kg, sold_quantity_kg) VALUES
(1, 120.00, 0.00, 0.00),
(2, 85.00, 0.00, 0.00),
(3, 35.00, 0.00, 0.00),
(4, 60.00, 0.00, 0.00),
(5, 150.00, 0.00, 0.00)
ON DUPLICATE KEY UPDATE available_quantity_kg=VALUES(available_quantity_kg);

-- Seed AI Analysis
INSERT INTO ai_analysis (material_id, model_name, predicted_class, confidence, other_predictions_json, defect_detected, defects_json, suggested_price, suggested_price_min, suggested_price_max) VALUES
(1, 'MobileNetV2-FabricClassifier', 'Cotton', 0.9420, '{"Denim": 0.031, "Linen": 0.017, "Polyester": 0.006}', FALSE, '[]', 45.00, 42.00, 48.00),
(2, 'MobileNetV2-FabricClassifier', 'Denim', 0.9650, '{"Cotton": 0.022, "Polyester": 0.008}', TRUE, '[{"defect": "Broken thread", "confidence": 0.88, "bbox": [120, 140, 210, 260]}]', 62.00, 58.00, 65.00),
(3, 'MobileNetV2-FabricClassifier', 'Silk', 0.9810, '{"Polyester": 0.012, "Linen": 0.004}', FALSE, '[]', 120.00, 110.00, 130.00)
ON DUPLICATE KEY UPDATE predicted_class=VALUES(predicted_class);
