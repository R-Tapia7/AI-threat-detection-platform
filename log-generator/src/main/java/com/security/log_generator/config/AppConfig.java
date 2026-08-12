package com.security.log_generator.config;

import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.config.RequestConfig;
import org.apache.hc.client5.http.impl.classic.HttpClientBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestClient;
import org.springframework.beans.factory.annotation.Value;

import java.util.concurrent.TimeUnit;

@Configuration
public class AppConfig {

        @Value("${PYTHON_ANALYZER_URL:http://localhost:8001}")
        private String pythonAnalyzerUrl;

        @Bean
        public RestClient restClient() {

                // Build an Apache HttpClient with a 2-minute response timeout.
                // This is necessary because Ollama can take 30-60 seconds to respond,
                // and the default RestClient timeout would cut the connection before that.
                RequestConfig requestConfig = RequestConfig.custom()
                                .setResponseTimeout(120, TimeUnit.SECONDS)
                                .build();

                HttpClient httpClient = HttpClientBuilder.create()
                                .setDefaultRequestConfig(requestConfig)
                                .build();

                HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);

                return RestClient.builder()
                                .baseUrl(pythonAnalyzerUrl)
                                .requestFactory(factory)
                                .build();
        }
}
