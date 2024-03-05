from flask import Flask, jsonify, request
from flask_cors import CORS
from etl import etl
from sql.db import fetch_temperature_data_by_date_range, fetch_temperature_data_by_id,insert_temperature_data, update_temperature_data_by_id, delete_temperature_data_by_id, fetch_distinct_cities
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/temperature/range')
def get_temperature_data_by_date_range():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not start_date or not end_date:
        return jsonify({"error": "Please provide both start and end dates"}), 400

    try:
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        temperature_data = fetch_temperature_data_by_date_range(start_year, start_month, start_day, end_year, end_month, end_day)
        if temperature_data is None or len(temperature_data) == 0:
            return jsonify({"error": "No temperature data found for the given date range"}), 404

        temperature_details = [
            {
                "id": data[0],
                "region": data[1],
                "country": data[2],
                "state": data[3],
                "city": data[4],
                "month": data[5],
                "day": data[6],
                "year": data[7],
                "avg_temperature": data[8]
            } for data in temperature_data
        ]
        return jsonify(temperature_details)
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/temperature/<int:temp_id>')
def get_temperature_data_by_id(temp_id):
    try:
        temperature_data = fetch_temperature_data_by_id(temp_id)
        if temperature_data is None:
            return jsonify({"error": "Temperature data not found"}), 404

        temperature_details = {
            "id": temperature_data[0],
            "region": temperature_data[1],
            "country": temperature_data[2],
            "state": temperature_data[3],
            "city": temperature_data[4],
            "month": temperature_data[5],
            "day": temperature_data[6],
            "year": temperature_data[7],
            "avg_temperature": temperature_data[8]
        }
        return jsonify(temperature_details)
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/temperatures', methods=['POST'])
def add_temperature_record():
    body = request.json
    required_fields = ["region", "country", "city", "month", "day", "year", "avg_temperature"]
    if not all(field in body for field in required_fields):
        return jsonify({"error": "Missing fields in payload"}), 400
    temperature_record = (
        body["region"],
        body["country"],
        body.get("state", ""),
        body["city"],
        body["month"],
        body["day"],
        body["year"],
        body["avg_temperature"]
    )

    try:
        insert_temperature_data([temperature_record])
        return jsonify({"message": "Record added successfully"}), 201
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/temperature/<int:temp_id>', methods=['PUT'])
def update_temperature_data(temp_id):
    body = request.json
    required_fields = ["region", "country", "city", "month", "day", "year", "avg_temperature"]

    if not all(field in body for field in required_fields):
        return jsonify({"error": "Missing fields in payload"}), 400

    update_payload = {
        "region": body["region"],
        "country": body["country"],
        "city": body["city"],
        "month": body["month"],
        "day": body["day"],
        "year": body["year"],
        "avg_temperature": body["avg_temperature"]
    }
    if "state" in body:
        update_payload["state"] = body["state"]

    try:
        update_temperature_data_by_id(temp_id, update_payload)
        return jsonify({"message": "Record updated successfully"}), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/temperature/<int:temp_id>', methods=['DELETE'])
def delete_temperature_data(temp_id):
    try:
        result = delete_temperature_data_by_id(temp_id)
        if result:
            return jsonify({"message": "Record deleted successfully"}), 200
        else:
            return jsonify({"error": "Temperature data not found or could not be deleted"}), 404
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cities')
def list_cities():
    try:
        cities = fetch_distinct_cities()
        if cities is None:
            raise Exception("Failed to fetch cities from the database.")
        city_list = [{"city": city[0], "country": city[1]} for city in cities]
        return jsonify(city_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.add_url_rule('/etl', view_func=etl, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
