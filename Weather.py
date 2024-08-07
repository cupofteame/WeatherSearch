from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from fuzzywuzzy import process
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')  # Get API key from environment variable
API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Predefined list of known locations for fuzzy matching
KNOWN_LOCATIONS = ["New York, USA", "Los Angeles, USA", "London, UK", "Paris, France", "Berlin, Germany"]

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
    error = None

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            try:
                lat, lon = geocode_location(location)

                if lat is None or lon is None:
                    # If location not found, find the closest match
                    best_match = process.extractOne(location, KNOWN_LOCATIONS)
                    if best_match:
                        location = best_match[0]
                        lat, lon = geocode_location(location)

                if lat is None or lon is None:
                    error = "Location not found."
                else:
                    # Fetch weather data using latitude and longitude
                    response_metric = requests.get(f"{API_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
                    response_metric.raise_for_status()
                    weather_data_metric = response_metric.json()

                    response_imperial = requests.get(f"{API_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial")
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
            except requests.RequestException as e:
                error = f"An error occurred: {str(e)}"

    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)