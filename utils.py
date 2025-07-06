import json
from datetime import datetime
import random
import time
import joblib
import numpy as np
import os

# Load ML model 
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
    # Extract meaningful features from event
    timestamp = event.get("timestamp", "")
    event_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S") if timestamp else datetime.utcnow()
    hour_of_day = event_time.hour
    
    event_type = event.get("event_type", "UNKNOWN")
    type_encoded = {
        "VITAL_SIGNS": 1,
        "LAB_RESULT": 2,
        "PRESCRIPTION": 3,
        "ADMISSION": 4,
        "DISCHARGE": 5
    }.get(event_type, 0)

    department_length = len(event.get("department", ""))
    notes_length = len(event.get("notes", ""))
    is_critical = 1 if "critical" in event.get("notes", "").lower() else 0
    
    return [
        hour_of_day,
        type_encoded,
        department_length,
        notes_length,
        is_critical
    ]

def predict_event_severity(event: dict) -> float:
    if not model:
        return round(random.uniform(0.1, 0.9), 2)
    features = generate_ml_features(event)
    severity_score = model.predict_proba([features])[0][1]  # probability of class 1
    return round(severity_score, 2)

def write_to_snowflake(event: dict):
    print("[Snowflake] Inserted:", json.dumps(event))
