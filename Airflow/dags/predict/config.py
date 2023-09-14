from datetime import timedelta

CONFIG = {
    'dag_owner': 'Alexey',
    'dag_retries': 3,
    'dag_retry_delay': timedelta(minutes=2)
}