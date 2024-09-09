import React, { useState } from 'react'
import styles from '../styles/Home.module.css'

interface Props {
  onSearch: (location: string) => void
}

const SearchForm: React.FC<Props> = ({ onSearch }) => {
  const [location, setLocation] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch(location)
  }

  return (
    <form className={styles.searchForm} onSubmit={handleSubmit}>
      <div className={styles.searchInputWrapper}>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter city or location"
          className={styles.searchInput}
          required
        />
        <button type="submit" className={styles.searchButton}>
          <i className="wi wi-day-cloudy"></i>
        </button>
      </div>
    </form>
  )
}

export default SearchForm