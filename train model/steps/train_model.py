import xgboost as xgb
import pandas as pd
from sklearn.metrics import mean_absolute_error
import mlflow
import os

def train_model(file_dirs, params):
    
    # Load data
    train_df = pd.read_csv(file_dirs['train-data-dir'], index_col='datetime')
    val_df = pd.read_csv(file_dirs['val-data-dir'], index_col='datetime')
    test_df = pd.read_csv(file_dirs['test-data-dir'], index_col='datetime')

    # Split target and features
    target_columns = ['temperature_3', 'temperature_6', 'temperature_9', 'temperature_12', 'temperature_15', 'temperature_18', 'temperature_21', 'temperature_24']
    X_train = train_df.drop(target_columns, axis=1)
    y_train = train_df[target_columns]
    X_val = val_df.drop(target_columns, axis=1)
    y_val = val_df[target_columns]
    X_test = test_df.drop(target_columns, axis=1)
    y_test = test_df[target_columns]

    # If param in config set as None, delete param
    params = {key: param for key, param in params.items() if param != None}

    with mlflow.start_run():
        mlflow.autolog()

        model = xgb.XGBRegressor(**params, early_stopping_rounds=50, eval_metric="mae")
        model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

        # Predict
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        mlflow.log_metric("MAE", mae)
        mlflow.log_artifact('config.py')

        # Check if the 'output' folder exists, and create it if it does not
        if not os.path.exists('output'):
            os.makedirs('output')
        # Save model to folder 'output'
        model.save_model('output/model.xgb')

    return mae