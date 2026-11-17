package com.cutloop.model;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;
import lombok.*;

@Entity
@DiscriminatorValue("BUYER")
@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class Buyer extends User {

    private String organizationName;
    private String industryType;
    private String shippingAddress;
    private String city;
    private String state;
    private String pincode;

    public Buyer(Long id, String fullName, String email, String passwordHash, String phone,
                 String organizationName, String industryType, String shippingAddress, String city, String state, String pincode) {
        super(id, fullName, email, passwordHash, phone, UserRole.BUYER, true, null);
        this.organizationName = organizationName;
        this.industryType = industryType;
        this.shippingAddress = shippingAddress;
        this.city = city;
        this.state = state;
        this.pincode = pincode;
    }
}
