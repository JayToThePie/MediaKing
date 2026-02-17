import { useState, useEffect } from 'react'
import axios from 'axios'
import FolderPicker from './components/FolderPicker'
import MovieGrid from './components/MovieGrid'
import './App.css'

function App() {
  const [movies, setMovies] = useState([])
  const [folder, setFolder] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    axios.get('/api/folder')
      .then(res => {
        if (res.data.folder) {
          setFolder(res.data.folder)
          loadMovies(res.data.folder)
        }
      })
      .catch(() => {})
  }, [])

  const handleFolderSelect = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const res = await axios.post('/api/select-folder')
      if (res.data.success) {
        setFolder(res.data.folder)
        loadMovies(res.data.folder)
      }
    } catch (err) {
      setError('Failed to select folder')
    } finally {
      setLoading(false)
    }
  }

  const loadMovies = async (folderPath) => {
    setLoading(true)
    try {
      const res = await axios.get('/api/movies')
      if (res.data.error) {
        setError(res.data.error)
      } else {
        setMovies(res.data.movies)
      }
    } catch (err) {
      setError('Failed to load movies')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🎬</span>
          <h1>MediaKing</h1>
        </div>
        <FolderPicker 
          onSelect={handleFolderSelect} 
          folder={folder}
          loading={loading}
        />
      </header>

      <main className="main">
        {error && <div className="error">{error}</div>}
        
        {!folder && !loading && (
          <div className="empty-state">
            <div className="empty-icon">📁</div>
            <h2>No folder selected</h2>
            <p>Select a folder containing your movies to get started</p>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Scanning movies...</p>
          </div>
        )}

        {folder && !loading && movies.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">🎥</div>
            <h2>No movies found</h2>
            <p>No movies with .mkv, .mp4, .avi, or .mov extensions found in this folder</p>
          </div>
        )}

        {!loading && movies.length > 0 && (
          <MovieGrid movies={movies} />
        )}
      </main>
    </div>
  )
}

export default App
