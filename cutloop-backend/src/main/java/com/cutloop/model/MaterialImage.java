package com.cutloop.model;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "material_images")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MaterialImage {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long materialId;

    @Column(nullable = false, length = 500)
    private String imageUrl;

    @Builder.Default
    private Boolean isPrimary = false;

    private LocalDateTime uploadedAt;

    @PrePersist
    protected void onCreate() {
        if (uploadedAt == null) {
            uploadedAt = LocalDateTime.now();
        }
    }
}
