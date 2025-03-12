from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import boto3
import os
from dotenv import load_dotenv
from schemas import schema

# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Kafka Configuration
KAFKA_BROKER = 'localhost:9093'
TOPICS = list(schema.keys())

# Initialize Boto3 S3 client with credentials from .env
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    print(f"S3 Bucket '{S3_BUCKET_NAME}' connection successful.")
except Exception as e:
    print(f"Error connecting to S3: {e}")
    exit(1) #Exit if S3 connection fails.

# Initialize the Spark session
try:
    spark = SparkSession.builder \
        .appName("Kafka2s3") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk:1.11.655") \
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID) \
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
        .getOrCreate()
except Exception as e:
    print(f"Error initializing Spark: {e}")
    exit(1) #Exit if Spark initialization fails.


# Example: Check Spark session
print(f'Spark version : {spark.version}')

# Read Kafka stream with Spark Structured Streaming
try:
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", ",".join(TOPICS)) \
        .option("startingOffsets", "earliest") \
        .load()
    print(f"Kafka connection successful. Able to read from topic: {TOPICS[0]}")
except Exception as e:
    print(f"Error connecting to Kafka: {e}")
    exit(1) #Exit if Kafka connection fails.

# Convert Kafka binary value column to string
df_string = df.selectExpr("CAST(value AS STRING) as json_value", "topic")

# Write the processed data to S3 in Parquet format, per topic
def write_to_s3(batch_df, batch_id):
    """Better alternative to .format(parquet) and .option(path, "path")"""
    print(f"write_to_s3 called with batch_id: {batch_id}")
    for topic in TOPICS:
        topic_df = batch_df.filter(col("topic") == topic)
        print(f"topic_df count: {topic_df.count()}")
        if not topic_df.rdd.isEmpty(): #Check if the topic has data.
            try:
                topic_df.write \
                    .mode("append") \
                    .parquet(f"s3a://{S3_BUCKET_NAME}/events/{topic}")
                print(f"Batch {batch_id} written to S3 for topic: {topic}")
            except Exception as e:
                print(f"Error writing to S3 for topic {topic}: {e}")

# Write the processed data to S3 in Parquet format
query = df_string.writeStream \
    .foreachBatch(write_to_s3) \
    .option("checkpointLocation", f"s3a://{S3_BUCKET_NAME}/checkpoint") \
    .trigger(processingTime="30 seconds") \
    .start()


# Await termination
query.awaitTermination()

