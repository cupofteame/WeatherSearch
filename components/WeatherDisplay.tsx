import React from 'react'
import styles from '../styles/Home.module.css'

interface WeatherData {
  city: string
  country: string
  temp_celsius: number
  temp_fahrenheit: number
  description: string
  icon: string
  humidity: number
  wind_speed: number
}

interface ForecastData {
  dt_txt: string
  main: {
    temp: number
  }
  weather: Array<{
    description: string
    icon: string
  }>
}

interface Props {
  weatherData: {
    weather: WeatherData
    forecast: ForecastData[]
  }
}

const getWeatherIcon = (iconCode: string) => {
  const iconMap: { [key: string]: string } = {
    '01d': 'wi-day-sunny',
    '01n': 'wi-night-clear',
    '02d': 'wi-day-cloudy',
    '02n': 'wi-night-alt-cloudy',
    '03d': 'wi-cloud',
    '03n': 'wi-cloud',
    '04d': 'wi-cloudy',
    '04n': 'wi-cloudy',
    '09d': 'wi-showers',
    '09n': 'wi-showers',
    '10d': 'wi-day-rain',
    '10n': 'wi-night-alt-rain',
    '11d': 'wi-thunderstorm',
    '11n': 'wi-thunderstorm',
    '13d': 'wi-snow',
    '13n': 'wi-snow',
    '50d': 'wi-fog',
    '50n': 'wi-fog'
  }
  return iconMap[iconCode] || 'wi-na'
}

const WeatherDisplay: React.FC<Props> = ({ weatherData }) => {
  const { weather, forecast } = weatherData

  return (
    <div className={styles.weatherContainer}>
      <div className={styles.currentWeather}>
        <h2 className={styles.location}>
          <i className="fas fa-map-marker-alt"></i> {weather.city}, {weather.country}
        </h2>
        <div className={styles.weatherMain}>
          <i className={`wi ${getWeatherIcon(weather.icon)} ${styles.weatherIcon}`}></i>
          <div className={styles.temperature}>
            <span className={styles.tempValue}>
              {Math.round(weather.temp_celsius)}°C / {Math.round(weather.temp_fahrenheit)}°F
            </span>
          </div>
        </div>
        <p className={styles.description}>{weather.description}</p>
        <div className={styles.weatherDetails}>
          <div className={`${styles.detailItem} ${styles.humidityItem}`}>
            <i className="wi wi-humidity"></i> {weather.humidity}%
          </div>
          <div className={`${styles.detailItem} ${styles.windItem}`}>
            <i className="wi wi-strong-wind"></i> {weather.wind_speed} m/s
          </div>
        </div>
      </div>

      <div className={styles.forecast}>
        <h3 className={styles.forecastTitle}>
          <i className="wi wi-time-1"></i> 5-Day Forecast
        </h3>
        <div className={styles.forecastItems}>
          {forecast.map((day, index) => (
            <div key={index} className={styles.forecastItem}>
              <p className={styles.forecastDate}>{new Date(day.dt_txt).toLocaleDateString('en-US', { weekday: 'short' })}</p>
              <i className={`wi ${getWeatherIcon(day.weather[0].icon)} ${styles.forecastIcon}`}></i>
              <p className={styles.forecastTemp}>
                {Math.round(day.main.temp)}°C / {Math.round((day.main.temp * 9/5) + 32)}°F
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default WeatherDisplay