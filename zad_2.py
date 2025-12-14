from typing import List

class Movie:
    def __init__(self, movieid: int, title: str, genres: List[str]):
        self.movieid = movieid
        self.title = title
        self.genres = genres
