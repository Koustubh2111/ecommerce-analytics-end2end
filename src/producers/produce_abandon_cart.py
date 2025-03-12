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

subject_name = 'abandon-cart'

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
    user_id = random.randint(1, 100)
    product_id = random.randint(101, 200)
    timestamp = datetime.now().isoformat() 
    return {
            'userId': user_id, \
            'productId': product_id, \
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



