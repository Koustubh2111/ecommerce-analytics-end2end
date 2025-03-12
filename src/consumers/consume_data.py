from confluent_kafka import Consumer, KafkaException, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
import json
import boto3
import os
from dotenv import load_dotenv
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from schemas import schema

# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


# Initialize Boto3 S3 client with credentials from .envpi
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Schema Registry Configuration
schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Kafka Consumer Configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9093',  # Internal connection to Kafka
    'group.id': 'ecommerce-consumer-group',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
}

def json_to_parquet(json_data):
    """Convert JSON to Parquet format"""
    # Convert the JSON to a pandas DataFrame
    df = pd.json_normalize(json_data)
    
    # Save DataFrame to a Parquet file in memory
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
    parquet_buffer.seek(0)  # Rewind to the beginning of the buffer
    return parquet_buffer

def upload_to_s3(parquet_data, s3_key):
    """Upload Parquet data to S3 bucket."""
    try:
        s3_client.put_object(Body=parquet_data, Bucket=S3_BUCKET_NAME, Key=s3_key)
        print(f"Data successfully uploaded to S3: {s3_key}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")




def consume_messages(json_deserializer, consumer):
    """Consume messages from Kafka and print them."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for a message with 1-second timeout
            
            if msg is None:
                # No message received within the timeout period
                continue
            if msg.error():
                # Handle error if any
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    print(f"Error: {msg.error()}")
                continue

            # Print the raw message value
            print(f"Consumed message: {msg.value()}")
            try:
                # Try deserializing the message if possible (if JSON formatted)
                serialization_context = SerializationContext(topic=msg.topic(), field=MessageField.VALUE)
                message_value = json_deserializer(msg.value(), serialization_context)
                if message_value is not None:
                    print(f"Deserialized message: {message_value}")
                    # Convert JSON message to Parquet and upload to S3
                    parquet_data = json_to_parquet(message_value)
                    s3_key = f"events/{msg.topic()}/{message_value['userId']}/{message_value['productId']}/{message_value['timestamp']}.parquet"
                    upload_to_s3(parquet_data, s3_key)
                else:
                    print(f"Deserialization failed for message: {msg.value()}")
            except Exception as e:
                print(f"Error deserializing message: {e}")
                
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
  for topic, schema_str in schema.items():

    # Define the deserializer
    json_deserializer = JSONDeserializer(schema_str=schema_str, schema_registry_client=schema_registry_client)

    # Initialize the consumer
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    #Consume
    consume_messages(json_deserializer, consumer)


