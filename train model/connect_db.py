import psycopg2
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
            print(f"{bcolors.FAIL}Failed to connect to DB{bcolors.ENDC}")
            connection.close()
            raise

    return connection
