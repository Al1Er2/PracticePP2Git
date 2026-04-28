import psycopg2
from config import load_config

def connect():
    """ Connect to the PostgreSQL database server """
    config = load_config()
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**config)
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
        # close the communication with the PostgreSQL
        cur.close()
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection Error: {error}")
        return None

if __name__ == '__main__':
    connection = connect()
    if connection:
        connection.close()
        print('Database connection closed.')