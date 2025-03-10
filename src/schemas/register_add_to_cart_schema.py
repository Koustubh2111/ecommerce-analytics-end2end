from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
import json

"""
schema - JSON schema version
title - schema title
properties - json fields
    userId - identifier of the user who added an product into the cart
    product_ID - Product identifier
    timestamp - timestamp when the product added to cart
    quantity - number of items of the product added to cart

"""

schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AddToCart",
  "description": "Schema for add-to-cart events",
  "type": "object",
  "properties": {
    "userId": {
      "type": "integer"
    },
    "productId": {
      "type": "integer"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "quantity": {
      "type": "integer"
    }
  },
  "required": ["userId", "productId", "timestamp", "quantity"] 
}
"""

schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

subject_name = 'add-to-cart-events'

schema = Schema(schema_str=schema_str, schema_type="JSON")

schema_registry_client.register_schema(subject_name=subject_name, schema=schema)

print(f"Schema registered for subject: {subject_name}")