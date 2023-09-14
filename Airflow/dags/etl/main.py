from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
from predict.config import CONFIG


def check_new_rows_found(**kwargs):
    xcom = kwargs['ti'].xcom_pull(task_ids='weather_etl') 
    if xcom['new_rows_found']:
        print('New rows found, starting DAG Weather_prediction')
        return 'trigger_predict'
    else:
        print('New rows not found')
        return 'do_nothing' 


with DAG(
    default_args={
    'owner': CONFIG['dag_owner'],
    'retries': CONFIG['dag_retries'],
    'retry_delay': CONFIG['dag_retry_delay']
    },
    dag_id = 'Weather_ETL',
    description='Download archive data for Moscow Weather',
    start_date=datetime(2023, 9, 1),
    schedule_interval='0 1/3 * * *',
    catchup=False
) as dag:
    Weather_etl = DockerOperator(
        task_id="weather_etl",
        image="weather-etl:latest",
        command="python main.py",
        docker_url='unix://var/run/docker.sock',
        mount_tmp_dir = False,
        auto_remove=True,
        retrieve_output=True,
        retrieve_output_path='/tmp/script.out'
    )

    check_new_rows = BranchPythonOperator(
    task_id='check_new_rows_found',
    python_callable=check_new_rows_found,
    provide_context=True
    )

    trigger_dag_predict = TriggerDagRunOperator(
        task_id='trigger_predict',
        trigger_dag_id='Weather_prediction',
        wait_for_completion=True
    )
    
    do_nothing_task = DummyOperator(
        task_id='do_nothing'
    )

Weather_etl >> check_new_rows >> [trigger_dag_predict, do_nothing_task]