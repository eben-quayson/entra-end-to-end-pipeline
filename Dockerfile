FROM apache/airflow:latest 

USER root

# Install system dependencies for dbt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch to airflow user
USER airflow

# Install dbt core and dbt-postgres
RUN pip install --no-cache-dir dbt-core==1.7.6 dbt-postgres==1.7.6 asyncpg

