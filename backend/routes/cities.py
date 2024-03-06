from flask import jsonify
from sql.db import fetch_distinct_cities
import logging

def register_city_routes(app):

    @app.route('/cities')
    def list_cities():
        try:
          cities = fetch_distinct_cities()
          if cities is None:
              logging.error("Failed to fetch cities from the database")
              raise Exception("Failed to fetch cities from the database.")
          city_list = [{"city": city[0], "country": city[1]} for city in cities]
          return jsonify(city_list)
        except Exception as e:
            logging.exception("Error occurred while listing cities")
            return jsonify({"error": str(e)}), 500