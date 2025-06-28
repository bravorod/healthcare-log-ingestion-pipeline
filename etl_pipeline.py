
# Sample ETL job that simulates pulling events from Kafka and writing to Snowflake
from kafka import KafkaConsumer
import json

def consume_kafka_messages():
    consumer = KafkaConsumer('ehr-logs', bootstrap_servers='localhost:9092')
    for message in consumer:
        event = json.loads(message.value)
        print("Ingested event:", event)

if __name__ == "__main__":
    consume_kafka_messages()
