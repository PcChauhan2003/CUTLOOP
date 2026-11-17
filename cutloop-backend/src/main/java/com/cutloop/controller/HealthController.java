package com.cutloop.controller;

import com.cutloop.service.AIService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class HealthController {

    private final AIService aiService;

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> getHealth() {
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "service", "CUTLOOP Java Spring Boot Core",
                "javaVersion", System.getProperty("java.version"),
                "timestamp", LocalDateTime.now()
        ));
    }

    @GetMapping("/ai-status")
    public ResponseEntity<Map<String, Object>> getAIStatus() {
        Map<String, Object> aiHealth = aiService.checkAIHealth();
        return ResponseEntity.ok(Map.of(
                "backendStatus", "UP",
                "aiService", aiHealth,
                "timestamp", LocalDateTime.now()
        ));
    }
}
