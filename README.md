# Weather App

This is a simple Flask-based weather application that allows users to check the current weather conditions for a specified city.

## Features

- Search for weather information by city name
- Displays temperature in Celsius and Fahrenheit
- Shows current weather condition with an icon
- Provides humidity and wind speed information

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

1. Sign up for a free API key at [WeatherAPI.com](https://www.weatherapi.com/).
2. Create a `.env` file in the root directory of the project.
3. Add your API key to the `.env` file:

   ```
   API_KEY_=your_api_key_here
   ```

4. Make sure to add `.env` to your `.gitignore` file to prevent accidentally committing your API key.

## Usage

1. Start the Flask development server:

   ```
   python Weather.py
   ```

2. Open a web browser and go to `http://localhost:5000`.
3. Enter a city name in the search box and click "Search" to get the current weather information.

## Project Structure

- `Weather.py`: Main Flask application file
- `templates/index.html`: HTML template for the weather app
- `static/styles.css`: CSS styles for the app
- `requirements.txt`: List of Python dependencies
- `.env`: Environment file for storing the API key

## Customization

You can customize the appearance of the app by modifying the `static/styles.css` file.

## Troubleshooting

If you encounter any issues or errors, please check the following:

1. Ensure you have a valid API key from WeatherAPI.com and it's correctly set in the `.env` file.
2. Check your internet connection.
3. Verify that all dependencies are installed correctly.
4. Make sure the `.env` file is in the root directory of your project.

## License

This project is open-source and available under the MIT License.