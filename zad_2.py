from typing import List

class Movie:
    def __init__(self, movieId: int, title: str, genres: List[str]):
        self.movieId = movieId
        self.title = title
        self.genres = genres
