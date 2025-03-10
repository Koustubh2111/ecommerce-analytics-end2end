# E-commerce Analytics Event Streaming Project

This project simulates an e-commerce analytics event streaming pipeline using Kafka, Python, Schema registry and Prefect for workflopw orchestration.
Fake user interactions and product-related events are generated to enable real-time analytics and insights.

## Project Overview

The goal is to build a foundation for:

* Real-time analytics dashboards.
* Personalized recommendations.

## Project Structure

```
your-project/
└── docker/
    ├── docker-compose.yml     # Docker Compose configuration for Kafka Zookeeper and Schema Registry
├── README.md              # This file
└── src/
    ├── schemas/
    │   ├── init.py    # Marks schemas as a Python package
    │   ├── register_add_to_cart_schema.py   # Schema definition for AddToCart events
    │   ├── register_abandoned_cart_schema.py # Schema definition for AbandonedCart events
    │   ├── register_product_catalog_schema.py # Schema definition for ProductCatalog events
    │   ├── register_product_view_schema.py # Schema definition for ProductView events
    │   ├── register_purchase_schema.py # Schema definition for Purchase events
    │   └── register_transaction_schema.py # Schema definition for Transaction events
    └── producers/
        ├── produce_add_to_cart.py   # Producer script for AddToCart events

```

1.  **Prerequisites:**
    * Docker and Docker Compose installed.
    * Requirements installed.
    ```bash
    pip install -r requirements.text
    ```

2.  **Start Docker Containers:**
    * Navigate to the [Docker compose file](./docker/docker-compose.yml):

        ```bash
        docker-compose up -d
        ```

3.  **Run Schema Registry Scripts:**
    * Navigate to the `src` directory.
    * Run the [schema registry scripts](./src/schemas/) using Python:

        ```bash
        python register_*.py
        ```
## TO DO

* **Implement Consumer Scripts:** Develop consumer applications to process and analyze the event data.
* **Implement Prefect Flows:** Develop Prefect flows to orchestrate the producer and consumer processes.
* **Data Aggregation and Transformation:** Create data pipelines for aggregating and transforming the raw event data.
* **Testing and Monitoring:** Add comprehensive unit tests and monitoring tools.
* **Cloud Deployment:** Deploy the pipeline to a cloud platform.


