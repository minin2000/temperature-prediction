import pandas as pd    

def postprocess_data(df, predictions):

    predictions = predictions.reshape(-1)

    start_date = df.index[0]
    end_date = df.index[0] + pd.Timedelta('24 hours')

    # Create indexes for 24 hours with step of 3 hours
    new_index = pd.date_range(start=start_date, end=end_date, freq='3H')

    # Create final Dataframe
    final_df = pd.DataFrame(index=new_index, columns=['temperature'], dtype=float)

    final_df.iloc[0]['temperature'] = df.iloc[0]['temperature']
    final_df.loc[final_df['temperature'].isna(), 'temperature'] = predictions

    final_df['temperature'] = final_df['temperature'].round(1)
    final_df['datetime'] = final_df.index

    return final_df