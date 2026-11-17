package com.cutloop.service;

import com.cutloop.model.Payment;
import java.math.BigDecimal;

public interface PaymentProcessor {
    Payment processPayment(Long orderId, BigDecimal amount, String method);
}
