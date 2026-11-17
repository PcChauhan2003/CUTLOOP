package com.cutloop.controller;

import com.cutloop.model.AIAnalysis;
import com.cutloop.model.Material;
import com.cutloop.service.AIService;
import com.cutloop.service.MaterialService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/api/materials")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
@Slf4j
public class MaterialController {

    private final MaterialService materialService;
    private final AIService aiService;

    @GetMapping
    public ResponseEntity<List<Material>> getAllMaterials(
            @RequestParam(required = false) String type,
            @RequestParam(required = false) String colour,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) String q
    ) {
        if (type != null || colour != null || maxPrice != null || location != null || q != null) {
            return ResponseEntity.ok(materialService.searchMaterials(type, colour, maxPrice, location, q));
        }
        return ResponseEntity.ok(materialService.getAllActiveMaterials());
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getMaterialById(@PathVariable Long id) {
        return materialService.getMaterialById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/seller/{sellerId}")
    public ResponseEntity<List<Material>> getSellerMaterials(@PathVariable Long sellerId) {
        return ResponseEntity.ok(materialService.getMaterialsBySeller(sellerId));
    }

    /**
     * Requirement 7.4: AI Material Matching endpoint
     */
    @GetMapping("/match")
    public ResponseEntity<List<Map<String, Object>>> matchMaterials(
            @RequestParam(required = false) String material,
            @RequestParam(required = false) BigDecimal budget,
            @RequestParam(required = false) BigDecimal quantity,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) String condition
    ) {
        List<Map<String, Object>> results = materialService.matchMaterials(
                material, budget, quantity, location, condition
        );
        return ResponseEntity.ok(results);
    }

    @PostMapping
    public ResponseEntity<Material> createMaterial(@RequestBody Material material) {
        Material saved = materialService.createMaterial(material);
        return ResponseEntity.ok(saved);
    }

    /**
     * Vertical Slice Milestone:
     * Seller uploads fabric image -> Java saves listing -> Python analyses image in background -> AI results stored.
     */
    @PostMapping("/upload-and-analyze")
    public ResponseEntity<?> uploadAndAnalyze(
            @RequestParam("file") MultipartFile file,
            @RequestParam("sellerId") Long sellerId,
            @RequestParam("materialName") String materialName,
            @RequestParam(value = "condition", defaultValue = "Good") String condition,
            @RequestParam(value = "quantityKg", defaultValue = "50") BigDecimal quantityKg,
            @RequestParam(value = "pricePerKg", defaultValue = "50") BigDecimal pricePerKg,
            @RequestParam(value = "location", defaultValue = "Ahmedabad") String location,
            @RequestParam(value = "description", required = false) String description
    ) {
        try {
            // 1. Save listing draft
            Material material = Material.builder()
                    .sellerId(sellerId)
                    .materialName(materialName)
                    .materialType("Analyzing...")
                    .colour("Standard")
                    .conditionType(condition)
                    .quantityKg(quantityKg)
                    .pricePerKg(pricePerKg)
                    .location(location)
                    .description(description)
                    .primaryImageUrl("/images/uploads/" + file.getOriginalFilename())
                    .build();

            Material savedMaterial = materialService.createMaterial(material);

            // 2. Multithreaded background call to Python AI Service
            byte[] fileBytes = file.getBytes();
            CompletableFuture<AIAnalysis> futureAnalysis = aiService.analyzeMaterialImageAsync(
                    savedMaterial.getId(),
                    fileBytes,
                    file.getOriginalFilename(),
                    condition,
                    quantityKg,
                    location
            );

            return ResponseEntity.ok(Map.of(
                    "status", "SUBMITTED_FOR_ANALYSIS",
                    "materialId", savedMaterial.getId(),
                    "material", savedMaterial,
                    "message", "Material draft created and AI classification pipeline queued."
            ));

        } catch (Exception e) {
            log.error("Failed to process upload and analysis", e);
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
}
