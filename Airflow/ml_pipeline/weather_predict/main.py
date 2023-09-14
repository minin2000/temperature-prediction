import xgboost as xgb
from config import CONFIG
from steps.download_raw_data import download_raw_data
from steps.preprocess_data import preprocess_data
from steps.postprocess_data import postprocess_data
from steps.create_db_table import create_db_table
from connect_db import connect_db
from steps.insert_to_db_table import insert_to_db_table
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def predict():
    connection = connect_db(CONFIG)

    # Check and create table 'weather_predictions' if it's not exist in Database
    create_db_table(connection)

    # Load model
    model = xgb.Booster()
    model.load_model('model.xgb')

    # Load latest data to do predictions
    df_raw = download_raw_data(connection)
    print('Data is loaded')

    # Preprocess data
    df = preprocess_data(df_raw)
    print('Data is preprocessed')

    # Predict
    data_matrix = xgb.DMatrix(df)
    predictions_df = model.predict(data_matrix)

    # Postprocess predictions to bring data to the correct form for writing to Database
    predictions_df = postprocess_data(df, predictions_df)
    
    # Insert predicted values to 'weather_predictions'
    insert_to_db_table(predictions_df, connection)

    from_datetime_str = predictions_df.iloc[0]['datetime'].strftime("%d.%m.%Y %H:%M")
    to_datetime_str = predictions_df.iloc[-1]['datetime'].strftime("%d.%m.%Y %H:%M")
    print(f'Temperature predicted for {from_datetime_str} - {to_datetime_str}')


if __name__== '__main__':
    predict()