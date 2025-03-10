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

## Key Learnings

* **Kafka Listener Configuration:** Pay close attention to the `KAFKA_ADVERTISED_LISTENERS` configuration to avoid port conflicts and ensure proper communication between internal and external clients.
* **Schema Registry Connection:** Explicitly specifying the `SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS` can resolve connection issues between the Schema Registry and Kafka.

This document serves as a record of the troubleshooting process and can be used as a reference for future setups.