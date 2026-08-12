package com.security.log_generator.controller;

import com.security.log_generator.model.SecurityLog;
import com.security.log_generator.service.LogGeneratorService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.client.RestClient;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/logs")
public class LogController {
    private static final Logger logger = LoggerFactory.getLogger(LogController.class);

    private final LogGeneratorService logService;
    private final RestClient restClient;

    public LogController(LogGeneratorService logService, RestClient restClient) {
        this.logService = logService;
        this.restClient = restClient;
    }

    /**
     * Handles HTTP GET requests to /api/logs
     * 
     * @RequestParam allows passing the size in the URL (e.g., /api/logs?size=20).
     *               Defaults to 10.
     */
    @GetMapping
    public List<SecurityLog> getLogs(@RequestParam(defaultValue = "10") int size) {
        return logService.generateBatch(size);
    }

    /**
     * Handles HTTP GET requests to /api/logs/single
     * Returns exactly one random log.
     */
    @GetMapping("/single")
    public SecurityLog getSingleLog() {
        return logService.generateSingleLog();
    }

    /**
     * Handles HTTP POST requests to /api/logs/attack/brute-force
     * 
     * @RequestBody maps the incoming JSON payload to the AttackRequest record.
     */
    @PostMapping("/attack/brute-force")
    public List<SecurityLog> simulateBruteForce(@RequestBody AttackRequest request) {
        List<SecurityLog> logs = logService.generateBruteForceAttack(request.ip());

        // Send the attack logs to Python like the scheduler does.
        try {
            restClient.post()
                    .uri("/analyze/")
                    .body(logs)
                    .retrieve()
                    .toBodilessEntity();

            logger.info("Brute force simulation: {} logs sent to Python analyzer", logs.size());

        } catch (Exception e) {
            // If Python is down, the simulation still works — we just log the warning.
            logger.warn("Could not forward attack logs to Python: {}", e.getMessage());
        }

        return logs;
    }

    /**
     * A Java Record is a concise way to create immutable data carrier classes.
     * This record expects a JSON like: { "ip": "123.45.67.89" }
     */
    record AttackRequest(String ip) {
    }
}
