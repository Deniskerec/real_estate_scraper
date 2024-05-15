import psycopg2
from psycopg2 import sql


def get_db_connection():
    conn = psycopg2.connect(
        dbname='real_estate',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    return conn


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties_test_1 (
        id SERIAL PRIMARY KEY,
        site TEXT,
        title TEXT,
        price TEXT,
        location TEXT,
        url TEXT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    try:
        create_table()
        print('Table created successfully')
    except Exception as e:
        print(e)


