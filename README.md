# Healthcare Log Ingestion Pipeline

This project showcases a simplified data ingestion pipeline designed for streaming and batch processing of healthcare-related event logs. It simulates an end-to-end architecture for ingesting semi-structured JSON data from a Kafka topic, processing it with Prefect, and loading it into a Snowflake data warehouse.

## 🧰 Technologies Used

- **Python** – core language for pipeline logic and orchestration
- **Kafka** – source system for streaming JSON logs
- **Prefect** – orchestration tool for DAG control and scheduling
- **Snowflake** – cloud data warehouse used for storing normalized healthcare data
- **JSON** – format for raw event data
- **SQL** – used for schema creation and transformation logic

## 📂 Project Structure

| File | Description |
|------|-------------|
| `etl_pipeline.py` | Main ETL script for reading Kafka messages and writing to Snowflake |
| `prefect_flow.py` | Prefect DAG definition for scheduling and orchestrating ETL jobs |
| `kafka_config.json` | Sample Kafka config stub with placeholder credentials and topic metadata |
| `sample_data.json` | Simulated input records containing healthcare event data |
| `snowflake_schema.sql` | SQL DDL script to create staging and analytics-ready tables |
| `README.md` | Project documentation |

## ⚙️ Pipeline Overview

1. **Data Source**: Simulated healthcare events are produced into a Kafka topic.
2. **Processing**: Prefect orchestrates a Python ETL flow which:
   - Reads and parses Kafka messages (`sample_data.json`)
   - Applies basic normalization and cleansing logic
   - Loads records into a Snowflake staging table
3. **Storage**: Snowflake holds the ingested data in both raw and transformed forms for downstream analytics.

## 🔍 Use Case

While simplified, this pipeline mimics the ingestion workflows used in healthcare environments where logs from electronic health records (EHR), SIEMs, or transactional systems must be processed reliably and securely for analytics and compliance monitoring.

## 🚧 Disclaimer

This repo is a demonstration project and does **not** include real PHI or production configurations. All data, credentials, and schemas are synthetic and for educational purposes only.
