from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from airflow import DAG

# Mapping: filename -> destination table name
CSV_FILES = {
    'apartments.csv': 'apartments',
    'apartment_attributes.csv': 'apartment_attributes',
    'user_viewings.csv': 'user_viewings',
}

DATA_DIR = '/opt/airflow/analytics_data/'  # Directory where CSV files are stored

def load_csvs_to_postgres():
    # SQLAlchemy connection to Postgres
    conn = BaseHook.get_connection('analytics_postgres')
    engine = create_engine(f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')

    for filename, table in CSV_FILES.items():
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            continue

        # Read CSV and push to Postgres
        df = pd.read_csv(file_path)
        df.to_sql(table, engine, if_exists='append', index=False)
        print(f"Inserted {len(df)} rows into {table}.")

with DAG(
    dag_id='db_load_csvs',
    start_date=datetime.now() - timedelta(days=1),
    schedule='@daily',
    catchup=False,
    tags=['csvs'],
) as dag:

    load_task = PythonOperator(
        task_id='load_csvs',
        python_callable=load_csvs_to_postgres
    )

    load_task
