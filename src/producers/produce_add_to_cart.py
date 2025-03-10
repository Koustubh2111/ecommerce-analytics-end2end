from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
import random
import time


# Schema Registry Configuration
schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Kafka Producer Configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092', #kafka port
}

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

subject_name = 'add-to-cart-events'

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

def generate_add_to_cart_event():
    """Generate random fake data for events"""
    user_id = random.randint(1, 100)
    product_id = random.randint(101, 200)
    quantity = random.randint(1, 10)
    timestamp = int(time.time())
    return {
            'userId': user_id, \
            'productId': product_id, \
            'quantity': quantity, \
            'timestamp': timestamp
           }

# Produce Events
test_events = 10
try:
    for i in range(test_events):  # Produce 10 events for testing
        """SerializationContext and MessageField allows for context to be sent, in this case the value"""
        event = generate_add_to_cart_event()
        producer.produce(topic=subject_name,
                         value=json_serializer(event, SerializationContext(subject_name, MessageField.VALUE)),
                         on_delivery=delivery_report) #call back to delivery_report sent 
        print(f"Produced message {i}, but not yet flushed.")
        producer.flush()
        print(" Flushed message")
        time.sleep(1)  # Wait for 1 second between events
except KeyboardInterrupt:
    pass
finally:
    print("Flushing All messages...")
    producer.flush()



