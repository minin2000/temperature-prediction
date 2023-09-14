import numpy as np
import pandas as pd

def feature_engineering(df):

    df['hour'] = df.index.hour
    df['month'] = df.index.month

    df['hour_sin'] = np.sin(10.2 + (2 * np.pi * df['hour'] / 24))
    df['month_sin'] = np.sin(4.1 + (2 * np.pi * df['month'] / 12))
    df = df.drop(['hour', 'month'], axis=1)

    target_map = df['temperature'].to_dict()
    df['lag_3_hours'] = (df.index - pd.Timedelta('3 hours')).map(target_map).astype(float)
    df['lag_6_hours'] = (df.index - pd.Timedelta('6 hours')).map(target_map).astype(float)
    df['lag_9_hours'] = (df.index - pd.Timedelta('9 hours')).map(target_map).astype(float)
    df['lag_12_hours'] = (df.index - pd.Timedelta('12 hours')).map(target_map).astype(float)
    df['lag_15_hours'] = (df.index - pd.Timedelta('15 hours')).map(target_map).astype(float)
    df['lag_18_hours'] = (df.index - pd.Timedelta('18 hours')).map(target_map).astype(float)
    df['lag_21_hours'] = (df.index - pd.Timedelta('21 hours')).map(target_map).astype(float)

    df['moving_average_1day'] = df['temperature'].rolling(window=8).mean().shift(-8)
    df['moving_average_1week'] = df['temperature'].rolling(window=56).mean().shift(-56)

    df.dropna(axis=0, inplace=True)
    
    return df
