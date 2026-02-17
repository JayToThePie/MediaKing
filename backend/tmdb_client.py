import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


class TMDBClient:
    def __init__(self):
        if not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
            raise ValueError("TMDB_API_KEY not configured in .env file")
        self.api_key = TMDB_API_KEY

    def search_movie(self, query, year=None):
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "include_adult": False,
            "language": "en-US"
        }
        if year:
            params["year"] = year

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            return data["results"][0]
        return None

    def get_movie_details(self, movie_id):
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_image_url(self, path):
        if path:
            return f"{TMDB_IMAGE_BASE}{path}"
        return None
