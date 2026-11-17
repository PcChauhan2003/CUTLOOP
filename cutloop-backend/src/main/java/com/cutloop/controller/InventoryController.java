package com.cutloop.controller;

import com.cutloop.service.InventoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api/inventory")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class InventoryController {

    private final InventoryService inventoryService;

    /**
     * Requirement 8.2: CSV Inventory Export endpoint
     */
    @GetMapping("/export-csv")
    public ResponseEntity<byte[]> exportCsv(@RequestParam(required = false) Long sellerId) {
        String csvContent = inventoryService.exportInventoryToCsv(sellerId);
        byte[] bytes = csvContent.getBytes();

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=cutloop_inventory.csv")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(bytes);
    }

    /**
     * Requirement 8.2: CSV Inventory Import endpoint
     */
    @PostMapping("/import-csv")
    public ResponseEntity<?> importCsv(
            @RequestParam("file") MultipartFile file,
            @RequestParam(required = false, defaultValue = "2") Long sellerId
    ) {
        try {
            int imported = inventoryService.importInventoryFromCsv(file.getInputStream(), sellerId);
            return ResponseEntity.ok(Map.of(
                    "status", "SUCCESS",
                    "recordsImported", imported,
                    "message", "Successfully imported inventory CSV"
            ));
        } catch (IOException e) {
            return ResponseEntity.badRequest().body(Map.of("error", "CSV parsing failed: " + e.getMessage()));
        }
    }
}
