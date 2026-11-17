package com.cutloop.config;

import com.cutloop.model.*;
import com.cutloop.repository.InventoryRepository;
import com.cutloop.repository.MaterialRepository;
import com.cutloop.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;

import java.math.BigDecimal;

@Configuration
@RequiredArgsConstructor
@Slf4j
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final MaterialRepository materialRepository;
    private final InventoryRepository inventoryRepository;

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            log.info("Database already seeded with {} users.", userRepository.count());
            return;
        }

        log.info("Seeding initial CUTLOOP demo data...");

        // 1. Seed Users
        User admin = User.builder()
                .fullName("Admin Moderation Team")
                .email("admin@cutloop.com")
                .passwordHash("password123")
                .phone("+919876543210")
                .role(UserRole.ADMIN)
                .build();
        userRepository.save(admin);

        User seller1 = User.builder()
                .fullName("Gujarat Textile Mills (Rajesh)")
                .email("rajesh@gujarattextiles.com")
                .passwordHash("password123")
                .phone("+919825000001")
                .role(UserRole.SELLER)
                .build();
        User savedSeller1 = userRepository.save(seller1);

        User seller2 = User.builder()
                .fullName("Surat Fabric Hub (Vikram)")
                .email("vikram@suratfabric.in")
                .passwordHash("password123")
                .phone("+919825000002")
                .role(UserRole.SELLER)
                .build();
        User savedSeller2 = userRepository.save(seller2);

        User buyer1 = User.builder()
                .fullName("Aarti Sharma - Artisans Studio")
                .email("aarti@craftstudio.in")
                .passwordHash("password123")
                .phone("+919825000003")
                .role(UserRole.BUYER)
                .build();
        userRepository.save(buyer1);

        User buyer2 = User.builder()
                .fullName("GreenThreads Apparel (Pooja)")
                .email("pooja@greenthreads.org")
                .passwordHash("password123")
                .phone("+919825000004")
                .role(UserRole.BUYER)
                .build();
        userRepository.save(buyer2);

        // 2. Seed Initial Materials
        seedMaterial(savedSeller1.getId(), "Surplus Raw Cotton Fabric Rolls", "Cotton", "Blue", "Good",
                BigDecimal.valueOf(120.0), BigDecimal.valueOf(45.0), BigDecimal.valueOf(42.0), BigDecimal.valueOf(48.0),
                "Ahmedabad", "High quality 100% natural cotton cut-offs from shirting production.", "/images/samples/cotton_blue.jpg");

        seedMaterial(savedSeller1.getId(), "Stonewashed Indigo Denim Offcuts", "Denim", "Blue", "Good",
                BigDecimal.valueOf(85.0), BigDecimal.valueOf(62.0), BigDecimal.valueOf(58.0), BigDecimal.valueOf(65.0),
                "Ahmedabad", "Heavyweight 12oz denim leftovers, ideal for tote bags and jackets.", "/images/samples/denim_indigo.jpg");

        seedMaterial(savedSeller2.getId(), "Pure Mulberry Raw Silk Scraps", "Silk", "Ivory", "New",
                BigDecimal.valueOf(35.0), BigDecimal.valueOf(120.0), BigDecimal.valueOf(110.0), BigDecimal.valueOf(130.0),
                "Surat", "Premium mulberry silk remnants from saree border trimming.", "/images/samples/silk_ivory.jpg");

        seedMaterial(savedSeller2.getId(), "Organic Breathable Linen Remnants", "Linen", "Natural Beige", "Good",
                BigDecimal.valueOf(60.0), BigDecimal.valueOf(75.0), BigDecimal.valueOf(70.0), BigDecimal.valueOf(80.0),
                "Surat", "Pre-washed pure linen rolls from luxury summer collection overruns.", "/images/samples/linen_beige.jpg");

        seedMaterial(savedSeller1.getId(), "Recycled Polyester Mesh Fabric", "Polyester", "Black", "Good",
                BigDecimal.valueOf(150.0), BigDecimal.valueOf(38.0), BigDecimal.valueOf(35.0), BigDecimal.valueOf(42.0),
                "Ahmedabad", "Lightweight polyester mesh remnants suitable for lining and activewear.", "/images/samples/polyester_black.jpg");

        log.info("Database seeding complete. Seeded {} materials and {} users.",
                materialRepository.count(), userRepository.count());
    }

    private void seedMaterial(
            Long sellerId, String name, String type, String colour, String condition,
            BigDecimal qty, BigDecimal price, BigDecimal priceMin, BigDecimal priceMax,
            String location, String desc, String imgUrl
    ) {
        Material m = Material.builder()
                .sellerId(sellerId)
                .materialName(name)
                .materialType(type)
                .colour(colour)
                .conditionType(condition)
                .quantityKg(qty)
                .minimumOrderKg(BigDecimal.valueOf(5.0))
                .pricePerKg(price)
                .suggestedPriceMin(priceMin)
                .suggestedPriceMax(priceMax)
                .location(location)
                .description(desc)
                .primaryImageUrl(imgUrl)
                .status(MaterialStatus.ACTIVE)
                .build();
        Material saved = materialRepository.save(m);

        Inventory inv = Inventory.builder()
                .materialId(saved.getId())
                .availableQuantityKg(qty)
                .reservedQuantityKg(BigDecimal.ZERO)
                .soldQuantityKg(BigDecimal.ZERO)
                .build();
        inventoryRepository.save(inv);
    }
}
