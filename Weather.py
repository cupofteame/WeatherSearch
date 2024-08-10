from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')  # Get API key from environment variable
CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'

geolocator = Nominatim(user_agent="weather_app")

def geocode_location(location):
    try:
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            return location_data.latitude, location_data.longitude
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error = None
    unique_days = []

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            try:
                lat, lon = geocode_location(location)

                if lat is None or lon is None:
                    error = "Location not found."
                else:
                    # Fetch current weather data using latitude and longitude
                    response_metric = requests.get(f"{CURRENT_WEATHER_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
                    response_metric.raise_for_status()
                    weather_data_metric = response_metric.json()

                    response_imperial = requests.get(f"{CURRENT_WEATHER_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial")
                    response_imperial.raise_for_status()
                    weather_data_imperial = response_imperial.json()

                    weather_data = {
                        'city': weather_data_metric['name'],
                        'country': weather_data_metric['sys']['country'],
                        'temp_celsius': weather_data_metric['main']['temp'],
                        'temp_fahrenheit': weather_data_imperial['main']['temp'],
                        'description': weather_data_metric['weather'][0]['description'],
                        'icon': weather_data_metric['weather'][0]['icon'],
                        'humidity': weather_data_metric['main']['humidity'],
                        'wind_speed': weather_data_metric['wind']['speed']
                    }

                    # Fetch forecast data
                    response_forecast = requests.get(f"{FORECAST_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
                    response_forecast.raise_for_status()
                    forecast_data = response_forecast.json()['list']

                    # Filter out the current day's forecast and format the dates
                    today = datetime.now().date()
                    forecast_data = [
                        forecast for forecast in forecast_data
                        if datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date() != today
                    ]

                    # Extract unique days from forecast data
                    unique_days = list({datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date().isoformat() for forecast in forecast_data})

            except requests.RequestException as e:
                error = f"An error occurred: {str(e)}"

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, unique_days=unique_days, error=error)

if __name__ == '__main__':
    app.run(debug=True)