import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import tkinter as tk
from tkinter import filedialog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tmdb_client import TMDBClient
from movie_scanner import scan_directory, extract_year_from_name
from info_store import read_info, write_info

app = Flask(__name__)
CORS(app)

current_folder = None
tmdb_client = None

try:
    tmdb_client = TMDBClient()
except ValueError as e:
    print(f"Warning: {e}")


@app.route('/api/select-folder', methods=['POST'])
def select_folder():
    global current_folder

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    folder_selected = filedialog.askdirectory(title="Select Movies Folder")
    
    root.destroy()
    
    if folder_selected:
        current_folder = folder_selected
        return jsonify({"success": True, "folder": folder_selected})
    
    return jsonify({"success": False})


@app.route('/api/folder', methods=['GET'])
def get_folder():
    return jsonify({"folder": current_folder})


@app.route('/api/movies', methods=['GET'])
def get_movies():
    global current_folder, tmdb_client

    if not current_folder:
        return jsonify({"movies": [], "error": "No folder selected"})

    if not tmdb_client:
        return jsonify({"movies": [], "error": "TMDB API not configured"})

    scanned_movies = scan_directory(current_folder)
    movies = []

    for movie in scanned_movies:
        info = read_info(movie["path"])

        if info:
            movies.append({
                "filename": movie["filename"],
                "name": movie["name"],
                "poster": info.get("poster"),
                "overview": info.get("overview"),
                "year": info.get("year"),
                "rating": info.get("rating"),
                "not_found": info.get("not_found", False)
            })
        else:
            search_name = movie["clean_name"]
            year = extract_year_from_name(movie["name"])

            try:
                result = tmdb_client.search_movie(search_name, year)
                
                if result:
                    details = tmdb_client.get_movie_details(result["id"])
                    poster = tmdb_client.get_image_url(details.get("poster_path"))
                    
                    info_data = {
                        "title": details.get("title"),
                        "overview": details.get("overview"),
                        "poster": poster,
                        "year": details.get("release_date", "")[:4] if details.get("release_date") else None,
                        "rating": details.get("vote_average"),
                        "not_found": False
                    }
                    write_info(movie["path"], info_data)

                    movies.append({
                        "filename": movie["filename"],
                        "name": info_data.get("title", movie["name"]),
                        "poster": poster,
                        "overview": info_data["overview"],
                        "year": info_data["year"],
                        "rating": info_data["rating"],
                        "not_found": False
                    })
                else:
                    info_data = {"not_found": True}
                    write_info(movie["path"], info_data)

                    movies.append({
                        "filename": movie["filename"],
                        "name": movie["name"],
                        "poster": None,
                        "overview": None,
                        "year": None,
                        "rating": None,
                        "not_found": True
                    })
            except Exception as e:
                print(f"Error processing {movie['name']}: {e}")
                movies.append({
                    "filename": movie["filename"],
                    "name": movie["name"],
                    "poster": None,
                    "overview": None,
                    "year": None,
                    "rating": None,
                    "not_found": True,
                    "error": str(e)
                })

    return jsonify({"movies": movies})


if __name__ == '__main__':
    print("MediaKing server starting on http://localhost:5000")
    app.run(port=5000, debug=True)
