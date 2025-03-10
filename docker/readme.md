# Docker Compose Setup Issues

This document outlines the issues encountered while setting up the Kafka, Zookeeper, and Schema Registry Docker Compose environment and their resolutions.

## Issues and Resolutions

1.  **Port Conflict (Kafka):**

    * **Issue:** Kafka failed to start due to a port conflict in the `KAFKA_ADVERTISED_LISTENERS` configuration. Both the internal (`PLAINTEXT`) and external (`HOST`) listeners were configured to use the same port (9092).
    * **Resolution:** Modified the `docker-compose.yml` file to assign a different port (9093) to the external listener:

        ```yaml
        kafka:
          environment:
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,HOST://localhost:9093
        ```

2.  **Schema Registry Connection Failure:**

    * **Issue:** The Schema Registry failed to start with the error "No supported Kafka endpoints are configured. kafkastore.bootstrap.servers must have at least one endpoint matching kafkastore.security.protocol." This indicated that the Schema Registry couldn't connect to Kafka.
    * **Resolution:** Explicitly added the `SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS` environment variable to the Schema Registry's configuration in `docker-compose.yml`:

        ```yaml
        schema-registry:
          environment:
            SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL: zookeeper:2181
            SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka:9092
        ```

    * This ensured the Schema Registry connected directly to the Kafka broker's internal listener.


3.  **Importance of Healthchecks in Docker:**

    * **Issue:** Facing a connectivity issue in your Docker environment, where the custom `register-schema` container was unable to connect to the `schema-registry` service running on port 8081. Despite using the correct hostname (`schema-registry`) and port (`8081`), the connection failed, resulting in an error message about connection refusal. This issue occurred because the `schema-registry` service was not fully initialized and ready to accept connections at the time the test was executed.
    * **Resolution:** Health checks provided a solution to this issue by ensuring that the `schema-registry` service was fully initialized and ready to accept connections before any dependent services (like `register-schema`) attempted to connect to it. By adding a health check to the `schema-registry` and `kafka` service, monitoring the service's health was possible. Once the `schema-registry` service was healthy and ready, Docker ensured that the `register-schema` service could connect to it without issues.
    In a **Docker Compose** file, you can configure a health check like below:

    ```yaml
    services:
      my-service:
        image: my-image
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8080"]
          interval: 30s
          retries: 3
          start_period: 10s
          timeout: 5s
    ```
