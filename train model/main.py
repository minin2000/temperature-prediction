from connect_db import connect_db
from steps.download_raw_data import load_raw_data
from steps.preprocess_data import preprocess_data
from steps.tune_model import tune_model
from steps.train_model import train_model
from config import CONFIG
import mlflow
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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

def pipeline():

    mlflow.set_experiment('Weather_prediction')

    connection = connect_db(CONFIG)
    params = CONFIG['params']

    print(f"{bcolors.OKCYAN}Loading data{bcolors.ENDC}")
    data_raw_location = load_raw_data(CONFIG, connection)
    print(f"{bcolors.OKCYAN}Data is loaded{bcolors.ENDC}")

    print(f"{bcolors.OKCYAN}Preprocessing data{bcolors.ENDC}")   
    file_dirs = preprocess_data(data_raw_location, CONFIG)
    print(f"{bcolors.OKCYAN}Data is preprocessed{bcolors.ENDC}")

    # Comment if doesn't need tune
    # print(f"{bcolors.OKCYAN}Tunning hyperparameters{bcolors.ENDC}")
    # params = tune_model(file_dirs, CONFIG)
    # print(f"{bcolors.OKCYAN}Hyperparameters tunning is finished{bcolors.ENDC}")
    
    print(f"{bcolors.OKCYAN}Training is started{bcolors.ENDC}")
    mae = train_model(file_dirs, params)
    print(f"{bcolors.OKGREEN}Final model is trained. \nTestset MAE: {mae}")
    
if __name__== '__main__':
    pipeline()