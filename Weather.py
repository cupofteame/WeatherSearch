from flask import Flask, render_template, request, jsonify
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

def get_weather_data(lat, lon):
    try:
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
        
        response_forecast = requests.get(f"{FORECAST_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
        response_forecast.raise_for_status()
        forecast_data = response_forecast.json()['list']
        
        today = datetime.now().date()
        forecast_data = [
            forecast for forecast in forecast_data
            if datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date() != today
        ]
        
        unique_days = list({datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date().isoformat() for forecast in forecast_data})
        
        return weather_data, forecast_data, unique_days
    except requests.RequestException as e:
        print(f"Weather API error: {e}")
        return None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    unique_days = []
    error = None
    if request.method == 'POST':
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        location = request.form.get('location')
        if lat and lon:
            # User provided geolocation
            weather_data, forecast_data, unique_days = get_weather_data(lat, lon)
        elif location:
            # User provided a location string
            lat, lon = geocode_location(location)
            if lat is not None and lon is not None:
                weather_data, forecast_data, unique_days = get_weather_data(lat, lon)
            else:
                error = "Location not found."
        
        if weather_data is None:
            error = "An error occurred while fetching weather data."
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # This is an AJAX request
            return jsonify({
                'weather_data': weather_data,
                'forecast_data': forecast_data,
                'unique_days': unique_days,
                'error': error
            })
    
    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, unique_days=unique_days, error=error)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)