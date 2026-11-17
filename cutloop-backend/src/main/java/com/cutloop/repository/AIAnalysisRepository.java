package com.cutloop.repository;

import com.cutloop.model.AIAnalysis;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface AIAnalysisRepository extends JpaRepository<AIAnalysis, Long> {
    List<AIAnalysis> findByMaterialId(Long materialId);
    Optional<AIAnalysis> findTopByMaterialIdOrderByIdDesc(Long materialId);
}
