import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = "data/mimic_sample.csv"
MODEL_OUTPUT_PATH = "ml_model/severity_predictor.pkl"
os.makedirs("ml_model", exist_ok=True)

def load_and_prepare_data(path):
    df = pd.read_csv(path)

    # Fill and engineer note features
    df["notes"] = df["notes"].fillna("").astype(str)
    df["note_length"] = df["notes"].apply(len)
    df["num_words"] = df["notes"].apply(lambda x: len(x.split()))
    df["avg_word_length"] = df["notes"].apply(lambda x: sum(len(w) for w in x.split()) / len(x.split()) if x.split() else 0)

    # Handle vitals/labs from available columns
    for col in ["heart_rate", "temperature", "systolic_bp", "diastolic_bp", "wbc_count", "hemoglobin"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())
        else:
            df[col] = 0

    df["has_notes"] = df["notes"].notna().astype(int)
    df["bp_diff"] = df["systolic_bp"] - df["diastolic_bp"]
    df["vitals_score"] = df["heart_rate"] + df["temperature"] + df["wbc_count"]

    # Categorical fields
    df["gender"] = df["gender"].fillna("UNKNOWN")
    df["admission_type"] = df["admission_type"].fillna("UNKNOWN")

    numeric_features = [
        "note_length", "num_words", "avg_word_length", "heart_rate", "temperature",
        "systolic_bp", "diastolic_bp", "wbc_count", "hemoglobin", "bp_diff",
        "vitals_score"
    ]
    categorical_features = ["gender", "admission_type"]

    if "severe" not in df.columns:
        df["severe"] = ((df["heart_rate"] > 100) | (df["wbc_count"] > 12)).astype(int)

    features = df[numeric_features + categorical_features]
    labels = df["severe"]

    return features, labels, numeric_features, categorical_features

def train_model(X, y, numeric_features, categorical_features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ])

    model_pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42))
    ])

    model_pipeline.fit(X_train, y_train)
    predictions = model_pipeline.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))

    joblib.dump(model_pipeline, MODEL_OUTPUT_PATH)
    print(f"Model saved to {MODEL_OUTPUT_PATH}")

if __name__ == "__main__":
    X, y, num_cols, cat_cols = load_and_prepare_data(DATA_PATH)
    train_model(X, y, num_cols, cat_cols)