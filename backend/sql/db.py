import psycopg2
from psycopg2.extras import execute_batch

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

def fetch_temperature_data_by_date_range(start_year, start_month, start_day, end_year, end_month, end_day):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT * FROM temperature_data
        WHERE (year > %s OR (year = %s AND month > %s) OR (year = %s AND month = %s AND day >= %s))
        AND (year < %s OR (year = %s AND month < %s) OR (year = %s AND month = %s AND day <= %s))
        ORDER BY year, month, day;
        """
        cursor.execute(query, (start_year, start_year, start_month, start_year, start_month, start_day,
                               end_year, end_year, end_month, end_year, end_month, end_day))
        temperature_data = cursor.fetchall()
        return temperature_data
    except Exception as e:
        print(str(e))
        return None
    finally:
        cursor.close()
        conn.close()

def fetch_temperature_data_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT * FROM temperature_data WHERE id = %s;
        """
        cursor.execute(query, (id,))
        temperature_data = cursor.fetchone()
        return temperature_data
    except Exception as e:
        print(str(e))
        return None
    finally:
        cursor.close()
        conn.close()

def update_temperature_data_by_id(temp_id, data):
    """
    Update temperature data for a given ID.

    :param temp_id: The ID of the temperature record to update.
    :param data: A dictionary containing the fields to update.
    """
    query = """
    UPDATE temperature_data
    SET region = %s, country = %s, city = %s, month = %s, day = %s, year = %s, avg_temperature = %s
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
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query, updated_temperature_values)
        conn.commit()
    conn.close()

def delete_temperature_data_by_id(temp_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM your_table_name WHERE id = %s", (temp_id,))
        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return False
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if not conn.closed:
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