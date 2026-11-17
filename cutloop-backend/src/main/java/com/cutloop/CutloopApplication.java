package com.cutloop;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class CutloopApplication {
    public static void main(String[] args) {
        SpringApplication.run(CutloopApplication.class, args);
    }
}
