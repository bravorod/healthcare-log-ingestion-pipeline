
from prefect import flow, task

@task
def extract():
    print("Extracting events from Kafka...")

@task
def transform():
    print("Transforming events...")

@task
def load():
    print("Loading events into Snowflake...")

@flow(name="Healthcare Log ETL")
def etl_flow():
    data = extract()
    processed = transform()
    load()

if __name__ == "__main__":
    etl_flow()
