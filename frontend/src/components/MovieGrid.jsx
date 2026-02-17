import MovieCard from './MovieCard'
import './MovieGrid.css'

function MovieGrid({ movies }) {
  return (
    <div className="movie-grid">
      {movies.map((movie, index) => (
        <MovieCard key={`${movie.filename}-${index}`} movie={movie} />
      ))}
    </div>
  )
}

export default MovieGrid
