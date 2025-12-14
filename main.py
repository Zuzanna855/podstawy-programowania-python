from fastapi import FastAPI
from zad_2 import Movie
from zad_3 import Rating, Link, Tag
import csv
import os

app = FastAPI()

def load_csv(file_name, model_class, genres_field=False):

    data_list = []
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if genres_field:
                row["genres"] = row["genres"].split("|")

            for key in row:
                if row[key].isdigit():
                    row[key] = int(row[key])
                else:
                    try:
                        row[key] = float(row[key])
                    except:
                        pass
            obj = model_class(**row)
            data_list.append(obj)
    return data_list


def load_movies(file_path="movies.csv"):
    movies_list = []
    file_path = os.path.join(os.path.dirname(__file__), file_path)


    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movieId = int(row["movieId"])
            title = row["title"]
            genres = row["genres"].split("|")  # zamiana stringa na listę
            movie = Movie(movieId, title, genres)
            movies_list.append(movie)
    return movies_list

@app.get("/movies")
def get_movies():
    movies = load_movies()
    return [movie.__dict__ for movie in movies]

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/links")
def get_links():
    links = load_csv("links.csv", Link)
    return [l.__dict__ for l in links]

@app.get("/ratings")
def get_ratings():
    ratings = load_csv("ratings.csv", Rating)
    return [r.__dict__ for r in ratings]

@app.get("/tags")
def get_tags():
    tags = load_csv("tags.csv", Tag)
    return [t.__dict__ for t in tags]


