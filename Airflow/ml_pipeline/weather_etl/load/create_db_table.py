import psycopg2.extras as extras
import pickle


def create_db_table(connection, data):
    with connection.cursor() as cursor:
        
        #Check weather table exist
        cursor.execute("select exists(select * from information_schema.tables where table_name='weather')")
        exists = cursor.fetchone()[0]
        
        if exists:
            print('| weather table exist.')
            return False
        else:
            print('| weather table not exist.')
            
            cursor.execute('''
            CREATE TABLE weather (
            datetime timestamp PRIMARY KEY,
            temperature decimal
            );
            ''')
            connection.commit()
            print("| weather table created.")
            
            #Fill data
            tuples = [tuple(x) for x in data.to_numpy()]
            cols = ','.join(list(data.columns))
            query = "INSERT INTO %s(%s) VALUES %%s" % ('weather', cols)
            extras.execute_values(cursor, query, tuples)
            connection.commit()
            print('| current data filled.')

            with open('/tmp/script.out', 'wb+') as tmp_file:
                pickle.dump({'new_rows_found': True}, tmp_file)

            return True
    pass