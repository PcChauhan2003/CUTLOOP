package com.cutloop.service;

import com.cutloop.model.Inventory;
import com.cutloop.model.Material;
import com.cutloop.model.MaterialStatus;
import com.cutloop.repository.InventoryRepository;
import com.cutloop.repository.MaterialRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class MaterialService {

    private final MaterialRepository materialRepository;
    private final InventoryRepository inventoryRepository;

    @Transactional(readOnly = true)
    public List<Material> getAllActiveMaterials() {
        return materialRepository.findByStatus(MaterialStatus.ACTIVE);
    }

    @Transactional(readOnly = true)
    public Optional<Material> getMaterialById(Long id) {
        return materialRepository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Material> getMaterialsBySeller(Long sellerId) {
        return materialRepository.findBySellerId(sellerId);
    }

    @Transactional
    public Material createMaterial(Material material) {
        if (material.getStatus() == null) {
            material.setStatus(MaterialStatus.ACTIVE);
        }
        Material saved = materialRepository.save(material);

        // Initialize inventory
        Inventory inventory = Inventory.builder()
                .materialId(saved.getId())
                .availableQuantityKg(saved.getQuantityKg())
                .reservedQuantityKg(BigDecimal.ZERO)
                .soldQuantityKg(BigDecimal.ZERO)
                .build();
        inventoryRepository.save(inventory);

        log.info("Created material listing: ID {} for seller {}", saved.getId(), saved.getSellerId());
        return saved;
    }

    @Transactional(readOnly = true)
    public List<Material> searchMaterials(String type, String colour, BigDecimal maxPrice, String location, String query) {
        return materialRepository.searchMaterials(
                (type != null && !type.isBlank()) ? type : null,
                (colour != null && !colour.isBlank()) ? colour : null,
                maxPrice,
                (location != null && !location.isBlank()) ? location : null,
                (query != null && !query.isBlank()) ? query : null
        );
    }

    /**
     * Requirement 7.4: AI Material Matching using weighted scoring:
     * Score = 0.35M + 0.25P + 0.20Q + 0.10C + 0.10L
     */
    @Transactional(readOnly = true)
    public List<Map<String, Object>> matchMaterials(
            String targetMaterial,
            BigDecimal budgetPerKg,
            BigDecimal requestedKg,
            String buyerLocation,
            String preferredCondition
    ) {
        List<Material> allActive = materialRepository.findByStatus(MaterialStatus.ACTIVE);
        List<Map<String, Object>> scoredResults = new ArrayList<>();

        for (Material m : allActive) {
            // M: Material compatibility (0.0 to 1.0)
            double scoreM = 0.0;
            if (targetMaterial != null && !targetMaterial.isBlank()) {
                if (m.getMaterialType().equalsIgnoreCase(targetMaterial.trim())) {
                    scoreM = 1.0;
                } else if (m.getMaterialName().toLowerCase().contains(targetMaterial.toLowerCase().trim())) {
                    scoreM = 0.85;
                } else if (m.getDescription() != null && m.getDescription().toLowerCase().contains(targetMaterial.toLowerCase().trim())) {
                    scoreM = 0.60;
                }
            } else {
                scoreM = 0.70;
            }

            // P: Price suitability (0.0 to 1.0)
            double scoreP = 1.0;
            if (budgetPerKg != null && budgetPerKg.compareTo(BigDecimal.ZERO) > 0) {
                double priceVal = m.getPricePerKg().doubleValue();
                double budgetVal = budgetPerKg.doubleValue();
                if (priceVal <= budgetVal) {
                    scoreP = 1.0;
                } else {
                    double overRatio = (priceVal - budgetVal) / budgetVal;
                    scoreP = Math.max(0.0, 1.0 - overRatio);
                }
            }

            // Q: Quantity suitability (0.0 to 1.0)
            double scoreQ = 1.0;
            if (requestedKg != null && requestedKg.compareTo(BigDecimal.ZERO) > 0) {
                BigDecimal available = inventoryRepository.findByMaterialId(m.getId())
                        .map(Inventory::getAvailableQuantityKg)
                        .orElse(m.getQuantityKg());
                double reqVal = requestedKg.doubleValue();
                double availVal = available.doubleValue();
                scoreQ = Math.min(1.0, availVal / reqVal);
            }

            // C: Condition suitability (0.0 to 1.0)
            double scoreC = switch (m.getConditionType().toLowerCase()) {
                case "new" -> 1.0;
                case "good" -> 0.85;
                case "fair" -> 0.60;
                default -> 0.35;
            };

            // L: Location suitability (0.0 to 1.0)
            double scoreL = 0.40;
            if (buyerLocation != null && !buyerLocation.isBlank()) {
                if (m.getLocation().equalsIgnoreCase(buyerLocation.trim())) {
                    scoreL = 1.0;
                } else if (m.getLocation().toLowerCase().contains(buyerLocation.toLowerCase().trim())) {
                    scoreL = 0.75;
                }
            }

            // Formula: Score = 0.35M + 0.25P + 0.20Q + 0.10C + 0.10L
            double totalScore = (0.35 * scoreM) + (0.25 * scoreP) + (0.20 * scoreQ) + (0.10 * scoreC) + (0.10 * scoreL);
            double matchPercentage = Math.round(totalScore * 100.0 * 10.0) / 10.0;

            Map<String, Object> entry = new HashMap<>();
            entry.put("material", m);
            entry.put("matchScore", matchPercentage);
            entry.put("componentScores", Map.of(
                    "materialComp", Math.round(scoreM * 100.0),
                    "priceSuit", Math.round(scoreP * 100.0),
                    "quantitySuit", Math.round(scoreQ * 100.0),
                    "conditionSuit", Math.round(scoreC * 100.0),
                    "locationSuit", Math.round(scoreL * 100.0)
            ));
            scoredResults.add(entry);
        }

        // Rank by matchScore descending
        scoredResults.sort((a, b) -> Double.compare((Double) b.get("matchScore"), (Double) a.get("matchScore")));
        return scoredResults;
    }
}
