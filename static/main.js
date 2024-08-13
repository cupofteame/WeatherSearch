document.addEventListener('DOMContentLoaded', function () {
    const loadingIndicator = document.getElementById('loading');
    const searchForm = document.querySelector('.search-form');
    const mainContent = document.querySelector('main');

    function updateWeatherDisplay(data) {
        // Clear existing content
        mainContent.innerHTML = '';

        if (data.error) {
            const errorSection = document.createElement('section');
            errorSection.className = 'error-section';
            errorSection.innerHTML = `
                <p class="error"><i class="fas fa-exclamation-circle"></i> ${data.error}</p>
            `;
            mainContent.appendChild(errorSection);
        } else if (data.weather_data) {
            const weatherSection = document.createElement('section');
            weatherSection.className = 'weather-section';
            weatherSection.innerHTML = `
                <div class="current-weather">
                    <h2>${data.weather_data.city}, ${data.weather_data.country}</h2>
                    <div class="weather-icon">
                        <img src="http://openweathermap.org/img/wn/${data.weather_data.icon}@2x.png" alt="${data.weather_data.description}">
                    </div>
                    <div class="weather-details">
                        <p class="temperature">
                            <i class="fas fa-thermometer-half"></i>
                            ${data.weather_data.temp_celsius}&deg;C / ${data.weather_data.temp_fahrenheit}&deg;F
                        </p>
                        <p class="condition"><i class="fas fa-cloud"></i> ${data.weather_data.description}</p>
                        <p class="humidity"><i class="fas fa-tint"></i> Humidity: ${data.weather_data.humidity}%</p>
                        <p class="wind"><i class="fas fa-wind"></i> Wind: ${data.weather_data.wind_speed} m/s</p>
                    </div>
                </div>
            `;
            mainContent.appendChild(weatherSection);

            if (data.forecast_data && data.forecast_data.length > 0) {
                const forecastSection = document.createElement('section');
                forecastSection.className = 'forecast-section';
                forecastSection.innerHTML = `
                    <h2><i class="fas fa-calendar-alt"></i> 5-Day Forecast</h2>
                    <div class="forecast-scroll">
                        <div class="forecast-items" id="forecast"></div>
                    </div>
                `;
                mainContent.appendChild(forecastSection);

                const forecastContainer = document.getElementById('forecast');
                const filteredData = data.forecast_data.filter((forecast, index) => index % 8 === 0);
                filteredData.forEach((forecast) => {
                    const date = new Date(forecast.dt_txt);
                    const day = date.toLocaleDateString('en-US', { weekday: 'long' });
                    const forecastItem = document.createElement('div');
                    forecastItem.className = 'forecast-item';
                    forecastItem.innerHTML = `
                        <p class="forecast-day">${day}</p>
                        <div class="forecast-icon">
                            <img src="http://openweathermap.org/img/wn/${forecast.weather[0].icon}@2x.png" alt="${forecast.weather[0].description}">
                        </div>
                        <p class="forecast-temp">${forecast.main.temp}&deg;C / ${(forecast.main.temp * 9 / 5 + 32).toFixed(2)}&deg;F</p>
                        <p class="forecast-condition">${forecast.weather[0].description}</p>
                    `;
                    forecastContainer.appendChild(forecastItem);
                });
            }
        }
    }

    // Handle form submission
    searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const location = this.querySelector('input[name="location"]').value;
        loadingIndicator.style.display = 'block';

        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `location=${encodeURIComponent(location)}`
        }).then(response => response.json())
            .then(data => {
                loadingIndicator.style.display = 'none';
                updateWeatherDisplay(data);
            })
            .catch(error => {
                loadingIndicator.style.display = 'none';
                console.error("An error occurred while fetching weather data:", error);
                updateWeatherDisplay({ error: "An error occurred while fetching weather data." });
            });
    });

    // Geolocation handling
    if ("geolocation" in navigator) {
        loadingIndicator.style.display = 'block';
        navigator.geolocation.getCurrentPosition(function (position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `lat=${lat}&lon=${lon}`
            }).then(response => response.json())
                .then(data => {
                    loadingIndicator.style.display = 'none';
                    updateWeatherDisplay(data);
                })
                .catch(error => {
                    loadingIndicator.style.display = 'none';
                    console.error("An error occurred while fetching weather data:", error);
                    updateWeatherDisplay({ error: "An error occurred while fetching weather data." });
                });
        }, function (error) {
            loadingIndicator.style.display = 'none';
            console.error("Geolocation error:", error);
            updateWeatherDisplay({ error: "Unable to retrieve your location. Please use the search form." });
        });
    } else {
        updateWeatherDisplay({ error: "Geolocation is not supported by your browser. Please use the search form." });
    }
});