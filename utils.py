import json
from datetime import datetime
import random
import time
import joblib
import numpy as np
import os

# Load pre-trained ML model
MODEL_PATH = "ml_model/severity_predictor.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def validate_event(event: dict) -> bool:
    required_fields = ["timestamp", "event_type", "patient_id"]
    return all(field in event for field in required_fields)

def enrich_event(event: dict) -> dict:
    event["processed_at"] = datetime.utcnow().isoformat()
    event["processing_latency_ms"] = random.randint(10, 100)
    event["etl_version"] = "v1.3.0"
    return event

def generate_ml_features(event: dict) -> list:
    # Create a numeric feature vector from event data
    return [
        float(event.get("heart_rate", 0)),
        float(event.get("spo2", 0)),
        float(event.get("sbp", 0)),
        float(event.get("dbp", 0)),
        float(event.get("temp_c", 0)),
        float(event.get("wbc_count", 0)),
        float(event.get("hemoglobin", 0)),
        float(event.get("platelets", 0)),
        len(str(event.get("notes", ""))),
        1 if event.get("event_type") == "VITAL_SIGNS" else 0,
        1 if event.get("event_type") == "LAB_RESULT" else 0
    ]

def predict_event_severity(event: dict) -> float:
    if not model:
        return round(random.uniform(0.1, 0.9), 2)
    features = generate_ml_features(event)
    severity_score = model.predict_proba([features])[0][1]  # probability of class 1
    return round(severity_score, 2)

def write_to_snowflake(event: dict):
    print("[Snowflake] Inserted:", json.dumps(event))
