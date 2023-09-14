import pandas as pd
from steps.feature_engineering import feature_engineering

def process_nans(df):
       
    for col in df.columns:

        nulls_prop = df[col].isnull().mean()
        print(f"{col} - {nulls_prop * 100}% missing")

        if nulls_prop > 0:
            print("Imputing", col)
            # If numeric, impute with bfill
            if df[col].dtype.kind == 'i':
                df[col] = df[col].bfill()
            else:
            # Else, impute with mode
                df[col] = df[col].fillna(df[col].mode()[0])

    return df

def preprocess_data(df):

    df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M')
    df['temperature'] = df['temperature'].astype(float)
    df = df.set_index('datetime')

    # Preprocess nulls
    df = process_nans(df)

    # Create features
    df = feature_engineering(df)

    return df