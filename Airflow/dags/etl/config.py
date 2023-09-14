from datetime import timedelta

CONFIG = {
    'dag_owner': 'Alexey',
    'dag_retries': 3,
    'dag_retry_delay': timedelta(minutes=2),
    'export_historical_data_path': '/tmp/Downloads/Historical_data',
    'postgres_conn_id': 'postgres_localhost',
    'postgres_schema': 'postgres',
    # Postgres connection
    'db_host' : 'localhost',
    'db_name' : 'postgres',
    'db_user' : 'username',
    'db_password' : 'qwerty',
    'db_port' : 5432
}