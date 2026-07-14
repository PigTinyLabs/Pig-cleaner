import { useState, useEffect } from 'react'

const isElectron = typeof window !== 'undefined' && window.pigAPI

export function useWeather() {
  const [weather, setWeather] = useState({
    condition: 'clear',
    windSpeed: 0,
    windDirection: 0,
    windForceX: 0,
    isStorm: false,
    description: 'Đang tải thời tiết...',
  })

  useEffect(() => {
    // Lấy thời tiết lần đầu
    if (isElectron) {
      window.pigAPI.getWeather().then((data) => {
        if (data) setWeather(data)
      })

      // Lắng nghe cập nhật mỗi 30 phút
      const unsub = window.pigAPI.onWeatherUpdate((data) => {
        setWeather(data)
      })
      return () => unsub?.()
    }
  }, [])

  return weather
}
