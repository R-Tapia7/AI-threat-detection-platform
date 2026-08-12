package com.security.log_generator.scheduler;

import com.security.log_generator.model.SecurityLog;
import com.security.log_generator.service.LogGeneratorService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import java.util.List;

@Component
@EnableScheduling
public class LogScheduler {

    // Logger instance to print information to the console
    private static final Logger logger = LoggerFactory.getLogger(LogScheduler.class);

    private final LogGeneratorService logService;

    // RestClient is Spring's HTTP client
    // Build it once here pointing to the Python service URL
    // Spring will reuse this same instance on every scheduled call
    private final RestClient restClient;

    public LogScheduler(LogGeneratorService logService, RestClient restClient) {
        this.logService = logService;
        this.restClient = restClient;
    }

    /**
     * @Scheduled executes this method repeatedly
     *            fixedRate = 5000 means it will run every 5000 milliseconds
     */
    @Scheduled(fixedRate = 5000)
    public void generateAndLogBatch() {
        // Generates a batch of 5 logs
        List<SecurityLog> logs = logService.generateBatch(5);

        // We iterate to see it ourselves in the Java terminal
        logs.forEach(log -> logger.info("[{}] {} - {} - {} - {}",
                log.getTimestamp(),
                log.getIp(),
                log.getUserId(),
                log.getAction(),
                log.getStatus()));

        // Send to Python
        try {
            var response = restClient.post() // HTTP POST
                    .uri("/analyze/") // appended to the baseUrl
                    .body(logs) // serializes the list to JSON automatically
                    .retrieve() // sends the request and gets the response
                    .toBodilessEntity(); // we only care about the status code, not the body

            logger.info("Batch of {} logs sent → HTTP {}", logs.size(), response.getStatusCode());

        } catch (Exception e) {
            // If Python is down, we log the error but don't crash Java
            // If one service fails, it should never bring down another
            logger.error("Could not reach Python analyzer: {}", e.getMessage());
        }
    }

}
