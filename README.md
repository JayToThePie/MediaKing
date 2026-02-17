# MediaKing

A Plex-like media server that scans movie directories and fetches metadata from TMDB.

## Features

- Scans directories for video files (.mkv, .mp4, .avi, .mov)
- Fetches movie metadata from The Movie Database (TMDB) API
- Stores movie info in `.info` files for caching
- Plex-style grid UI with movie posters
- Displays "?" placeholder for movies not found on TMDB

## Prerequisites

- Node.js 18+
- Python 3.9+
- TMDB API key (get one at https://www.themoviedb.org/settings/api)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm run install:all
   ```
3. Add your TMDB API key to `.env`:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

## Running

```bash
npm run dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## Usage

1. Click "Select Folder" to choose your movies directory
2. The app will scan for video files and fetch metadata from TMDB
3. Movie info is cached in `.info` files for faster reloads
4. Movies not found on TMDB display a "?" placeholder

## Project Structure

```
MediaKing/
├── backend/              # Python Flask server
│   ├── app.py           # Main server
│   ├── tmdb_client.py   # TMDB API client
│   ├── movie_scanner.py # Directory scanner
│   └── info_store.py   # .info file handler
├── frontend/            # React + Vite
│   └── src/components/ # UI components
├── .env                 # API keys (not committed)
└── package.json
```
