package com.cutloop.controller;

import com.cutloop.model.Material;
import com.cutloop.model.Order;
import com.cutloop.model.User;
import com.cutloop.repository.MaterialRepository;
import com.cutloop.repository.OrderRepository;
import com.cutloop.repository.UserRepository;
import com.cutloop.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class AdminController {

    private final UserRepository userRepository;
    private final MaterialRepository materialRepository;
    private final OrderRepository orderRepository;
    private final UserService userService;

    @GetMapping("/users")
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userRepository.findAll());
    }

    @PutMapping("/users/{id}/status")
    public ResponseEntity<?> toggleUserStatus(@PathVariable Long id, @RequestParam boolean active) {
        userService.setUserActive(id, active);
        return ResponseEntity.ok(Map.of("message", "User status updated"));
    }

    /**
     * Requirement 9: Seller, Platform & Sustainability Analytics
     */
    @GetMapping("/analytics")
    public ResponseEntity<Map<String, Object>> getPlatformAnalytics() {
        long totalUsers = userRepository.count();
        long totalMaterials = materialRepository.count();
        List<Order> orders = orderRepository.findAll();

        BigDecimal totalRevenue = orders.stream()
                .map(Order::getTotalAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        // Sustainability Metric: Material Recovered Through CUTLOOP (Total KG traded)
        BigDecimal totalMaterialRecoveredKg = orders.stream()
                .map(Order::getTotalKg)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        return ResponseEntity.ok(Map.of(
                "totalUsers", totalUsers,
                "totalListings", totalMaterials,
                "totalOrders", orders.size(),
                "totalTransactionValue", totalRevenue,
                "materialRecoveredKg", totalMaterialRecoveredKg,
                "co2EmissionsSavedKg", totalMaterialRecoveredKg.multiply(BigDecimal.valueOf(1.85)), // ~1.85kg CO2 saved per kg reused textile
                "activeSellersCount", 2
        ));
    }
}
