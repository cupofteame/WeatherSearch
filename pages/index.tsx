import { useState, useEffect } from 'react'
import styles from '../styles/Home.module.css'
import WeatherDisplay from '../components/WeatherDisplay'
import SearchForm from '../components/SearchForm'

export default function Home() {
  const [weatherData, setWeatherData] = useState(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Request user's location when the component mounts
    if ("geolocation" in navigator) {
      setLoading(true)
      navigator.geolocation.getCurrentPosition(
        position => {
          const { latitude, longitude } = position.coords
          fetchWeatherByCoords(latitude, longitude)
        },
        error => {
          console.error("Error getting location:", error)
          setError("Unable to get your location. Please search for a city manually.")
          setLoading(false)
        }
      )
    } else {
      setError("Geolocation is not supported by your browser. Please search for a city manually.")
    }
  }, [])

  const fetchWeatherByCoords = async (lat: number, lon: number) => {
    try {
      const response = await fetch(`/api/weather?lat=${lat}&lon=${lon}`)
      const data = await response.json()
      if (data.error) {
        setError(data.error)
      } else {
        setWeatherData(data)
      }
    } catch (err) {
      setError('An error occurred while fetching weather data.')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (location: string) => {
    setError(null)
    setLoading(true)
    try {
      const response = await fetch(`/api/weather?location=${encodeURIComponent(location)}`)
      const data = await response.json()
      if (data.error) {
        setError(data.error)
      } else {
        setWeatherData(data)
      }
    } catch (err) {
      setError('An error occurred while fetching weather data.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Weather App</h1>
        <SearchForm onSearch={handleSearch} />
        {loading && <p className={styles.loading}>Loading weather data...</p>}
        {error && <p className={styles.error}>{error}</p>}
        {weatherData && <WeatherDisplay weatherData={weatherData} />}
      </main>

      <footer className={styles.footer}>
        <p className={styles.disclaimer}>Disclaimer: This is an example site, please expect errors/bugs.</p>
        <div className={styles.githubIcon}>
          <a href="https://github.com/cupofteame/WeatherSearch" target="_blank" rel="noopener noreferrer">
            <i className="fab fa-github"></i>
          </a>
        </div>
      </footer>
    </div>
  )
}