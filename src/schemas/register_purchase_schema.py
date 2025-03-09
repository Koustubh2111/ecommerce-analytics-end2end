from confluent_kafka.schema_registry import SchemaRegistryClient
import json

"""
properties - json fields
    userId - identifier of the user who purchased the product
    orderID - Order identifier
    product_ID - Product identifier
    timestamp - timestamp when the purchase was made
    quantity - number of items of the product purchased
    price - single unit price
"""

schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Purchase",
  "description": "Schema for purchase events",
  "type": "object",
  "properties": {
    "userId": {
      "type": "integer"
    },
    "orderId": {
      "type": "string"
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
    },
    "price": {
      "type": "number"
    }
  },
  "required": ["userId", "orderId", "productId", "timestamp", "quantity", "price"]
}
"""

schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

subject_name = 'purchase-events'
schema_registry_client.register_schema(subject_name, schema_str, schema_type="JSON")

print(f"Schema registered for subject: {subject_name}")