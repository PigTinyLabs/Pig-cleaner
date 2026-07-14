import React, { useEffect, useState, useMemo } from 'react'

// Số lượng hạt tối đa — giữ thấp để không lag
const MAX_RAIN = 40
const MAX_SNOW = 25
const MAX_WIND_STREAKS = 8

function randomBetween(a, b) {
  return a + Math.random() * (b - a)
}

// ─── Mưa ────────────────────────────────────────────────────────────────────
function RainLayer({ windForceX, intensity = 1 }) {
  const drops = useMemo(() => {
    return Array.from({ length: Math.round(MAX_RAIN * intensity) }, (_, i) => ({
      id: i,
      left: randomBetween(0, 100),    // %
      delay: randomBetween(0, 1.5),   // s
      duration: randomBetween(0.6, 1.2), // s
      height: randomBetween(15, 30),  // px
      opacity: randomBetween(0.5, 0.9),
    }))
  }, [intensity])

  // Gió lệch hạt mưa: windForceX ∈ [-1, 1] → skew ±30deg
  const skewDeg = windForceX * 30

  return (
    <div style={{
      position: 'fixed', inset: 0,
      pointerEvents: 'none', zIndex: 50,
      overflow: 'hidden',
    }}>
      {drops.map(d => (
        <div key={d.id} style={{
          position: 'absolute',
          left: `${d.left}%`,
          top: '-40px',
          width: '2px',
          height: `${d.height}px`,
          background: 'linear-gradient(transparent, rgba(180, 210, 255, 0.8))',
          borderRadius: '1px',
          transform: `skewX(${skewDeg}deg)`,
          opacity: d.opacity,
          animation: `rain-fall ${d.duration}s ${d.delay}s linear infinite`,
        }} />
      ))}
    </div>
  )
}

// ─── Tuyết ───────────────────────────────────────────────────────────────────
function SnowLayer({ windForceX }) {
  const flakes = useMemo(() => {
    return Array.from({ length: MAX_SNOW }, (_, i) => ({
      id: i,
      left: randomBetween(0, 100),
      delay: randomBetween(0, 4),
      duration: randomBetween(3, 6),
      size: randomBetween(4, 10),
      opacity: randomBetween(0.6, 1),
    }))
  }, [])

  const drift = windForceX * 50 // px ngang thêm khi rơi

  return (
    <div style={{
      position: 'fixed', inset: 0,
      pointerEvents: 'none', zIndex: 50,
      overflow: 'hidden',
    }}>
      {flakes.map(f => (
        <div key={f.id} style={{
          position: 'absolute',
          left: `${f.left}%`,
          top: '-20px',
          width: `${f.size}px`,
          height: `${f.size}px`,
          borderRadius: '50%',
          background: 'rgba(220, 235, 255, 0.95)',
          boxShadow: '0 0 4px rgba(180,210,255,0.8)',
          opacity: f.opacity,
          animation: `snow-fall ${f.duration}s ${f.delay}s ease-in infinite`,
          '--drift': `${drift}px`,
        }} />
      ))}
    </div>
  )
}

// ─── Gió mạnh (dải gió ngang) ────────────────────────────────────────────────
function WindStreaks({ windForceX, windSpeed }) {
  const streaks = useMemo(() => {
    return Array.from({ length: MAX_WIND_STREAKS }, (_, i) => ({
      id: i,
      top: randomBetween(10, 85),     // % vh
      delay: randomBetween(0, 1),
      duration: randomBetween(0.4, 0.9),
      width: randomBetween(60, 180),  // px
      opacity: randomBetween(0.3, 0.65),
    }))
  }, [])

  // Gió thổi trái → dải bay sang phải, ngược lại → từ phải sang trái
  const dir = windForceX >= 0 ? 1 : -1

  return (
    <div style={{
      position: 'fixed', inset: 0,
      pointerEvents: 'none', zIndex: 50,
      overflow: 'hidden',
    }}>
      {streaks.map(s => (
        <div key={s.id} style={{
          position: 'absolute',
          top: `${s.top}vh`,
          left: dir > 0 ? '-200px' : 'auto',
          right: dir < 0 ? '-200px' : 'auto',
          width: `${s.width}px`,
          height: '2px',
          background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent)',
          opacity: s.opacity,
          borderRadius: '1px',
          animation: `wind-streak-${dir > 0 ? 'right' : 'left'} ${s.duration}s ${s.delay}s linear infinite`,
        }} />
      ))}
    </div>
  )
}

// ─── Chớp sét ────────────────────────────────────────────────────────────────
function LightningFlash() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    function flash() {
      setVisible(true)
      setTimeout(() => setVisible(false), 120)
      // Flash lại ngẫu nhiên sau 4-15 giây
      setTimeout(flash, randomBetween(4000, 15000))
    }
    const t = setTimeout(flash, randomBetween(1000, 5000))
    return () => clearTimeout(t)
  }, [])

  if (!visible) return null
  return (
    <div style={{
      position: 'fixed', inset: 0,
      background: 'rgba(200, 220, 255, 0.3)',
      pointerEvents: 'none', zIndex: 55,
      animation: 'lightning-flash 0.12s ease-out',
    }} />
  )
}

// ─── WeatherEffects (main export) ────────────────────────────────────────────
export default function WeatherEffects({ weather }) {
  if (!weather) return null

  const { condition, windForceX, windSpeed, isStorm } = weather
  const showRain = condition === 'rain' || condition === 'drizzle' || condition === 'thunderstorm'
  const showSnow = condition === 'snow'
  const showWind = windSpeed > 25
  const showLightning = condition === 'thunderstorm'
  const rainIntensity = condition === 'drizzle' ? 0.4 : condition === 'thunderstorm' ? 1.5 : 1.0

  if (!showRain && !showSnow && !showWind && !showLightning) return null

  return (
    <>
      {showRain && <RainLayer windForceX={windForceX} intensity={Math.min(rainIntensity, 1)} />}
      {showSnow && <SnowLayer windForceX={windForceX} />}
      {showWind && <WindStreaks windForceX={windForceX} windSpeed={windSpeed} />}
      {showLightning && <LightningFlash />}
    </>
  )
}
