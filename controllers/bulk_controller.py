import os
import pandas as pd
import requests
import random
import sqlite3
from flask import Blueprint, request, jsonify, render_template
from models.weather_model import db, WeatherData

bulk_bp = Blueprint("bulk", __name__)

CSV_URL = "https://corgis-edu.github.io/corgis/datasets/csv/weather/weather.csv"

@bulk_bp.route('/fetch_bulk', methods=['GET'])
def fetch_bulk_data():
    """Fetch and insert 1M weather records"""
    try:
        csv_path = "weather_data.csv"
        response = requests.get(CSV_URL)

        if response.status_code != 200:
            return jsonify({"error": "Failed to download weather CSV"}), response.status_code

        with open(csv_path, "wb") as file:
            file.write(response.content)

        df = pd.read_csv(csv_path)
        db.session.query(WeatherData).delete()
        db.session.commit()

        records_to_insert = []
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Foggy", "Snowy", "Thunderstorm", None, "", "UNKNOWN"]

        total_records = 1000000
        records_processed = 0
        for i in range(total_records):
            row = df.sample(n=1).iloc[0]
            random_weather = random.choice(weather_conditions)

            weather_entry = WeatherData(
                city=row["Station.City"] if random.random() > 0.05 else "",
                date=row["Date.Full"],
                temperature=row["Data.Temperature.Avg Temp"] if random.random() > 0.02 else None,
                weather=random_weather
            )
            records_to_insert.append(weather_entry)

            if len(records_to_insert) % 10000 == 0:
                db.session.bulk_save_objects(records_to_insert)
                db.session.commit()
                records_to_insert = []
                records_processed += 10000
                print(f"Processed {records_processed}/{total_records} records...")

        if records_to_insert:
            db.session.bulk_save_objects(records_to_insert)
            db.session.commit()
            records_processed += len(records_to_insert)

        return jsonify({"message": f"{records_processed} records inserted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bulk_bp.route('/clean_data', methods=['GET'])
def fetch_cleaned_data():
    """Fetch cleaned aggregated weather data for dashboard"""
    try:
        conn = sqlite3.connect("weather_data.db")
        df = pd.read_sql_query("SELECT city, avg_temperature, weather FROM clean_weather_data", conn)
        conn.close()

        city_avg_temp = df.groupby("city")["avg_temperature"].mean().to_dict()
        weather_counts = df["weather"].value_counts().to_dict()

        return jsonify({
            "cities": list(city_avg_temp.keys()),
            "avg_temperatures": list(city_avg_temp.values()),
            "weather_conditions": list(weather_counts.keys()),
            "weather_counts": list(weather_counts.values())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bulk_bp.route('/view_weather_data', methods=['GET'])
def view_weather_data():
    """View paginated weather data"""
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        paginated_data = WeatherData.query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('index.html', data=paginated_data)
    except Exception as e:
        return f"Error: {str(e)}", 500

@bulk_bp.route('/cities', methods=['GET'])
def get_cities():
    """Fetch all cities in DB for the dropdown search"""
    cities = db.session.query(WeatherData.city).distinct().all()
    cities = [city[0] for city in cities]
    return jsonify(cities)

@bulk_bp.route('/temperature', methods=['GET'])
def fetch_temperature():
    """Fetch temperature for a specific city and date"""
    try:
        city = request.args.get('city')
        date = request.args.get('date')

        # Query the database to get the temperature for the specific city and date
        weather_entry = WeatherData.query.filter_by(city=city, date=date).first()

        if not weather_entry:
            return jsonify({"error": "No data found for the selected city and date."}), 404

        return jsonify({
            "city": city,
            "date": date,
            "avg_temperature": weather_entry.temperature
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

