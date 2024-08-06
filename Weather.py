from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')  # Get API key from environment variable
API_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                response_metric = requests.get(f"{API_URL}?q={city}&appid={API_KEY}&units=metric")
                response_metric.raise_for_status()
                weather_data_metric = response_metric.json()

                response_imperial = requests.get(f"{API_URL}?q={city}&appid={API_KEY}&units=imperial")
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
