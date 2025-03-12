# E-commerce Analytics Event Streaming Project

This project simulates an e-commerce analytics event streaming pipeline using Kafka, Python, Schema registry and Prefect for workflow orchestration.
Fake user interactions and product-related events are generated to enable real-time analytics and insights.

## Project Overview

The goal is to build a foundation for:

* Real-time analytics dashboards.
* Personalized recommendations.

## Project Structure

```
e-commerce-analytics/
└── docker/
    ├── docker-compose.kafka.yml     # Kafka Zookeeper and Schema Registry
    ├── docker-compose.app.yml       # register schema and producer
├── README.md              # This file
└── src/
    ├── schemas/
    │   ├── register_add_to_cart_schema.py   # Schema definition for AddToCart events
    │   ├── register_abandoned_cart_schema.py 
    │   ├── register_product_catalog_schema.py 
    │   ├── register_all_schemas.py #All schemas
    │   ├── register_purchase_schema.py
    │   └── register_transaction_schema.py 
    └── producers/
    │    ├── produce_add_to_cart.py   # Producer script for AddToCart events
    │    ├── produce_abandoned_cart.py 
    │   ├── produce_product_catalog.py 
    │   ├── produce_purchase.py 
    │   └── produce_transaction.py
    │    └── start_producers.sh #bash script for running all producers
    └── consumers/
        ├── consume_data.py #Consumes data and loads parquet to S3 bucket
```

1.  **Prerequisites:**
    * Docker and Docker Compose installed.
    * Requirements installed.
    ```bash
    pip install -r requirements.text
    ```
    * Amazon S3 bucket

## TO DO

* **Implement Prefect Flows:** Develop Prefect flows to orchestrate the producer and consumer processes.
* **Data Aggregation and Transformation (DBT):** Create data pipelines for aggregating and transforming the raw event data.
* **Testing and Monitoring:** Add comprehensive unit tests and monitoring tools.
* **Cloud Deployment:** Deploy the pipeline to a cloud platform.


