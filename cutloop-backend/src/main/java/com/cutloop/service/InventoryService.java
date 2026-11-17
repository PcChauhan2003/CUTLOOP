package com.cutloop.service;

import com.cutloop.exception.InsufficientStockException;
import com.cutloop.model.Inventory;
import com.cutloop.model.Material;
import com.cutloop.repository.InventoryRepository;
import com.cutloop.repository.MaterialRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.*;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class InventoryService {

    private final InventoryRepository inventoryRepository;
    private final MaterialRepository materialRepository;

    @Transactional(readOnly = true)
    public BigDecimal getAvailableStock(Long materialId) {
        return inventoryRepository.findByMaterialId(materialId)
                .map(Inventory::getAvailableQuantityKg)
                .orElse(BigDecimal.ZERO);
    }

    @Transactional
    public void deductStock(Long materialId, BigDecimal requestedKg) {
        Inventory inv = inventoryRepository.findByMaterialId(materialId)
                .orElseThrow(() -> new InsufficientStockException("Inventory not found for Material ID: " + materialId));

        if (inv.getAvailableQuantityKg().compareTo(requestedKg) < 0) {
            throw new InsufficientStockException(
                    String.format("Insufficient stock for material %d. Requested: %s kg, Available: %s kg",
                            materialId, requestedKg, inv.getAvailableQuantityKg())
            );
        }

        inv.setAvailableQuantityKg(inv.getAvailableQuantityKg().subtract(requestedKg));
        inv.setSoldQuantityKg(inv.getSoldQuantityKg().add(requestedKg));
        inventoryRepository.save(inv);
        log.info("Stock deducted for material {}: deducted {} kg, remaining {} kg",
                materialId, requestedKg, inv.getAvailableQuantityKg());
    }

    @Transactional
    public void restock(Long materialId, BigDecimal addKg) {
        Inventory inv = inventoryRepository.findByMaterialId(materialId)
                .orElseGet(() -> Inventory.builder()
                        .materialId(materialId)
                        .availableQuantityKg(BigDecimal.ZERO)
                        .reservedQuantityKg(BigDecimal.ZERO)
                        .soldQuantityKg(BigDecimal.ZERO)
                        .build());

        inv.setAvailableQuantityKg(inv.getAvailableQuantityKg().add(addKg));
        inventoryRepository.save(inv);
        log.info("Restocked material {}: added {} kg, total now {} kg", materialId, addKg, inv.getAvailableQuantityKg());
    }

    /**
     * Requirement 8.2: CSV Inventory Export
     */
    public String exportInventoryToCsv(Long sellerId) {
        List<Material> materials = (sellerId != null)
                ? materialRepository.findBySellerId(sellerId)
                : materialRepository.findAll();

        StringBuilder csv = new StringBuilder();
        csv.append("material_id,material_name,material_type,available_quantity_kg,price_per_kg,location,status\n");

        for (Material m : materials) {
            BigDecimal qty = inventoryRepository.findByMaterialId(m.getId())
                    .map(Inventory::getAvailableQuantityKg)
                    .orElse(m.getQuantityKg());

            csv.append(String.format("%d,\"%s\",\"%s\",%.2f,%.2f,\"%s\",\"%s\"\n",
                    m.getId(),
                    m.getMaterialName().replace("\"", "\"\""),
                    m.getMaterialType(),
                    qty,
                    m.getPricePerKg(),
                    m.getLocation(),
                    m.getStatus()));
        }

        log.info("Exported CSV inventory with {} items", materials.size());
        return csv.toString();
    }

    /**
     * Requirement 8.2: CSV Inventory Import
     */
    @Transactional
    public int importInventoryFromCsv(InputStream inputStream, Long defaultSellerId) throws IOException {
        int importedCount = 0;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            String line = reader.readLine(); // skip header
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                String[] parts = line.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");
                if (parts.length >= 4) {
                    try {
                        String name = parts[1].replace("\"", "").trim();
                        String type = parts.length > 2 ? parts[2].replace("\"", "").trim() : "Cotton";
                        BigDecimal qty = new BigDecimal(parts[3].trim());
                        BigDecimal price = parts.length > 4 ? new BigDecimal(parts[4].trim()) : BigDecimal.valueOf(50.0);
                        String loc = parts.length > 5 ? parts[5].replace("\"", "").trim() : "Ahmedabad";

                        Material material = Material.builder()
                                .sellerId(defaultSellerId != null ? defaultSellerId : 2L)
                                .materialName(name)
                                .materialType(type)
                                .colour("Standard")
                                .conditionType("Good")
                                .quantityKg(qty)
                                .minimumOrderKg(BigDecimal.valueOf(5.0))
                                .pricePerKg(price)
                                .location(loc)
                                .description("Imported from CSV inventory sync")
                                .build();

                        Material saved = materialRepository.save(material);

                        Inventory inv = Inventory.builder()
                                .materialId(saved.getId())
                                .availableQuantityKg(qty)
                                .reservedQuantityKg(BigDecimal.ZERO)
                                .soldQuantityKg(BigDecimal.ZERO)
                                .build();
                        inventoryRepository.save(inv);
                        importedCount++;
                    } catch (Exception e) {
                        log.warn("Skipping invalid CSV row: {}", line, e);
                    }
                }
            }
        }
        log.info("Successfully imported {} materials from CSV", importedCount);
        return importedCount;
    }

    /**
     * Requirement 8.1: Multithreaded Async report generation
     */
    @Async("cutloopAsyncExecutor")
    public CompletableFuture<String> generateAsyncInventoryReport(Long sellerId) {
        log.info("Background thread generating inventory report for seller {}", sellerId);
        try {
            // Simulated heavy calculation in background thread
            Thread.sleep(500);
            String csvReport = exportInventoryToCsv(sellerId);
            return CompletableFuture.completedFuture(csvReport);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return CompletableFuture.failedFuture(e);
        }
    }
}
