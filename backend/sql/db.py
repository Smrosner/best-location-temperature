import psycopg2
from psycopg2.extras import execute_batch
import logging

logging.basicConfig(level=logging.ERROR, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="flaskproject",
        user="shayrosner",
        password="password"
    )
def create_temperature_table():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
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
    except Exception as e:
        logging.error("Error creating temperature_data table: %s", e)

def fetch_temperature_data_by_date_range(start_year, start_month, start_day, end_year, end_month, end_day):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM temperature_data
                WHERE (year > %s OR (year = %s AND month > %s) OR (year = %s AND month = %s AND day >= %s))
                AND (year < %s OR (year = %s AND month < %s) OR (year = %s AND month = %s AND day <= %s))
                ORDER BY year, month, day;
                """
                cursor.execute(query, (start_year, start_year, start_month, start_year, start_month, start_day,
                                       end_year, end_year, end_month, end_year, end_month, end_day))
                return cursor.fetchall() or "No temperature data was found"
    except Exception as e:
        logging.error("Error fetching temperature data by date range: %s", e)
        return None

def fetch_temperature_data_by_id(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM temperature_data WHERE id = %s;
                """
                cursor.execute(query, (id,))
                temperature_data = cursor.fetchone()
                return temperature_data or "Temperature data not found"
    except Exception as e:
        logging.error("Error fetching temperature data by ID: %s", e)
        return None

def update_temperature_data_by_id(temp_id, data):
    """
    Update temperature data for a given ID.

    :param temp_id: The ID of the temperature record to update.
    :param data: A dictionary containing the fields to update.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                UPDATE temperature_data
                SET region = %s, country = %s, state = %s, city = %s, month = %s, day = %s, year = %s, avg_temperature = %s
                WHERE id = %s
                """
                updated_temperature_values = (
                    data['region'],
                    data['country'],
                    data['state'],
                    data['city'],
                    data['month'],
                    data['day'],
                    data['year'],
                    data['avg_temperature'],
                    temp_id,
                )
                cur.execute(query, updated_temperature_values)
    except Exception as e:
        logging.error("Error updating temperature data by ID: %s", e)

def delete_temperature_data_by_id(temp_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                DELETE FROM temperature_data WHERE id = %s;
                """
                cursor.execute(query, (temp_id,))
                return cursor.rowcount > 0
    except Exception as e:
        logging.error("Error deleting temperature data by ID: %s", e)
        return False

def insert_temperature_data(data):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO temperature_data (region, country, state, city, month, day, year, avg_temperature)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_batch(cursor, query, data)
    except Exception as e:
        logging.error("Error inserting temperature data: %s", e)
        return False

def fetch_distinct_cities():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = 'SELECT DISTINCT city, country FROM temperature_data ORDER BY city;'
                cursor.execute(query)
                cities = cursor.fetchall()
                return cities or "No cities found"
    except Exception as e:
        logging.error("Error fetching distinct cities: %s", e)
        return None
