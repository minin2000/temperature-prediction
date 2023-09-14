import psycopg2.extras as extras

def insert_to_db_table(df, connection):

    cursor = connection.cursor() 
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT (datetime) DO UPDATE SET temperature=EXCLUDED.temperature" % ('weather_predictions', cols)
    extras.execute_values(cursor, query, tuples)
    connection.commit()
    cursor.close()