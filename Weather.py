from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from fuzzywuzzy import process

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')  # Get API key from environment variable
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'

# Predefined list of known locations for fuzzy matching
KNOWN_LOCATIONS = ["New York, USA", "Los Angeles, USA", "London, UK", "Paris, France", "Berlin, Germany"]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            try:
                # Geocode the location to get latitude and longitude
                geocode_response = requests.get(f"{GEOCODE_URL}?q={location}&limit=1&appid={API_KEY}")
                geocode_response.raise_for_status()
                geocode_data = geocode_response.json()

                if not geocode_data:
                    # If location not found, find the closest match
                    best_match = process.extractOne(location, KNOWN_LOCATIONS)
                    if best_match:
                        location = best_match[0]
                        geocode_response = requests.get(f"{GEOCODE_URL}?q={location}&limit=1&appid={API_KEY}")
                        geocode_response.raise_for_status()
                        geocode_data = geocode_response.json()

                if not geocode_data:
                    error = "Location not found."
                else:
                    lat = geocode_data[0]['lat']
                    lon = geocode_data[0]['lon']

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