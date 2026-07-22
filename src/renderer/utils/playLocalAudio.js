const MIME_MAP = {
  mp3: 'audio/mpeg',
  wav: 'audio/wav',
  ogg: 'audio/ogg',
  m4a: 'audio/mp4',
  aac: 'audio/aac',
  flac: 'audio/flac',
}

export async function playLocalAudio(filePath) {
  if (!filePath) return
  try {
    const ext = filePath.split('.').pop().toLowerCase()
    const mime = MIME_MAP[ext] || 'audio/mpeg'

    if (typeof window !== 'undefined' && window.pigAPI?.readSoundFile) {
      const base64 = await window.pigAPI.readSoundFile(filePath)
      if (!base64) return
      const audio = new Audio(`data:${mime};base64,${base64}`)
      await audio.play()
    } else {
      const audio = new Audio(filePath)
      await audio.play()
    }
  } catch (e) {
    console.log('playLocalAudio error:', e)
  }
}
