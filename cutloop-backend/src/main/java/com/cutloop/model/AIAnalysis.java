package com.cutloop.model;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "ai_analysis")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AIAnalysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long materialId;

    @Column(nullable = false, length = 100)
    private String modelName;

    @Column(length = 100)
    private String predictedClass;

    @Column(precision = 6, scale = 4)
    private BigDecimal confidence;

    @Column(columnDefinition = "TEXT")
    private String otherPredictionsJson;

    @Builder.Default
    private Boolean defectDetected = false;

    @Column(columnDefinition = "TEXT")
    private String defectsJson;

    @Column(precision = 10, scale = 2)
    private BigDecimal suggestedPrice;

    @Column(precision = 10, scale = 2)
    private BigDecimal suggestedPriceMin;

    @Column(precision = 10, scale = 2)
    private BigDecimal suggestedPriceMax;

    @Column(length = 500)
    private String gradcamImageUrl;

    @Column(length = 40)
    @Builder.Default
    private String analysisStatus = "COMPLETED";

    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }
}
