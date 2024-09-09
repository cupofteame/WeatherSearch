import type { NextApiRequest, NextApiResponse } from 'next'
import axios from 'axios'

const API_KEY = process.env.API_KEY
const CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
const FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'
const GEOCODING_URL = 'http://api.openweathermap.org/geo/1.0/direct'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { location, lat, lon } = req.query

  try {
    let latitude: number, longitude: number

    if (lat && lon) {
      latitude = parseFloat(lat as string)
      longitude = parseFloat(lon as string)
    } else if (location) {
      // Geocoding
      const geoRes = await axios.get(`${GEOCODING_URL}?q=${location}&limit=1&appid=${API_KEY}`)
      if (geoRes.data.length === 0) {
        return res.status(404).json({ error: 'Location not found.' })
      }
      latitude = geoRes.data[0].lat
      longitude = geoRes.data[0].lon
    } else {
      return res.status(400).json({ error: 'Invalid request. Provide either location or coordinates.' })
    }

    // Weather and forecast data
    const [weatherRes, forecastRes] = await Promise.all([
      axios.get(`${CURRENT_WEATHER_URL}?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric`),
      axios.get(`${FORECAST_URL}?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric`)
    ])

    const weatherData = {
      city: weatherRes.data.name,
      country: weatherRes.data.sys.country,
      temp_celsius: weatherRes.data.main.temp,
      temp_fahrenheit: (weatherRes.data.main.temp * 9/5) + 32,
      description: weatherRes.data.weather[0].description,
      icon: weatherRes.data.weather[0].icon,
      humidity: weatherRes.data.main.humidity,
      wind_speed: weatherRes.data.wind.speed
    }

    const forecastData = forecastRes.data.list.filter((item: any, index: number) => index % 8 === 0)

    res.status(200).json({ weather: weatherData, forecast: forecastData })
  } catch (error) {
    console.error('Error fetching weather data:', error)
    res.status(500).json({ error: 'Error fetching weather data' })
  }
}