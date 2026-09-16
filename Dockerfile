FROM apache/airflow:2.7.1-python3.11

USER root
#Install system dependencies if needed
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

USER airflow
#Copy requirements and install custom dependencies into Airflow container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy source code into Airflow's python path
COPY src/ /opt/airflow/src/