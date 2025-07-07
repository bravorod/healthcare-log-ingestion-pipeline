import json
import logging
from datetime import datetime
from kafka import KafkaConsumer
from utils import (
    validate_event,
    enrich_event,
    write_to_snowflake,
    predict_event_severity
)
from config import load_kafka_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("realtime_etl.log"),
        logging.StreamHandler()
    ]
)

class HealthcareETLPipeline:
    def __init__(self):
        kafka_cfg = load_kafka_config()
        self.topic = kafka_cfg["topic"]
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=kafka_cfg["group_id"]
        )
        logging.info(f"Initialized Kafka consumer on topic: {self.topic}")

    def run(self):
        logging.info("Starting message consumption loop...")
        for message in self.consumer:
            try:
                raw_event = message.value
                logging.debug(f"Received event: {raw_event}")

                if not validate_event(raw_event):
                    logging.warning("Invalid event structure. Skipping...")
                    continue

                enriched_event = enrich_event(raw_event)

                # Predict severity using full DataFrame feature logic
                severity_score = predict_event_severity(enriched_event)
                enriched_event["severity_score"] = severity_score

                logging.info(f"Event scored with severity {severity_score}. Writing to Snowflake...")
                write_to_snowflake(enriched_event)

            except Exception:
                logging.error("Error processing event:", exc_info=True)

if __name__ == "__main__":
    etl = HealthcareETLPipeline()
    etl.run()
