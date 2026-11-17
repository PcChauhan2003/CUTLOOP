package com.cutloop.model;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@DiscriminatorValue("ADMIN")
@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class Admin extends User {

    private String department;

    public Admin(Long id, String fullName, String email, String passwordHash, String phone, String department) {
        super(id, fullName, email, passwordHash, phone, UserRole.ADMIN, true, null);
        this.department = department;
    }
}
