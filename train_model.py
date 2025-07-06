import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib, os
from utils import generate_ml_features

# Paths
DATA_DIR = "data/mimiciv"
MODEL_DIR = "ml_model"
os.makedirs(MODEL_DIR, exist_ok=True)

# Load required tables
print("Loading MIMIC-IV tables...")
chartevents = pd.read_csv(f"{DATA_DIR}/chartevents.csv", usecols=[
    "subject_id", "hadm_id", "charttime", "itemid", "valuenum"])
labevents = pd.read_csv(f"{DATA_DIR}/labevents.csv", usecols=[
    "subject_id", "hadm_id", "charttime", "itemid", "valuenum"])
icustays = pd.read_csv(f"{DATA_DIR}/icustays.csv", usecols=[
    "subject_id", "hadm_id", "intime", "outtime"])
admissions = pd.read_csv(f"{DATA_DIR}/admissions.csv", usecols=[
    "subject_id", "hadm_id", "admittime", "dischtime", "hospital_expire_flag"])
noteevents = pd.read_csv(f"{DATA_DIR}/noteevents.csv", usecols=[
    "subject_id", "hadm_id", "chartdate", "text"])

# Use mortality label as severity
admissions['severity'] = admissions['hospital_expire_flag']

# Merge labevents with severity
print("Merging and cleaning data...")
df = pd.merge(labevents, admissions[['subject_id', 'hadm_id', 'severity']],
              on=['subject_id', 'hadm_id'])
df = pd.merge(df, noteevents, on=['subject_id', 'hadm_id'], how='left')
df = df.dropna(subset=['valuenum', 'text'])

print("Preprocessing features...")
df['hour'] = pd.to_datetime(df['charttime']).dt.hour
df['note_len'] = df['text'].str.len()

def extract_features(row):
    return generate_ml_features({
        "notes": row['text'],
        "event_type": "LAB_RESULT",
        "department": "N/A",
        "note_len": row['note_len'],
        "valuenum": row['valuenum'],
        "hour": row['hour']
    })

features = df.apply(extract_features, axis=1, result_type='expand')
labels = df['severity']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train model
print("Training model...")
model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
model.fit(X_train, y_train)
print("Model accuracy:", model.score(X_test, y_test))

joblib.dump(model, f"{MODEL_DIR}/severity_predictor.pkl")
print("Model saved to ml_model/severity_predictor.pkl")
