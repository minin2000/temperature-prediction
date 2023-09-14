from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from predict.config import CONFIG

with DAG(
    default_args={
    'owner': CONFIG['dag_owner'],
    'retries': CONFIG['dag_retries'],
    'retry_delay': CONFIG['dag_retry_delay']
    },
    dag_id = 'Weather_prediction',
    description='Predict weather for the next 24 hours',
    start_date=datetime(2023, 9, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    predict = DockerOperator(
        task_id="predict",
        image="weather-prediction:latest",
        command="python main.py",
        docker_url='unix://var/run/docker.sock',
        mount_tmp_dir = False,
        auto_remove=True
    )

    predict