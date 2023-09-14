import pandas as pd
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

def load_raw_data(CONFIG, connection):
    # If run in Docker, change db_host (Connect to local DB)
    if os.path.exists('/proc/1/cgroup'):
        CONFIG['db_host'] = 'host.docker.internal'

    # Select rows from DB
    cursor = connection.cursor()  
    cursor.execute(f'''  SELECT *
                FROM weather where datetime >='{CONFIG['date_from']}' and datetime <= '{CONFIG['date_to']}'
                and EXTRACT(HOUR FROM datetime) % 3 = 0
                ORDER BY datetime ASC; 
        ''')    
    rows = cursor.fetchall()

    # Create Pandas Dataframe
    column_names = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(rows, columns=column_names)

    # Check if the destination folder exists, and create it if it does not
    destination_folder = "./data/"
    raw_destination_folder = os.path.join(destination_folder, "raw")
    if not os.path.exists(raw_destination_folder):
        os.makedirs(raw_destination_folder)

    # Extract data as CSV file
    csv_location = raw_destination_folder + '/data.csv'
    data.to_csv(csv_location, index = False)

    return csv_location