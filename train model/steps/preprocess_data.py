import pandas as pd
import os
from steps.feature_engineering import feature_engineering

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

def process_nans(df, drop_threshold: float = 0.95):
       
    for col in df.columns:

        nulls_prop = df[col].isnull().mean()
        print(f"{col} - {nulls_prop * 100}% missing")

        # drop if missing more than a threshold
        if nulls_prop >= drop_threshold:
            print(f"{bcolors.WARNING}Dropping {col}{bcolors.ENDC}")
            df = df.drop(col, axis=1)
        elif nulls_prop > 0:
            print("Imputing", col)
            # If numeric, impute with bfill
            if df[col].dtype.kind == 'i':
                df[col] = df[col].bfill()
            else:
            # Else, impute with mode
                df[col] = df[col].fillna(df[col].mode()[0])

    return df

def train_val_test_split(df, val_size = 0.2, test_size = 0.1):

    # Calculate the number of rows for each set
    num_rows = len(df)
    val_rows = int(num_rows * val_size)
    test_rows = int(num_rows * test_size)
    train_rows = num_rows - val_rows - test_rows

    # Split the data into train, validation, and test sets
    train_df = df.iloc[:train_rows]
    val_df = df.iloc[train_rows:train_rows+val_rows]
    test_df = df.iloc[train_rows+val_rows:]

    return train_df, val_df, test_df

def create_targets(df):

    df['temperature_3'] = df.shift(-1)['temperature'].astype(float)
    df['temperature_6'] = df.shift(-2)['temperature'].astype(float)
    df['temperature_9'] = df.shift(-3)['temperature'].astype(float)
    df['temperature_12'] = df.shift(-4)['temperature'].astype(float)
    df['temperature_15'] = df.shift(-5)['temperature'].astype(float)
    df['temperature_18'] = df.shift(-6)['temperature'].astype(float)
    df['temperature_21'] = df.shift(-7)['temperature'].astype(float)
    df['temperature_24'] = df.shift(-8)['temperature'].astype(float)

    df.dropna(axis=0, inplace=True)

    return df

def preprocess_data(file_location, CONFIG):

    df = pd.read_csv(file_location, engine='pyarrow', dtype_backend='pyarrow')
    df['temperature'] = df['temperature'].astype(float)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M')
    df = df.set_index('datetime')

    # Preprocess nulls
    df = process_nans(df)

    # Create features
    df = feature_engineering(df)

    # Create targets
    df = create_targets(df)

    # Split data on train, validation, test
    train_df, val_df, test_df = train_val_test_split(df, CONFIG['val_size'], CONFIG['test_size'])

    # Save data
    split_destination_folder = './data/processed'
    if not os.path.exists(split_destination_folder):
        os.makedirs(split_destination_folder)
    
    train_location = split_destination_folder + '/train.csv'
    validation_location = split_destination_folder + '/validation.csv'
    test_location = split_destination_folder + '/test.csv'

    train_df.to_csv(train_location, index=True)
    val_df.to_csv(validation_location, index=True)
    test_df.to_csv(test_location, index=True)

    file_locations = {
        'train-data-dir': train_location,
        'val-data-dir': validation_location,
        'test-data-dir': test_location,
    }

    return file_locations