
def create_db_table(connection):

    #Check weather_predictions table exist
    cursor = connection.cursor() 
    cursor.execute("select exists(select * from information_schema.tables where table_name='weather_predictions')")
    exists = cursor.fetchone()[0]
    
    if exists == False:
        print('weather_predictions table not exist.')
        
        cursor.execute('''
        CREATE TABLE weather_predictions (
        datetime timestamp PRIMARY KEY,
        temperature decimal
        );
        ''')

        print("weather_predictions table created.")
        
        connection.commit()
        cursor.close()

