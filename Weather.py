from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'your_api_key_here'  # Replace with your actual API key
API_URL = 'http://api.weatherapi.com/v1/current.json'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                response = requests.get(f"{API_URL}?key={API_KEY}&q={city}")
                response.raise_for_status()
                weather_data = response.json()
            except requests.RequestException as e:
                error = f"An error occurred: {str(e)}"

    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)