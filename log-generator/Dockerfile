# Build
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml first and download dependencies separately.
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy the source code and build the JAR
COPY src ./src
RUN mvn package -DskipTests -B

# Runtime
FROM eclipse-temurin:21-jre

WORKDIR /app

# Copy only the compiled JAR from the builder stage
COPY --from=builder /app/target/*.jar app.jar

# The port Spring Boot listens on
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]