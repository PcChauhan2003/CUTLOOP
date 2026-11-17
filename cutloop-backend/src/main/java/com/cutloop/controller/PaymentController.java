package com.cutloop.controller;

import com.cutloop.model.Payment;
import com.cutloop.service.PaymentProcessor;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api/payments")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class PaymentController {

    private final PaymentProcessor paymentProcessor;

    @PostMapping("/process")
    public ResponseEntity<?> processPayment(@RequestBody Map<String, Object> payload) {
        try {
            Long orderId = Long.valueOf(payload.get("orderId").toString());
            BigDecimal amount = new BigDecimal(payload.get("amount").toString());
            String method = payload.getOrDefault("method", "SIMULATED_TEST_GATEWAY").toString();

            Payment payment = paymentProcessor.processPayment(orderId, amount, method);
            return ResponseEntity.ok(payment);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
