# MIMIC EHR Severity Prediction Pipeline

This project simulates real-time EHR data ingestion using synthetic MIMIC-IV patient data and applies a machine learning pipeline to classify patient severity. It includes an end-to-end system for data streaming, feature engineering, model training, prediction, and exporting results to Snowflake for downstream analytics and clinical decision support.

## Features

- Real-time simulation of patient telemetry and note data
- Feature engineering from clinical text and vitals/labs
- Severity classification using Random Forest
- Outputs augmented data streams to Snowflake
- Modular and extensible pipeline for future model integration

## Machine Learning Details

The model is a `RandomForestClassifier` trained on derived features including:
- Text-derived statistics (note length, word count)
- Vitals and lab values (e.g., heart rate, WBC count)
- Categorical data (gender, admission type)
- Engineered features (blood pressure difference, vitals score)

Labels are binary (`severe` vs. `non-severe`) based on thresholding heuristics.

## File Structure

```
mimic-ehr-pipeline/
├── data/                      # Input CSVs (vitals, labs, notes)
├── ml_model/                  # Trained model artifacts (.pkl files)
├── config.py                  # Configuration settings (Snowflake, thresholds)
├── train_model.py             # Training pipeline for feature extraction and model fitting
├── realtime_etl.py            # Simulates real-time ingestion + scoring
└── utils.py                   # Helper functions (feature engineering)              
```


## Use Case
This script uses patient data to train a Random Forest model and serialize it to model.pkl. Ideal for data scientists and clinical engineers prototyping risk scoring models on real-time health data feeds.

### Start Kafka locally or connect to your streaming service.

```bash
pip install -r requirements.txt
python stream_producer.py
```

### Run the ETL + ML scoring pipeline:

```bash
python etl_pipeline.py
```

### Model Training 

```bash
python train_model.py #
```

## License
This project is licensed under the MIT License.
