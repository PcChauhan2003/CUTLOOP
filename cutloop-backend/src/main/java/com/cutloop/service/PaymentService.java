package com.cutloop.service;

import com.cutloop.exception.PaymentFailedException;
import com.cutloop.model.Payment;
import com.cutloop.model.PaymentStatus;
import com.cutloop.repository.PaymentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class PaymentService implements PaymentProcessor {

    private final PaymentRepository paymentRepository;

    @Override
    @Transactional
    public Payment processPayment(Long orderId, BigDecimal amount, String method) {
        log.info("Processing simulated test payment for Order ID: {}, Amount: INR {}", orderId, amount);

        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new PaymentFailedException("Invalid payment amount: " + amount);
        }

        // Test payment simulation: always succeeds in sandbox
        String txnRef = "TXN-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();

        Payment payment = Payment.builder()
                .orderId(orderId)
                .transactionReference(txnRef)
                .amount(amount)
                .currency("INR")
                .paymentMethod(method != null ? method : "SIMULATED_GATEWAY")
                .paymentStatus(PaymentStatus.SUCCESS)
                .build();

        Payment saved = paymentRepository.save(payment);
        log.info("Payment SUCCESS: TxnRef: {}", txnRef);
        return saved;
    }
}
