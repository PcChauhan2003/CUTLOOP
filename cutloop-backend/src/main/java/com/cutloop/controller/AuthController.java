package com.cutloop.controller;

import com.cutloop.model.User;
import com.cutloop.model.UserRole;
import com.cutloop.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> credentials) {
        String email = credentials.get("email");
        String password = credentials.get("password");

        Optional<User> userOpt = userService.getUserByEmail(email);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            // Prototype check: accepts password123 or any test password for seeded users
            return ResponseEntity.ok(Map.of(
                    "token", "demo-token-" + user.getId(),
                    "user", user
            ));
        }
        return ResponseEntity.badRequest().body(Map.of("error", "Invalid email or user not found"));
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody User user) {
        try {
            User saved = userService.registerUser(user);
            return ResponseEntity.ok(Map.of(
                    "message", "User registered successfully",
                    "user", saved
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
