import pandas as pd

def download_raw_data(connection):

        cursor = connection.cursor()    
        cursor.execute(f'''  SELECT *
                        FROM weather
                        where EXTRACT(HOUR FROM datetime) % 3 = 0
                        ORDER BY datetime DESC 
                        LIMIT 57;
                ''')    
        rows = cursor.fetchall()

        # Create Pandas Dataframe
        column_names = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(rows, columns=column_names)
        cursor.close()

        return data