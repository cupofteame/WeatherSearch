# Weather App

This is a Flask-based weather application that allows users to check the current weather conditions and a 5-day forecast for a specified location.

## Features

- Search for weather information by location name
- Displays current temperature in both Celsius and Fahrenheit
- Shows current weather condition with an icon
- Provides humidity and wind speed information
- Uses geocoding to find locations
- Displays a 5-day weather forecast

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Sign up for a free API key at [OpenWeatherMap.com](https://openweathermap.org/api).
2. Create a `.env` file in the root directory of the project.
3. Add your API key to the `.env` file:
   ```
   API_KEY=your_api_key_here
   ```
4. Make sure to add `.env` to your `.gitignore` file to prevent accidentally committing your API key.

## Usage

1. Start the Flask development server:
   ```
   python Weather.py
   ```
2. Open a web browser and go to `http://localhost:5000`.
3. Enter a location name in the search box and click "Search" to get the current weather information and forecast.

## Project Structure

- `Weather.py`: Main Flask application file
- `templates/index.html`: HTML template for the weather app
- `static/styles.css`: CSS styles for the app
- `requirements.txt`: List of Python dependencies
- `.env`: Environment file for storing the API key

## Dependencies

- Flask: Web framework
- requests: HTTP library for API requests
- python-dotenv: Loading environment variables
- geopy: Geocoding library

## Troubleshooting

If you encounter any issues or errors, please check the following:

1. Ensure you have a valid API key from OpenWeatherMap and it's correctly set in the `.env` file.
2. Check your internet connection.
3. Verify that all dependencies are installed correctly.
4. Make sure the `.env` file is in the root directory of your project.

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.