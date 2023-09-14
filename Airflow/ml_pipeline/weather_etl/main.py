import shutil
import os
from datetime import datetime
from extract.init_browser import init_browser
from extract.download_archive import download_archive
from extract.unzip_archive import unzip_archive
from transform.preprocess_data import preprocess_data
from load.update_db_table import update_db_table
from load.create_db_table import create_db_table
from connect_db import connect_db
from config import CONFIG

# Extract XLS with Weather data (https://rp5.ru/Weather_archive_in_Moscow) from date_from_str to date_to_str
def extract(date_from_str = '01.02.2005', date_to_str = datetime.today().strftime('%d.%m.%Y')):
        
    print('Start extract process')

    # Create export folder
    if os.path.exists(CONFIG['export_historical_data_path']):
        shutil.rmtree(CONFIG['export_historical_data_path'])
    os.makedirs(CONFIG['export_historical_data_path'])

    driver = init_browser(CONFIG)

    # Download archive with historical data
    try:
        file_path = download_archive(driver, date_from_str, date_to_str, CONFIG)
    except Exception as ex:
        print(ex)
        print('Failed to load archive')
    finally:
        driver.quit() 

    print('Extract process finished')

    return file_path 


# Transform data to correct format
def transform(file_path):

    print('Start transform process')

    file_path = unzip_archive(file_path)
    data = preprocess_data(file_path)

    print('Transform process finished')

    return data

    
# load to Postgres
def load(data):

    print('Start load process')        
    connection = connect_db(CONFIG)

    #Create weather table if not exist and fill with data 
    first_run = create_db_table(connection, data)
    
    if first_run == False:
        #Update weather table if found new rows
        update_db_table(connection, data)
        print('Load process finished')




def main():

    file_path = extract()
    data = transform(file_path)
    load(data)

if __name__== '__main__':
    main()