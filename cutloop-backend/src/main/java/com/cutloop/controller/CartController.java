package com.cutloop.controller;

import com.cutloop.model.Cart;
import com.cutloop.service.CartService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api/cart")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class CartController {

    private final CartService cartService;

    @GetMapping("/{userId}")
    public ResponseEntity<Cart> getCart(@PathVariable Long userId) {
        return ResponseEntity.ok(cartService.getOrCreateCart(userId));
    }

    @PostMapping("/add")
    public ResponseEntity<Cart> addToCart(@RequestBody Map<String, Object> payload) {
        Long userId = Long.valueOf(payload.get("userId").toString());
        Long materialId = Long.valueOf(payload.get("materialId").toString());
        BigDecimal quantityKg = new BigDecimal(payload.get("quantityKg").toString());

        Cart updated = cartService.addToCart(userId, materialId, quantityKg);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/items/{cartItemId}")
    public ResponseEntity<Cart> removeFromCart(@RequestParam Long userId, @PathVariable Long cartItemId) {
        return ResponseEntity.ok(cartService.removeFromCart(userId, cartItemId));
    }

    @DeleteMapping("/clear/{userId}")
    public ResponseEntity<?> clearCart(@PathVariable Long userId) {
        cartService.clearCart(userId);
        return ResponseEntity.ok(Map.of("message", "Cart cleared"));
    }
}
