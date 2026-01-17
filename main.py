from zad_2 import Movie
from zad_3 import Rating, Link, Tag
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import csv
import os


class MovieSchema(BaseModel):
    movieId: int
    title: str
    genres: List[str]


class LinkSchema(BaseModel):
    movieId: int
    imdbId: str
    tmdbId: Optional[str] = None


class RatingSchema(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


class TagSchema(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


app = FastAPI()

db_movies: List[MovieSchema] = []
db_links: List[LinkSchema] = []
db_ratings: List[RatingSchema] = []
db_tags: List[TagSchema] = []


def load_data_at_startup():
    # Helper path
    def get_path(filename):
        return os.path.join(os.path.dirname(__file__), filename)


    if os.path.exists(get_path("movies.csv")):
        with open(get_path("movies.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db_movies.append(MovieSchema(
                    movieId=int(row["movieId"]),
                    title=row["title"],
                    genres=row["genres"].split("|")
                ))

    if os.path.exists(get_path("links.csv")):
        with open(get_path("links.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db_links.append(LinkSchema(
                    movieId=int(row["movieId"]),
                    imdbId=row["imdbId"],
                    tmdbId=row["tmdbId"]
                ))

    if os.path.exists(get_path("ratings.csv")):
        with open(get_path("ratings.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i > 1000: break
                db_ratings.append(RatingSchema(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"])
                ))

    if os.path.exists(get_path("tags.csv")):
        with open(get_path("tags.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db_tags.append(TagSchema(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    tag=row["tag"],
                    timestamp=int(row["timestamp"])
                ))


load_data_at_startup()


@app.get("/")
def root():
    return {"message": "MovieLens API is running"}


@app.get("/movies", response_model=List[MovieSchema])
def get_movies():
    return db_movies


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieSchema):
    if any(m.movieId == movie.movieId for m in db_movies):
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")
    db_movies.append(movie)
    return movie


@app.get("/movies/{movie_id}", response_model=MovieSchema)
def get_movie(movie_id: int):
    for movie in db_movies:
        if movie.movieId == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: MovieSchema):
    for i, movie in enumerate(db_movies):
        if movie.movieId == movie_id:
            db_movies[i] = updated_movie
            return updated_movie
    raise HTTPException(status_code=404, detail="Movie not found")


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    for i, movie in enumerate(db_movies):
        if movie.movieId == movie_id:
            del db_movies[i]
            return
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/links", response_model=List[LinkSchema])
def get_links():
    return db_links


@app.post("/links", status_code=status.HTTP_201_CREATED)
def create_link(link: LinkSchema):
    if any(l.movieId == link.movieId for l in db_links):
        raise HTTPException(status_code=400, detail="Link for this Movie ID already exists")
    db_links.append(link)
    return link


@app.get("/links/{movie_id}", response_model=LinkSchema)
def get_link(movie_id: int):
    for link in db_links:
        if link.movieId == movie_id:
            return link
    raise HTTPException(status_code=404, detail="Link not found")


@app.put("/links/{movie_id}")
def update_link(movie_id: int, updated_link: LinkSchema):
    for i, link in enumerate(db_links):
        if link.movieId == movie_id:
            db_links[i] = updated_link
            return updated_link
    raise HTTPException(status_code=404, detail="Link not found")


@app.delete("/links/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(movie_id: int):
    for i, link in enumerate(db_links):
        if link.movieId == movie_id:
            del db_links[i]
            return
    raise HTTPException(status_code=404, detail="Link not found")


@app.get("/ratings", response_model=List[RatingSchema])
def get_ratings():
    return db_ratings


@app.post("/ratings", status_code=status.HTTP_201_CREATED)
def create_rating(rating: RatingSchema):
    if any(r.userId == rating.userId and r.movieId == rating.movieId for r in db_ratings):
        raise HTTPException(status_code=400, detail="Rating already exists")
    db_ratings.append(rating)
    return rating


@app.get("/ratings/{user_id}/{movie_id}", response_model=RatingSchema)
def get_rating(user_id: int, movie_id: int):
    for rating in db_ratings:
        if rating.userId == user_id and rating.movieId == movie_id:
            return rating
    raise HTTPException(status_code=404, detail="Rating not found")


@app.put("/ratings/{user_id}/{movie_id}")
def update_rating(user_id: int, movie_id: int, updated_rating: RatingSchema):
    for i, rating in enumerate(db_ratings):
        if rating.userId == user_id and rating.movieId == movie_id:
            db_ratings[i] = updated_rating
            return updated_rating
    raise HTTPException(status_code=404, detail="Rating not found")


@app.delete("/ratings/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(user_id: int, movie_id: int):
    for i, rating in enumerate(db_ratings):
        if rating.userId == user_id and rating.movieId == movie_id:
            del db_ratings[i]
            return
    raise HTTPException(status_code=404, detail="Rating not found")


@app.get("/tags", response_model=List[TagSchema])
def get_tags():
    return db_tags


@app.post("/tags", status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagSchema):
    db_tags.append(tag)
    return tag


@app.get("/tags/{user_id}/{movie_id}", response_model=List[TagSchema])
def get_tags_for_user_movie(user_id: int, movie_id: int):
    found_tags = [t for t in db_tags if t.userId == user_id and t.movieId == movie_id]
    if not found_tags:
        raise HTTPException(status_code=404, detail="Tags not found")
    return found_tags


@app.delete("/tags/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tags_for_user_movie(user_id: int, movie_id: int):
    global db_tags
    initial_len = len(db_tags)
    filtered_tags = [t for t in db_tags if not (t.userId == user_id and t.movieId == movie_id)]
    if len(filtered_tags) == initial_len:
        raise HTTPException(status_code=404, detail="Tags not found")
    db_tags[:] = filtered_tags

    return