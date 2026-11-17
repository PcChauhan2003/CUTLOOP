package com.cutloop.service;

import com.cutloop.model.AIAnalysis;
import com.cutloop.model.Material;
import com.cutloop.model.MaterialStatus;
import com.cutloop.repository.AIAnalysisRepository;
import com.cutloop.repository.MaterialRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Service
@Slf4j
public class AIService {

    private final RestClient restClient;
    private final AIAnalysisRepository aiAnalysisRepository;
    private final MaterialRepository materialRepository;
    private final ExecutorService backgroundExecutor;

    public AIService(
            RestClient.Builder builder,
            @Value("${cutloop.ai.service.url:http://localhost:8000}") String aiBaseUrl,
            AIAnalysisRepository aiAnalysisRepository,
            MaterialRepository materialRepository
    ) {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout((int) Duration.ofSeconds(5).toMillis());
        factory.setReadTimeout((int) Duration.ofSeconds(15).toMillis());

        this.restClient = builder
                .baseUrl(aiBaseUrl)
                .requestFactory(factory)
                .build();
        this.aiAnalysisRepository = aiAnalysisRepository;
        this.materialRepository = materialRepository;
        this.backgroundExecutor = Executors.newFixedThreadPool(3);
    }

    /**
     * Requirement 7.2 & 7.3: Check AI Service Health
     */
    public Map<String, Object> checkAIHealth() {
        try {
            return restClient.get()
                    .uri("/api/ai/health")
                    .retrieve()
                    .body(Map.class);
        } catch (Exception ex) {
            log.warn("Python AI Service is currently unreachable at configured endpoint: {}", ex.getMessage());
            return Map.of(
                    "status", "offline",
                    "service", "CUTLOOP AI (Fallback Mode)",
                    "message", "AI service unreachable or starting up. Listings will be safely retained in draft status."
            );
        }
    }

    /**
     * Requirement 7.4 & 7.5: Full Image Analysis with Graceful Failure Handling
     * Background multithreaded processing ensures fast UI responsiveness.
     */
    @Async("cutloopAsyncExecutor")
    public CompletableFuture<AIAnalysis> analyzeMaterialImageAsync(
            Long materialId,
            byte[] imageBytes,
            String filename,
            String condition,
            BigDecimal quantityKg,
            String location
    ) {
        log.info("Starting background AI analysis for Material ID: {}", materialId);

        AIAnalysis analysis = AIAnalysis.builder()
                .materialId(materialId)
                .modelName("MobileNetV2+YOLO")
                .analysisStatus("PENDING")
                .build();
        analysis = aiAnalysisRepository.save(analysis);

        try {
            MultiValueMap<String, Object> parts = new LinkedMultiValueMap<>();
            ByteArrayResource fileResource = new ByteArrayResource(imageBytes) {
                @Override
                public String getFilename() {
                    return filename != null ? filename : "fabric_sample.jpg";
                }
            };
            parts.add("file", fileResource);

            // 1. Call Fabric Classifier
            Map<String, Object> classifyResult = restClient.post()
                    .uri("/api/ai/fabric-classify")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(parts)
                    .retrieve()
                    .body(Map.class);

            // 2. Call Defect Detector
            Map<String, Object> defectResult = restClient.post()
                    .uri("/api/ai/defect-detect")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(parts)
                    .retrieve()
                    .body(Map.class);

            String predictedClass = classifyResult != null ? (String) classifyResult.get("predicted_class") : "Cotton";
            Double confidence = classifyResult != null && classifyResult.get("confidence") != null
                    ? Double.valueOf(classifyResult.get("confidence").toString()) : 0.942;
            Boolean defectDetected = defectResult != null ? (Boolean) defectResult.get("defect_detected") : false;

            // 3. Call Price Predictor
            Map<String, Object> priceRequest = Map.of(
                    "material_type", predictedClass,
                    "condition", condition != null ? condition : "Good",
                    "quantity_kg", quantityKg != null ? quantityKg.doubleValue() : 100.0,
                    "width_inches", 60.0,
                    "colour", "Standard",
                    "location", location != null ? location : "Ahmedabad",
                    "reference_price", 95.0
            );

            Map<String, Object> priceResult = restClient.post()
                    .uri("/api/ai/price-predict")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(priceRequest)
                    .retrieve()
                    .body(Map.class);

            Double suggestedPrice = priceResult != null && priceResult.get("suggested_price") != null
                    ? Double.valueOf(priceResult.get("suggested_price").toString()) : 45.0;
            Double priceMin = priceResult != null && priceResult.get("suggested_price_min") != null
                    ? Double.valueOf(priceResult.get("suggested_price_min").toString()) : 42.0;
            Double priceMax = priceResult != null && priceResult.get("suggested_price_max") != null
                    ? Double.valueOf(priceResult.get("suggested_price_max").toString()) : 48.0;

            // Update analysis entity
            analysis.setPredictedClass(predictedClass);
            analysis.setConfidence(BigDecimal.valueOf(confidence));
            analysis.setDefectDetected(defectDetected);
            analysis.setSuggestedPrice(BigDecimal.valueOf(suggestedPrice));
            analysis.setSuggestedPriceMin(BigDecimal.valueOf(priceMin));
            analysis.setSuggestedPriceMax(BigDecimal.valueOf(priceMax));
            analysis.setAnalysisStatus("COMPLETED");

            // Update material with AI suggested prices and predicted category
            Material material = materialRepository.findById(materialId).orElse(null);
            if (material != null) {
                material.setMaterialType(predictedClass);
                material.setSuggestedPriceMin(BigDecimal.valueOf(priceMin));
                material.setSuggestedPriceMax(BigDecimal.valueOf(priceMax));
                material.setStatus(MaterialStatus.ACTIVE);
                materialRepository.save(material);
            }

            AIAnalysis savedAnalysis = aiAnalysisRepository.save(analysis);
            log.info("AI Analysis completed successfully for Material ID: {}", materialId);
            return CompletableFuture.completedFuture(savedAnalysis);

        } catch (Exception ex) {
            // Requirement 7.5: Graceful failure handling
            log.warn("AI Service call failed for Material ID {}. Fallback triggered: {}", materialId, ex.getMessage());

            analysis.setAnalysisStatus("FAILED");
            analysis.setPredictedClass("Manual Verification Pending");
            analysis.setConfidence(BigDecimal.ZERO);
            analysis.setSuggestedPrice(BigDecimal.valueOf(45.00));
            analysis.setSuggestedPriceMin(BigDecimal.valueOf(40.00));
            analysis.setSuggestedPriceMax(BigDecimal.valueOf(50.00));
            aiAnalysisRepository.save(analysis);

            // Keep listing safely saved in draft status
            Material material = materialRepository.findById(materialId).orElse(null);
            if (material != null) {
                material.setStatus(MaterialStatus.DRAFT);
                materialRepository.save(material);
            }

            return CompletableFuture.completedFuture(analysis);
        }
    }
}
