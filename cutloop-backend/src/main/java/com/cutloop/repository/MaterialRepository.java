package com.cutloop.repository;

import com.cutloop.model.Material;
import com.cutloop.model.MaterialStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

@Repository
public interface MaterialRepository extends JpaRepository<Material, Long> {
    List<Material> findBySellerId(Long sellerId);
    List<Material> findByStatus(MaterialStatus status);

    @Query("SELECT m FROM Material m WHERE m.status = 'ACTIVE' " +
           "AND (:materialType IS NULL OR LOWER(m.materialType) = LOWER(:materialType)) " +
           "AND (:colour IS NULL OR LOWER(m.colour) LIKE LOWER(CONCAT('%', :colour, '%'))) " +
           "AND (:maxPrice IS NULL OR m.pricePerKg <= :maxPrice) " +
           "AND (:location IS NULL OR LOWER(m.location) LIKE LOWER(CONCAT('%', :location, '%'))) " +
           "AND (:keyword IS NULL OR LOWER(m.materialName) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(m.description) LIKE LOWER(CONCAT('%', :keyword, '%')))")
    List<Material> searchMaterials(
            @Param("materialType") String materialType,
            @Param("colour") String colour,
            @Param("maxPrice") BigDecimal maxPrice,
            @Param("location") String location,
            @Param("keyword") String keyword
    );
}
