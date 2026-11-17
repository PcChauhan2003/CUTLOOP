package com.cutloop.model;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "materials")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Material {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long sellerId;

    @Column(nullable = false, length = 200)
    private String materialName;

    @Column(nullable = false, length = 100)
    private String materialType; // Cotton, Denim, Polyester, Silk, Wool, Linen

    @Column(nullable = false, length = 50)
    private String colour;

    @Column(nullable = false, length = 50)
    private String conditionType; // New, Good, Fair, Poor

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal quantityKg;

    @Column(nullable = false, precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal minimumOrderKg = BigDecimal.valueOf(5.0);

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal pricePerKg;

    @Column(precision = 10, scale = 2)
    private BigDecimal suggestedPriceMin;

    @Column(precision = 10, scale = 2)
    private BigDecimal suggestedPriceMax;

    @Column(precision = 6, scale = 2)
    private BigDecimal widthInches;

    @Column(nullable = false, length = 150)
    private String location;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 40)
    @Builder.Default
    private MaterialStatus status = MaterialStatus.ACTIVE;

    @Column(length = 500)
    private String primaryImageUrl;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
