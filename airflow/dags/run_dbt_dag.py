from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Paths inside the container
DBT_DIR = '/opt/airflow/dbt'
LOG_DIR = '/opt/airflow/logs'

dag = DAG(
    dag_id='dbt_run_with_logging',
    start_date=datetime.now() - timedelta(days=1),
    schedule='@daily',
    catchup=False,
    tags=['dbt'],
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command=(
        f'cd {DBT_DIR} && '
        f'dbt run --profiles-dir {DBT_DIR} --project-dir . '
        f'--log-path {LOG_DIR} --log-level debug '
        f'2>&1 | tee {LOG_DIR}/dbt_run_{{{{ ts_nodash }}}}.log'
    ),
    dag=dag,
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=(
        f'mkdir -p {LOG_DIR} && '
        f'cd {DBT_DIR} && '
        f'dbt test --profiles-dir {DBT_DIR} --project-dir . '
        f'--log-path {LOG_DIR} --log-level debug '
        f'2>&1 | tee {LOG_DIR}/dbt_test_{{{{ ts_nodash }}}}.log'
    ),
    dag=dag,
)

dbt_run >> dbt_test

