from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
import json

"""
properties - json fields
    productID - product identifier
    name - name of the product
    price - price of the product
    stock - current stock quantity
    category - prodyct category
    reviews - array of customer reviews about the product
"""

schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProductCatalog",
  "description": "Schema for product catalog data",
  "type": "object",
  "properties": {
    "productId": {
      "type": "integer"
    },
    "name": {
      "type": "string"
    },
    "price": {
      "type": "number"
    },
    "stock": {
      "type": "integer"
    },
    "category": {
      "type": "string"
    },
    "reviews": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["productId", "name", "price", "stock", "category", "reviews"]
}
"""

schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

subject_name = 'product-catalogue'
schema = Schema(schema_str=schema_str, schema_type="JSON")

schema_registry_client.register_schema(subject_name=subject_name, schema=schema)

print(f"Schema registered for subject: {subject_name}")