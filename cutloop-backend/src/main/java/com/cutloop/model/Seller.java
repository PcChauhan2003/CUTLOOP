package com.cutloop.model;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@DiscriminatorValue("SELLER")
@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class Seller extends User {

    private String companyName;
    private String gstNumber;
    private String factoryAddress;
    private String city;
    private String state;
    private String pincode;

    public Seller(Long id, String fullName, String email, String passwordHash, String phone,
                  String companyName, String gstNumber, String factoryAddress, String city, String state, String pincode) {
        super(id, fullName, email, passwordHash, phone, UserRole.SELLER, true, null);
        this.companyName = companyName;
        this.gstNumber = gstNumber;
        this.factoryAddress = factoryAddress;
        this.city = city;
        this.state = state;
        this.pincode = pincode;
    }
}
