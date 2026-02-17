import { useState } from 'react'
import './MovieCard.css'

function MovieCard({ movie }) {
  const [imageError, setImageError] = useState(false)
  const showPlaceholder = movie.not_found || !movie.poster || imageError

  return (
    <div className="movie-card">
      <div className="movie-poster">
        {showPlaceholder ? (
          <div className="placeholder">
            <pre className="question-mark">
{`
  _   _
 (_) (_)
  .   .
  |\\_/|
  \\_ _/
   / \\
  (_|_)
`}
            </pre>
            <span className="placeholder-label">?</span>
          </div>
        ) : (
          <img 
            src={movie.poster} 
            alt={movie.name}
            onError={() => setImageError(true)}
          />
        )}
        {movie.rating && (
          <div className="rating">
            <span>★</span> {movie.rating.toFixed(1)}
          </div>
        )}
      </div>
      <div className="movie-info">
        <h3 className="movie-title" title={movie.name}>
          {movie.name}
        </h3>
        {movie.year && (
          <span className="movie-year">{movie.year}</span>
        )}
      </div>
    </div>
  )
}

export default MovieCard
