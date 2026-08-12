package com.security.log_generator.model;

import java.time.LocalDateTime;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class SecurityLog {
    private String logId; // Log identifier
    private LocalDateTime timestamp; // Date and time of the event
    private String ip; // Ip address
    private String userId; // User identifier
    private String action; // Action performed (LOGIN_ATTEMPT, FILE_DOWNLOAD, etc)
    private String status; // Success or failure
    private int attempts; // Number of attempts from that IP address
    private String country; // Country (detect impossible travels)
    private String resource; // Resource accessed
}
