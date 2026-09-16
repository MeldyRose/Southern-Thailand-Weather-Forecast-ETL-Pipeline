FROM apache/airflow:3.2.0

USER airflow

# Copy requirements and install custom dependencies into Airflow container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into Airflow's python path
COPY src/ /opt/airflow/src/