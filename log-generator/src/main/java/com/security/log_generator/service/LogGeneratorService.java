package com.security.log_generator.service;

import com.security.log_generator.model.SecurityLog;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.UUID;
import java.util.List;
import java.util.ArrayList;
import java.util.Random;

@Service
public class LogGeneratorService {

        // Dummy data lists to randomly pick values from when generating logs
        private static final List<String> IPS = List.of(
                        "192.168.1.10", "10.0.0.5", "172.16.0.3",
                        "203.0.113.42", "198.51.100.7", "45.33.32.156");

        private static final List<String> FIRST_NAMES = List.of(
                        "alice", "bob", "carol", "maria", "david", "mohamed", "sofia", "michael", "rodrigo");

        private static final List<String> LAST_NAMES = List.of(
                        "smith", "jones", "garcia", "williams", "brown", "davis", "wilson", "johnson", "rodriguez");

        private static final List<String> COUNTRIES = List.of(
                        "ES", "US", "RU", "CN", "BR", "DE", "IN", "IR", "ENG");

        private static final List<String> RESOURCES = List.of(
                        "/dashboard",
                        "/api/users",
                        "/api/profile",
                        "/files/reports",
                        "/files/documents",
                        "/api/payments",
                        "/api/orders",
                        "/api/products",
                        "/search",
                        "/notifications",
                        "/admin/panel", // critical
                        "/config/secrets" // critical
        );

        // Enumeration representing possible actions a user can take
        public enum Action {
                LOGIN_ATTEMPT, FILE_DOWNLOAD, DATA_EXPORT,
                CONFIG_ACCESS, PASSWORD_CHANGE, ADMIN_ACCESS;
        }

        private final Random random = new Random();

        public SecurityLog generateSingleLog() {
                // Simulates a 30% chance of the action failing
                String status = random.nextInt(10) < 3 ? "FAILURE" : "SUCCESS";

                return SecurityLog.builder()
                                .logId(UUID.randomUUID().toString()) // Generates a random unique ID
                                .timestamp(LocalDateTime.now()) // Generates the current timestamp
                                .ip(IPS.get(random.nextInt(IPS.size()))) // Selects a random IP from the list
                                .userId(FIRST_NAMES.get(random.nextInt(FIRST_NAMES.size())) + "." +
                                                LAST_NAMES.get(random.nextInt(LAST_NAMES.size()))) // Selects a random
                                                                                                   // user from the list
                                .action(Action.values()[random.nextInt(Action.values().length)].name()) // Random action
                                .status(status)
                                // If it's a failure, simulate between 1 and 60 attempts; otherwise, just 1
                                .attempts(status.equals("FAILURE") ? random.nextInt(60) + 1 : 1)
                                .country(COUNTRIES.get(random.nextInt(COUNTRIES.size())))
                                .resource(RESOURCES.get(random.nextInt(RESOURCES.size())))
                                .build();
        }

        // Generates a list of multiple random security logs
        public List<SecurityLog> generateBatch(int size) {
                List<SecurityLog> logs = new ArrayList<>();
                for (int i = 0; i < size; i++) {
                        logs.add(generateSingleLog());
                }
                return logs;
        }

        /*
         * Simulates a brute force attack by generating 60 consecutive failed login
         * attempts from the same IP address targeting the admin panel.
         */
        public List<SecurityLog> generateBruteForceAttack(String attackerIp) {
                List<SecurityLog> logs = new ArrayList<>();
                for (int i = 1; i <= 60; i++) {
                        logs.add(SecurityLog.builder()
                                        .logId(UUID.randomUUID().toString())
                                        .timestamp(LocalDateTime.now())
                                        .ip(attackerIp) // Uses the provided malicious IP
                                        .userId("unknown") // Unknown user since they are trying to break in
                                        .action("LOGIN_ATTEMPT")
                                        .status("FAILURE") // All attempts fail
                                        .attempts(i) // Increments the attempt counter
                                        .country("RU") // Hardcoded to "RU" for this simulation
                                        .resource("/admin/panel") // Target resource
                                        .build());
                }
                return logs;
        }

}
