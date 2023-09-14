import pandas as pd

def preprocess_data(file_path):
    
    data = pd.read_excel(file_path, skiprows=6, usecols=['Local time in Moscow', 'T'])
    data.rename(columns={'Local time in Moscow': 'datetime', 'T': 'temperature'}, inplace=True)
    data['datetime'] = pd.to_datetime(data['datetime'], dayfirst=True)

    return data