# Weather App

This is a Next.js-based weather application that allows users to check current weather conditions and a 5-day forecast for a specified location.

## Features

- Current weather display
- 5-day weather forecast
- Geolocation support
- Search functionality for any location
- Responsive design
- Dark theme

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Node.js (v14 or later)
- npm (v6 or later)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/cupofteame/WeatherSearch.git
   ```

2. Navigate to the project directory:
   ```
   cd weathersearch
   ```

3. Install the dependencies:
   ```
   npm install
   ```

## Configuration

1. Create a `.env.local` file in the root directory of the project.
2. Add your OpenWeatherMap API key to the file:
   ```
   API_KEY=your_api_key_here
   ```

## Running the App

To run the app in development mode:

```
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to view the app.

## Building for Production

To create a production build:

```
npm run build
```

To start the production server:

```
npm start
```

## How It Works

### Pages

- `pages/index.tsx`: The main page of the application. It handles the state for weather data, errors, and loading status. It also includes the geolocation functionality and the main layout of the app.

### Components

- `components/SearchForm.tsx`: Renders the search input field and handles user input for location searches.
- `components/WeatherDisplay.tsx`: Displays the current weather and 5-day forecast based on the data received from the API.

### API

- `pages/api/weather.ts` (not provided in the given files, but assumed to exist): Handles API requests to OpenWeatherMap and returns weather data for the frontend.

### Styles

- `styles/globals.css`: Contains global styles and CSS variables for theming.
- `styles/Home.module.css`: Contains component-specific styles using CSS modules.

### Functionality

1. When the app loads, it attempts to get the user's current location using the browser's geolocation API.
2. If successful, it fetches weather data for the user's location.
3. Users can also search for weather in any location using the search form.
4. The app displays current weather conditions including temperature, description, humidity, and wind speed.
5. A 5-day forecast is shown below the current weather, displaying the expected temperature and weather icon for each day.

## Contributing

Contributions to the Weather App are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).