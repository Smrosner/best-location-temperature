import csv
from sql.db import create_temperature_table, insert_temperature_data

def etl():
    csv_file_path = 'data/city_temperature.csv'

    create_temperature_table()

    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append((row['Region'], row['Country'], row['State'], row['City'], row['Month'], row['Day'], row['Year'], row['AvgTemperature']))

            insert_temperature_data(data)
            print("Data inserted successfully")
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    etl()
