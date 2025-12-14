from fastapi import FastAPI
from zad_2 import Movie
import csv
import os

app = FastAPI()


def load_movies(file_path="movies.csv"):
    movies_list = []
    file_path = os.path.join(os.path.dirname(__file__), file_path)


    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movieid = int(row["movieid"])
            title = row["title"]
            genres = row["genres"].split("|")  # zamiana stringa na listę
            movie = Movie(movieid, title, genres)
            movies_list.append(movie)
    return movies_list

@app.get("/movies")
def get_movies():
    movies = load_movies()
    return [movie.__dict__ for movie in movies]

@app.get("/")
def root():
    return {"hello": "world"}
