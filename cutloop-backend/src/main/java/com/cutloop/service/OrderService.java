package com.cutloop.service;

import com.cutloop.dto.OrderRequest;
import com.cutloop.exception.InsufficientStockException;
import com.cutloop.model.*;
import com.cutloop.repository.CartRepository;
import com.cutloop.repository.MaterialRepository;
import com.cutloop.repository.OrderRepository;
import com.cutloop.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

    private final OrderRepository orderRepository;
    private final MaterialRepository materialRepository;
    private final UserRepository userRepository;
    private final CartRepository cartRepository;
    private final InventoryService inventoryService;
    private final PaymentProcessor paymentProcessor;

    /**
     * Requirement 8.2 & 8.4: Atomic Order Processing with Custom InsufficientStockException
     */
    @Transactional
    public Order placeOrder(OrderRequest request) {
        log.info("Initiating order placement for buyer ID: {}", request.getBuyerId());

        User buyer = userRepository.findById(request.getBuyerId())
                .orElseThrow(() -> new IllegalArgumentException("Buyer not found with ID: " + request.getBuyerId()));

        if (request.getItems() == null || request.getItems().isEmpty()) {
            throw new IllegalArgumentException("Order items list cannot be empty");
        }

        BigDecimal subtotal = BigDecimal.ZERO;
        BigDecimal totalKg = BigDecimal.ZERO;
        List<OrderItem> orderItems = new ArrayList<>();

        String orderNum = "ORD-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 4).toUpperCase();

        Order order = Order.builder()
                .orderNumber(orderNum)
                .buyerId(buyer.getId())
                .shippingAddress(request.getShippingAddress() != null ? request.getShippingAddress() : "Default Address")
                .orderStatus(OrderStatus.CONFIRMED)
                .build();

        // 1. Validate stock and calculate prices atomically
        for (OrderRequest.ItemRequest itemReq : request.getItems()) {
            Material material = materialRepository.findById(itemReq.getMaterialId())
                    .orElseThrow(() -> new IllegalArgumentException("Material not found: " + itemReq.getMaterialId()));

            BigDecimal requestedQty = itemReq.getQuantityKg();

            // Check stock using InventoryService
            BigDecimal available = inventoryService.getAvailableStock(material.getId());
            if (available.compareTo(requestedQty) < 0) {
                throw new InsufficientStockException(
                        String.format("Stock unavailable for '%s'. Available: %s kg, Requested: %s kg",
                                material.getMaterialName(), available, requestedQty)
                );
            }

            // Deduct stock atomically
            inventoryService.deductStock(material.getId(), requestedQty);

            BigDecimal itemTotal = material.getPricePerKg().multiply(requestedQty).setScale(2, RoundingMode.HALF_UP);
            subtotal = subtotal.add(itemTotal);
            totalKg = totalKg.add(requestedQty);

            OrderItem orderItem = OrderItem.builder()
                    .order(order)
                    .materialId(material.getId())
                    .materialName(material.getMaterialName())
                    .sellerId(material.getSellerId())
                    .quantityKg(requestedQty)
                    .pricePerKg(material.getPricePerKg())
                    .totalPrice(itemTotal)
                    .build();

            orderItems.add(orderItem);
        }

        // 5% Platform commission & delivery fee calculation
        BigDecimal commission = subtotal.multiply(BigDecimal.valueOf(0.05)).setScale(2, RoundingMode.HALF_UP);
        BigDecimal deliveryFee = totalKg.compareTo(BigDecimal.valueOf(50)) > 0 ? BigDecimal.valueOf(350.00) : BigDecimal.valueOf(150.00);
        BigDecimal totalAmount = subtotal.add(deliveryFee);

        order.setSubtotal(subtotal);
        order.setPlatformCommission(commission);
        order.setDeliveryFee(deliveryFee);
        order.setTotalAmount(totalAmount);
        order.setTotalKg(totalKg);
        order.setItems(orderItems);

        Order savedOrder = orderRepository.save(order);

        // 2. Process Simulated Payment
        paymentProcessor.processPayment(savedOrder.getId(), totalAmount, request.getPaymentMethod());

        // 3. Clear shopping cart if needed
        cartRepository.findByUserId(buyer.getId()).ifPresent(cart -> {
            cart.getItems().clear();
            cartRepository.save(cart);
        });

        log.info("Order placed successfully: {} for Total INR {}", savedOrder.getOrderNumber(), totalAmount);
        return savedOrder;
    }

    @Transactional(readOnly = true)
    public List<Order> getOrdersByBuyer(Long buyerId) {
        return orderRepository.findByBuyerIdOrderByCreatedAtDesc(buyerId);
    }

    @Transactional(readOnly = true)
    public Order getOrderById(Long id) {
        return orderRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Order not found with ID: " + id));
    }
}
