import pytest
from fastapi.testclient import TestClient
from main import app, db_movies, db_links, db_ratings, db_tags
from main import MovieSchema, LinkSchema, RatingSchema, TagSchema

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_data():
    db_movies.clear()
    db_links.clear()
    db_ratings.clear()
    db_tags.clear()

    db_movies.append(MovieSchema(movieId=1, title="Toy Story", genres=["Adventure", "Animation"]))
    db_links.append(LinkSchema(movieId=1, imdbId="0114709", tmdbId="862"))
    db_ratings.append(RatingSchema(userId=1, movieId=1, rating=4.0, timestamp=964982703))
    db_tags.append(TagSchema(userId=1, movieId=1, tag="pixar", timestamp=1139045764))

    yield





def test_movies_crud_flow():
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Toy Story"

    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["movieId"] == 1

    response = client.get("/movies/999")
    assert response.status_code == 404

    new_movie = {"movieId": 2, "title": "Jumanji", "genres": ["Adventure"]}
    response = client.post("/movies", json=new_movie)
    assert response.status_code == 201
    assert len(db_movies) == 2
    assert db_movies[1].title == "Jumanji"

    updated_data = {"movieId": 1, "title": "Toy Story Updated", "genres": ["Animation"]}
    response = client.put("/movies/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Toy Story Updated"
    assert db_movies[0].title == "Toy Story Updated"

    response = client.delete("/movies/1")
    assert response.status_code == 204
    assert len(db_movies) == 1


def test_links_crud_flow():
    response = client.get("/links")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/links/1")
    assert response.status_code == 200
    assert response.json()["imdbId"] == "0114709"

    response = client.get("/links/999")
    assert response.status_code == 404

    new_link = {"movieId": 2, "imdbId": "12345", "tmdbId": "67890"}
    response = client.post("/links", json=new_link)
    assert response.status_code == 201
    assert len(db_links) == 2

    update_link = {"movieId": 1, "imdbId": "9999999", "tmdbId": "862"}
    response = client.put("/links/1", json=update_link)
    assert response.status_code == 200
    assert db_links[0].imdbId == "9999999"

    client.delete("/links/1")
    assert len(db_links) == 1



def test_ratings_crud_flow():
    response = client.get("/ratings")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/ratings/1/1")
    assert response.status_code == 200
    assert response.json()["rating"] == 4.0

    response = client.get("/ratings/1/999")
    assert response.status_code == 404

    new_rating = {"userId": 2, "movieId": 1, "rating": 5.0, "timestamp": 11111}
    response = client.post("/ratings", json=new_rating)
    assert response.status_code == 201
    assert len(db_ratings) == 2

    update_rating = {"userId": 1, "movieId": 1, "rating": 0.5, "timestamp": 964982703}
    response = client.put("/ratings/1/1", json=update_rating)
    assert response.status_code == 200
    assert db_ratings[0].rating == 0.5

    client.delete("/ratings/1/1")
    assert len(db_ratings) == 1


def test_tags_crud_flow():
    response = client.get("/tags")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/tags/1/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["tag"] == "pixar"

    response = client.get("/tags/999/999")
    assert response.status_code == 404

    new_tag = {"userId": 1, "movieId": 1, "tag": "fun", "timestamp": 22222}
    response = client.post("/tags", json=new_tag)
    assert response.status_code == 201
    assert len(db_tags) == 2

    response = client.delete("/tags/1/1")
    assert response.status_code == 204
    assert len(db_tags) == 0