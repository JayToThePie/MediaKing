import os
import json


def get_info_path(movie_path):
    directory = os.path.dirname(movie_path)
    filename = os.path.basename(movie_path)
    name_without_ext = os.path.splitext(filename)[0]
    return os.path.join(directory, f"{name_without_ext}.info")


def read_info(movie_path):
    info_path = get_info_path(movie_path)
    
    if os.path.exists(info_path):
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def write_info(movie_path, data):
    info_path = get_info_path(movie_path)
    
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    return info_path
