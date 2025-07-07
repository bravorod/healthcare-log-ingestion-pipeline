# config.py

def load_kafka_config():
    return {
        "bootstrap_servers": "localhost:9092",
        "topic": "ehr-logs",
        "group_id": "etl-consumer-group"
    }
