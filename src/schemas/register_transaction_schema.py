from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
import json

"""
properties - json fields
    transactionID - transaction identifier
    userID - user identifier for the transaction
    orderID - order identifier for the transaction
    paymentInfo - information about type of payment
    refunded - refund flag
    fraudSignal - potentially fradualent transaction
    timstamp - transaction timestamp
"""

schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Transaction",
  "description": "Schema for transaction data",
  "type": "object",
  "properties": {
    "transactionId": {
      "type": "string"
    },
    "userId": {
      "type": "integer"
    },
    "orderId": {
      "type": "string"
    },
    "paymentInfo": {
      "type": "string"
    },
    "refunded": {
      "type": "boolean"
    },
    "fraudSignal": {
      "type": "boolean"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["transactionId", "userId", "orderId", "paymentInfo", "refunded", "fraudSignal", "timestamp"]
}
"""

schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

subject_name = 'transactions'
schema = Schema(schema_str=schema_str, schema_type="JSON")

schema_registry_client.register_schema(subject_name=subject_name, schema=schema)

print(f"Schema registered for subject: {subject_name}")