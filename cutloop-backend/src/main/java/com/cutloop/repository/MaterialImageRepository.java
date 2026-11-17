package com.cutloop.repository;

import com.cutloop.model.MaterialImage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MaterialImageRepository extends JpaRepository<MaterialImage, Long> {
    List<MaterialImage> findByMaterialId(Long materialId);
}
