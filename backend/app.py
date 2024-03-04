from flask import Flask, jsonify
from flask_cors import CORS
from etl import etl
from sql.db import fetch_distinct_cities

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/')
def hello():
    return "Hello, World!"

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
