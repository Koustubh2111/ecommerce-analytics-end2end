from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
import random
import time
from datetime import datetime


# Schema Registry Configuration
schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Kafka Producer Configuration
producer_conf = {
    'bootstrap.servers': 'kafka:9092', #internal connection
}

schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Transaction",
  "description": "Schema for transaction data",
  "type": "object",
  "properties": {
    "transactionId": {
      "type": "integer"
    },
    "userId": {
      "type": "integer"
    },
    "orderId": {
      "type": "integer"
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

subject_name = 'transactions'

#Schema serializer
json_serializer = JSONSerializer(schema_str=schema_str, schema_registry_client=schema_registry_client)

#Config the producer
producer = Producer(producer_conf)

def delivery_report(err, msg):
    """Message delivery"""
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def generate_event():
    """Generate random fake data for events"""
    transaction_id = random.randint(1, 100)
    user_id = random.randint(1, 100)
    order_id = random.randint(1,100)
    payment_info = random.choice(["Debit", "Credit"])
    refunded = random.choice([True, False])
    fraud_signal = random.choice([True, False])
    timestamp = datetime.now().isoformat() 
    return {
            'transactionId' : transaction_id, \
            'userId': user_id, \
            'orderId' : order_id, \
            'paymentInfo' : payment_info, \
            'refunded' : refunded, \
            'fraudSignal' : fraud_signal, \
            'timestamp': timestamp
           }

# Produce Events
test_events = 10
try:
    for i in range(test_events):  # Produce 10 events for testing
        """SerializationContext and MessageField allows for context to be sent, in this case the value"""
        event = generate_event()
        producer.produce(topic=subject_name,
                         value=json_serializer(event, SerializationContext(subject_name, MessageField.VALUE)),
                         on_delivery=delivery_report) #call back to delivery_report sent 
        print(f"Produced message {i+1}, but not yet flushed.")
        producer.flush()
        print(" Flushed message")
        time.sleep(1)  # Wait for 1 second between events
except KeyboardInterrupt:
    pass
finally:
    print("Flushing All messages...")
    producer.flush()



