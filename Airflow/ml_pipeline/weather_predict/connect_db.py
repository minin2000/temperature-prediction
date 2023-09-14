import psycopg2
import os

def connect_db(CONFIG):

    # If run in Docker, change db_host (Connect to local DB)
    SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
    if SECRET_KEY:
        CONFIG['db_host'] = 'host.docker.internal'
        
    try:
        connection = psycopg2.connect(
            host = CONFIG['db_host'],
            dbname = CONFIG['db_name'],
            user = CONFIG['db_user'],
            password = CONFIG['db_password'],
            port = CONFIG['db_port']
        )
    except Exception as error:
            print(error)
            print('Failed to connect to DB')
            connection.close()
            raise

    return connection
