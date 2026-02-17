import os
import re

VIDEO_EXTENSIONS = {'.mkv', '.mp4', '.avi', '.mov'}


def scan_directory(directory):
    movies = []

    if not os.path.isdir(directory):
        return movies

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            if ext.lower() in VIDEO_EXTENSIONS:
                movie_name = os.path.splitext(filename)[0]
                cleaned_name = clean_movie_name(movie_name)
                movies.append({
                    "filename": filename,
                    "name": movie_name,
                    "clean_name": cleaned_name,
                    "path": file_path
                })

    return movies


def clean_movie_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    name = re.sub(r'\d{3,4}p', '', name)
    name = re.sub(r'BluRay|x264|x265|H264|H265|HEVC|DTS|AC3|AAC', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()
    return name


def extract_year_from_name(name):
    year_match = re.search(r'(19|20)\d{2}', name)
    if year_match:
        return year_match.group()
    return None
