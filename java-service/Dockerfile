FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn -q -DskipTests package

# Intentionally old runtime line for scanner evaluation.
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /app/target/java-service-1.0.0.jar /app/service.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "/app/service.jar"]
