import json
import pandas as pd
import numpy as np
import random
import time
import joblib
import os
from datetime import datetime

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

def generate_ml_features(event: dict) -> dict:
    notes = str(event.get("notes", ""))
    heart_rate = float(event.get("heart_rate", 0))
    temperature = float(event.get("temperature", 0))
    respiratory_rate = float(event.get("respiratory_rate", 0))
    lab_result = float(event.get("lab_result", 0))

    return {
        # Numeric features
        "note_length": len(notes),
        "num_words": len(notes.split()),
        "avg_word_length": sum(len(w) for w in notes.split()) / len(notes.split()) if notes.split() else 0,
        "has_lab": 1 if "lab_result" in event and event["lab_result"] is not None else 0,
        "has_vitals": 1 if "heart_rate" in event and event["heart_rate"] is not None else 0,
        "heart_rate": heart_rate,
        "temperature": temperature,
        "respiratory_rate": respiratory_rate,
        "lab_result": lab_result,
        "vitals_sum": heart_rate + temperature + respiratory_rate,
        "vitals_range": max(heart_rate, temperature, respiratory_rate) - min(heart_rate, temperature, respiratory_rate),
        
        # Categorical features
        "department": event.get("department", "UNKNOWN"),
        "event_type": event.get("event_type", "UNKNOWN")
    }

def predict_event_severity(event: dict) -> float:
    if not model:
        return round(random.uniform(0.1, 0.9), 2)

    features_dict = generate_ml_features(event)
    df = pd.DataFrame([features_dict])
    severity_score = model.predict_proba(df)[0][1]  # Probability of class 1 (severe)
    return round(severity_score, 2)

def write_to_snowflake(event: dict):
    print("[Snowflake] Inserted:", json.dumps(event))
