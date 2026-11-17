package com.cutloop.service;

import com.cutloop.model.User;
import com.cutloop.model.UserRole;
import com.cutloop.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository userRepository;

    @Transactional(readOnly = true)
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional(readOnly = true)
    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Transactional
    public User registerUser(User user) {
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new IllegalArgumentException("User with email " + user.getEmail() + " already exists");
        }
        if (user.getRole() == null) {
            user.setRole(UserRole.BUYER);
        }
        return userRepository.save(user);
    }

    @Transactional
    public void setUserActive(Long id, boolean active) {
        userRepository.findById(id).ifPresent(user -> {
            user.setIsActive(active);
            userRepository.save(user);
        });
    }
}
