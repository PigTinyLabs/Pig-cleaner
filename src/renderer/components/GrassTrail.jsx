import React, { useState, useEffect, useRef } from 'react'

const GRASS_TYPES = ['🌱', '🌿', '☘️', '🍀']
const SNOW_TYPES = ['❄️', '❄️', '❄️']

export default function GrassTrail({ x, y, isWalking, trailType = 'grass' }) {
  const [grasses, setGrasses] = useState([])
  const lastSpawnXRef = useRef(x)

  useEffect(() => {
    // Chỉ mọc cỏ/tuyết khi lợn đang đi bộ và ở dưới đất
    if (!isWalking || y < 0) return

    // Khoảng cách giữa các khóm
    const SPAWN_DISTANCE = 35

    if (Math.abs(x - lastSpawnXRef.current) > SPAWN_DISTANCE) {
      lastSpawnXRef.current = x
      
      const types = trailType === 'snow' ? SNOW_TYPES : GRASS_TYPES
      const newGrass = {
        id: Date.now() + Math.random(),
        x: x + 60, // Căn giữa khoảng x (chiều rộng lợn ~150px)
        type: types[Math.floor(Math.random() * types.length)],
        size: Math.random() > 0.5 ? '20px' : '24px',
        // Hơi lộn xộn một chút về y
        offsetY: Math.floor(Math.random() * 5),
      }

      setGrasses(prev => [...prev, newGrass])

      // Tự động xóa khỏi DOM sau 6 giây (phải đồng bộ với CSS animation duration)
      setTimeout(() => {
        setGrasses(prev => prev.filter(g => g.id !== newGrass.id))
      }, 6000)
    }
  }, [x, y, isWalking])

  return (
    <div 
      className="grass-trail"
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        width: '100%',
        pointerEvents: 'none',
        zIndex: 0 // Dưới heo
      }}
    >
      {grasses.map(grass => (
        <div 
          key={grass.id}
          style={{
            position: 'absolute',
            bottom: `${grass.offsetY}px`,
            left: `${grass.x}px`,
            fontSize: grass.size,
            animation: 'growAndFade 6s ease-in-out forwards',
            transformOrigin: 'bottom center',
            filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
          }}
        >
          {grass.type}
        </div>
      ))}
    </div>
  )
}
