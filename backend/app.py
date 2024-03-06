import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from etl import etl
from routes.temperature import register_temperature_routes
from routes.cities import register_city_routes

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

register_temperature_routes(app)
register_city_routes(app)

app.add_url_rule('/etl', view_func=etl, methods=['POST'])

if __name__ == '__main__':
    logging.info("Starting Flask application on port 5001")
    app.run(debug=True, port=5001)

