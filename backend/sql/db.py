import psycopg2
from psycopg2.extras import execute_batch

# Define a function to get database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="flaskproject",
        user="shayrosner",
        password="password"
    )
def create_temperature_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS temperature_data (
            id SERIAL PRIMARY KEY,
            region VARCHAR(255),
            country VARCHAR(255),
            state VARCHAR(255),
            city VARCHAR(255),
            month INT,
            day INT,
            year INT,
            avg_temperature FLOAT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
    except Exception as e:
        print(str(e))
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_temperature_data(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO temperature_data (region, country, state, city, month, day, year, avg_temperature)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_batch(cursor, query, data)
        conn.commit()
    except Exception as e:
        print(str(e))
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def fetch_distinct_cities():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = 'SELECT DISTINCT city, country FROM temperature_data ORDER BY city;'
        cursor.execute(query)
        cities = cursor.fetchall()
        return cities
    except Exception as e:
        print(str(e))
        return None
    finally:
        cursor.close()
        conn.close()