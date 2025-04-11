from flask import Blueprint, request, jsonify, render_template
import requests

weather_bp = Blueprint('weather', __name__)

API_KEY = "eeab40ff68eb0bfb53e7f1c38ac3efe0"

@weather_bp.route('/')
def index():
    return render_template('index.html')

@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Failed to fetch weather data")}), response.status_code

        return jsonify({
            "location": data.get("name", "Unknown"),
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
