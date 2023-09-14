import psycopg2.extras as extras
import pickle

def update_db_table(connection, data):
    with connection.cursor() as cursor:
        
        #Check weather table exist
        cursor.execute('''  SELECT datetime
                            FROM weather 
                            ORDER BY datetime DESC
                            LIMIT 1; 
                    ''')
        last_datetime_DB = cursor.fetchone()[0]
        data = data[data['datetime'] > last_datetime_DB]
        if data.shape[0] > 0:
            tuples = [tuple(x) for x in data.to_numpy()]
            cols = ','.join(list(data.columns))
            query = "INSERT INTO %s(%s) VALUES %%s" % ('weather', cols)
            extras.execute_values(cursor, query, tuples)
            connection.commit()
            
            print('| Found {} new rows, added them to weather datatable.'.format(data.shape[0]))
            new_rows_found = True
        else:
            print('| Found 0 new rows.')
            new_rows_found = False
        
        with open('/tmp/script.out', 'wb+') as tmp_file:
            pickle.dump({'new_rows_found': new_rows_found}, tmp_file)
    pass