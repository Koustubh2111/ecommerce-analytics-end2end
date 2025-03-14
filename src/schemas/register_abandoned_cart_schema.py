from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
import json

"""
properties - json fields
    userId - identifier of the user who abandoned the cart
    product_ID - abandoned product identifier
    timestamp - timestamp when product was abandoned
"""

schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AbandonedCart",
  "description": "Schema for abandoned cart events",
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
    }
  },
  "required": ["userId", "productId", "timestamp"]
}
"""

schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

subject_name = 'abandon-cart'
schema = Schema(schema_str=schema_str, schema_type="JSON")

schema_registry_client.register_schema(subject_name=subject_name, schema=schema)

print(f"Schema registered for subject: {subject_name}")